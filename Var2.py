# Importar paquetes
import numpy as np
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from scipy.stats import norm
# Función para descargar precios de cierre ajustados de varios activos a la vez:
def get_closes(tickers, start_date=None, end_date=None, freq=None):
    # Fecha inicio por defecto (start_date='2010-01-01') y fecha fin por defecto (end_date=today)
    # Frecuencia de muestreo por defecto (freq='d')
    # Importamos paquetes necesarios
    import pandas as pd
    pd.core.common.is_list_like = pd.api.types.is_list_like
    import pandas_datareader.data as web  
    # Creamos DataFrame vacío de precios, con el índice de las fechas
    closes = pd.DataFrame(columns = tickers, index=web.YahooDailyReader(symbols=tickers[0], start=start_date, end=end_date, interval=freq).read().index)
    # Agregamos cada uno de los precios con YahooDailyReader
    for ticker in tickers:
        df = web.YahooDailyReader(symbols=ticker, start=start_date, end=end_date, interval=freq).read()
        closes[ticker]=df['Adj Close']
    closes.index_name = 'Date'
    closes = closes.sort_index()
    return closes
##metodo parametrico, 1 mes
ticker=['GMEXICO','BECLE','LIVERPOOL', 'VOLARIS']
start,end='2017-08-24','2019-08-24' ##poner un día menos del actual
closes=pd.read_csv('../Data/datos.csv')
ret=closes.pct_change().dropna()
cov=ret.cov()
numberport=int(input("Quantity of stocks: "))
prices=np.empty((numberport,1))
for x in range(0,numberport):
    prices[x][0] = closes[ticker[x]].iloc[-1]
titles=np.empty((numberport,1))
for x in range(0,numberport):
    titles[x][0]=int(input("Quantity of titles of stock in order: "))
totalmatrix=np.multiply(prices, titles)
exposure = 0
for n in totalmatrix:
        exposure += n
exposure=float(exposure) 
print(totalmatrix)
print (exposure)
ws=totalmatrix/exposure
wt=np.transpose(ws)
cov=np.matrix(cov)
x=wt*cov*ws
risk=norm.ppf(1-((float(input("risk level in percentage ")))/100))
var=risk*(exposure)*np.sqrt(x)
print(var)
### metodo no parametrico, 1 año
start,end='2018-08-22','2019-08-20'
closes=get_closes(ticker,start,end,freq='d')
ret=closes.pct_change().dropna()
ret=pd.DataFrame(ret)
prodw=[]
for r in range(0,len(ret)):
    row=np.matrix(ret.iloc[r])
    row=np.transpose(row)
    sumpro=np.multiply(ws,row)
    sumprod = 0
    for n in sumpro:
        sumprod += n
    prodw.append(float(sumprod))
p = np.percentile(prodw, 2.5)
print(p)
print(exposure)
var2=p*exposure
print(var2)