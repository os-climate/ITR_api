FROM python:3.7

COPY requirements.txt config/config.yaml /project/

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install -r /project/requirements.txt \
 && rm -r /root/.cache

ARG uid=210
ARG gid=210

RUN groupadd -g ${gid} dock_itr_api \
 && useradd -u ${uid} -g ${gid} dock_itr_api \
 && mkdir /home/dock_itr_api \
 && chown -R dock_itr_api:dock_itr_api /home/dock_itr_api

RUN rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default \
 && mkdir -p /vol/log/nginx /vol/tmp/nginx \
 && touch /vol/log/nginx/{access.log,error.log} \
 && rm -rf /var/log/nginx \
 && ln -s /vol/log/nginx /var/log/nginx

COPY app /project/app
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/api-nginx.conf /etc/nginx/sites-available/api-nginx.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY app/config.json /project/config.json
COPY app/data /project/data


RUN ln -s /etc/nginx/sites-available/api-nginx.conf /etc/nginx/sites-enabled/api-nginx.conf \
 && chown -R dock_itr_api:dock_itr_api /project /vol

WORKDIR /project

USER dock_itr_api
EXPOSE 80
CMD ["/usr/bin/supervisord"]


