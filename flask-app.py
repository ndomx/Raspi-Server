import os
import sys
import werkzeug.exceptions as wexs

from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from filemanager import get_file_extension, is_valid_format, get_image_attributes, get_audio_attributes, FileType
from http_errors import HttpError

run_on_windows = True

home_path = 'E:\\' if (run_on_windows) else '/home/pi/'
imgs_path = 'E:\\Pictures\\' if (run_on_windows) else '/home/pi/Pictures/'
videos_path = 'E:\\Videos\\' if (run_on_windows) else '/home/pi/Videos/'
music_path = 'E:\\Music\\' if (run_on_windows) else '/home/pi/Music/'
docs_path = 'E:\\Documents\\' if (run_on_windows) else '/home/pi/Documents/'

invalid_path = '__invalid__'
parent_path = '__parent__'

roots = {
    'home': home_path, 
    'pictures': imgs_path, 
    'videos': videos_path, 
    'music': music_path, 
    'docs': docs_path
}

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
def index():
    cdir = os.listdir(home_path)
    return render_template('index.html', files=cdir)

@app.route('/pictures', methods=['GET', 'POST'])
@app.route('/pictures/', methods=['GET', 'POST'])
@app.route('/pictures/<path:varargs>', methods=['GET', 'POST'])
def picture_folders(varargs: str = ''):
    if (request.method == 'GET'):
        return display_pictures(varargs)

    elif (request.method == 'POST'):
        return upload_file(imgs_path, varargs)

    else:
        raise wexs.MethodNotAllowed()

def display_pictures(varargs: str = ''):
    varargs = varargs.strip('/')

    dirs = []
    files = []
    folder_size = 0
    folder_path = imgs_path
    current = ''

    if (varargs != ''):
        current = varargs + '/'
        folder_path = imgs_path + current

    try:
        for path in os.listdir(folder_path):
            abspath = folder_path + path
            if os.path.isdir(abspath):
                dirs.append({'relative': path, 'url': current + path})
            elif os.path.isfile(abspath):
                if (is_valid_format(path, FileType.PICTURE)):
                    atts = get_image_attributes(abspath)
                    atts['name'] = path
                    files.append(atts)

                    folder_size += atts['size']

        return render_template('pictures.html', dirs=dirs, files=files, folder_size=folder_size, current=current)

    except FileNotFoundError:
        raise wexs.NotFound()

@app.route('/pictures/__parent__/')
@app.route('/pictures/__parent__')
@app.route('/pictures/__parent__/<path:varargs>')
def find_parent_pictures(varargs: str = '')->str:
    print('empty' if (varargs == '') else varargs)
    if (varargs == ''):
        return redirect(url_for('index'))

    abspath = imgs_path + varargs
    abspath = os.path.abspath(os.path.join(abspath, os.pardir))
    new_path = os.path.relpath(abspath, imgs_path)

    return redirect(url_for('picture_folders', varargs=new_path))

def upload_file(root: str, save_path: str = ''):
    if ('file' not in request.files):
        # flash('No file part')
        return redirect(request.url)
    
    upload = request.files['file']
    if (upload.filename == ''):
        # flash('No selected file')
        return redirect(request.url)

    full_path = os.path.join(root, save_path)
    if (upload and is_valid_format(upload.filename, FileType.PICTURE)):
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

@app.route('/__delete__/<root_folder>')
def remove_file(root_folder: str):
    if (root_folder not in roots.keys()):
        raise wexs.Forbidden()

    if ('filepath' not in request.args.keys()):
        # flash('No file part')
        return redirect(request.url)

    file_path = request.args['filepath']
    file_path = file_path.strip('/')
    if (file_path == ''):
        # flash('No selected file')
        return redirect(request.url)

    full_path = os.path.join(roots[root_folder], file_path)
    try:
        if (os.path.isfile(full_path)):
            os.remove(full_path)

        elif (os.path.isdir(full_path)):
            if (run_on_windows):
                full_path = full_path.replace('/', '\\')

            cmd = ('rmdir /Q /S ' if (run_on_windows) else 'rm -r ') + full_path 
            os.system(cmd)

        else:
            raise OSError('Path is neither a file nor directory')


        if ('urlpath' not in request.args.keys()):
            return redirect('/')
        else:
            return redirect(request.args['urlpath'])

    except OSError as e:
        raise wexs.Forbidden(e)

    raise wexs.BadRequest()

@app.route('/music')
@app.route('/music/')
@app.route('/music/<path:varargs>')
def audios(varargs: str = ''):
    varargs = varargs.strip('/')

    dirs = []
    files = []
    folder_size = 0
    folder_path = music_path
    current = ''

    if (varargs != ''):
        current = varargs + '/'
        folder_path = music_path + current

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
    return send_file(imgs_path, filename)

@app.route('/__music__/<filename>/')
def send_audio(filename):
    return send_file(music_path, filename)

@app.route('/<path>/<filename>/')
def send_file(path, filename):
    return send_from_directory(path, filename)

if (__name__ == '__main__'):
    if (len(sys.argv) == 1 or sys.argv[1] == 'debug'):
        app.run(debug=True)
    elif (sys.argv[1] == 'server'):
        app.run('0.0.0.0', debug=True)
    elif (sys.argv[1] == 'deploy'):
        app.run('0.0.0.0', debug=False)