import calendar
from math import isnan

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pycountry_convert import (
    country_alpha2_to_continent_code,
    country_alpha2_to_country_name,
    country_name_to_country_alpha3,
)

import data

## Used to convert default 2 character continent codes to full continent names
continents = {
    "NA": "North America",
    "SA": "South America",
    "AS": "Asia",
    "OC": "Australia",
    "AF": "Africa",
    "EU": "Europe",
}

df = data.generate_flattened_dataframe()

## creates column in dataframe containing ISO-Alpha3 conversion of ISO-Alpha2 country codes
df["victim.country.alpha3"] = df["victim.country.0"].apply(
    lambda c: c
    if c == "Unknown"
    else country_name_to_country_alpha3(country_alpha2_to_country_name(c))
)
## creates column in dataframe containing continent name corresponding to ISO-Alpha2 country code
df["victim.continent"] = df["victim.country.0"].apply(
    lambda c: c
    if c == "Unknown"
    else "Asia"
    if c == "TL"
    else "North America"
    if c == "UM"
    else continents[country_alpha2_to_continent_code(c)]
)

## Figure representing # Incidents / Incident Year as a bar chart
fig_incident_year = px.bar(
    df[df["timeline.incident.year"].astype(int) >= 2000]["timeline.incident.year"]
    .value_counts()[lambda x: x != 0]
    .rename("count")
    .reset_index(),
    x="index",
    y="count",
    labels={"index": "Incident Year", "count": "# Incidents"},
    title="# Incidents / year",
)
fig_incident_year.update_xaxes(tickmode="linear", tickfont=dict(size=10))
fig_incident_year.update_yaxes(fixedrange=True)

fig_avg_incident_month = px.bar(
    df["timeline.incident.month"]
    .value_counts()
    .apply(lambda c: c / len(pd.unique(df["timeline.incident.year"])))[lambda x: x != 0]
    .rename("count")
    .reset_index(),
    x="index",
    # x=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    y="count",
    labels={"index": "Incident Month", "count": "Avg # Incidents"},
    title="Average # Incidents / Month",
)
fig_avg_incident_month.update_xaxes(tickmode="linear")
fig_avg_incident_month.update_yaxes(fixedrange=True)

## Figure representing # Incidents / Error variety as a bar chart
fig_error_variety = px.bar(
    df["action.error.variety.0"].value_counts().rename("count").reset_index(),
    x="index",
    y="count",
    color="index",
    labels={"index": "Error Variety", "count": "# Incidents"},
    title="# Incidents / Error Variety",
)
fig_error_variety.update_layout(showlegend=False)
fig_error_variety.update_xaxes(tickangle=70, tickfont=dict(size=10))

fig_incident_victims = px.bar(
    df["victim.victim_id"]
    .value_counts()[lambda c: c > 10]
    .rename("count")
    .reset_index(),
    x="index",
    y="count",
    labels={"index", "Incident Victim", "count", "# Incidents"},
    title="Most common incident victims",
)

## Figure representing # Incidents / Country as a geographical scatter plot
## TODO -> Join continent code and use to encode color
fig_incident_locations = px.scatter_geo(
    df[df["victim.country.alpha3"] != "Unknown"]["victim.country.alpha3"]
    .value_counts()[lambda x: x > 10]
    .rename("count")
    .reset_index(),
    locations="index",
    size="count",
    size_max=100,
    color="index",
    projection="natural earth",
    title="Incident Locations",
    labels={"index": "Country", "count": "# of Incidents"},
)

fig_data_variety = px.pie(
    df["attribute.confidentiality.data.0.variety"]
    .value_counts()
    .rename("count")
    .reset_index(),
    names="index",
    values="count",
    color="index",
    title="Confidential Data Occurences",
    labels={"index": "Confidential Data Category", "count": "# Occurences"},
)
fig_data_variety.update_traces(textposition="inside")
fig_data_variety.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")

summary_table = dbc.Table.from_dataframe(
    df.iloc[:, [18, 22]]
    .reset_index()
    .rename(
        columns={
            "index": "#",
            "reference": "Incident Reference",
            "summary": "Incident Summary",
        }
    ),
    bordered=True,
    hover=True,
    color="primary",
    responsive="sm",
    size="sm",
    style={
        "word-break": "break-word",
        "font-size": 12,
    },
)
