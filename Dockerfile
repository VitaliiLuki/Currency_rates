FROM python:3.8-slim

WORKDIR /bot

COPY requirements.txt /bot

RUN python -m pip install --upgrade pip

RUN pip3 install -r /bot/requirements.txt --no-cache-dir

COPY . /bot

CMD ["python3", "bot.py" ]