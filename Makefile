.PHONY: compose minio trino install 
current_dir = $(shell pwd)

compose:
	docker compose up -d

install:
	poetry install


minio:
	s3cmd --config minio.s3cfg --configure
	s3cmd --config minio.s3cfg mb s3://satellite
	s3cmd --config minio.s3cfg la
trino:
	./trino --execute "$(shell cat create.sql)"