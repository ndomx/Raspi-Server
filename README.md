# Raspi-Server
Raspi-Server is a local cloud file hosting program, that exposes the RPi filesystem to the local network.

The app was made using [Flask](https://flask.palletsprojects.com/en/1.1.x/) and raw HTML, with most of the CSS provded by [Materialize](https://materializecss.com/).

## Usage
Install the required dependencies:
~~~bash
$ sudo apt install python3 python3-pip
$ pip3 install -r requirements.txt
~~~
And run the app:
~~~
python3 flask-app.py
~~~