#!/usr/bin/env python
from flask import Flask
from flask import render_template, Response
# from flask_restful import Resource, Api

from src.videostream_handler import Camera_from_url

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('videostream/videostream.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera_from_url()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555, debug=True)
