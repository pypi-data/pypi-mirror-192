import pandas


def snowflake_pull(query: str, username: str, warehouse: str, role: str, database: str = 'NA', sample_table: bool = False,
                   sample_val: bool = False, table_sample: dict = None, dtypes_conv=None) -> pandas.DataFrame:

    un, wh, db = username, warehouse, database

    """
    function: pulls snowflake data

    dependencies: [
        pandas,
        snowflake.connector,
        time,
        datetime.datetime
    ]

    :param query: str
        SQL query to run on Snowflake
        query = "SELECT * FROM  NGP_DA_PROD.POS.TO_DATE_AGG_CHANNEL_CY"

    :param un: str
        Nike Snowflake Username
            "USERNAME"

    :param db: str, default 'NA'
        Name of the Database

    :param wh: str
        Name of the Wharehouse
        e.g. "DA_DSM_SCANALYTICS_REPORTING_PROD"

    :param role: str
        Name of the role under which you are running Snowflake
            "DF_######"

    :param sample_table: bool, default: False

    :param sample_val: bool, default: False

    :param table_sample: dict, default: None
        later
            if table_sample = None
                table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}

    :param dtypes_conv: default: None

    :return: pandas.DataFrame
    """

    # snowflake connection packages:
    import pandas as pd
    import snowflake.connector
    # other packages:
    import time
    from datetime import datetime

    if table_sample is None:
        table_sample = {'db': None, 'schema': None, 'table': None, 'col': None}

    # --> take a random sample from a table in snowflake
    query = f'''SELECT * FROM {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} LIMIT 500''' if sample_table == True else query
    # --> take a random sample of a column from a table in snowflake
    query = f'''SELECT DISTINCT {table_sample['col']} FROM {table_sample['db']}.{table_sample['schema']}.{table_sample['table']} ORDER BY 1 LIMIT 10''' if sample_val == True else query

    print(f'Started query: {datetime.now().strftime("%H:%M:%S")}')
    tic = time.perf_counter()  # start timer
    conn = snowflake.connector.connect(
        user=un,
        account='nike',
        authenticator='externalbrowser',  # opens separate browser window to confirm authentication
        warehouse=wh,
        database=db,
        role=role
    )  # connection settings
    cur = conn.cursor()  # connect to snowflake using conn variables
    cur.execute(query)  # execute sql, store into-->
    try:
        df = cur.fetch_pandas_all() if dtypes_conv == None else cur.fetch_pandas_all().astype(
            dtypes_conv)  # final data pull --> allows datatype-memory optimization
    except:  # --> allows metadata querying
        temp_df = cur.fetchall()  # return data
        cols = [x.name for x in cur.description]  # get column names
        df = pd.DataFrame(temp_df, columns=cols)  # create dataset

    conn.close()
    cur.close()  # close connections
    toc = time.perf_counter()  # end timer
    print(f'''Query finished in {toc - tic:0.4f} seconds ({(toc - tic) / 60:0.4f} minutes)
    ''')
    return df


