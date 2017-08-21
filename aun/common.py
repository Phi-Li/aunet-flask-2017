# common function
import time
import random
from io import BytesIO
from urllib import request
import os
import base64
from bs4 import BeautifulSoup
from PIL import Image

from flask_restful import abort


def abort_if_not_exist(data, message):
    """ 
    if data doesn't exists, then raise 404
    """
    if data is None:
        abort(404, message="{} Not Found".format(message))


def abort_if_exist(data, message):
    """ 
    if data already exists, then raise 400
    """
    if data != None:
        abort(
            400, message="{} has existed ,please try another".format(message))


def abort_if_unauthorized(message):
    """ 
    if don't have permission, then then raise 401
    """
    abort(401, message="{} permission Unauthorized".format(message))


def handle_html(html):
    """ 
    change the img url into dataurl ,and return the first image
    """
    soup = BeautifulSoup(html, "html.parser")
    image_num = 0  # judge if  these
    for img in soup.find_all('img'):
        imgurl = img.get('src')
        data = request.urlopen(imgurl).read()
        img_buf = BytesIO(data)  # change image in ram to batesIo
        i = Image.open(img_buf)
        filename = str(int(random.uniform(1, 1000)+time.time()))+".png"
        path = os.path.join(
            aun_app.config['BASEDIR'], 'aunet/static/Uploads/News', filename)
        i.save(path, quality="192")
        with open(path, "rb") as f:
            data = f.read()
        data = base64.b64encode(data)  #
        data = str(data)
        data = data[2:-1]
        data = "data:image/jpg;base64,"+data
        img['src'] = data
        # return img
        image_num = image_num+1
        if image_num > 1:
            # remove extra images, only save the first image
            os.remove(path)
        else:
            img_url_first = "static/Uploads/News/"+filename
    if image_num == 0:
        # the default image file
        img_url_first = "static/Uploads/News/default.jpg"
    return soup, img_url_first


def dataurl_to_img(img_url):
    """ 
    change imgurl into img and save it ,and save the path to the database
    """

    data = request.urlopen(img_url).read()
    img_buf = BytesIO(data)
    img = Image.open(img_buf)
    filename = str(int(random.uniform(1, 1000)+time.time()))+".png"
    path = os.path.join(
        aun_app.config['BASEDIR'], 'aunet/static/Uploads/News', filename)
    img.save(path, quality="192")
    return 'static/Uploads/News/'+filename
