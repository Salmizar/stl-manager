'linux: #!/user/bin/env python3'
import os
from flask import Flask, render_template
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

app.run()
