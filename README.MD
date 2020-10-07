![example workflow name](https://github.com/alexshaulskyi/foodgram/workflows/foodgram_workflow/badge.svg)

### Foodgram

A place where you can share how to prepare a cuisine masterpiece. Know how to make
a perfect dish with a piece of bread and an axe? This is the perfect place to tell
others how.

#### Setup

The application is running in 3 containers one of which contains PostgreSQL, another
one for Django and the last one for Nginx. In order to run application you need to
create an ```.env``` file with PostgreSQL settings:

```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_super_secret_password
DB_HOST=db
DB_PORT=5432
```

If you want to use default ```sqlite``` DB in development just uncomment respective section
in ```settings.py``` file. Do not forget to uncomment ```STATICFILES_DIRS``` and switch ```DEBUG``` to ```True```
in order to serve static files properly in development.

Includes ```json`` with around 2k ingredients. Use on your own will.

#### Description

The application allows to post recipes which contain information about ingredients, required cooking time
author, description and picture. Anonymous users may watch all recipes, their detailed description, selected
author page. Authenticated users may post recipes, edit and delete their own recipes, subscribe to selected
authors, add recipes to favorites and to shopping list which will allow further downloading of PDF file with
ingredients and their amount.


