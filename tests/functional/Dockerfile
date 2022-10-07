FROM python:3.10

WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY start_tests.sh start_tests.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . /opt/app/tests/functional

RUN chmod 777 /opt/app/start_tests.sh

ENTRYPOINT ["/opt/app/start_tests.sh"]