FROM python:3.12.0rc2

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Expose port 8050 to the outside world
EXPOSE 8050

ENV PYTHONPATH='.'

# Execute get_data.py and then data_viz.py sequentially
CMD ["bash", "-c", " python data_manipulation/get_data.py && python data_analysis/data_viz.py"]
