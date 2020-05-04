#Tableau Python Integration

#pip install tabpy-server
#pip install tabpy

SCRIPT_REAL("
import statsmodels.api as sm

import pandas as pd
import numpy as np
import scipy.stats as scs
from datetime import datetime
df = pd.DataFrame({'Month':_arg1, 'milk':_arg2})
df['milk'] = df['milk'].astype('float64')
df['Month'] = pd.to_datetime(_arg2)
df = df[['Month','milk']].set_index('Month')
df = df.fillna(0)


model=sm.tsa.ARIMA(endog = df['milk'], order=(min(_arg4),min(_arg5),min(_arg6)))
results=model.fit()
fitted_vals = list(results.fittedvalues.values)

return(fitted_vals)
"
,ATTR([Month]),ATTR([Sales]), MIN([Months Forecast]), MIN([AR (Time Lag)]), MIN([Seasonal Difference]), MIN([MA (Moving Average)]))