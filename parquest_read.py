import pyarrow.parquet as pq

# parquet_file = "~/downloads/part-00001.parquet"
parquet_file = "~/downloads/customers_new.parquet"
# parquet_file = "~/downloads/users.parquet"
# parquet_file = "~/downloads/users_new.parquet"
parquet_schema = pq.read_schema(parquet_file)

for field in parquet_schema:
    print(f"{field.name}: {field.type}")
