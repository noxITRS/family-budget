FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y gdal-bin

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/local.txt \
    && rm -rf /requirements

COPY ./docker/local/django/entrypoint /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

RUN mkdir /app
COPY ./app /app
RUN chown -R django /app
USER django

WORKDIR /app

ENTRYPOINT [ "/entrypoint" ]
