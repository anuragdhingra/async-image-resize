from flask_restful import Api

from app import flaskAppInstance
from .Image import Image

restServer = Api(flaskAppInstance)
restServer.add_resource(Image, "/api/v1/resize")