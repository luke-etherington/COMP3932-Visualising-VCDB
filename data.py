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
# data.py
# =============================================================================

import json

import pandas as pd
from flatten_json import flatten
from pycountry_convert import (
    country_alpha2_to_continent_code,
    country_alpha2_to_country_name,
    country_name_to_country_alpha3,
)

from data_update import update_zip_file

DATA_FILE = "./data/vcdb_1-of-1.json"


## Given a specified JSON filename, returns the JSON data contained in the file
def read_json_file(filename):
    f = open(filename, "r")
    data = json.loads(f.read())
    f.close()
    return data


## Given some JSON data, returns a pandas dataframe object containing the fully flattened version of the provided JSON data
def get_flattened_dataframe(json_data):
    return pd.DataFrame([flatten(d, ".") for d in json_data])


## Provides a pandas dataframe of the flattened JSON data from file
def generate_flattened_dataframe():
    # update_zip_file()
    data = read_json_file(DATA_FILE)
    df = get_flattened_dataframe(data)

    ## Used to convert default 2 character continent codes to full continent names
    continents = {
        "NA": "North America",
        "SA": "South America",
        "AS": "Asia",
        "OC": "Australia",
        "AF": "Africa",
        "EU": "Europe",
    }

    # Reduce dataframe to required fields
    df = df[
        [
            "victim.country.0",
            "actor.external.country.0",
            "timeline.incident.year",
            "timeline.incident.month",
            "action.error.variety.0",
            "victim.victim_id",
            "attribute.confidentiality.data_disclosure",
            "attribute.confidentiality.data.0.variety",
            "reference",
            "summary",
        ]
    ]

    ## create column in dataframe containing full country name corresponding to ISO-Alpha2 country code
    df["victim.country.fullname"] = df["victim.country.0"].apply(
        lambda c: c if c == "Unknown" else country_alpha2_to_country_name(c)
    )

    ## creates column in dataframe containing ISO-Alpha3 conversion of ISO-Alpha2 country codes for victim country
    df["victim.country.alpha3"] = df["victim.country.fullname"].apply(
        lambda c: c if c == "Unknown" else country_name_to_country_alpha3(c)
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

    ## create column in dataframe containing full country name corresponding to ISO-Alpha2 country code for actor country
    df["actor.external.country.fullname"] = df["actor.external.country.0"].apply(
        lambda c: ""
        if c == "Unknown" or c == "Other" or type(c) == float
        else country_alpha2_to_country_name(c)
    )

    ## creates column in dataframe containing ISO-Alpha3 conversion of ISO-Alpha2 country codes for actor country
    df["actor.external.country.alpha3"] = df["actor.external.country.fullname"].apply(
        lambda c: "" if c == "" else country_name_to_country_alpha3(c)
    )

    ## create column in dataframe containing continent name corresponding to ISO-Alpha2 country code for actor country
    df["actor.external.continent"] = df["actor.external.country.0"].apply(
        lambda c: c
        if type(c).__name__ == "float" or c == "Unknown" or c == "Other"
        else continents[country_alpha2_to_continent_code(c)]
    )

    return df


## Utility function used to output pandas dataframe to excel file
## USE FOR DEBUGGING PURPOSES ONLY
def generate_excel_output(df):
    return df.to_excel("./data/output.xlsx")
