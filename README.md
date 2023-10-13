Primitive application
Create python virtual environment.
Install packages from requirements.txt
run $alembic init alembic
run $alembic revision --autogenerate -m "create account table"
run $alembic upgrade head
To run application via $uvicorn main:app --reload
