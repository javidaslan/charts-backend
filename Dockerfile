FROM python:3

USER root
COPY ./ /opt/src
WORKDIR /opt/src
RUN pip install -r requirements.txt

CMD ["python", "app.py"]