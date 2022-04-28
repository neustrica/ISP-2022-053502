FROM python:latest

WORKDIR /app/lab1

COPY /lab1 /app/lab1/

CMD ["python3", "lab1_isp.py"]
