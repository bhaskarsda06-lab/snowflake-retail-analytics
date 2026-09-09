import os
from snowflake.snowpark import Session
from snowflake.snowpark.functions import sum as sf_sum

# =====================================================
# Validate Environment Variables
# =====================================================

required_vars = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_PRIVATE_KEY_FILE"
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing environment variable: {var}")

# =====================================================
# Snowflake Connection
# =====================================================

connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "authenticator": "SNOWFLAKE_JWT",
    "private_key_file": os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": "RAW",
    "role": os.getenv("SNOWFLAKE_ROLE")
}

session = None

try:

    session = Session.builder.configs(
        connection_parameters
    ).create()

    print("✅ Connected Successfully")

    # =====================================================
    # Source Table
    # =====================================================

    sales_df = session.table("RETAIL_DB.RAW.SALES")

    # =====================================================
    # Revenue By Product
    # =====================================================

    product_sales = (
        sales_df
        .group_by("PRODUCT_ID")
        .agg(
            sf_sum("AMOUNT").alias("TOTAL_SALES")
        )
        .sort("TOTAL_SALES", ascending=False)
    )

    product_sales.show()

    product_sales.write.mode("overwrite").save_as_table(
        "RETAIL_DB.CURATED.PRODUCT_SALES_SUMMARY"
    )

    # =====================================================
    # Revenue By Customer
    # =====================================================

    customer_revenue = (
        sales_df
        .group_by("CUSTOMER_ID")
        .agg(
            sf_sum("AMOUNT").alias("TOTAL_SPENT")
        )
        .sort("TOTAL_SPENT", ascending=False)
    )

    customer_revenue.show()

    customer_revenue.write.mode("overwrite").save_as_table(
        "RETAIL_DB.CURATED.CUSTOMER_REVENUE_SUMMARY"
    )

    # =====================================================
    # Revenue By Store
    # =====================================================

    store_revenue = (
        sales_df
        .group_by("STORE_ID")
        .agg(
            sf_sum("AMOUNT").alias("TOTAL_REVENUE")
        )
        .sort("TOTAL_REVENUE", ascending=False)
    )

    store_revenue.show()

    store_revenue.write.mode("overwrite").save_as_table(
        "RETAIL_DB.CURATED.STORE_REVENUE_SUMMARY"
    )

    # =====================================================
    # Daily Revenue
    # =====================================================

    daily_revenue = (
        sales_df
        .group_by("SALE_DATE")
        .agg(
            sf_sum("AMOUNT").alias("TOTAL_REVENUE")
        )
        .sort("SALE_DATE")
    )

    daily_revenue.show()

    daily_revenue.write.mode("overwrite").save_as_table(
        "RETAIL_DB.CURATED.DAILY_REVENUE"
    )

    # =====================================================
    # Top Products
    # =====================================================

    session.sql("""
    CREATE OR REPLACE TABLE RETAIL_DB.CURATED.TOP_PRODUCTS AS
    SELECT
        PRODUCT_ID,
        SUM(AMOUNT) AS TOTAL_REVENUE
    FROM RETAIL_DB.RAW.SALES
    GROUP BY PRODUCT_ID
    ORDER BY TOTAL_REVENUE DESC
    """).collect()

    # =====================================================
    # Validation
    # =====================================================

    print("===== Product Sales Summary =====")
    session.table(
        "RETAIL_DB.CURATED.PRODUCT_SALES_SUMMARY"
    ).show()

    print("===== Customer Revenue Summary =====")
    session.table(
        "RETAIL_DB.CURATED.CUSTOMER_REVENUE_SUMMARY"
    ).show()

    print("===== Store Revenue Summary =====")
    session.table(
        "RETAIL_DB.CURATED.STORE_REVENUE_SUMMARY"
    ).show()

    print("===== Daily Revenue =====")
    session.table(
        "RETAIL_DB.CURATED.DAILY_REVENUE"
    ).show()

    print("✅ Snowpark Analytics Completed Successfully")

except Exception as e:
    print(f"❌ Error: {e}")
    raise

finally:
    if session:
        session.close()

    print("✅ Session Closed")