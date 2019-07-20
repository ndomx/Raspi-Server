__img_extensions = ['.apng', '.bmp', '.gif', '.ico', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.tiff', '.tif', '.webp', '.xbm']

def is_valid_img_format(filename: str)->bool:
    for ext in __img_extensions:
        if (filename.endswith(ext)):
            return True
    
    return False