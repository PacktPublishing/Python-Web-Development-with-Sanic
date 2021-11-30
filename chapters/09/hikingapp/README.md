# Chapter 9 - Full Hiking App

## Getting started

```
docker-compose build
```

```
docker-compose up
```

## Checkout some endpoints:

```
curl localhost:7777/v1/trails
curl localhost:7777/v1/users/alice/hikes
curl localhost:7777/v1/slow
```

_Make sure to hit `curl localhost:7777/v1/slow` multiple times to see the difference_
