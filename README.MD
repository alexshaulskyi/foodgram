![example workflow name](https://github.com/alexshaulskyi/foodgram/workflows/foodgram_workflow/badge.svg)

### Foodgram

A place where you can share how to prepare a cuisine masterpiece. Know how to make
a perfect dish with a piece of bread and an axe? This is the perfect place to tell
others how.

#### Usage

The application is running in 3 containers one of which contains PostgreSQL, another
one for Django and the last one for Nginx. In order to run application you need to
create an ```.env``` file with PostgreSQL settings:

```DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=supersecretpw
DB_HOST=db
DB_PORT=5432
```
