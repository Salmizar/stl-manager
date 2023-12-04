import os
from PIL import Image
import pathlib
from convertSTL import ConvertSTL
thumb_file_formats = ['.png', '.jpg', '.gif', '.svg']
thumb_size = {"width":225, "height":115}
def GenerateThumbnails(folder_location, folder_name):
    thumb_generated = False
    thumb_location = folder_location + '\\data\\' + folder_name + '.png'
    for file_name in next(os.walk(folder_location))[2]:
        if pathlib.Path(file_name).suffix in thumb_file_formats:
            file_location = folder_location + '\\' + file_name
            if not os.path.exists(thumb_location):
                image = Image.open(file_location)
                MAX_SIZE = (thumb_size["width"], thumb_size["height"])
                image.thumbnail(MAX_SIZE)
                image.save(thumb_location)
            thumb_generated = True
            break
    #if no thumb was generated from previous step, create one from first STL
    if not thumb_generated:
        for file_name in next(os.walk(folder_location))[2]:
            if pathlib.Path(file_name).suffix == '.stl':
                file_location = folder_location + '\\' + file_name
                ConvertSTL(file_location, thumb_location)
                break
    #Generate a thumb for each STL and image file
    for file_name in next(os.walk(folder_location))[2]:
        if pathlib.Path(file_name).suffix == '.stl':
            file_location = folder_location + '\\' + file_name
            thumb_location = folder_location + '\\data\\' + pathlib.Path(file_name).stem + '.png'
            if not os.path.exists(thumb_location):
                ConvertSTL(file_location, thumb_location)
        elif pathlib.Path(file_name).suffix in thumb_file_formats:
            file_location = folder_location + '\\' + file_name
            thumb_location = folder_location + '\\data\\' + pathlib.Path(file_name).stem + '.png'
            if not os.path.exists(thumb_location):
                image = Image.open(file_location)
                MAX_SIZE = (thumb_size["width"], thumb_size["height"])
                image.thumbnail(MAX_SIZE)
                image.save(thumb_location)