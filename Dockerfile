FROM python:3.10

WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install system packages, including libGL
RUN apt-get update && \
    apt-get install -y zip unzip libgl1 ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

CMD ["python3", "-m", "group_bot"]
