from __future__ import print_function
import requests
import json
import cv2

addr = 'http://192.168.43.47:8888'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}
# capture = cv2.VideoCapture(0)
# ret, frame = capture.read()
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
while 1:
    img = cv2.imread('2.png')
    # ret, img = capture.read()
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img, encode_param)
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    # decode response
    print(json.loads(response.text))

# expected output: {u'message': u'image received. size=124x124'}