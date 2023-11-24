def convertSTLFile(file_convert, file_name):
    try:
        from stl import mesh
        from mpl_toolkits import mplot3d
        from matplotlib import pyplot
        import matplotlib
        matplotlib.use('AGG')
        # Create a new plot
        figure = pyplot.figure(dpi=200)
        axes = figure.add_subplot(projection='3d')
        
        your_mesh = mesh.Mesh.from_file(file_convert)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        # Auto scale to the mesh size
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
        from PIL import Image 
        img = Image.open(file_name)
        left = find_edge(img, 'l')
        top = find_edge(img, 't')
        right = find_edge(img, 'r')
        bottom = find_edge(img, 'b')
        img_res = img.crop((left, top, right, bottom))

        '''base_width= 300
        img = Image.open('somepic.jpg')
        wpercent = (base_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img.resize((basewidth, hsize), Image.Resampling.LANCZOS)'''

        img_res.save(file_name)
        return True
    
    except Exception as e:
        print(e)
        return False
    
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
