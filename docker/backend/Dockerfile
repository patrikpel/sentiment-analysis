FROM python:3.13

RUN pip install notebook

COPY ../ /home/

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

EXPOSE 8888