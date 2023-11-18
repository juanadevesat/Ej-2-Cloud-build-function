FROM python:3.12.0-alpine3.18

WORKDIR /
COPY web web/
WORKDIR /web/

RUN sudo pip install -r "requirements.txt"

CMD ["python", "app.py"]
