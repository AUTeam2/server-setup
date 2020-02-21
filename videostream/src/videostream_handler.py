#!/usr/bin/env python
from cv2 import VideoCapture, imencode, resize


class Camera_from_url(object):
    """Camera_from_url captures video from a <url>.mjpg source
    using open cv2 "VideoCapture" and encodes it as jpeg using imencode

    :param object: <URL>.mjpg
    :type object: mjpg
    :return: jpeg in raw bytes
    :rtype: bytes
    """

    def __init__(self):
        self.video = VideoCapture(
            'http://188.178.124.160:80/mjpg/video.mjpg')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, image = self.video.read()
        image = resize(image, (1920, 1080))
        _, jpeg = imencode('.jpg', image)
        return jpeg.tobytes()
