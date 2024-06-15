FROM python:3.10-slim
LABEL authors="pavelivanov"
WORKDIR /workdir
COPY .. .
RUN apt-get update \
    && apt-get install -y iputils-ping
CMD ["python3", "main.py", "brazzers.com"]
