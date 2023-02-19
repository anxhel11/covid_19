#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Load COVID-19 dataset
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'       'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'       'confirmed_global.csv'
df_confirmed = pd.read_csv(url)

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'       'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'       'deaths_global.csv'
df_deaths = pd.read_csv(url)

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'       'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'       'recovered_global.csv'
df_recovered = pd.read_csv(url)

# Combine confirmed, deaths, and recovered data into one dataframe
df = pd.concat([df_confirmed, df_deaths.iloc[:, 4:], df_recovered.iloc[:, 4:]], axis=1)
df.rename(columns={'Province/State': 'State', 'Country/Region': 'Country', 'Lat': 'Latitude', 'Long': 'Longitude'},
          inplace=True)

# Melt the dataframe to convert from wide to long format
df_melted = df.melt(id_vars=['State', 'Country', 'Latitude', 'Longitude'], var_name='Date', value_name='Cases')

# Group by country and date to get cumulative cases and deaths
df_grouped = df_melted.groupby(['Country', 'Date'])['Cases'].sum().reset_index()

# Impute missing values with zeros
imputer = SimpleImputer(strategy='constant', fill_value=0)
df_grouped_imputed = pd.DataFrame(imputer.fit_transform(df_grouped), columns=df_grouped.columns)

# Plot data for each country
countries = df_grouped_imputed['Country'].unique()
for country in countries:
    df_country = df_grouped_imputed[df_grouped_imputed['Country'] == country].reset_index()
    plt.plot(np.arange(0, len(df_country)), df_country['Cases'], label=country)
plt.title('Cumulative COVID-19 Cases by Country')
plt.xlabel('Days since January 22, 2020')
plt.ylabel('Number of Cases')
plt.legend()
plt.show()


# In[ ]:





# In[ ]:




