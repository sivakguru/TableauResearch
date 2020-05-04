#using pantab
#pantab is a wrapper on top of existing Hyper.api from tableau 

import pandas as pd
import tableauserverclient as TSC
import pantab as pt
from tableauhyperapi import TableName

#read data from csv using pandas in to a dataframe
data = pd.read_csv('C:\\Users\\sivkumar\\Documents\\Study Materials\\GeoSpatial\\placenamelatlon.csv', header='infer', sep=',')
#making a hyper file from dataframe
pt.frame_to_hyper(data, 'C:/Users/sivkumar/Documents/My Tableau Repository/Datasources/pantab_test.hyper', table='zip_data')

#make a table name using tableau hyperapi import TableName
table_name = TableName('Extract', 'Extract')
#using pantab to read hyper data in to a dataframe
capex = pt.frame_from_hyper('C:/Users/sivkumar/Documents/My Tableau Repository/Datasources/test_g20.hyper', table=table_name)

executive = pt.frame_from_hyper('C:/Users/sivkumar/Documents/My Tableau Repository/Datasources/executive_mbb.hyper', table=table_name)
