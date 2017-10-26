FROM python:2.7

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR ./app

COPY app /app
RUN pip install -r requirements.txt
RUN python ./backend/db.py
RUN python ./backend/data.py


EXPOSE 8888

CMD python ./backend/server.py
