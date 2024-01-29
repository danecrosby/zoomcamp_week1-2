#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv.gz'

    #download the csv
    os.system(f"wget {url} -O {csv_name}")
    os.system(f"gzip -d {csv_name}")



    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv("output.csv", iterator = True, chunksize = 100000)
    df = next(df_iter)


    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


    while True: 
        t_start = time() # get starting time
        
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
        
        t_end = time() # get ending time
        
        print('Inserted another chunk taking %.3f seconds' % (t_end - t_start)) # subtract end time from start time


if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres.')
        # user, password, host, port, database name, table name, url of the csv

        parser.add_argument('--user', help='user name for postgres (example:root)')
        parser.add_argument('--password', help='password for postgres (example:password)')
        parser.add_argument('--host', help='host for postgres (example:db-postgres)')
        parser.add_argument('--port', help='port number for postgres (example:5432)')
        parser.add_argument('--db', help='database name for postgres (example:pg-database)')
        parser.add_argument('--table_name', help='name of the table where we write (example:pg-database)')
        parser.add_argument('--url', help='url of the csv file (example:pg-database)')

        args = parser.parse_args()

        main(args)




