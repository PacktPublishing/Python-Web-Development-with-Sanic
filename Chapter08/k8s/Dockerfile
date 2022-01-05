FROM sanicframework/sanic:3.9-latest

COPY . /srv
WORKDIR /srv
EXPOSE 7777

ENTRYPOINT ["sanic", "server:app", "--port=7777", "--host=0.0.0.0"]
