from snowflake.snowpark import Session
from snowflake.snowpark.functions import sum as sf_sum

# Connection Parameters
connection_parameters = {
    "account": "ACCOUNT",
    "user": "USER",
    "password": "PASSWORD",
    "warehouse": "RETAIL_WH",
    "database": "RETAIL_DB",
    "schema": "RAW"
}

# Create Snowpark Session
session = Session.builder.configs(
    connection_parameters
).create()

# Read SALES table
sales_df = session.table("SALES")

# Calculate total sales by product
result = (
    sales_df
    .group_by("PRODUCT_ID")
    .agg(
        sf_sum("AMOUNT").alias("TOTAL_SALES")
    )
)

# Display results
result.show()

# Optional: Save results to a Snowflake table
result.write.mode("overwrite").save_as_table(
    "CURATED.PRODUCT_SALES_SUMMARY"
)

# Close session
session.close()