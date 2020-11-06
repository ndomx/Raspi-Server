# Raspi-Server
Raspi-Server is a local cloud file hosting program, that exposes the RPi filesystem to the local network. You can upload and download files. The app also support media files, and they can be reproduced without having to download them.

The app was made using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and raw HTML, with most of the CSS provded by [Materialize](https://materializecss.com/).

## Usage
Install the required dependencies:
~~~bash
$ sudo apt install python3 python3-pip
$ pip3 install -r requirements.txt
~~~
And run the app:
~~~bash
$ python3 flask-app.py # run debug version
$ python3 flask-app.py server # run debug version
$ python3 flask-app.py deploy # deploy program
~~~