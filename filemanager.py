import os

from abc import ABC, abstractmethod

from typing import List, Dict, Tuple, Any
from enum import unique, IntEnum

from PIL import Image
from tinytag import TinyTag
from moviepy.editor import VideoFileClip

@unique
class FileType(IntEnum):
    PICTURE = 1
    AUDIO = 2
    VIDEO = 3
    OTHER = 0

class _File(ABC):
    
    name = ''
    ctime = ''
    atime = ''
    mtime = ''
    size = 0

    filetype = FileType.OTHER
    extensions: List[str] = []

    @property
    def extension(self)->str:
        index = self.name.rindex('.')
        return self.name[index::]

    @property
    @abstractmethod
    def mime_type(self)->str:
        pass

    @staticmethod
    @abstractmethod
    def from_abspath(abspath: str):
        pass

    def __str__(self):
        return self.name

class AnyFile(_File):
    def mime_type(self)->str:
        return 'text/plain'

    def from_abspath(abspath: str)->_File:
        if not os.path.isfile:
            raise FileNotFoundError('path not set to directory')

        file = AnyFile()
        file.name = os.path.split(abspath)[-1]

        stats = os.stat(abspath)
        file.size = stats.st_size
        file.ctime = stats.st_ctime
        file.atime = stats.st_atime
        file.mtime = stats.st_mtime

        return file

class VideoFile(_File):

    width = 0
    height = 0
    duration = 0

    filetype = FileType.VIDEO
    extensions = ['.mp4', '.webm', '.ogg']

    def mime_type(self)->str:
        return F'video/{self.extension}'

    def from_abspath(abspath: str)->_File:
        if not os.path.isfile:
            raise FileNotFoundError('path not set to directory')

        video = VideoFile()
        video.name = os.path.split(abspath)[-1]

        stats = os.stat(abspath)
        video.size = stats.st_size
        video.ctime = stats.st_ctime
        video.atime = stats.st_atime
        video.mtime = stats.st_mtime

        clip = VideoFileClip(abspath)
        width, height = clip.size
        video.width = width
        video.height = height
        video.duration = clip.duration

        return video

class AudioFile(_File):

    artist = ''
    album = ''
    title = ''
    year = 0
    duration = 0

    filetype = FileType.AUDIO
    extensions = [
        '.wav', '.mp3', '.mp4',
        '.aac', '.ogg', '.flac'
    ]

    def mime_type(self)->str:
        return F'audio/{self.extension}'

    def from_abspath(abspath: str)->_File:
        if not os.path.isfile:
            raise FileNotFoundError('path not set to directory')

        audio = AudioFile()
        audio.name = os.path.split(abspath)[-1]

        stats = os.stat(abspath)
        audio.size = stats.st_size
        audio.ctime = stats.st_ctime
        audio.atime = stats.st_atime
        audio.mtime = stats.st_mtime

        tag = TinyTag.get(abspath)

        audio.artist = tag.artist if (tag.artist is not None) else ''
        audio.album = tag.album if (tag.album is not None) else ''
        audio.title = tag.title if (tag.title is not None) else ''
        audio.year = tag.year if (tag.year is not None) else 0
        audio.duration = tag.duration if (tag.duration is not None) else 0

        return audio

class PictureFile(_File):

    width = ''
    height = ''

    filetype = FileType.PICTURE
    extensions = [
        '.apng', '.bmp', '.gif', '.ico', '.jpg', '.jpeg',
        '.jfif', '.pjpeg', '.pjp', '.png', '.svg', 
        '.tiff', '.tif', '.webp', '.xbm' 
    ]

    def mime_type(self)->str:
        ext = ''
        if (self.extension == '.apng'):
            ext = 'png'
        elif (self.extension in ('.jpeg', '.jfif', '.pjpeg', '.pjp')):
            ext = 'jpg'
        elif (self.extension == '.tiff'):
            ext = 'tif'
        else:
            ext = self.extension

        return F'image/{ext}'

    def from_abspath(abspath: str)->_File:
        if not os.path.isfile:
            raise FileNotFoundError('path not set to directory')

        img = PictureFile()
        img.name = os.path.split(abspath)[-1]

        stats = os.stat(abspath)
        img.size = stats.st_size

        # datetime.fromtimestamp(stats.st_ctime).strftime('%d-%b-%Y (%H:%M:%S)')
        img.ctime = stats.st_ctime
        img.atime = stats.st_atime
        img.mtime = stats.st_mtime

        with Image.open(abspath) as _img:
            width, height = _img.size
            img.width = width
            img.height = height

        return img

def _get_extension(abspath: str)->str:
    filename = os.path.split(abspath)
    index = filename.rindex('.')
    return filename[rindex::]

def file_from_abspath(abspath: str)->_File:
    if not os.path.isfile:
        raise FileNotFoundError('path not set to directory')

    filename = os.path.split(abspath)[-1]
    rindex = filename.rindex('.')
    ext = filename[rindex::]

    if (ext in PictureFile.extensions):
        return PictureFile.from_abspath(abspath)
    elif (ext in AudioFile.extensions):
        return AudioFile.from_abspath(abspath)
    elif (ext in VideoFile.extensions):
        return VideoFile.from_abspath(abspath)
    else:
        return AnyFile.from_abspath(abspath)