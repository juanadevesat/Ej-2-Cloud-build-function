FROM python:3.12.0-alpine3.18

COPY web web/
WORKDIR web/

RUN pip install -r "requirements.txt"

CMD ["python", "app.py"]
