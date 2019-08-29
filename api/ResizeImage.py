from flask_restful import reqparse, Resource
from PIL import Image
import logging as logger
import base64
import flask
import os
import uuid

parser = reqparse.RequestParser()
parser.add_argument('imageData', type=str, location='json',required=True)

class ResizeImage(Resource):

    def post(self):
        logger.debug("POST Image")
        arg =   parser.parse_args()
        img_string = arg['imageData']
        new_file_uuid = str(uuid.uuid4())

        temp_filename = new_file_uuid + "_temp.jpg"
        with open(temp_filename, "wb") as fh:
            fh.write(base64.decodebytes(img_string.encode()))
        img = Image.open(temp_filename)  

        #for .png images where there is no alpha
        rgb_img = img.convert('RGB')
        new_filename = new_file_uuid + ".jpg"
        new_img = rgb_img.resize((100,100), Image.ANTIALIAS)
        new_img.save(new_filename,'JPEG',optimize=True, quality=100)

        #remove the temporary file
        try:
            os.remove(temp_filename)
        except OSError:
            pass

        return {"success": "true", "token": new_file_uuid},200
