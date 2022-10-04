FROM python:3.10

# Настройки
ARG APP_USER=appuser
ARG APP_USER_UID=1000
ARG APP_ROOT=/opt/app

# Добавь пользователя
RUN useradd --create-home --uid=${APP_USER_UID} ${APP_USER}

# Обнови систему
RUN  apt-get update \
     && pip install --upgrade pip

# Установи рабочую директорию
WORKDIR ${APP_ROOT}

# Переменные окружения
ENV  PYTHONDONTWRITEBYTECODE=1 \
     PYTHONUNBUFFERED=1

# Скопируй список и установи зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Скопируй приложение
COPY --chown=${APP_USER}:${APP_USER} ./src ${APP_ROOT}

# Скопируй и дай права на запуск точки входа
COPY --chown=${APP_USER}:${APP_USER} start_etl.sh start_etl.sh
RUN chmod +x ${APP_ROOT}/start_etl.sh

# Точка входа
ENTRYPOINT ["/opt/app/start_etl.sh"]
