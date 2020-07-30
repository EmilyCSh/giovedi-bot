FROM python:3
MAINTAINER = "chic_luke"
LABEL description="Ti dice se è giovedì"
WORKDIR /app/giovedibot
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py"]