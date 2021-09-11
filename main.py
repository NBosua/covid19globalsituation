from numpy import int64
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_daily = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

df_confirmed = pd.DataFrame()
df_daily = pd.DataFrame()

st.set_page_config(page_title="COVID19 Dashboard", layout="wide")

#@st.cache
def load_data_sources():
    global df_confirmed
    global df_daily

    #df_confirmed = pd.read_csv(url_confirmed, header=0)
    #df_confirmed.rename(columns={'Lat': "lat", 'Long':"lon"}, inplace=True) # fore use in map
    #df_confirmed['lat'] = df_confirmed['lat'].astype(float)
    #df_confirmed['lon'] = df_confirmed['lon'].astype(float)

    
    current_date = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')
    df_daily = pd.read_csv(url_daily+current_date+'.csv', header=0)


def load_dashboard():
    st.title("COVID19 Global Situation Report")
  
    cols = st.columns(7)

    cols[0].metric(label="COUNTRIES", value=str(len(df_daily['Country_Region'].unique())))
    cols[1].metric(label="CONFIRMED", value=str(df_daily['Confirmed'].sum()))
    cols[2].metric(label="DEATHS", value=str(df_daily['Deaths'].sum()))
    cols[3].metric(label="RECOVERED", value=str(df_daily['Recovered'].sum()))
    cols[4].metric(label="ACTIVE", value=str(df_daily['Active'].sum()))
    cols[5].metric(label="INCIDENT RATE", value=str(round(df_daily['Incident_Rate'].mean(),3)))
    cols[6].metric(label="FATALITY RATIO", value=str(round(df_daily['Case_Fatality_Ratio'].mean(),3)))

    #st.map(df_confirmed, zoom=3)

    st.table(df_daily[['Country_Region', 'Province_State', 'Confirmed', 'Deaths', 'Active', 'Recovered', 'Case_Fatality_Ratio']].groupby(['Country_Region']).sum().sort_values(by='Confirmed', ascending=False))
    print(df_daily.dtypes)


def main():
    load_data_sources()
    load_dashboard()


if __name__ == "__main__":
    main()