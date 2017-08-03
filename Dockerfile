FROM debian:stretch
MAINTAINER James McFeeters "jmcfeeters@usgs.gov"

ARG config
ARG ref
ARG thumbnail

RUN apt-get update && apt-get install -y \
    python3-pip \
    nginx-light \
    curl \
    apt-transport-https \
    git \
    libfontconfig

COPY . /app
WORKDIR /app


RUN cp nginx.conf /etc/nginx

RUN cp $config instance/config.py

RUN cp $ref instance/reference.json

RUN rm -f /etc/apt/sources.list.d/chris-lea-node_js-jessie.list \
&& curl https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
&& echo 'deb https://deb.nodesource.com/node_6.x jessie main' > /etc/apt/sources.list.d/nodesource.list \
&& apt-get update \
&& apt-get install -y nodejs

RUN pip3 install -r requirements.txt

RUN npm update

RUN node_modules/bower/bin/bower install --allow-root

ENV THUMBNAIL=$thumbnail

RUN python3 run.py --freeze --norun

RUN if $thumbnail -eq "true"; then node floodviz/thumbnail/thumbnail.js; fi

EXPOSE 80

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
