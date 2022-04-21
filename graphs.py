# !/usr/bin/env python3
# coding=utf-8
# =============================================================================
# Author: Luke Etherington
# Email: sc18lge@leeds.ac.uk
# Module: COMP3932 - Synoptic project
# Supervisor: Nick Efford
#
# Visualising Data Security Incidents using VCDB
#
# graphs.py
# =============================================================================

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

import data

# Used to convert month numbers to full month names
months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

# Populate dataframe
df = data.generate_flattened_dataframe()

## Figure representing # Incidents / Incident Year as a bar chart
fig_incident_year = px.bar(
    df[df["timeline.incident.year"].astype(int) >= 2000]["timeline.incident.year"]
    .value_counts()[lambda x: x != 0]
    .rename("count")
    .reset_index(),
    x="index",
    y="count",
    labels={"index": "Incident Year", "count": "# Incidents"},
    title="# Incidents / year since 2000",
)
fig_incident_year.update_xaxes(tickmode="linear", tickfont=dict(size=10))

# Figure representing average # incidents / month
fig_avg_incident_month = px.bar(
    df["timeline.incident.month"]
    .apply(lambda m: m if m not in months.keys() else months[m])
    .value_counts()[list(months.values())]
    .apply(lambda c: round(c / len(pd.unique(df["timeline.incident.year"]))))[
        lambda x: x != 0
    ]
    .rename("count")
    .reset_index(),
    x="index",
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
    labels={
        "index": "Error Variety",
        "count": "# Incidents",
    },
    title="# Incidents / Error Variety<br><sup> The type of error made by the actor at fault which influenced the incident</sup>",
)
fig_error_variety.update_layout(showlegend=False)
fig_error_variety.update_xaxes(tickangle=70, tickfont=dict(size=10))

# Figure representing top 10 victims by # incidents
fig_incident_victims = px.bar(
    df[["victim.victim_id", "attribute.confidentiality.data_disclosure"]][
        df["victim.victim_id"].isin(
            df[df["victim.victim_id"] != "Unknown"]["victim.victim_id"]
            .value_counts()
            .nlargest(10)
            .index.tolist()
        )
    ]
    .value_counts()
    .rename("count")
    .reset_index(),
    y="victim.victim_id",
    x="count",
    color="attribute.confidentiality.data_disclosure",
    barmode="group",
    orientation="h",
    log_x=True,
    hover_data={
        "victim.victim_id": True,
        "attribute.confidentiality.data_disclosure": True,
        "count": True,
    },
    labels={
        "victim.victim_id": "Incident Victim",
        "attribute.confidentiality.data_disclosure": "Confidential Data Disclosure",
        "count": "# Incidents",
    },
    title="10 Most Common Incident Victims<br><sup>Split by confidential data loss status of incident</sup>",
)
fig_incident_victims.update_layout(legend=dict(orientation="h", x=0.5, y=1))

## Figure representing # Incidents / Country as a geographical scatter plot
fig_incident_locations = px.scatter_geo(
    df.loc[
        df["victim.country.alpha3"] != "Unknown",
        ["victim.country.alpha3", "victim.continent", "victim.country.fullname"],
    ]
    .value_counts()
    .reset_index()
    .rename(columns={0: "count"}),
    locations="victim.country.alpha3",
    size="count",
    size_max=200,
    color="victim.continent",
    hover_name="victim.country.fullname",
    hover_data={
        "victim.country.alpha3": False,
        "victim.country.fullname": False,
        "victim.continent": False,
        "count": True,
    },
    projection="natural earth",
    title="Incident Locations<br><sup> Location of Incident Victims. Hover a bubble to see more details. Click + Drag to navigate. Scroll wheel to zoom (or use the navigation buttons in the top right).</sup>",
    labels={
        "victim.country.fullname": "Country",
        "count": "# of Incidents",
        "victim.continent": "Continent",
    },
)

## Figure representing # Incidents / actor location as a geographical scatter plot
fig_actor_locations = px.scatter_geo(
    df.loc[
        df["actor.external.country.alpha3"] != "",
        [
            "actor.external.country.alpha3",
            "actor.external.country.fullname",
            "actor.external.continent",
        ],
    ]
    .value_counts()
    .reset_index()
    .rename(columns={0: "count"}),
    locations="actor.external.country.alpha3",
    size="count",
    size_max=100,
    color="actor.external.continent",
    hover_name="actor.external.country.fullname",
    hover_data={
        "actor.external.country.alpha3": False,
        "actor.external.country.fullname": False,
        "actor.external.continent": False,
        "count": True,
    },
    projection="natural earth",
    title="External Actor Locations<br><sup> Main location of malicious actors. Hover a bubble to see more details.  Click + Drag to navigate. Scroll wheel to zoom (or use the navigation buttons in the top right)</sup>",
    labels={
        "actor.external.country.fullname": "Country",
        "actor.external.continent": "Continent",
        "count": "# of Incidents",
    },
)

# Figure representing % split of incidents per confidential data type
fig_data_variety = px.pie(
    df["attribute.confidentiality.data.0.variety"]
    .value_counts()
    .rename("count")
    .reset_index(),
    names="index",
    values="count",
    color="index",
    title="Confidential Data Occurences<br><sup> The type of confidential data effected by the incident.",
    labels={"index": "Confidential Data Category", "count": "# Occurences"},
)
fig_data_variety.update_traces(textposition="inside")
fig_data_variety.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")

# Table chart showing incident reference and incident summary
summary_table = dbc.Table.from_dataframe(
    df[["reference", "summary"]]
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
