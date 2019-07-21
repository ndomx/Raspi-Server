import os
import sys

from flask import Flask, render_template, send_from_directory, Response
from process_imgs import is_valid_img_format, get_image_attributes

run_on_windows = True

home_path = 'E:\\' if (run_on_windows) else '/home/pi/'
imgs_path = 'E:\\Pictures\\' if (run_on_windows) else '/home/pi/Pictures/'
videos_path = 'E:\\Videos\\' if (run_on_windows) else '/home/pi/Videos/'
music_path = 'E:\\Music\\' if (run_on_windows) else '/home/pi/Music/'
docs_path = 'E:\\Documents\\' if (run_on_windows) else '/home/pi/Documents/'

app = Flask(__name__)

@app.route('/')
def index():
    cdir = os.listdir(home_path)
    return render_template('index.html', files=cdir)

@app.route('/pictures')
def display_pictures():
    dirs = []
    files = []
    folder_size = 0
    for path in os.listdir(imgs_path):
        abspath = imgs_path + path
        if os.path.isdir(abspath):
            dirs.append(path)
        elif os.path.isfile(abspath):
            if (is_valid_img_format(path)):
                atts = get_image_attributes(abspath)
                atts['name'] = path
                files.append(atts)

                folder_size += atts['size']

    return render_template('pictures.html', dirs=dirs, files=files, folder_size=folder_size)

@app.route('/pictures/<dir_path>')
def display_pictures_dir(dir_path):
    dirs = []
    files = []
    folder_size = 0
    for path in os.listdir(imgs_path):
        abspath = imgs_path + path
        if os.path.isdir(abspath):
            dirs.append(path)
        elif os.path.isfile(abspath):
            if (is_valid_img_format(path)):
                atts = get_image_attributes(abspath)
                atts['name'] = path
                files.append(atts)

                folder_size += atts['size']

    return render_template('pictures.html', dirs=dirs, files=files, folder_size=folder_size)

@app.route('/music')
def audios():
    return render_template('audio.html')

@app.route('/imgs/<filename>')
def send_imgs(filename):
    return send_file(imgs_path, filename)

@app.route('/<path>/<filename>')
def send_file(path, filename):
    return send_from_directory(path, filename)

if (__name__ == '__main__'):
    if (len(sys.argv) == 1 or sys.argv[1] == 'debug'):
        app.run(debug=True)
    elif (sys.argv[1] == 'server'):
        app.run('0.0.0.0', debug=True)
    elif (sys.argv[1] == 'deploy'):
        app.run('0.0.0.0', debug=False)