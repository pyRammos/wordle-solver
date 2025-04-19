FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure we don't copy the venv directory
RUN rm -rf venv

EXPOSE 5000

CMD ["python", "app.py"]
