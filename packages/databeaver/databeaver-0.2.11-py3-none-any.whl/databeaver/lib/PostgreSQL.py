import psycopg2
import psycopg2.extras
import logging

from .DataStorage import DataStorage
import sys


class PostgreSQL(DataStorage):
    """
    Provides PostgreSQL database functionality. 
    Implements the DataStorage abstraction.
    """

    RESERVED_WORDS = ['and','any', 'analyse', 'analyze', 'group']
    
    def __init__(self, host, database, user, password, port='5432'):
        """
        Responsible For:        
        Instantiating a PostgreSQL object.
        Calling DataStorage.__init__()
        Establishing a connection to the PostgreSQL Database Server
        
        :param host: Host to connect to
        :param database: Database to connect
        :param user: Username to connect with
        :param password: Password to connect with
        """
        # Call DataStorage.__init__()
        super().__init__()

        # 'Private' Variables 
        self._logger = self.get_logger()

        # Public Variables
        self.connection = None
        self.database = database
        self.host = host
        self.password = password
        self.type = self.STORAGE_TYPE_POSTGRESQL
        self.user = user
        self.port = int(port)

        # Connect to PostgreSQL
        connection_established = self.connect(host=self.host, database=self.database, user=self.user, password=self.password, port=self.port)
        if connection_established is False:
            self._logger.warning(f"No connection could be established to {self.host}/{self.database}/{self.user}")
            

    ##################
    # Public Methods #
    ##################
    def connect(self, host, database, user, password, port):
        """
        Connect to the server. If a connection already exists do nothing.

        :return: True if a connection was created. Otherwise False.
        """

        # If we already have a connection then do nothing
        if self.connection is None:
            self.connection = psycopg2.connect(host=host,
                                               database=database,
                                               user=user,
                                               password=password,
                                               port=port)
            return True

        # We did not create a new connection during this call.
        # This does not mean we are not connected...
        return False

    def create_table(self, schema='', table_name=None, columns=None):
        """
        Description
            Creates a new table in the requested based on the column information supplied

        Responsible For
            1. Seeing if the table already exists in the given schema and raises an error as needed
            2. Creating the table as specified

        Arguments
            :param schema: Schema to write table into
            :param table_name: Name of the new table we want to create
            :param columns: Column Information for the table we want to create
            :return: True if a new table was created, False otherwise
        """

        # Check that the table_name was supplied
        if table_name is None:
            self._logger.warn("table_name must be defined")
            return

        # Format the schema to use in sql below
        if schema != '':
            schema = f"{schema}."

        # Format the column information in a PostgreSQL specific format
        column_list = ""
        for column in columns:
            if 'type' in column:
                data_type = column['type']
            else:
                data_type = "VARCHAR(255)"
            column_list += f"\n{column['name']} {data_type},"
        column_list = column_list[0:-1]

        try:
            cursor = self.connection.cursor()

            # create the table
            command = f"CREATE TABLE {schema}{table_name}\n(\n{column_list}\n)"
            self._logger.debug(command)
            cursor.execute(command)

            # close communication with the PostgreSQL database server
            cursor.close()

            # commit the changes
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

            # Transaction has been aborted, we need to close the existing cursor and get
            cursor.close()

            # Restart the connection
            self.connection = None
            self.connect(self.host, self.database, self.user, self.password, self.port)

            # Get new cursor (not sure if I need this but for now)
            cursor = self.connection.cursor()
        finally:
            cursor.close()

    def delete_rows(self, table_name, keys_to_delete={}, schema="public", log_level=logging.DEBUG):
        """
        Delete Rows the given table

        :param table_name:
        :param keys_to_delete:
        :param schema: Schema the table resides in. Default is 'public'
        :param log_level: Logging in this method will be done at the specified level. Default debug
        :return:
        """

        # Delete all rows in the table
        where_clause = "WHERE 1=1\n"
        for key, values in keys_to_delete.items():
            new_values = []
            for val in values:
                new_values.append(f"'{val}'")

            new_values = ", ".join(new_values)
            where_clause += f"AND {str(key)} IN ({new_values})\n"

        delete_stmt = f"DELETE FROM {schema}.{table_name}\n{where_clause};\n"
        try:
            cursor = self.connection.cursor()

            # create the table
            self._logger.log(log_level, delete_stmt)
            cursor.execute(delete_stmt)

            rows_deleted = cursor.rowcount
            self._logger.log(log_level, f"{rows_deleted} rows were deleted from {table_name}")

        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
        finally:
            cursor.close()

        ###############################################
        # Close the Cursor and commit the transaction #
        ###############################################
        try:
            # Commit the changes
            self.connection.commit()

            # Close communication with the PostgreSQL database server
            cursor.close()

        except(Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
        finally:
            cursor.close()

    def drop_table(self, table_name=None, schema="public"):
        """
        Drops the table in the given schema
        :param table_name:
        :param schema:
        :return:
        """

        drop_stmt = f"DROP TABLE {schema}.{table_name};"

        try:
            cursor = self.connection.cursor()

            # create the table
            cursor.execute(drop_stmt)
            self._logger.debug(drop_stmt)

            # close communication with the PostgreSQL database server
            cursor.close()

            # commit the changes
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
        finally:
            cursor.close()

    def execute(self, sql, ignore_errors=False, log_level=logging.DEBUG):
        try:
            # Get a cursor
            cursor = self.connection.cursor()

            # Execute the statement
            self._logger.log(log_level, sql)
            cursor.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(sql)
            self._logger.error(error)
            if ignore_errors is False:
                raise error
        finally:
            cursor.close()

        # Close the Cursor and commit the transaction
        try:
            # Commit the changes
            self.connection.commit()

            # Close communication with the PostgreSQL database server
            cursor.close()

        except(Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)
            if ignore_errors is False:
                raise error
        finally:
            cursor.close()

    def execute_sql_file(self, filename, substitution_variables={},
                    cursor_factory=psycopg2.extras.RealDictCursor, log_level=logging.DEBUG):
        """

        :param log_level: level that method logging will be performed at
        :param cursor_factory: Defaults to list of dictionaries, pass in None to get a list of tuples
        :param filename:
        :param substitution_variables:
        :return:
        """
        template_file_path = f"{sys.path[0]}/sql/{filename}"
        with open(template_file_path) as f:
            raw_sql = f.read()

        sql = raw_sql
        for key, value in substitution_variables.items():
            sql = self.replace_text(sql, key, value)

        self._logger.log(log_level, sql)
        return self.postgresql.fetchall(sql, cursor_factory)

    def fetchall(self, query, cursor_factory=psycopg2.extras.RealDictCursor, log_level=logging.DEBUG):
        """

        :param cursor_factory: Set to None if you want list of tuples returned
        :param query: SQL statement to be executed
        :param log_level: Level to Log non error statements as. Defaults to debug
        :return result_set: Results From The Execution of <query>
        """

        with self.connection.cursor(cursor_factory=cursor_factory) as cursor:
            # Execute the SELECT EXISTS query to see if the table is already there or not
            cursor.execute(query)
            self._logger.log(log_level, query)

            # Return True if the table exists, false otherwise
            return cursor.fetchall()

    def insert_multi_rows(self, table_name, headers=None, data=None):
        """
        Inserts all rows in a single INSERT VALUES(), VALUES() statement

        :param table_name: Name of the table the data will be inserted into
        :param headers:
        :param data:
        :return:
        """

        if headers is None or data is None or table_name is None:
            self._logger.warn("No data to insert")
            return

        # Create a cursor to use for our processing
        try:
            cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

        # Loop over every row of data and attempt to insert it
        headers_string = ",".join(headers)
        insert_stmt = f"INSERT INTO {table_name} ({headers_string})\n VALUES\n"
        for row in data:
            row_string = []
            for value in row:
                value = str(value).replace("'", "")
                value = f"'{value}'"
                value = value.replace("'None'", "NULL")
                row_string.append(value)

            row_string = ", ".join(row_string)
            insert_stmt += f"({row_string}),\n"

        insert_stmt = f"{insert_stmt[:-2]};"
        try:
            # create the table
            self._logger.info(insert_stmt)
            cursor.execute(insert_stmt)
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

        try:
            # close communication with the PostgreSQL database server
            cursor.close()

            # commit the changes
            self.connection.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

    def insert_list_of_tuples(self, table_name=None, schema=None, headers=None, data=None):
        """
        Generates individual insert statements and executes them against the database

        :param table_name: string - Table name to be loaded
        :param schema: string - Schema to use, will default to public if no schema is provided
        :param headers: list of strings - Columns names for the matching row data
        :param data: list of tuples -  Data to be inserted.

        :return: True if a new row was created, False otherwise
        """
        # Make sure we got data to work with
        if headers is None or data is None or table_name is None:
            self._logger.warn("No data to insert")
            return

        # Create a cursor to use for our processing
        try:
            cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

        # Determine if we have a schema or not, and build sql accordingly
        schema_clause = ''
        if schema:
            schema_clause = f"{schema}."

        # Loop over every row of data and attempt to insert it
        for row in data:
            # Create the insert statement for this row
            headers_string = ",".join(headers)

            row_string = []
            for value in row:
                value = str(value).replace("'", "")
                value = f"'{value}'"
                value = value.replace("'None'", "NULL")
                row_string.append(value)

            row_string = ", ".join(row_string)
            insert_stmt = f"INSERT INTO {schema_clause}{table_name} ({headers_string})\n VALUES({row_string});"

            try:
                # create the table
                cursor.execute(insert_stmt)
                self._logger.debug(insert_stmt)
            except (Exception, psycopg2.DatabaseError) as error:
                self._logger.error(error)

        try:
            # close communication with the PostgreSQL database server
            cursor.close()

            # commit the changes
            self.connection.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

    def insert_list_of_dictionaries(self, table_name, rows, schema=None, log_level=logging.DEBUG):
        """
        Inserts rows into a table from a list of dictionaries

        :param table_name: String - Name of the Table to Inserted Into
        :param rows: list of dictionaries - Rows to be inserted
        :param log_level: Set the log level for level configurable log messages
        :param schema: Optional schema to insert data into
        :return:
        """

        # Determine if we have a schema or not, and build sql accordingly
        schema_clause = ''
        if schema:
            schema_clause = f"{schema}."

        # Create a cursor to use for our processing
        try:
            cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

        # Clean the data and group each record by the columns it would insert (so we can run them as one statement)
        data_to_insert = {}
        for row in rows:
            columns = []
            values = []
            for key, value in row.items():
                columns.append(key)
                value = str(value).replace("'", "")
                value = f"'{value}'"
                values.append(value)

            columns = self.quote_columns(columns)
            values_string = ", ".join(values)
            columns_string = ", ".join(columns)
            if columns_string not in data_to_insert:
                data_to_insert[columns_string] = ""
            data_to_insert[columns_string] += f"({values_string}),\n"

        # Insert all records grouped by the columns they will insert
        for columns_string, insert_values in data_to_insert.items():
            insert_stmt = f"INSERT INTO {schema_clause}{table_name} ({columns_string})\n VALUES\n{insert_values}"
            insert_stmt = f"{insert_stmt[:-2]};"
            insert_stmt = insert_stmt.replace("'None'", "NULL")
            insert_stmt = insert_stmt.replace("'Null'", "NULL")
            insert_stmt = insert_stmt.replace("''", "NULL")
            try:
                self._logger.log(log_level, insert_stmt)
                cursor.execute(insert_stmt)
            except (Exception, psycopg2.DatabaseError) as error:
                self._logger.error(insert_stmt)
                self._logger.error(error)
                break

        # Close the cursor and commit
        try:
            # close communication with the PostgreSQL database server
            cursor.close()

            # commit the changes
            self.connection.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            self._logger.error(error)

    def list_schema(self):
        """
        List all schema in the database
        :return list_of_schema: List of the names of all schema
        """

        select_stmt = """
                      SELECT schema_name
                      FROM   information_schema.schemata
                      """
        with self.connection.cursor() as cursor:
            # Execute the query
            cursor.execute(select_stmt)
            self._logger.debug(select_stmt)

            # Fetch the result set
            results = cursor.fetchall()

        return results

    def list_tables(self, schema):
        """
        Return a list of tables for the specified schema

        :param schema:
        :return:
        """
        select = f"""
                  SELECT tablename 
                  FROM pg_tables 
                  WHERE schemaname = '{schema}';
                  """
        with self.connection.cursor() as cursor:
            self._logger.debug(schema)
            cursor.execute(select)
            results = cursor.fetchall()

        clean_results = [row[0] for row in results]

        return clean_results

    def quote_columns(self, columns=[]):
        """
        Adds quotes around column names that are also PostgreSQL reserved words

        :param columns: A list of column names
        :return quoted_columns: A list of all columns we received with reserved words now quoted
        """
        # ?? Should we raise a warning here?
        if type(columns) == type(str):
            columns = columns.split(',')

        # Iterate over the columns and add quotes around each column name
        quoted_columns = []
        for col in columns:
            if str(col).lower() in self.RESERVED_WORDS:
                quoted_columns.append(f"\"{col}\"")
            else:
                quoted_columns.append(col)

        return quoted_columns

    def table_exists(self, table_name=None, schema='public'):
        """

        :param schema:
        :param table_name:
        :return:
        """

        select_stmt = f"SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table_name}');"

        with self.connection.cursor() as cursor:
            # Execute the SELECT EXISTS query to see if the table is already there or not
            cursor.execute(select_stmt)
            self._logger.debug(select_stmt)

            # Return True if the table exists, false otherwise
            return cursor.fetchone()[0]


