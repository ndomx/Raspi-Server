from typing import List, Dict

__img_extensions: Dict[str, str] = {
    '.apng': 'image/png', 
    '.bmp': 'image/bmp', 
    '.gif': 'image/gif', 
    '.ico': 'image/ico', 
    '.jpg': 'image/jpg', 
    '.jpeg': 'image/jpg', 
    '.jfif': 'image/jpg', 
    '.pjpeg': 'image/jpg', 
    '.pjp': 'image/jpg', 
    '.png': 'image/png', 
    '.svg': 'image/svg', 
    '.tiff': 'image/tif', 
    '.tif': 'image/tif', 
    '.webp': 'image/webp', 
    '.xbm': 'image/xbm'
}

def __get_file_extension(filename: str)->str:
    index = filename.rindex('.')
    return filename[index::]

def is_valid_img_format(filename: str)->bool:
    ext = __get_file_extension(filename)
    return (ext in __img_extensions.keys())

def get_mime_type(filename: str)->str:
    try:
        ext = __get_file_extension(filename)
        mime = __img_extensions[ext]
    except IndexError as e:
        mime = 'text/plain'

    return mime
        