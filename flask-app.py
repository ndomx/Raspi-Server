import os
import sys
import werkzeug.exceptions as wexs

from flask import Flask, render_template, send_from_directory, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from process_imgs import is_valid_img_format, get_image_attributes
from http_errors import HttpError

run_on_windows = True

home_path = 'E:\\' if (run_on_windows) else '/home/pi/'
imgs_path = 'E:\\Pictures\\' if (run_on_windows) else '/home/pi/Pictures/'
videos_path = 'E:\\Videos\\' if (run_on_windows) else '/home/pi/Videos/'
music_path = 'E:\\Music\\' if (run_on_windows) else '/home/pi/Music/'
docs_path = 'E:\\Documents\\' if (run_on_windows) else '/home/pi/Documents/'

invalid_path = '__invalid__'
parent_path = '__parent__'

app = Flask(__name__)

def get_root_dir(folder: str)->str:
    if (folder == 'pictures'):
        return imgs_path
    elif (folder == 'videos'):
        return videos_path
    elif (folder == 'music'):
        return music_path
    elif (folder == 'docs'):
        return docs_path
    else:
        return invalid_path

@app.errorhandler(wexs.Forbidden)
def handle_forbbiden(e):
    return 'Forbbiden', 403

@app.errorhandler(wexs.BadRequest)
def handle_bad_request(e):
    return 'Bad Request', 400

@app.errorhandler(wexs.NotFound)
def handle_not_found(e):
    return render_template('404.html', error=HttpError.error404()), 404

@app.route('/')
def index():
    cdir = os.listdir(home_path)
    return render_template('index.html', files=cdir)

@app.route('/pictures')
@app.route('/pictures/')
@app.route('/pictures/<path:varargs>')
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

    for path in os.listdir(folder_path):
        abspath = folder_path + path
        if os.path.isdir(abspath):
            dirs.append({'relative': path, 'url': current + path})
        elif os.path.isfile(abspath):
            if (is_valid_img_format(path)):
                atts = get_image_attributes(abspath)
                atts['name'] = path
                files.append(atts)

                folder_size += atts['size']

    return render_template('pictures.html', dirs=dirs, files=files, folder_size=folder_size, current=current)

@app.route('/pictures/__parent__/')
@app.route('/pictures/__parent__')
@app.route('/pictures/__parent__/<path:varargs>')
def find_parent(varargs: str = '')->str:
    print('empty' if (varargs == '') else varargs)
    if (varargs == ''):
        return redirect(url_for('index'))

    abspath = imgs_path + varargs
    abspath = os.path.abspath(os.path.join(abspath, os.pardir))
    new_path = os.path.relpath(abspath, imgs_path)

    return redirect(url_for('display_pictures', varargs=new_path))

@app.route('/uploads/<folder>', methods=['POST'])
@app.route('/uploads/<folder>/', methods=['POST'])
@app.route('/uploads/<folder>/<path:save_path>', methods=['POST'])
def upload_picture(folder: str, save_path: str = ''):
    root = get_root_dir(folder)
    if (root == invalid_path):
        raise wexs.Forbidden()

    if ('file' not in request.files):
        flash('No file part')
        return redirect(request.url)
    
    upload = request.files['file']
    if (upload.filename == ''):
        flash('No selected file')
        return redirect(request.url)

    full_path = os.path.join(root, save_path)
    if (upload and is_valid_img_format(upload.filename)):
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(full_path, filename))
        return redirect(request.url)

    raise wexs.BadRequest()


@app.route('/music/')
def audios():
    return render_template('audio.html')

@app.route('/imgs/<filename>/')
def send_imgs(filename):
    return send_file(imgs_path, filename)

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