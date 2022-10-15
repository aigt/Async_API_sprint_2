# Функциональные тесты movies_api

## Запуск в docker-compose

```bash
docker-compose up --build
```

## Запуск локально

### Подготовка окружения для локального запуска

1. Запустить среду тестирования
```bash
docker-compose -f docker-compose.dev.yaml up --build -d
```

2. Создать виртуальное окружение
```bash
python -m venv tenv
```

3. Активировать виртуальное окружение
```bash
source tenv/bin/activate
```

4. Обновить pip
```bash
pip install --upgrade pip
```

5. Установить зависимости
```bash
pip install -r requirements.txt
```

### Запуск тестов локально
```bash
python -m pytest .
```