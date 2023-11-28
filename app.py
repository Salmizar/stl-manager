'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template, send_file, request
from dotenv import load_dotenv
import pathlib
import shutil

app = Flask(__name__)
load_dotenv()
files_location = os.getenv('FILES_LOCATION', None)

@app.route('/empty')
def empty():
	return ''

@app.route('/')
@app.route('/list/<folder_name>')
@app.route('/edit/<folder_name>')
def main(folder_name=None):
	print('base_url', request.base_url)
	return render_template("index.html", folder_name=folder_name, editing='/edit/' in request.base_url)

@app.route('/listitems')
def list():
	folders = []
	incriment = 1
	for folder_name in next(os.walk(files_location))[1]:
		folders.append({"id":incriment,"name":folder_name})
		incriment = incriment + 1
	return render_template("list.html", folders=folders)

@app.route('/listitems', methods=["POST"])
def listsearch():
	folders = []
	incriment = 1
	for folder_name in next(os.walk(files_location))[1]:
		if request.form['search'].lower() in folder_name.lower():
			folders.append({"id":incriment,"name":folder_name})
			incriment = incriment + 1
	return render_template("list.html", folders=folders)

@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/delete/<folder_name>', methods=["DELETE"])
def delete(folder_name):
	folder_location = files_location + '\\' + folder_name
	if os.path.exists(folder_location):
		os.rmdir(folder_location)
	return ''

@app.route('/thumb/<thumb_name>')
@app.route('/thumb/<thumb_name>/<folder_name>')
def thumb(thumb_name, folder_name=None):
	try:
		if folder_name != None:
			thumb_dir = files_location + '\\'+ folder_name + '\\'
		else:
			thumb_dir = files_location + '\\'+ thumb_name + '\\'
		thumb_location =  thumb_dir + thumb_name + '.png'
		print('thumb_location',thumb_location)
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
			else:
				return send_file( 'static/images/thumb.png')

	except Exception as e:
		print('error', e)
		return send_file( 'static/images/thumb.png')

@app.route('/view/<folder_name>')
def view(folder_name):
	files = []
	incriment = 1
	print('folder_name', folder_name)
	for file_name in next(os.walk(files_location+'\\'+folder_name))[2]:
		suffix = pathlib.Path(file_name).suffix
		file_location = files_location + '\\' + folder_name + '\\' + file_name
		if suffix == '.png' and folder_name != file_name.split(".")[0]:
			files.append({"id":incriment,"name":file_name.split(".")[0]})
			incriment = incriment + 1
		elif suffix not in ['.png', '.txt', '.db', '.stl']:
			files.append({"id":incriment,"name":file_name.split(".")[0]})
			incriment = incriment + 1
	folder_info = ''
	if (os.path.isfile(files_location+'\\'+folder_name+"\\description.txt")):
		with open(files_location+'\\'+folder_name+"\\description.txt") as f:
			folder_info = f.readlines()
	return render_template("view.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name)

@app.route('/download/<folder_name>')
def download(folder_name):
	zipfile = shutil.make_archive(files_location+'\\temp\\'+folder_name, 'zip', files_location+'\\'+folder_name) 
	return send_file(zipfile)
@app.route('/edititem/<folder_name>')
def edit(folder_name):
	files = []
	incriment = 1
	for file_name in next(os.walk(files_location+'\\'+folder_name))[2]:
		suffix = pathlib.Path(file_name).suffix
		file_location = files_location + '\\' + folder_name + '\\' + file_name
		if suffix == '.png' and folder_name != file_name.split(".")[0]:
			files.append({"id":incriment,"name":file_name.split(".")[0]})
			incriment = incriment + 1
		elif suffix not in ['.png', '.txt', '.db', '.stl']:
			files.append({"id":incriment,"name":file_name.split(".")[0]})
			incriment = incriment + 1
	folder_info = ''
	if (os.path.isfile(files_location+'\\'+folder_name+"\\description.txt")):
		with open(files_location+'\\'+folder_name+"\\description.txt") as f:
			folder_info = f.readlines()
	return render_template("edit.html", files=files, folder_info=''.join(folder_info), folder_name=folder_name)

app.run()
