#!/usr/bin/env python
from cv2 import VideoCapture, imencode, resize

# "/vstream/test-stand/0" is just a test channel
web_cam_url = {"0": "http://188.178.124.160:80/mjpg/video.mjpg"}


class Camera_from_url(object):
    """Camera_from_url captures video from a <url>.mjpg source
    using open cv2 "VideoCapture" and encodes it as jpeg using imencode

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
