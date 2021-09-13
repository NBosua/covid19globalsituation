from numpy import int64
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from urllib.error import HTTPError
import plotly.express as px


url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_daily = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

df_confirmed = pd.DataFrame()
df_daily = pd.DataFrame()
current_date = datetime.today()

st.set_page_config(page_title="COVID19 Dashboard", layout="wide")


def extract_data(adjust_days):
    global df_daily
    global current_date

    current_date = (datetime.today() - timedelta(days=adjust_days)).strftime('%m-%d-%Y')
    #print('reading file with date:'+str(current_date))
    try:
        df_daily = pd.read_csv(url_daily+current_date+'.csv', header=0)
    except HTTPError as e:
        if e.code == 404:
            extract_data(adjust_days+1)
    

#@st.cache
def load_data_sources():
    global df_confirmed
    global df_daily

    #df_confirmed = pd.read_csv(url_confirmed, header=0)
    #df_confirmed.rename(columns={'Lat': "lat", 'Long':"lon"}, inplace=True) # fore use in map
    #df_confirmed['lat'] = df_confirmed['lat'].astype(float)
    #df_confirmed['lon'] = df_confirmed['lon'].astype(float)

    extract_data(1)


def load_dashboard():
    cols_header = st.columns(2)
    cols_header[0].title("COVID19 Global Situation Report")
    cols_header[1].subheader("Lastest update: "+current_date)
  
    cols = st.columns(7)

    cols[0].metric(label="COUNTRIES", value=str(len(df_daily['Country_Region'].unique())))
    cols[1].metric(label="CONFIRMED", value=str(df_daily['Confirmed'].sum()))
    cols[2].metric(label="DEATHS", value=str(df_daily['Deaths'].sum()))
    cols[3].metric(label="RECOVERED", value=str(df_daily['Recovered'].sum()))
    cols[4].metric(label="ACTIVE", value=str(df_daily['Active'].sum()))
    cols[5].metric(label="INCIDENT RATE", value=str(round(df_daily['Incident_Rate'].mean(),3)))
    cols[6].metric(label="FATALITY RATIO", value=str(round(df_daily['Case_Fatality_Ratio'].mean(),3)))

    #st.map(df_confirmed, zoom=3)
    st.subheader("Top 20 Countries by Confirmed Cases")

    #st.bar_chart(df_daily[['Country_Region', 'Confirmed', 'Deaths']].groupby(['Country_Region']).sum().sort_values(by='Confirmed', ascending=False).head(20))
    
    fig = px.bar(df_daily[['Country_Region', 'Confirmed']].groupby(['Country_Region']).sum().sort_values(by='Confirmed', ascending=False).reset_index().head(20), y='Confirmed', x='Country_Region')
    st.plotly_chart(fig, use_container_width=True)

    st.table(df_daily[['Country_Region', 'Province_State', 'Confirmed', 'Deaths', 'Active', 'Recovered', 'Case_Fatality_Ratio']].groupby(['Country_Region']).sum().sort_values(by='Confirmed', ascending=False))


def main():
    load_data_sources()
    load_dashboard()


if __name__ == "__main__":
    main()