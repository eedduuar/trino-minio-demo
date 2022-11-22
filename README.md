# Onion lab: take home test

## Components
Basic trino and minio installation. The idea is to use minio as a storage layer and trino as db engine.

`main.py` will create the parquet file with the expected format.

Then, to run the queries you should run `./trino`

### TrinoDB: https://trino.io/docs/current/overview.html 

### Minio storage (local S3) : https://github.com/minio/minio

### hive-metastore: https://blog.jetbrains.com/big-data-tools/2022/07/01/why-we-need-hive-metastore/ 

===============

## prerequisites
```
brew install s3cmd
brew install openjdk@11
curl -sSL https://install.python-poetry.org | python3 -
```

## Setup

```
make compose
make minio
make trino
```

## install and run the app 
```
poetry install
poetry shell
python3 src/main.py
```

## Queries
### PART 3: get latest position for a given satellite and hour

```
trino> select max(creation_date) from minio.satellite.starlink 
  where object_id = '2021-005BA' 
  and date_trunc('hour',creation_date) = from_iso8601_timestamp('2021-01-26T06:00:00.000');
          _col0          
-------------------------
 2021-01-26 06:26:10.000 
(1 row)

Query 20221122_053439_00070_9zmmz, FINISHED, 1 node
Splits: 18 total, 18 done (100.00%)
0.96 [3.14K rows, 36.5KB] [3.29K rows/s, 38.1KB/s]

```

### PART 4 : get the 5 closer satellites to Paris (45.7597, 4.8422) 
reference: https://trino.io/docs/current/functions/geospatial.html

```
trino> select object_id, creation_date,  ST_Distance(ST_Point(48.8567,  2.3508 ), ST_Point(latitude, longitude)) as dist from minio.satellite.starlink 
    -> order by dist asc limit 5;
 object_id  |      creation_date      |        dist        
------------+-------------------------+--------------------
 2020-073P  | 2021-01-21 06:26:10.000 |  1.414480774396697 
 2020-088BA | 2021-01-26 06:26:10.000 | 1.4649688438263628 
 2020-025AQ | 2021-01-26 06:26:10.000 | 1.9504319538548247 
 2020-057B  | 2021-01-26 02:30:00.000 | 2.3511165038290978 
 2020-006AT | 2021-01-26 02:30:00.000 | 2.4241704062927267 
(5 rows)

Query 20221122_054823_00074_9zmmz, FINISHED, 1 node
Splits: 18 total, 18 done (100.00%)
0.45 [3.14K rows, 50.1KB] [6.93K rows/s, 111KB/s]

```



trino-minio template from :  https://github.com/njanakiev/trino-minio-docker
