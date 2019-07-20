import os
import sys
from flask import Flask, request, render_template, send_from_directory

home_path = '/home/pi/'
imgs_path = 'E:\\Pictures\\' # home_path + '/Pictures/'
videos_path = home_path + '/Videos/'
music_path = home_path + '/Music/'
docs_path = home_path + '/Documents/'

app = Flask(__name__)

@app.route('/')
def index():
    cdir = os.listdir(home_path)
    return render_template('index.html', files=cdir)

@app.route('/pictures')
def display_img():
    dirs = []
    files = []
    for path in os.listdir(imgs_path):
        if os.path.isdir(imgs_path + path):
            dirs.append(path)
        elif os.path.isfile(imgs_path + path):
            files.append(path)
    return render_template('pictures.html', dirs=dirs, files=files)

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