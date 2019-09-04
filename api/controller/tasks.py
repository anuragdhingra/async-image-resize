from celery import Celery
from PIL import Image
import logging
import base64
import os
import time

logger = logging.getLogger()
celery = Celery(__name__, autofinalize=False)

# Task to resize the image
@celery.task(bind=True)
def async_resize(self,file_uuid,img_string):
    logger.info("Started resizing...")
    self.update_state(state='IN_PROGRESS', meta=None)

    img_str = img_string.split("base64,",1)[1]
    temp_filename = file_uuid + "_temp.jpg"

    with open(temp_filename, "wb") as fh:
        fh.write(base64.decodebytes(img_str.encode()))
    img = Image.open(temp_filename) 

    # For .png images where there is no alpha
    rgb_img = img.convert('RGB')
    new_filename = file_uuid + ".jpg"
    new_img = rgb_img.resize((100,100), Image.ANTIALIAS)
    new_img.save(new_filename,'JPEG',optimize=True, quality=100)

    # Sleep to test task status
    time.sleep(20)
    logger.info("Completed resizing...")

    # Remove the temporary file
    try:
        os.remove(temp_filename)
    except OSError:
        pass
    return new_filename


def check_status(task_id):
    task = celery.AsyncResult(task_id)
    state = {'status': task.status, 'info': task.info}
    return state
