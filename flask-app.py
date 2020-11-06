import os
import sys
import werkzeug.exceptions as wexs

from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from filemanager import FileType, AnyFile, VideoFile, AudioFile, PictureFile, file_from_abspath
from http_errors import HttpError

HOME_PATH = '/home/pi' + os.sep

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
                try:
                    pathfile = file_from_abspath(abspath)
                except OSError:
                    continue
                finally:
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

@app.route('/__delete__/<path:full_path>')
def remove_file(full_path: str = ''):
    abspath = os.path.join(HOME_PATH, full_path)

    if not (os.path.exists(abspath)):
        raise wexs.BadRequest()

    try:
        if (os.path.isfile(abspath)):
            absdir = os.path.dirname(full_path)
            os.remove(abspath)
            return redirect(url_for('index', varargs=absdir))

        elif (os.path.isdir(abspath)):
            abspath = abspath.replace('/', os.sep)

            cmd = f'rmdir /Q /S "{abspath}"'
            code = os.system(cmd)

            assert code == 0, f'Process returned with code {code}. Failed to remove folder'

            parent = os.path.join(full_path, os.pardir)
            parent = os.path.normpath(parent)

            return redirect(url_for('index', varargs=parent))

        else:
            raise OSError('Path is neither a file nor directory')

    except OSError as e:
        raise wexs.Forbidden(e)

    except AssertionError as e:
        raise wexs.BadRequest(e)

    raise wexs.BadRequest('Unknown error!')

@app.route('/__file__/<path:abspath>/')
def send_file(abspath: str = ''):
    abspath = os.path.join(HOME_PATH, abspath)

    if not os.path.isfile(abspath):
        raise wexs.Forbidden()

    path, filename = os.path.split(abspath)
    return send_from_directory(path, filename)

@app.route('/<path:save_path>', methods=['POST'])
def upload_file(save_path: str = ''):
    try:
        assert 'file' in request.files, 'No file part'

        upload = request.files['file']
        assert upload, 'Whoops, could get file!'

        filename = ''
        if 'filename' in request.form.keys():
            if request.form['filename'] == '':
                filename = secure_filename(upload.filename)
            else:
                ext = os.path.splitext(upload.filename)[-1]
                filename = secure_filename(request.form['filename'] + ext)

        else:
            filename = secure_filename(upload.filename)

        assert filename != '', 'File cannot have empty name'

        folder_path = os.path.join(HOME_PATH, save_path)
        abspath = os.path.join(folder_path, filename)
        assert not os.path.exists(abspath), 'Cannot overwrite existing files'

        upload.save(abspath)
        return redirect(request.url)

    except AssertionError as e:
        # TODO: Add logic to assertion errors
        raise wexs.BadRequest(e)

if (__name__ == '__main__'):
    if (len(sys.argv) == 1 or sys.argv[1] == 'debug'):
        app.run(debug=True)
    elif (sys.argv[1] == 'server'):
        app.run('0.0.0.0', debug=True)
    elif (sys.argv[1] == 'deploy'):
        app.run('0.0.0.0', debug=False)