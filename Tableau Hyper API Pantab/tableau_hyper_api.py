#Intall Tableau Hyper API
#pip install tableauhyperapi

# To Upgrade the Old version of Hyper API
#pip install --upgrade tableauhyperapi

#import necessary packages
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, NOT_NULLABLE, NULLABLE, SqlType, \
TableDefinition, Inserter, escape_name, escape_string_literal, HyperException, TableName

import pandas as pd

column_names = []
with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    #create a connection to the existing hyper data file
    with Connection(hyper.endpoint, database='C:/Users/sivkumar/Documents/My Tableau Repository/Datasources/test_g20.hyper') as connection:
        table_names = list(connection.catalog.get_table_names('Extract'))
        for table in table_names:
            table_defenition = connection.catalog.get_table_definition(name=table)
            print(table)
            for column in table_defenition.columns:
                column_names.append(str(column.name).replace('"', ''))
                #print(column.name)

#open Hyper process bata base
#using with condition to open the Hyper process makes sure the server is shut down when the process is done
with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    #create a connection to the existing hyper data file
    with Connection(hyper.endpoint, database='C:/Users/sivkumar/Documents/My Tableau Repository/Datasources/test_g20.hyper') as connection:
        with connection.execute_query(query= f"select * from {TableName('Extract', 'Extract')} limit 10 ") as result:
            rows = list(result)
            #print(rows)

data = pd.DataFrame(rows)

df_columns = data.columns

dict_column_names = dict(zip(df_columns, column_names))

data.rename(columns=dict_column_names, inplace=True)

from shapely import wkb

test = geo_data.loc[0,'geom']

test = test.decode('cp855')

test = test.encode('utf-8')

shp = wkb.loads(test, hex=True)