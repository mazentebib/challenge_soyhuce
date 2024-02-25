FROM python:3.12.0rc2

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Execute get_data.py and then data_viz.py sequentially
CMD ["bash", "-c", "python get_data.py && python data_viz.py"]
