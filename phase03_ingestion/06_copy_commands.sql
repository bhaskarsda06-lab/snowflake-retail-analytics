/*USE DATABASE RETAIL_DB;
USE SCHEMA RAW;
USE SCHEMA STAGE ;

COPY INTO RAW.CUSTOMERS
FROM @CSV_STAGE/customers.csv;

COPY INTO RAW.PRODUCTS
FROM @RETAIL_STAGE/products.csv;

COPY INTO RAW.STORES
FROM @RETAIL_STAGE/stores.csv;

COPY INTO RAW.SALES
FROM @RETAIL*/



- name: Upload Data Files
  run: |
    snow stage copy data/customers.csv @RETAIL_DB.STAGE.CUSTOMERS_STAGE -c default
    snow stage copy data/products.csv @RETAIL_DB.STAGE.PRODUCTS_STAGE -c default
    snow stage copy data/stores.csv @RETAIL_DB.STAGE.STORES_STAGE -c default
    snow stage copy data/sales.csv @RETAIL_DB.STAGE.SALES_STAGE -c default