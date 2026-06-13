import os
import snowflake.connector

def setup():
    account = os.environ['SNOWFLAKE_ACCOUNT']
    user = os.environ['SNOWFLAKE_USER']
    password = os.environ['SNOWFLAKE_PASSWORD']
    warehouse = os.environ['SNOWFLAKE_WAREHOUSE']
    database = os.environ['SNOWFLAKE_DB']
    schema = os.environ['SNOWFLAKE_SCHEMA']

    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
    )
    cursor = conn.cursor()

    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {warehouse} WAREHOUSE_SIZE = 'X-SMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")
    cursor.execute(f"USE WAREHOUSE {warehouse}")
    cursor.execute(f"USE DATABASE {database}")
    cursor.execute(f"USE SCHEMA {schema}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FHIR_RESOURCES (
            resource_id     VARCHAR        NOT NULL,
            resource_type   VARCHAR        NOT NULL,
            raw_data        VARIANT        NOT NULL,
            loaded_at       TIMESTAMP_NTZ  NOT NULL DEFAULT SYSDATE(),
            CONSTRAINT pk_fhir_resources PRIMARY KEY (resource_id)
        )
    """)

    print(f"Schema setup complete: {database}.{schema}")
    conn.close()

if __name__ == '__main__':
    setup()
