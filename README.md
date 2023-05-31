Телеграм бот, показывающий актуальный курс выбранных валютных пар.

### Запуск проекта

### Клонировать репозиторий на локальную машину:

```
https://github.com/VitaliiLuki/Currency_rates
```

### Создать в корне проекта файл с переменными окружения

```
touch .env
```

### Ввести следующие переменные в .env:

- URL_EXCHANGE - внешний API откуда подтягиваются актуальные курсы валют.

- BOT_TOKEN - токен бота, полученный при создании от BotFather.

```
echo URL_EXCHANGE='https://api.exchangerate.host/latest' >> .env
echo BOT_TOKEN=<Токен полученный от BotFather> >> .env
```

Если Docker установлен:

1. Перейти в директорию с проектом.

```
cd Currency_rates/
```

2. Выполнить команду в терминале:

```
docker-compose up -d
```

Если Docker не установлен:

1. Перейти в директорию с проектом.

```
cd Currency_rates/
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
. venv/bin/activate
```

3. Обновить pip и установить зависимости:

```
pip install --upgrade pip && pip install -r requirements.txt
```

4. Запуск бота.

```
python3 bot.py
```
