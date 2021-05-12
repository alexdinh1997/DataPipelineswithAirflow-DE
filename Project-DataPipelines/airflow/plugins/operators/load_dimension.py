from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 conn_id,
                 table,
                 query,
                 truncate=False,
                 *args, **kwargs):
       
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.conn_id = conn_id
        self.table=table
        self.query=query
        self.truncate=truncate

        #truncate variable is for delete all row of table if existing

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.conn_id)
        if self.truncate:
            redshift.run(f"TRUNCATE TABLE {self.table}")
        redshift.run(f"INSERT INTO {self.table} {self.query}")
