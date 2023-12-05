# STL-Manager 
An app to manager STL files. Built with Python, Flask and HTMX, matplotlib. Run in a docker container.

# Environment Variable for files location

.env
```
export FILES_LOCATION=""
```

# Create virtual environment: 
Require packages: flask, dotenv, numpy-stl, matplotlib
```
PS stl-manager> pip install flask
PS stl-manager> pip install python-dotenv
PS stl-manager> pip install numpy-stl
PS stl-manager> pip install matplotlib
PS stl-manager> pip install virtualenv
PS stl-manager> virtualenv venv
PS stl-manager> venv\Scripts\activate
(venv) PS stl-manager> py app.py
```

# Build/Run Docker Image

```
docker build -t stl-manager .
docker run -d -p 5000:5000 stl-manager
```

# Fix no module named 'pip' even after successful installation

run: https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py


