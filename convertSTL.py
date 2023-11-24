from PIL import Image
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import matplotlib
import os
def convertSTLFile(file_convert, file_name):
    try:
        matplotlib.use('AGG')
        # Create a new plot
        figure = pyplot.figure(dpi=200)
        axes = figure.add_subplot(projection='3d')
        your_mesh = mesh.Mesh.from_file(file_convert)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
        pyplot.axis('off')
        pyplot.savefig(file_name, bbox_inches='tight', pad_inches = 0)
        pyplot.close()
        figure.clear()
        crop(file_name)
        return True
    except Exception as e:
        print(e)
        return False
    
def crop(file_name):
    try:
        img = Image.open(file_name)
        left = find_edge(img, 'l')
        top = find_edge(img, 't')
        right = find_edge(img, 'r')
        bottom = find_edge(img, 'b')
        if left != None and top != None and right != None and bottom != None:
            img_res = img.crop((left, top, right, bottom))
            img_res = resize(img_res, 225, 165)
            img_res.save(file_name)
            return True
        else:
            #blank thumbnail, clear it
            os.remove(file_name)
            return False
    except Exception as e:
        print(e)
        return False

def resize(img, w, h):
    if img.width > w or img.height > h:
        if w / img.width < h / img.height:
            resize_percentage = (w / img.width)
        else:
            resize_percentage = (h / img.height)
        width = img.width * resize_percentage 
        height = img.height * resize_percentage
        img_res = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)
        return img_res
    else:
        return img
def find_edge(img, edge):
    white_pixel = (255, 255, 255, 255)
    if edge == "l":
        for p_x in range(img.width):
            for p_y in range(img.height):
                if (img.getpixel((p_x,p_y)) != white_pixel):
                    return p_x
    elif edge == "t":
        for p_y in range(img.height):
            for p_x in range(img.width):
                if (img.getpixel((p_x,p_y)) != white_pixel):
                    return p_y
    elif edge == "r":
        for p_x in range(img.width):
            for p_y in range(img.height):
                if (img.getpixel((img.width - 1 - p_x,img.height - 1 - p_y)) != white_pixel):
                    return img.width - p_x
    elif edge == "b":
        for p_y in range(img.height):
            for p_x in range(img.width):
                if (img.getpixel((img.width - 1 - p_x,img.height - 1 - p_y)) != white_pixel):
                    return img.height - p_y
