import os
import json
import sys
import glob
import snowflake.connector

def load_bundles():
    conn = snowflake.connector.connect(
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        database=os.environ['SNOWFLAKE_DB'],
        schema=os.environ['SNOWFLAKE_SCHEMA']
    )
    cursor = conn.cursor()

    # Truncate before load to keep the table idempotent across runs
    cursor.execute("TRUNCATE TABLE FHIR_RESOURCES")

    bundle_files = glob.glob('output/fhir/*.json')
    rows = []

    for bundle_file in bundle_files:
        with open(bundle_file) as f:
            bundle = json.load(f)
        for entry in bundle.get('entry', []):
            resource = entry.get('resource', {})
            resource_type = resource.get('resourceType')
            if resource_type:
                rows.append((json.dumps(resource), resource_type))

    # Batch insert
    cursor.executemany("""
        INSERT INTO FHIR_RESOURCES (raw_data, resource_type)
        SELECT PARSE_JSON(%s), %s
    """, rows)

    print(f"Loaded {len(rows)} resources from {len(bundle_files)} bundles")
    conn.close()

if __name__ == '__main__':
    load_bundles()