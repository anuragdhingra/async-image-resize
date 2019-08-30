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
