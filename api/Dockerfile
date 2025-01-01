FROM python:3.10

RUN pip install torch fastai pandas fastapi[standard] supervisor

COPY ../ /home/

WORKDIR /home

CMD ["/usr/local/bin/supervisord", "-c", "/home/supervisord.conf"]

EXPOSE 8888 8000
