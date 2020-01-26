import os
import sys
import werkzeug.exceptions as wexs

from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from filemanager import FileType, AnyFile, VideoFile, AudioFile, PictureFile, file_from_abspath
from http_errors import HttpError

HOME_PATH = 'D:' + os.sep

app = Flask(__name__)

@app.errorhandler(wexs.Forbidden)
def handle_forbbiden(e):
    return 'Forbbiden', 403

@app.errorhandler(wexs.BadRequest)
def handle_bad_request(e):
    return 'Bad Request', 400

@app.errorhandler(wexs.NotFound)
def handle_not_found(e):
    return render_template('error.html', error=HttpError.error404()), 404

@app.route('/')
@app.route('/<path:varargs>')
def index(varargs: str = '/'):
    current = os.path.join(HOME_PATH, varargs)
    current = os.path.abspath(current)

    varargs = os.fspath(varargs)
    varargs = varargs.replace('/', os.sep)
    paths = varargs.split(os.sep)
    
    dirs = []
    files = []
    folder_size = 0

    try:
        for path in os.listdir(current):
            abspath = os.path.join(current, path)

            if os.path.isdir(abspath):
                dirs.append(path)

            elif os.path.isfile(abspath):
                pathfile = file_from_abspath(abspath)
                folder_size += pathfile.size
                files.append(pathfile)

        return render_template('index.html', paths=paths, dirs=dirs, files=files)

    except FileNotFoundError:
        raise wexs.NotFound() 

@app.route('/__parent__')
@app.route('/__parent__/')
@app.route('/__parent__/<path:varargs>')
def find_parent(varargs: str = ''):
    if (varargs == ''):
        return redirect(url_for('index'))

    abspath = HOME_PATH + varargs
    abspath = os.path.abspath(os.path.join(abspath, os.pardir))

    new_path = os.path.relpath(abspath, HOME_PATH)
    new_path = new_path.replace(os.sep, '/')

    return redirect(url_for('index', varargs=new_path))

def upload_file(root: str, save_path: str = ''):
    if ('file' not in request.files):
        # flash('No file part')
        return redirect(request.url)
    
    upload = request.files['file']
    if (upload.filename == ''):
        # flash('No selected file')
        return redirect(request.url)

    full_path = os.path.join(root, save_path)
    if (upload and is_valid_format(upload.filename, FileType.ANY)):
        if ('filename' in request.form.keys()):
            if (request.form['filename'] == ''):
                filename = secure_filename(upload.filename)
            else:
                ext = get_file_extension(upload.filename)
                filename = secure_filename(request.form['filename'] + ext)
        else:
            filename = secure_filename(upload.filename)

        assert filename != ''   
        upload.save(os.path.join(full_path, filename))
        return redirect(request.url)

    raise wexs.BadRequest()

@app.route('/__delete__/<path:varargs>')
def remove_file(varargs: str = ''):
    abspath = os.path.join(HOME_PATH, path)
    parent = os.path.join(abspath, os.pardir)
    try:
        if (os.path.isfile(full_path)):
            os.remove(full_path)
            return redirect(url_for('index', varargs=abspath))

        elif (os.path.isdir(full_path)):
            full_path = full_path.replace('/', os.sep)

            cmd = 'rmdir /Q /S ' + full_path 
            os.system(cmd)

            return redirect(url_for('index', varargs=parent))

        else:
            raise OSError('Path is neither a file nor directory')

    except OSError as e:
        raise wexs.Forbidden(e)

    raise wexs.BadRequest()


    varargs = varargs.strip('/')

    dirs = []
    files = []
    folder_size = 0
    folder_path = MUSIC_PATH
    current = ''

    if (varargs != ''):
        current = varargs + '/'
        folder_path = MUSIC_PATH + current

    try:
        for path in os.listdir(folder_path):
            abspath = folder_path + path
            if (os.path.isdir(abspath)):
                dirs.append({'relative': path, 'url': current + path})
            elif (os.path.isfile(abspath)):
                if (is_valid_format(path, FileType.AUDIO)):
                    atts = get_audio_attributes(abspath)
                    atts['name'] = path
                    files.append(atts)

                    folder_size += atts['size']

        return render_template('audio.html', dirs=dirs, files=files, folder_size=folder_size, current=current)

    except FileNotFoundError:
        raise wexs.NotFound()
    
@app.route('/__pictures__/<path:filename>/')
def send_imgs(filename):
    return send_file(IMGS_PATH, filename)

@app.route('/__music__/<path:filename>/')
def send_audio(filename):
    return send_file(MUSIC_PATH, filename)

@app.route('/__videos__/<path:filename>')
def send_video(filename):
    return send_file(VIDEOS_PATH, filename)

@app.route('/__docs__/<path:filename>')
def send_docs(filename):
    return send_file(DOCS_PATH, filename)

@app.route('/__file__/<path:abspath>/')
def send_file(abspath: str = ''):
    abspath = os.path.join(HOME_PATH, abspath)

    if not os.path.isfile(abspath):
        raise wexs.Forbidden()

    path, filename = os.path.split(abspath)
    return send_from_directory(path, filename)

if (__name__ == '__main__'):
    if (len(sys.argv) == 1 or sys.argv[1] == 'debug'):
        app.run(debug=True)
    elif (sys.argv[1] == 'server'):
        app.run('0.0.0.0', debug=True)
    elif (sys.argv[1] == 'deploy'):
        app.run('0.0.0.0', debug=False)