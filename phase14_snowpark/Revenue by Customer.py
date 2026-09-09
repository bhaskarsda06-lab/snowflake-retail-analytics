customer_summary = (
    sales_df
    .group_by("CUSTOMER_ID")
    .agg(
        sf_sum("AMOUNT").alias("TOTAL_SPENT")
    )
)

customer_summary.show()