FROM python:3.10

ARG TESTS_ROOT=/tests/functional
ENV TESTS_ROOT=${TESTS_ROOT}
ENV PYTHONPATH ${TESTS_ROOT}

WORKDIR ${TESTS_ROOT}

COPY requirements.txt requirements.txt
COPY start_tests.sh start_tests.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . ${TESTS_ROOT}

RUN chmod 777 ${TESTS_ROOT}/start_tests.sh

ENTRYPOINT ${TESTS_ROOT}/start_tests.sh
