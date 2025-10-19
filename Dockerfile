FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    gettext \
    build-essential

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN chmod +x wait-for-it.sh
