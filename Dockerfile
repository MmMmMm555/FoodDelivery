FROM python:3.8-slim-buster 
ENV PYTHONUNBUFFERED=1
WORKDIR /food
COPY requirements/base.txt requirements/base.txt
# COPY entrypoint.sh entrypoint.sh
# ENTRYPOINT ["entrypoint.sh"]

RUN pip3 install -r requirements/base.txt
RUN apt-get update \
    && apt-get install -y gdal-bin libgdal-dev \
    && apt-get install -y postgis

# RUN sleep 10 && psql -U postgres -c "CREATE EXTENSION postgis;"
