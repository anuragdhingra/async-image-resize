# cogent-assignment
BE engineering assignment for cogent labs

## Starting the application
```docker
docker-compose up
```
This would spin up three containers:
- image_resize_api @ localhost:5000
- redis_broker @ localhost:6379
- celery_worker 

## API
- **POST** `http://localhost:5000/api/v1/resize`

    Headers 
     `Content-Type: application/json`
     
    Request Body

        ```
        {
            "imageData": "base64 encoded image"
        }
        ``` 
     Response

        ```
        {
            "success": true,
            "token": "Type-5 UUID(same as task-id)"
        }
        ``` 
    Example - 

    REQUEST: `curl http://localhost:5000/api/v1/resize  -d @request.json -H "Content-Type: application/json"`

    RESPONSE: `{"success":true,"token":"bce0e926-f6b4-4e7d-ada3-0548d0a1c2b6"}`
    
- **GET** `http://localhost:5000/api/v1/resize/<token>`
     
    Response

        ```
        {
            "status": SUCESSS,
            "resized_image_url": "image_url"
        }
        ```
    Example - 
    REQUEST: `curl http://localhost:5000/api/v1/resize`

    RESPONSE: `{"resized_image_url":"72a77200-18e4-4df1-992b-d4f80c26c739.jpg","status":"SUCCESS"}`

## Testing
Before running the tests please install the following in your local environment or you may also activate a fresh virtual environment to install these.
- `pip install nose mock`
>Using `nose` to discover and run tests. `mock` is being used to inject/mock testing configuration while instantiating the app.

Run the tests using: `nosetests tests/test_api.py`
> Please make sure as to start the server using `docker-compose up` before running them.

## Structure
The repo has the following structure:
- `api/` 
  - `api/factory.py` responsible for app and worker instantiation, each of them can be instantiated independently thus allowing loose coupling
  - `api/controller/routes.py` defines the endpoints
  - `api/controller/tasks.py` defines Celery tasks
- `tests/`
  - `tests/test_api.py` contains all the tests for the apis
- `app.py` is the entry point for starting the Flask app server
- `worker.py` is the entry point for the Celery worker
- `requirements.txt` is the list of python dependencies for pip
- `docker-compose.yml` all the service containers
- `Dockerfile` is the image for the app & celery worker

#### Dependencies
 - `flask` - micro web application framework, makes getting started quick and easy. Using the inbuilt server too.
 - `pillow` - python imaging library, used for resizing the image
 - `celery` - distributed task queue used for asynchronous task processing
 - `redis` - used as a message broker as well as the result backend for celery to communicate with the flask server.

## Architecture/Flow
![flask-celery-redis.png](https://github.com/anuragdhingra/cogent-assignment/blob/develop/flask-celery-redis.png)
- To implement the long-running tasks in application's work flow to resize images we should handle these tasks in the background, outside the basic application flow as a separate worker process.
- As an image is sent via a request to our flask server, it passes the task of resizing off to a task queue and immediately sends back a `token` i.e same as the `task-id` as a response back to the client.
- Flask server connects to the Redis message broker and the message broker talks to the Celery worker.Celery communicates via messages, usually using a broker to mediate between clients and workers. 
- Celery worker then identifies the methods decorated with `@celery.task` and runs them asynchronously updating the status of tasks to redis container also used as a result backend.


## Improvements
#### Application:
- The current application doesn't supports different configurations for different environment configurations like development, staging, production etc. We could implement it using a separate `config.py` module which would define these properties for different environments.
- The current also lacks error handling, logging modes and handling the corner cases (example- image sent as the request is too large or of size zero or corrupted) which is a must for a production grade application. Similarily 
- There is no persistent data storage used by the application, so we could use something like MySQL/PostgreSQL to persist task related data. We might also need some tool to manage the migrations.
- The application also lacks basic authentication/authorization which could be implemented. APIs should validate requests to contain basic security headers/keys.

#### Testing:
- There are no independent unit tests written thus currently we need the start the server running to test the entire flow of the API and its integration with the task-queue.
- Tests also lack to check the corner cases as defined above, which needs to be included.
- To unit test the asynchronous tasks we can run those methods synchronously. 

#### Infra
- Although Flask has a built-in web server, it’s not suitable for production and needs to be put behind a real web server able to communicate with Flask through a WSGI protocol. A common choice for that is Gunicorn— a Python WSGI HTTP server.
- While being an HTTP web server, Gunicorn, is not suited to face the web. That’s why we need Nginx as a reverse proxy and to serve static files. In case we need to scale up our application to multiple servers, Nginx will take care of load balancing as well.
- Currently, the resized images are created in a shared docker volume, assigned while creating the services. In a real-life application scenario, we'd require to upload these images to a object storage service(example- S3, Google cloud storage) and access them via a CDN. 

#### Other
- Monitoring of celery workers is also not implemented, for which we could use [Flower](https://flower.readthedocs.io/en/latest/). Flower also supports basic HTTP auth, oAuth and can also be used to manage the worker pool size and auto scale settings.
- The current application lacks continuous integration and continuous deployment.







