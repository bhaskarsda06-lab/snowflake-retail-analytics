from snowflake.snowpark import Session
from snowflake.snowpark.functions import sum as sf_sum

session = Session.builder.configs(connection_parameters).create()

sales_df = session.table("SALES")

store_summary = (
    sales_df
    .group_by("STORE_ID")
    .agg(
        sf_sum("AMOUNT").alias("TOTAL_REVENUE")
    )
    .sort("TOTAL_REVENUE", ascending=False)
)

store_summary.show()

session.close()