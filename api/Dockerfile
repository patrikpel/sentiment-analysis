FROM python:3.10

RUN pip install notebook torch fastai pandas fastapi[standard] uvicorn supervisor

COPY ../ /home/

WORKDIR /home/notebook

CMD ["/usr/local/bin/supervisord", "-c", "/home/supervisord.conf"]

EXPOSE 8888 8000
