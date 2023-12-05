'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template, send_file, request
from dotenv import load_dotenv
import pathlib
import shutil
import re
from generateThumbnails import GenerateThumbnails
app = Flask(__name__)
load_dotenv()
files_location = os.getenv('FILES_LOCATION', None)
thumb_file_formats = ['.png', '.jpg', '.gif', '.svg']
thumb_size = {"width":225, "height":115}
omit_folders = ['data', 'temp']
omit_files = ['.txt', '.db']
@app.route('/empty')
def empty():
	return ''

@app.route('/')
@app.route('/add')
@app.route('/list/<folder_name>')
@app.route('/edit/<folder_name>')
def main(folder_name=None):
	return render_template("index.html", folder_name=folder_name, editing='/edit/' in request.base_url, adding='/add' in request.base_url)

@app.route('/listitems')
def list():
	folders = []
	incriment = 1
	if os.path.exists(files_location):
		for folder_name in next(os.walk(files_location))[1]:
			if folder_name not in omit_folders:
				folders.append({"id":incriment,"name":folder_name, "process":not os.path.exists(files_location+"\\"+folder_name+"\\data")})
				incriment = incriment + 1
	return render_template("list.html", folders=folders)

@app.route('/listitems', methods=["POST"])
def listsearch():
	folders = []
	incriment = 1
	if os.path.exists(files_location):
		for folder_name in next(os.walk(files_location))[1]:
			if request.form['search'].lower() in folder_name.lower() and folder_name not in omit_folders:
				folders.append({"id":incriment,"name":folder_name, "process":not os.path.exists(files_location+"\\"+folder_name+"\\data")})
				incriment = incriment + 1
	return render_template("list.html", folders=folders)

@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/file')
def file():
	return render_template("file.html", 
						folder_name=request.args.get('folder_name'),
						file_id=request.args.get('file_id'),
						file_name=request.args.get('file_name'),
						file_size=request.args.get('file_size'))

@app.route('/delete/<folder_name>', methods=["DELETE"])
def delete(folder_name):
	folder_location = files_location + '\\' + folder_name
	if os.path.exists(folder_location):
		os.rmdir(folder_location)
	return ''

@app.route('/thumb/<folder_name>')
@app.route('/thumb/<folder_name>/<thumb_name>')
def thumb(folder_name, thumb_name=None):
	try:
		thumb_dir = files_location + '\\'+ folder_name + '\\data\\'
		thumb_location = ''
		if thumb_name != None:
			thumb_location =  thumb_dir + thumb_name + '.png'
		elif os.path.exists(thumb_dir + folder_name + '.png'):
			thumb_location =  thumb_dir + folder_name + '.png'
		elif os.path.exists(thumb_dir):
			for file_name in next(os.walk(thumb_dir))[2]:
				if pathlib.Path(file_name).suffix in thumb_file_formats:
					thumb_location =  thumb_dir + file_name
					break
		if os.path.exists(thumb_location):
			return send_file(thumb_location)
		else:
			return send_file('static/images/thumb.png')
	except Exception as e:
		print('error', e)
		return send_file('static/images/thumb.png')

@app.route('/process/<folder_name>')
def process(folder_name):
	folder_location = files_location + '\\' + folder_name
	if os.path.exists(folder_location):
		if not os.path.exists(folder_location+'\\data'):
			os.mkdir(folder_location+'\\data')
			with open(folder_location+'\\data\\info.txt', 'w') as f:
				f.write('')
		GenerateThumbnails(folder_location, folder_name)
	return '<img class="thumb" src="/thumb/'+folder_name+'" />'
		
@app.route('/download/<folder_name>')
def download(folder_name):
	zipfile = shutil.make_archive(files_location+'\\temp\\'+folder_name, 'zip', files_location+'\\'+folder_name) 
	return send_file(zipfile)

