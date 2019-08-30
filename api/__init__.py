from flask_restful import Api

from app import app
from .ResizeImage import ResizeImage

restServer = Api(app)
restServer.add_resource(ResizeImage, "/api/v1/resize")