FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY start_etl.sh start_etl.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY ./src .

RUN chmod 777 /opt/app/start_etl.sh

ENTRYPOINT ["/opt/app/start_etl.sh"]
