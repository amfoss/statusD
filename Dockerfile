FROM python:3.13-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Run the application.
CMD ["python3", "app.py"]
