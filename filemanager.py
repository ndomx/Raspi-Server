import os

from typing import List, Dict, Tuple, Any
from datetime import datetime
from enum import Enum

from PIL import Image
from tinytag import TinyTag
from moviepy.editor import VideoFileClip

class FileType(Enum):
    PICTURE = 0
    AUDIO = 1
    VIDEO = 2
    DOCUMENT = 3
    INVALID = -1
    ANY = -2   

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

_video_extensions: Dict[str, str] = {
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.ogg': 'video/ogg'
}

_valid_extensions: List[Tuple[FileType, Dict[str, str]]] = [
    (FileType.PICTURE, _img_extensions),
    (FileType.VIDEO, _video_extensions)
]

def get_file_extension(filename: str)->str:
    index = filename.rindex('.')
    return filename[index::]

def is_valid_format(filename: str, filetype: FileType = FileType.ANY)->bool:
    ext = get_file_extension(filename)
    if (filetype == FileType.ANY):
        for (_, exts) in _valid_extensions:
            if (ext in exts.keys()):
                return True

    for (_type, exts) in _valid_extensions:
        if (_type == filetype):
            return (ext in exts.keys())

    return False

def get_mime_type(filename: str, filetype: FileType)->str:
    try:
        ext = get_file_extension(filename)
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
    att['size'] = round(stats.st_size / 1_048_576, 1)
    att['ctime'] = datetime.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['atime'] = datetime.fromtimestamp(stats.st_atime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['mtime'] = datetime.fromtimestamp(stats.st_mtime).strftime('%d-%b-%Y (%H:%M:%S)')

    tag = TinyTag.get(abspath)

    att['artist'] = tag.artist if (tag.artist is not None) else ''
    att['album'] = tag.album if (tag.album is not None) else ''
    att['title'] = tag.title if (tag.title is not None) else ''

    duration = tag.duration
    if (duration is None):
        att['duration'] = 0
    else:
        millis = int(1000*duration)
        att['duration'] = '{mins:02d}:{secs:02d}.{mils:03d}'.format(mins=millis // 60000, secs=millis // 1000, mils=millis % 1000)

    return att

def get_video_attributes(abspath: str)->Dict[str, Any]:
    att = {}
    stats = os.stat(abspath)
    att['size'] = round(stats.st_size / 1_048_576, 1)
    att['ctime'] = datetime.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['atime'] = datetime.fromtimestamp(stats.st_atime).strftime('%d-%b-%Y (%H:%M:%S)')
    att['mtime'] = datetime.fromtimestamp(stats.st_mtime).strftime('%d-%b-%Y (%H:%M:%S)')

    clip = VideoFileClip(abspath)
    w, h = clip.size

    att['width'] = w
    att['height'] = h
    att['resolution'] = F'{w}x{h}'

    d = int(clip.duration)
    hours = d // 3_600

    d %= 3_600
    minutes = d // 60

    d %= 60
    seconds = d 

    att['duration'] = F'{hours:02d}:{minutes:02d}:{seconds:02d}'

    return att