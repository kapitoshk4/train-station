FROM python:3.12.5-alpine3.19
LABEL maintainer="dmytroshchoma@gmail.com"

ENV PYTHOUNNBUFFERED=1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]