'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template, send_file
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
filesLocation = os.getenv('FILES_LOCATION', None)

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/list')
def list():
	files = []
	for folder_name in next(os.walk(filesLocation))[1]:
		files.append({"name":folder_name})
	return render_template("list.html", files=files)

@app.route('/search')
def search():
	return render_template("search.html")

@app.route('/empty')
def empty():
	return ''

@app.route('/thumb/<thumbname>')
def thumb(thumbname):
	try:
		thumbLocation =  filesLocation + '\\'+ thumbname + '\\' + thumbname + '.png'
		if os.path.isfile(thumbLocation):
			return send_file( thumbLocation)
		else:
			from convertSTL import convertSTLFile
			if os.path.isfile(thumbLocation):
				return send_file( thumbLocation)
			else:
				return send_file( 'static/images/thumb.png')

	except Exception as e:
		print('error', e)
		return send_file( 'static/images/thumb.png')

app.run()
