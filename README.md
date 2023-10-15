# Minimal application on fastapi-asyncpg-postgres stack

## Technology Stack:
* FastAPI
* Uvicorn
* Pytest
* Sqlalchemy
* Postgres


Create python virtual environment and activate it.
Install packages from requirements.txt
```
run $alembic init alembic
```
Fill env.py and alembic.ini
Enroll your migrations and save into database.
```
run $alembic revision --autogenerate -m "create account table"
run $alembic upgrade head
```


To run application via
```
$uvicorn main:app --reload
```
### Enjoy
