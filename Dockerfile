FROM python:3.8

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./eat_db /eat_db

CMD ["uvicorn", "eat_db.api.main:APP", "--host", "0.0.0.0", "--port", "80"]
