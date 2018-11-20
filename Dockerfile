FROM python:3.6-alpine3.6

ENV OJ_ENV production

ADD . /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python2 /app/deploy/health_check.py

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install --no-cache-dir -i https://mirrors.ustc.edu.cn/pypi/web/simple -r /app/deploy/requirements.txt && \
    apk add git

ENTRYPOINT /app/deploy/entrypoint.sh
