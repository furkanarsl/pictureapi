FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app/
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY ./src/ ./src
ENV MODULE_NAME=src.main
RUN mkdir saved