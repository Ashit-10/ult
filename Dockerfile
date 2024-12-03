FROM python:3.9-slim


WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install system packages, including libGL
RUN apt-get update && \
    apt-get install -y zip unzip libgl1 ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y build-essential

# Copy the rest of the application
COPY . .

CMD ["python", "-m", "group_bot"]
