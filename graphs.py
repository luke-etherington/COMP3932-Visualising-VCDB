from turtle import color
import pandas as pd
import data
import plotly.express as px
from pycountry_convert import country_alpha2_to_continent_code, country_alpha2_to_country_name, country_name_to_country_alpha3
from dash import dcc
import dash_bootstrap_components as dbc

## Used to convert default 2 character continent codes to full continent names
continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}

df = data.generate_flattened_dataframe()

## creates column in dataframe containing ISO-Alpha3 conversion of ISO-Alpha2 country codes
df['victim.country.alpha3'] = df['victim.country.0'].apply(lambda c : c if c == 'Unknown' else country_name_to_country_alpha3(country_alpha2_to_country_name(c)))
## creates column in dataframe containing continent name corresponding to ISO-Alpha2 country code
df['victim.continent'] = df['victim.country.0'].apply(lambda c: c if c == 'Unknown' else 'Asia' if c == 'TL' else 'North America' if c == 'UM' else continents[country_alpha2_to_continent_code(c)])


## Figure representing # Incidents / Error variety as a bar chart
fig_error_variety = px.bar(df['action.error.variety.0'].value_counts().rename("count").reset_index(), 
    x='index', 
    y='count', 
    color='index',
    labels={
        "index" : "Error Variety",
        "count" : "Count"
    },
    title="Count of Error Variety"
)

## Figure representing # Incidents / Country as a geographical scatter plot
## TODO -> Join continent code and use to encode color
fig_incident_locations = px.scatter_geo(df[df['victim.country.alpha3'] != 'Unknown']['victim.country.alpha3'].value_counts()[lambda x: x > 10].rename("count").reset_index(), 
    locations='index', 
    size='count', 
    size_max=100,
    color='index',
    projection='natural earth',
    title="Incident Locations",
    labels={
        'index' : "Country",
        'count' : "# of Incidents"
    }
)

fig_data_variety = px.pie(df['attribute.confidentiality.data.0.variety'].value_counts().rename("count").reset_index(),
    names ='index',
    values='count',
    color='index',
    title="Confidential Data Occurences",
    labels={
        "index": "Confidential Data Category",
        "count": "# Occurences"
    }
)

summary_table = dbc.Table.from_dataframe(df.iloc[:, [18,22]].reset_index().rename(columns={"index": "#", "reference": "Incident Reference", "summary": "Incident Summary"}), 
    bordered=True, 
    hover=True,
    color='primary',
    responsive='sm', 
    size='sm', 
    style={
        'word-break': 'break-word', 
        'font-size': 12,
    }
)