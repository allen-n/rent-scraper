import pandas as pd
import pymysql


import sys
import os
import json
# import boto3

ENDPOINT = "rent-db.cgnpe3p2zb7c.us-west-1.rds.amazonaws.com"
PORT = "3306"
USR = "admin"
REGION = "us-west-1"
DBNAME = "sf_rent"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

# # gets the credentials from .aws/credentials
# session = boto3.Session(profile_name='default')
# client = boto3.client('rds', region_name=REGION)
# client.describe_instances()

# token = client.generate_db_auth_token(
#     DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)
with open('config.json', 'r') as f:
    config = json.load(f)
token = config['db-pass']
try:
    connection = pymysql.connect(host=ENDPOINT,
                                 user=USR,
                                 password=token,
                                 database=DBNAME,
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            

            connection.close()
    # with connection:
    #     with connection.cursor() as cursor:
    #         # Create a new record
    #         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    #     # connection is not autocommit by default. So you must commit to save
    #     # your changes.
    #     connection.commit()

    #     with connection.cursor() as cursor:
    #         # Read a single record
    #         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    #         cursor.execute(sql, ('webmaster@python.org',))
    #         result = cursor.fetchone()
    #         print(result)

except Exception as e:
    print("Database connection failed due to {}".format(e))
