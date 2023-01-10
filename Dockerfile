FROM python:3.11.1-alpine

ENV FLASK_APP runner.py
ENV FLASK_CONFIG production

WORKDIR /home/danquest2023

RUN python -m venv venv
# Enable venv
ENV PATH="/home/danquest2023/venv/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /home/danquest2023/logs

EXPOSE 2023

CMD [ "python", "waitress_server.py" ]