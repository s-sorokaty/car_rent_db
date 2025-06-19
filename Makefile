include .env

EXECUTOR_CONTAINER_NAME=script_executor


up:
	docker compose up -d  --build --force-recreate
	sudo chmod -R 775 ./volumes/*

down:
	docker compose down

create_migrations:
	RUN_COMMAND="alembic revision --autogenerate" \
	docker compose up $(EXECUTOR_CONTAINER_NAME)

apply_migrations:
	RUN_COMMAND="alembic upgrade head" \
	docker compose up $(EXECUTOR_CONTAINER_NAME)

downgrade_migrations:
	RUN_COMMAND="alembic downgrade -1" \
	docker compose up $(EXECUTOR_CONTAINER_NAME)

init_db:
	docker compose up $(EXECUTOR_CONTAINER_NAME)

run_test:
	RUN_COMMAND="pytest test.py --capture=no" \
	docker compose up $(EXECUTOR_CONTAINER_NAME)