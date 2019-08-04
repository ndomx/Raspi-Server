import os

from abc import ABC
from typing import List, Dict, Tuple, Any
from PIL import Image
from datetime import datetime
from enum import Enum

class FileType(Enum):
    PICTURE = 0
    AUDIO = 1
    VIDEO = 2
    DOCUMENT = 3
    INVALID = -1   

_img_extensions: Dict[str, str] = {
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

_audio_extensions: Dict[str, str] = {
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.mp4': 'audio/mp4',
    '.aac': 'audio/aac',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac'
}

_valid_extensions: List[Tuple[FileType, Dict[str, str]]] = [
    (FileType.PICTURE, _img_extensions),
    (FileType.AUDIO, _audio_extensions)
]

def _get_file_extension(filename: str)->str:
    index = filename.rindex('.')
    return filename[index::]

def is_valid_format(filename: str, filetype: FileType)->bool:
    ext = _get_file_extension(filename)
    for (_type, exts) in _valid_extensions:
        if (_type == filetype):
            return (ext in exts.keys())

    return False

def get_mime_type(filename: str, filetype: FileType)->str:
    try:
        ext = _get_file_extension(filename)
        mime = ''

        for (_type, exts) in _valid_extensions:
            if (_type == filetype):
                mime = exts[ext]
                break

    except IndexError:
        mime = 'text/plain'

    return mime

def get_image_attributes(abspath: str)->Dict[str, Any]:
    att = {}
    stats = os.stat(abspath)
    att['size'] = stats.st_size
    att['ctime'] = datetime.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['atime'] = datetime.fromtimestamp(stats.st_atime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['mtime'] = datetime.fromtimestamp(stats.st_mtime).strftime('%d-%b-%Y (%H:%M:%S)')

    with Image.open(abspath) as img:
        w, h = img.size
        att['width'] = w
        att['height'] = h

    return att

def get_audio_attributes(abspath: str)->Dict[str, Any]:
    att = {}
    stats = os.stat(abspath)
    att['size'] = stats.st_size
    att['ctime'] = datetime.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['atime'] = datetime.fromtimestamp(stats.st_atime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['mtime'] = datetime.fromtimestamp(stats.st_mtime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['duration'] = 0

    return att