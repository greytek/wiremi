from drivers.db.conn import connection_string_live, connection_string_local
import pyodbc
import pandas as pd


def exec_store_proc_post(name, params, is_col_required=False):
    try:
        conn = pyodbc.connect(connection_string_live)
        cursor = conn.cursor()
        if params:
            param_string = ','.join(['?' for _ in range(len(params))])
            cursor.execute(f"EXEC [dbo].{name} {param_string}", params)
        else:
            cursor.execute(f"EXEC [dbo].{name}")
        cursor.commit()
    except Exception as e:
        print(e)
        pass


def exec_query(sql_query, is_col_required=False):
    try:
        conn = pyodbc.connect(connection_string_live)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if is_col_required:
            columns = [column[0] for column in cursor.description]
            results = pd.DataFrame.from_records(results, columns=columns)
            return results
        return results
    except Exception as e:
        pass


def exec_store_proc_get(name, params, is_col_required=False):
    try:
        conn = pyodbc.connect(connection_string_live)
        cursor = conn.cursor()
        if params:
            param_string = ','.join(['?'] * len(params))
        else:
            param_string = ''
        if params:
            result = cursor.execute("EXEC [dbo]." + name + param_string, params)
        else:
            result = cursor.execute(f"EXEC [dbo]. {name}")
        results = cursor.fetchall()
        if is_col_required:
            columns = [column[0] for column in cursor.description]
            results = pd.DataFrame.from_records(results, columns=columns)
            return results
        return results
    except Exception as e:
        print(str(e))
