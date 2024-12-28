FROM python:3.10

RUN pip install notebook torch fastai pandas fastapi uvicorn

COPY ../ /home/

WORKDIR /home/

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.password=''"]

EXPOSE 8888 8000