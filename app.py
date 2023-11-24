'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template, send_file
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
files_location = os.getenv('FILES_LOCATION', None)

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/list')
def list():
	files = []
	incriment = 1
	for folder_name in next(os.walk(files_location))[1]:
		files.append({"id":incriment,"name":folder_name})
		incriment = incriment + 1
	return render_template("list.html", files=files)

@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/empty')
def empty():
	return ''

@app.route('/delete/<folder_name>', methods=["DELETE"])
def delete(folder_name):
	folder_location = files_location + '\\' + folder_name
	if os.path.exists(folder_location):
		os.rmdir(folder_location)
	return ''

@app.route('/thumb/<thumb_name>')
def thumb(thumb_name):
	try:
		thumb_dir = files_location + '\\'+ thumb_name + '\\'
		thumb_location =  thumb_dir + thumb_name + '.png'
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

app.run()
