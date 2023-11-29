'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template, send_file, request
from dotenv import load_dotenv
import pathlib
import shutil

app = Flask(__name__)
load_dotenv()
files_location = os.getenv('FILES_LOCATION', None)
file_formats = ['.png', '.jpg', '.gif', '.svg']
omit_folders = ['data', 'temp']
omit_files = ['.txt', '.db']
@app.route('/empty')
def empty():
	return ''

@app.route('/')
@app.route('/list/<folder_name>')
@app.route('/edit/<folder_name>')
def main(folder_name=None):
	return render_template("index.html", folder_name=folder_name, editing='/edit/' in request.base_url)

@app.route('/listitems')
def list():
	folders = []
	incriment = 1
	for folder_name in next(os.walk(files_location))[1]:
		if folder_name not in omit_folders:
			folders.append({"id":incriment,"name":folder_name})
			incriment = incriment + 1
	return render_template("list.html", folders=folders)

@app.route('/listitems', methods=["POST"])
def listsearch():
	folders = []
	incriment = 1
	for folder_name in next(os.walk(files_location))[1]:
		if request.form['search'].lower() in folder_name.lower() and folder_name not in omit_folders:
			folders.append({"id":incriment,"name":folder_name})
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
		else:
			for file_name in next(os.walk(thumb_dir))[2]:
				if pathlib.Path(file_name).suffix in file_formats:
					thumb_location =  thumb_dir + file_name
					break
		if os.path.exists(thumb_location):
			return send_file(thumb_location)
		else:
			return send_file( 'static/images/thumb.png')
	except Exception as e:
		print('error', e)
		return send_file( 'static/images/thumb.png')

@app.route('/process/<folder_name>')
def process(folder_name):
	return send_file( 'static/images/thumb.png')
	'''thumb_location = thumb_dir + os.listdir(thumb_dir)[0]
	if thumb_location == None:
		thumb_location = 
	
	if os.path.isfile(thumb_location):
		return send_file( thumb_location)
	else:
		from convertSTL import convertSTLFile
		stl_location = thumb_dir + thumb_name + '.stl'
		if os.path.isfile(stl_location):
			convertSTLFile(stl_location, thumb_location)
		else:
			#find first STL file to convert
			convertSTLFile(thumb_dir + '\\' + os.listdir(thumb_dir)[0], thumb_location)

		if os.path.isfile(thumb_location):
			return send_file( thumb_location)
	'''
		
@app.route('/download/<folder_name>')
def download(folder_name):
	zipfile = shutil.make_archive(files_location+'\\temp\\'+folder_name, 'zip', files_location+'\\'+folder_name) 
	return send_file(zipfile)

@app.route('/view/<folder_name>')
def view(folder_name):
	files = []
	incriment = 1
	data_folder = files_location + '\\' + folder_name + '\\data\\'
	for file_name in next(os.walk(data_folder))[2]:
		suffix = pathlib.Path(file_name).suffix
		if suffix in file_formats:
			files.append({"id":incriment,"name":pathlib.Path(file_name).stem})
			incriment = incriment + 1
	folder_info = ''
	if (os.path.isfile(data_folder+"\\data\\info.txt")):
		with open(data_folder+"\\data\\info.txt") as f:
			folder_info = f.readlines()
	return render_template("view.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name)

@app.route('/edititem/<folder_name>')
def edit(folder_name):
	files = []
	file_names = ''
	incriment = 0
	data_folder = files_location + '\\' + folder_name + '\\'
	for file_name in next(os.walk(data_folder))[2]:
		suffix = pathlib.Path(file_name).suffix
		file_location = data_folder + '\\' + file_name
		if suffix not in omit_files:
			incriment = incriment + 1
			files.append({"url":"/file?file_id="+str(incriment)+"&file_name="+pathlib.Path(file_name).stem+"&file_size="+str(round(os.path.getsize(file_location)/1024))+"&folder_name="+folder_name})
			file_names += ','+file_name if file_names!='' else file_name
	
	folder_info = ''
	if (os.path.isfile(data_folder+"\\data\\info.txt")):
		with open(data_folder+"\\data\\info.txt") as f:
			folder_info = f.readlines()
	return render_template("edit.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name, file_names=file_names)

@app.route('/upload/<folder_name>', methods=['POST'])
def upload(folder_name):
	folder_location = files_location + '\\' + folder_name
	#update title
	if folder_name != request.form["title"]:
		os.rename(folder_location,files_location+'\\'+request.form['title'])
		folder_location = files_location + '\\' + request.form['title']
	#update existing Files
	files2remove = request.form["files2remove"].split(",")
	for file_name in files2remove:
		if file_name!= '' and os.path.exists(folder_location+'\\'+file_name):
			os.remove(folder_location+'\\'+file_name)
		if os.path.exists(folder_location+'\\data\\'+pathlib.Path(file_name).stem+'.png'):
			os.remove(folder_location+'\\data\\'+pathlib.Path(file_name).stem+'.png')
	#Update description
	with open(folder_location+'\\data\\info.txt', 'w') as f:
		f.write(request.form["info"])
	#add new files
	for file in request.files.getlist('file_upload'):
		if file.filename in request.form["newfiles2add"]:
			file.save(folder_location + '\\' + file.filename)
	return ''

app.run()