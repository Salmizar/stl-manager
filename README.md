# STL-Manager 
An app to manager STL files. Built with Python, Flask and HTMX, matplotlib. Run in a docker container.

# Environment variable for files location

.env
```
export FILES_LOCATION=""
```

# Docker command helpers

Build docker image: In App root folder
```
docker build -t stl-manager .
```
Create password protected network volume
```
docker volume create --driver local --opt type=cifs --opt device=//192.168.1.xxx/files/location --opt o=user=user,domain=domain,password=paswrd stlfiles
```
Run Image in container: Specify preconfigured volume, change env variable
```
docker run -v stlfiles:/nas -d -p 5000:5000 -e "FILES_LOCATION=/stlfiles" stl-manager
```
Run Image in container: Create attached volume and change env variable
```
docker run -v "C:\Users\Chris\Desktop\Projects\My Projects\backup:/stlfiles" -d -p 5000:5000 -e "FILES_LOCATION=/stlfiles" stl-manager
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


