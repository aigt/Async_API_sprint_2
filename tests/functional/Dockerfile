FROM python:3.10

ARG TESTS_ROOT=/tests/functional
ENV PYTHONPATH ${TESTS_ROOT}

WORKDIR ${TESTS_ROOT}

RUN  pip install --upgrade pip

COPY . ${TESTS_ROOT}
