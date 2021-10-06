FROM python:3.10.0

ENV Token "The_Token"

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
CMD ["python", "./cop.py"]
