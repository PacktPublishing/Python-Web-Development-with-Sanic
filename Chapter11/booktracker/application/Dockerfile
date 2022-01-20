FROM python:3.10

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn

RUN mkdir /app
WORKDIR /app

COPY ./package.json /app/package.json
COPY ./rollup.config.js /app/rollup.config.js
RUN yarn install

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./booktracker /app/booktracker
COPY ./ui /app/ui
