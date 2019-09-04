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
            "token": "6f4e0a68-40a5-4b44-b47e-49db86dcce72"
        }
        ```   
- **GET** `http://localhost:5000/api/v1/status`

    Headers 
     `Content-Type: application/json`
     
    Request Body

        ```
        {
            "token": "6f4e0a68-40a5-4b44-b47e-49db86dcce72"
        }
        ``` 
    Response

        ```
        {
            "status": SUCESSS,
            "resized_image_url": "f1c2e157-7b4c-4855-9e74-be3c9d71df17.jpg"
        }
        ```
