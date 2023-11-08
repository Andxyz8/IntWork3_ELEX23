from json import load as json_load
from pandas import DataFrame
from psycopg2 import connect as psql_connect

class RDSDatabase:

    def __init__(self):
        self.df_select = None
        self.__database = None
        self.__db_connection = None
        self.__db_cursor = None
        self.__host: str = None
        self.__port: str = None
        self.__user: str = None
        self.__password: str = None

        self.__load_credentials()

    def __load_credentials(self) -> None:
        """Load database credentials for this project.
        """
        with open("./database/credentials.json", 'r', encoding = 'utf-8') as json_file:
            credentials = json_load(json_file)

            self.__host = credentials["host_cloud_server"]
            self.__port = credentials["port_cloud_server"]
            self.__database = credentials["database_cloud_server"]
            self.__user = credentials["user_cloud_server"]
            self.__password = credentials["password_cloud_server"]

    def operation_without_commit(operation):
        """Decorator that allows a function to execute a query at the cloud database
            and return info in a DataFrame without needing a commit.
        """
        def execute_database_operation(self, *args, **kwargs):
            self.open_connection()

            try:
                operation(self, *args, **kwargs)
            except Exception as excpt:
                self.close_connection()
                raise excpt

            self.result_to_dataframe()
            self.close_connection()

            return self.df_select

        return execute_database_operation

    def operation_with_commit(operation):
        """Decorator that allows a function to execute a query at the cloud database
            and return the id of the last insert or None in case of nothing inserted.
        """
        def execute_database_operation(self, *args, **kwargs):
            self.open_connection()
            # Verifies if the operation must return the id
            try:
                return_id = kwargs['return_id']
            except KeyError:
                return_id = False

            try:
                operation(self, *args, **kwargs)
            except Exception as excpt:
                self.close_connection()
                raise excpt

            self.commita_alteracoes()
            self.close_connection()

            if return_id:
                return self.df_select
            return None

        return execute_database_operation

    def __execute_insert_returning_id(self, query_insert):
        """Execute an INSERT returning the inserted id.

        Args:
            query_insert (str): insert statement.
        """
        # Perform the insert
        self.__execute_query(query_insert)

        # get the id of the last insert
        last_id_inserted = self.__db_cursor.fetchall()

        self.df_select = int(last_id_inserted[0][0])

    def __execute_query(self, query: str) -> None:
        """Runs a query at the RDSDatabase.

        Args:
            query (str): query to be executed.
        """
        print(f"EXECUTING QUERY: {query}")
        self.__db_cursor.execute(query)

    def result_to_dataframe(self):
        """Turn the entries for the last select performed in a DataFrame.

        Returns:
            DataFrame: entries for the last select statement.
        """
        self.df_select = DataFrame(
            data = self.__db_cursor.fetchall(),
            columns = [column_name[0] for column_name in self.__db_cursor.description]
        )

    def commita_alteracoes(self):
        """Commit everything from the current open connection.
        """
        self.__db_connection.commit()

    def close_connection(self) -> None:
        """Close the current connection with the RDSDatabase.
        """
        self.__db_cursor.close()
        self.__db_connection.close()

    def open_connection(self) -> None:
        """Open the connection with de RDS Database.

        Raises:
            NotImplementedError: raised if the connection specified is not implemented.
        """
        if self.__database == 'patrole_iw3':
            self.__db_connection = psql_connect(
                host = self.__host,
                port = self.__port,
                database = self.__database,
                user = self.__user,
                password = self.__password
            )
        else:
            raise NotImplementedError

        self.__db_cursor = self.__db_connection.cursor()

    @operation_without_commit
    def execute_select(self, query_select) -> DataFrame:
        """Allows a SELECT statement to be performed in the cloud databse.

        Args:
            query_select (str): select statement.
        
        Returns:
            DataFrame: entries for the select performed.
        """
        self.__execute_query(query_select)

    @operation_with_commit
    def execute_insert(self, query_insert, return_id = False) -> int:
        """Allows a INSERT statement to be performed in the cloud databse.

        Args:
            query_insert (str): insert a ser executado.
        """
        if return_id:
            self.__execute_insert_returning_id(query_insert)
        else:
            self.__execute_query(query_insert)

    @operation_with_commit
    def execute_update(self, query_update) -> None:
        """Allows a UPDATE statement to be performed in the cloud databse.

        Args:
            query_update (str): update statement.
        """
        self.__execute_query(query_update)

    @operation_with_commit
    def execute_delete(self, query_delete) -> None:
        """Allows a DELETE statement to be performed in the cloud databse.

        Args:
            query_delete (str): delete statement.
        """
        self.__execute_query(query_delete)
