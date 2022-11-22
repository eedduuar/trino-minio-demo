
CREATE SCHEMA IF NOT EXISTS minio.satellite
WITH (location = 's3a://satellite/');

CREATE TABLE IF NOT EXISTS minio.satellite.starlink (
creation_date TIMESTAMP,
object_id  VARCHAR,
longitude  BIGINT,
latitude DOUBLE
)
WITH (
external_location = 's3a://satellite/starlink',
format = 'PARQUET'
);
