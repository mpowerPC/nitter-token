FROM python:3

WORKDIR /src/

RUN mkdir -p /src/logs

RUN mkdir -p /src/output

COPY requirements.txt .

RUN cat requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]