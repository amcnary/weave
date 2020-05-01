FROM python:2.7
COPY . /directory_app
WORKDIR /directory_app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]