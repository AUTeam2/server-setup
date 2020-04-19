#!/usr/bin/env python
from cv2 import VideoCapture, imencode, resize

# Static import of webcam settings from Webinterface
WEBINTERFACE_PATH = "/usr/src/webinterface/"

import sys
sys.path.append(WEBINTERFACE_PATH)
from webinterface.settings import CAMS

# Build a structure similar to that implemented by Daniel
# but using data from the Webinterface. Will look similar to:
# web_cam_url = {
#     "0": "http://188.178.124.160:80/mjpg/video.mjpg",
#     "1": "http://soemon-cho.miemasu.net:63107/nphMotionJpeg?Resolution=640x480&Quality=Motion",
# }
web_cam_url = dict([(entry[1]["id"], entry[1]["src"]) for entry in CAMS.items()])

class Camera_from_url(object):
    """
    Camera_from_url captures video from a <url>.mjpg source
    using open cv2 "VideoCapture" and encodes it as jpeg using imencode

    Janus 23/3/2020 - This needs to be a static object of a sort, otherwise
    we will be opening multiple streams to the test stand if there are multiple
    viewers. That is redudant load on the test stand.

    :param object: <URL>.mjpg
    :type object: mjpg
    :return: jpeg in raw bytes
    :rtype: bytes
    """

    def __init__(self):
        nothing_to_do = "yes"

    def init_teststand(self, url):
        if url is None:
            self.video = None
        elif url is not None:
            self.video = VideoCapture(url)

    def __del__(self):
        if self.video is None:
            nothing_to_do = "yes"
        else:
            self.video.release()

    def get_frame(self):
        _, image = self.video.read()
        image = resize(image, (1920, 1080))
        _, jpeg = imencode('.jpg', image)
        return jpeg.tobytes()
