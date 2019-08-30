FROM python:3
MAINTAINER Anurag Dhingra <anuragdhingra101@gmail.com>

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
