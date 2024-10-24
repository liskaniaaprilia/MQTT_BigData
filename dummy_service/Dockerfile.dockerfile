FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install paho-mqtt
CMD ["python", "dummy_service.py"]
