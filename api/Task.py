from flask_restful import reqparse, Resource
import logging as logger
import base64
import flask

parser = reqparse.RequestParser()
parser.add_argument('imageData', type=str)

class Task(Resource):

    def post(self):
        logger.debug("POST Image")
        arg =   parser.parse_args()
        string = arg['imageData']
        with open("testImage.png", "wb") as fh:
            fh.write(base64.decodebytes(string.encode()))
        return {"message": "Done"},200
