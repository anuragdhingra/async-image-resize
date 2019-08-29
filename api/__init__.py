from flask_restful import Api

from app import flaskAppInstance
from .ResizeImage import ResizeImage

restServer = Api(flaskAppInstance)
restServer.add_resource(ResizeImage, "/api/v1/resize")