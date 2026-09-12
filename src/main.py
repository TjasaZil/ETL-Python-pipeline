# Automating ETL Process wth Python
from src.pipelines.customers import customers_pipeline
from src.pipelines.products import products_pipeline
from src.pipelines.orders import orders_pipeline
from src.paths import customers_path, orders_path, products_path

if __name__ == '__main__':
    df_1=customers_pipeline(customers_path)
    df_2=products_pipeline(products_path)
    orders_pipeline(orders_path, df_1, df_2)


