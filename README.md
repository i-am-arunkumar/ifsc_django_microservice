## IFSC Django microservice



1. create virtual env (python -m venv virtualenv_name) and activate the virtual environment

2. install required packages.



### cache__handler

This Cache handler server handles the client requests and respond with cached data. if cache is mismatched or not found, it will request the server running in port 8080 to generate the response. the ifsc api and cache hits are stored in redis inmemory.

Redis server is required for inmemory api cache.

###### endpoints :

- api/ifsc/:ifsc_code (curl http://localhost:8080/api/ifsc/SBIN0000002/)
- api/ifsc/leaderboard?fetchcount=10&sortorder=DESC (curl http://localhost:8080/api/ifsc/leaderboard/)
- api/ifsc/statistics?fetchcount=10&sortorder=DESC (curl http://localhost:8080/api/ifsc/statistics/)



### ifsc_app

Done using django and drf. excel (.xls) will have three banks records as individual sheets in same xls file (file name and sheets can be modified in ifsc_app/settings.py). excel file is loaded into sqlite database as "db.sqlite3" or ":inmemory:" based on DATABASES NAME in settings.

###### Migrations

- ./manage makemigrations
- ./manage migrate
- ./manage sqlmigrate ifsc_app 0001 #for ifsc db
- ./manage sqlmigrate ifsc_app 0002 # api history db
- ./manage runserver

###### endpoints

1. api/ifsc (curl http://localhost:8000/api/ifsc)
2. api/ifsc/:ifsc_code (curl http://localhost:8000/api/ifsc/SBIN0000002/)
3. api/ifsc/leaderboard?fetchcount=10&sortorder=DESC (curl http://localhost:8000/api/ifsc/leaderboard/)
4. api/ifsc/statistics?fetchcount=10&sortorder=DESC (curl http://localhost:8000/api/ifsc/statistics/)

###### Api hits

api hits are stored in sqlite3 database as individual entry and same is used for statistics.

1. api/hits/ifsc_hits (curl http://localhost:8000/api/hits/ifsc_hits/)
2. api/hits/api_hits (curl http://localhost:8000/api/hits/api_hits/)
