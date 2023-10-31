FROM python:3.10

WORKDIR /example

COPY . . 

CMD ["flask","run","--host","0.0.0.0"]