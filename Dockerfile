FROM python:3.11-alpine

WORKDIR /app

# Install dependencies first (this caches the downloads to speed up future builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
