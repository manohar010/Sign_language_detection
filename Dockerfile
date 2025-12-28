# Use Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for OpenCV and Camera
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files (including runs/ folder)
COPY . .

# Expose Port 8080
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]