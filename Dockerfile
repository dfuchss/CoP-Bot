FROM python:3.11.0a4

ENV Token "The_Token"

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
CMD ["python", "./cop.py"]
