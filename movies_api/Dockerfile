FROM python:3.10

# Настройки
ARG APP_USER=appuser
ARG APP_USER_UID=1000
ARG APP_ROOT=/code

EXPOSE 8000/tcp

# Добавить пользователя
RUN useradd --create-home --uid=${APP_USER_UID} ${APP_USER}

# Обновить систему
RUN apt-get update \
    && pip install --upgrade pip

WORKDIR ${APP_ROOT}

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


COPY ./requirements.txt ${APP_ROOT}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY --chown=${APP_USER}:${APP_USER} ./src ${APP_ROOT}

USER ${APP_USER}:${APP_USER}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]