@app.route('/view/<folder_name>')
def view(folder_name):
	files = []
	incriment = 1
	folder_info = ''
	folder_location = files_location + '\\' + folder_name
	if os.path.exists(folder_location):
		for file_name in next(os.walk(folder_location))[2]:
			if pathlib.Path(file_name).suffix not in omit_files:
				if pathlib.Path(file_name).suffix in thumb_file_formats:
					files.insert(0, {"id":incriment, "name":pathlib.Path(file_name).stem, "fullname":pathlib.Path(file_name).name})
				else:
					files.append({"id":incriment, "name":pathlib.Path(file_name).stem, "fullname":pathlib.Path(file_name).name})
				incriment = incriment + 1		
		if (os.path.isfile(folder_location+"info.txt")):
			with open(folder_location+"info.txt") as f:
				folder_info = f.readlines()
		return render_template("view.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name)
	else:
		return render_template("notfound.html", folder_name=folder_name)

@app.route('/edititem/<folder_name>')
def edit(folder_name):
	files = []
	file_names = ''
	folder_info = ''
	incriment = 0
	item_folder = files_location + '\\' + folder_name + '\\'
	if os.path.exists(item_folder):
		for file_name in next(os.walk(item_folder))[2]:
			file_location = item_folder + '\\' + file_name
			if pathlib.Path(file_name).suffix not in omit_files:
				files.append({"url":"/file?file_id="+str(incriment)+"&file_name="+pathlib.Path(file_name).stem+"&file_size="+str(round(os.path.getsize(file_location)/1024))+"&folder_name="+folder_name})
				incriment = incriment + 1
				file_names += ','+file_name if file_names!='' else file_name
		if (os.path.isfile(item_folder+"\\data\\info.txt")):
			with open(item_folder+"\\data\\info.txt") as f:
				folder_info = f.readlines()
		return render_template("edit.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name, file_names=file_names)
	else:
		return ''

@app.route('/additem')
def add():
	return render_template("edit.html", files=[], folder_info='', folder_name='', file_names='')

@app.route('/upload', methods=['POST'])
@app.route('/upload/<folder_name>', methods=['POST'])
def upload(folder_name=None):
	#Update title
	new_folder_name = re.sub('[^a-zA-Z0-9_ -]+', '', request.form['title'])
	if folder_name != new_folder_name:
		if folder_name == None:
			if not os.path.exists(files_location+'\\'+new_folder_name):
				os.mkdir(files_location+'\\'+new_folder_name)
			if not os.path.exists(files_location+'\\'+new_folder_name+'\\data'):
				os.mkdir(files_location+'\\'+new_folder_name+'\\data')
		elif os.path.exists(files_location + '\\' + folder_name):
			os.rename(files_location + '\\' + folder_name, files_location+'\\'+new_folder_name)
		else:
			return render_template("notfound.html", folder_name=folder_name)
	folder_location = files_location + '\\' + new_folder_name
	#Update existing files
	files2remove = request.form["files2remove"].split(",")
	for file_name in files2remove:
		if file_name != '' and os.path.exists(folder_location+'\\'+file_name):
			os.remove(folder_location+'\\'+file_name)
		if os.path.exists(folder_location+'\\data\\'+pathlib.Path(file_name).stem+'.png'):
			os.remove(folder_location+'\\data\\'+pathlib.Path(file_name).stem+'.png')
	#Update description
	with open(folder_location+'\\data\\info.txt', 'w') as f:
		f.write(request.form["info"])
	#Add new files
	for file in request.files.getlist('file_upload'):
		if file.filename in request.form["newfiles2add"]:
			file.save(folder_location + '\\' + file.filename)
	#Generate a default thumbnails
	GenerateThumbnails(folder_location, new_folder_name);
	return '<div hx-get="/list/'+new_folder_name+'" hx-trigger="load" hx-push-url="true" hx-target="body"></div>'



if __name__ == "__main__":
	app.run(debug=True)