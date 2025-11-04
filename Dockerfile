FROM python:3.14-alpine
WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip python3-dev build-essential python3-venv
COPY . .
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

RUN pip3 install -U -r requirements.txt

CMD ["faststream", "run", "main:app"]