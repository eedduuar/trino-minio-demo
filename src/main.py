import logging
import json
import subprocess
import pandas as pd

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

INPUT_DATA_PATH = "../input_data"
DATA_PATH = "../data"
SOURCE_FILE = INPUT_DATA_PATH + "/starlink_historical_data.json"
DEST_PATH = DATA_PATH + "/starlink/starlink.parquet"


def main():
    logging.info("Satellite APP")
    fileData = open(SOURCE_FILE)
    data = json.load(fileData)
    logging.debug("original json len %d", len(data))
    df = pd.json_normalize(data)
    logging.debug("dataframe len %d", len(data))
    # logging.debug('dataframe columns %s',df.columns)
    df = df.rename(
        columns={
            "spaceTrack.CREATION_DATE": "creation_date",
            "spaceTrack.OBJECT_ID": "object_id",
        }
    )
    df["creation_date"] = pd.to_datetime(df["creation_date"])
    df["longitude"] = pd.to_numeric(df["longitude"])
    df["latitude"] = pd.to_numeric(df["latitude"])
    df["object_id"] = df["object_id"].astype("str")
    df = df.fillna(0)
    df[["creation_date", "object_id", "longitude", "latitude"]].to_parquet(
        DEST_PATH, index=False
    )
    # replace subprecess by boto3
    command = [
        "s3cmd",
        "--config",
        "../minio.s3cfg",
        "put",
        f"{DEST_PATH}",
        "s3://satellite/starlink/starlink.parquet",
    ]
    logging.debug(command)
    try:
        subprocess.run(command, capture_output=True)
    except subprocess.CalledProcessError as e:
        logging.error(e)

main()
