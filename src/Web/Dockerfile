FROM python:3.10
WORKDIR /code
COPY ./src/Web/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src/Web .
EXPOSE 8000
ENTRYPOINT ["gunicorn", "app:app"]