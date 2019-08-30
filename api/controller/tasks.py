from celery import Celery
from PIL import Image
import logging
import uuid
import base64
import os

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

@celery.task()
def async_resize(file_uuid,img_string):
    logger.info("Started resizing...")

    temp_filename = file_uuid + "_temp.jpg"

    with open(temp_filename, "wb") as fh:
        fh.write(base64.decodebytes(img_string.encode()))
    img = Image.open(temp_filename) 

    #for .png images where there is no alpha
    rgb_img = img.convert('RGB')
    new_filename = file_uuid + ".jpg"
    new_img = rgb_img.resize((100,100), Image.ANTIALIAS)
    new_img.save(new_filename,'JPEG',optimize=True, quality=100)

    logger.info("Completed resizing...")

    #remove the temporary file
    try:
        os.remove(temp_filename)
    except OSError:
        pass
    return "Saved as: " + new_filename
