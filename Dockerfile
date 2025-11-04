FROM python:3.12-slim
ENV TZ="Europe/Moscow"

WORKDIR /home/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      libffi-dev \
      zbar-tools \
      postgresql-client \
      ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -U -r requirements.txt
COPY . .
CMD ["faststream", "run", "main:app"]
