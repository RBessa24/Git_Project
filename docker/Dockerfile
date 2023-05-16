FROM python:3.9-slim

COPY ./api /app

WORKDIR /app
 
RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
