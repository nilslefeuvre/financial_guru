import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime 
from dateutil.relativedelta import relativedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.header("Quel avenir pour le cours de mon action ?")
st.write("Les prévisions sont réalisées à partir d"+"'"+"un modèle Prophet")
st.write("Le modèle est entrainé sur les 5 dernières années")

url = "https://fr.finance.yahoo.com/quote/%5EFCHI/components?p=%5EFCHI"
st.write("Pour accéder à l'ensemble des tickers du CAC40, cliquer [ici](%s)" % url)

user_input = st.text_input("Entrer le symbole de l'actif désiré :",'MSFT')

nb_jours = int(st.text_input("Entrer l'horizon de temps souhaité pour la prévision (en nombre de jours) :",365))

option = st.selectbox(
    'Sélectionner un modèle de prévision :',
    ('SARIMAX', 'Prophet'))

# Pour mettre une date à choisir
# d = st.date_input("Date de début")

# paramétrage des dates
start_date = (datetime.today()- relativedelta(years=5)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")

# Set the ticker
ticker = user_input

# Get the data
data = yf.download(ticker, start_date, end_date)
test = data.reset_index()

# Dataprep
input = test[['Date','Adj Close']]
input.columns = ['ds','y']
input['ds'] = pd.to_datetime(input['ds']).dt.strftime("%Y-%m-%d")

if option == 'Prophet':
  # modelling
  m = Prophet(daily_seasonality=True)
  m.fit(input)
  future = m.make_future_dataframe(periods=nb_jours)
  forecast = m.predict(future)

  # Plot 
  fig = px.line(test, x="Date",y="Adj Close")
  fig.data[0].name="Prix observé"
  fig.data[0].line.color = "#3A49F9"
  fig.update_traces(showlegend=True)
  fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Prix prévisionnel', line=dict(color="#F5241E"))
  # fig.update_layout(title_text=f'Predicted {ticker} Stock Prices For Next Year', title_x=0.5)
  title = f"Voici le cours prévisionnel de l"+"'"+f"actif {ticker} pour les {nb_jours} prochains jours"
  
  st.markdown(f"<h3 style='text-align: center; color: grey;'>{title}</h3>",unsafe_allow_html=True)
  st.plotly_chart(fig)
  
elif option == 'SARIMAX':
  # modelling
  model = sm.tsa.SARIMAX(input, order=(1,1,1), seasonal_order=(2,2,0,12))
  results = model.fit()
  forecast = results.predict(start=end_date, end=(pd.to_datetime(end_date) + relativedelta(days=nb_jours)).strftime("%Y-%m-%d"))
    
  # Plot
  fig,(ax1,ax2) = plt.subplots(2,figsize=(18,10))
  forecast.plot(label='Forecasts',ax=ax1,title='SARIMA Forecasting')
  test.plot(label='Actual',ax=ax1)
  ax1.set_ylabel('Stock Price')
  ax1.legend()
  ax2.legend()
  plt.tight_layout(pad=2)
  title = f"Voici le cours prévisionnel de l"+"'"+f"actif {ticker} pour les {nb_jours} prochains jours"

#   fig = px.line(test, x="Date",y="Adj Close")
#   fig.data[0].name="Prix observé"
#   fig.data[0].line.color = "#3A49F9"
#   fig.update_traces(showlegend=True)
#   fig.add_scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Prix prévisionnel', line=dict(color="#F5241E"))
#   # fig.update_layout(title_text=f'Predicted {ticker} Stock Prices For Next Year', title_x=0.5)
#   title = f"Voici le cours prévisionnel de l"+"'"+f"actif {ticker} pour les {nb_jours} prochains jours"




