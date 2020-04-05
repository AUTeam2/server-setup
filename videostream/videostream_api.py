#!/usr/bin/env python
import os
from flask import Flask, request
from flask import render_template, Response
from flask_restful import Resource, Api

from src.videostream_handler import Camera_from_url, web_cam_url

app = Flask(__name__)
api = Api(app)
app.config.from_object(os.environ['APP_SETTINGS'])

test_stand_id = 0


class Init_Webcam(Resource):
    def get(self, ts_id):
        test_stand_id = web_cam_url.get(ts_id)
        return {ts_id: web_cam_url[ts_id]}

    def put(self, ts_id):
        web_cam_url[ts_id] = request.form['data']
        test_stand_id = web_cam_url.get(ts_id)
        return {ts_id: web_cam_url[ts_id]}


def gen(stream):
    while True:
        frame = stream.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    global test_stand_id
    if test_stand_id is None:
        nothing_to_do = "yes"
    else:
        stream = Camera_from_url()
        stream.init_teststand(test_stand_id)
        return Response(gen(stream),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


api.add_resource(Init_Webcam, '/install-test-stand/<path:ts_id>')


@app.route('/vstream-direct/test-stand/<string:ts_id>')
def index_vstream2(ts_id):
    global test_stand_id

    test_stand_id = web_cam_url.get(ts_id)

    stream = Camera_from_url()
    stream.init_teststand(test_stand_id)
    return Response(gen(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    # if test_stand_id == "":
    #     test_stand_id = None
    # if test_stand_id is not None:
    #     return render_template('videostream/videostream.html')
    # else:
    #     return render_template('videostream/videostream-not-installed.html')




@app.route('/vstream/test-stand/<string:ts_id>')
def index(ts_id):
    global test_stand_id
    test_stand_id = web_cam_url.get(ts_id)
    if test_stand_id == "":
        test_stand_id = None
    if test_stand_id is not None:
        return render_template('videostream/videostream.html')
    else:
        return render_template('videostream/videostream-not-installed.html')


@app.route('/')
def index2():
    return render_template('videostream/videostream-not-installed.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
