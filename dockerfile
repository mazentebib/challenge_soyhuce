FROM python:3.12.0rc2

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "get_data.py"]  # Replace "get_data.py" with your script name
