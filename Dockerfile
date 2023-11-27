# pull official base image
FROM python:3.11-bookworm

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DJANGO_SETTINGS_MODULE="subawardsApp.settings.prod"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN mkdir -p /var/log/subawards

RUN mkdir -p /var/log/gunicorn

# ENV SECRET_KEY="m7^ml46p2h6@m(($k^z50$=y#j8d%j+$x*6sdr!(r9(^an!^cd"

# ENV DBPASS="eOGPOSwM"
# # ENV DBPASS="root"

# # ENV DBHOST="db-8a20bf280a8446f28e3e63b994f919a7.svc.local"
# ENV DBHOST="db-8a20bf280a8446f28e3e63b994f919a7.svc.local"

# ENV DJANGO_SUPERUSER_USERNAME=admin

# ENV DJANGO_SUPERUSER_PASSWORD=sam12345

# ENV DJANGO_SUPERUSER_EMAIL=sam.gangwal97@gmail.com

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
