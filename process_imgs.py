import os

from typing import List, Dict, Any
from PIL import Image
from datetime import date

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

def get_image_attributes(abspath: str)->Dict[str, Any]:
    att = {}
    stats = os.stat(abspath)
    att['size'] = stats.st_size
    att['ctime'] = date.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['atime'] = date.fromtimestamp(stats.st_atime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['mtime'] = date.fromtimestamp(stats.st_mtime).strftime('%d-%b-%Y (%H:%M:%S)')

    with Image.open(abspath) as img:
        w, h = img.size
        att['width'] = w
        att['height'] = h

    return att
        