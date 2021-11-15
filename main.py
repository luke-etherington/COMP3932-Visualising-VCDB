#!/usr/bin/env python3
# coding=utf-8
# =============================================================================
"""
Author: Luke Etherington
Email: sc18lge@leeds.ac.uk
Module: COMP3932 - Synoptic project
Supervisor: Nick Efford
"""
# =============================================================================
""" Visualising Data Security Incidents using VCDB

"""

import pandas as pd
import matplotlib.pyplot as plt
import json
DATA_FILE = "./data/vcdb_1-of-1.json"


def main():
    vcdbData = pd.read_json(DATA_FILE)
    plotIncidentVariety(vcdbData)

def plotIncidentVariety(vcdbData):
    actionData = pd.json_normalize(vcdbData['action'])
    actionVarieties = actionData.filter(regex='.variety$')
    actionVarietySum = actionVarieties.count()
    actionVarietySum.plot.bar(x="Incident Variety", y="# Incidents")
    plt.tight_layout()
    plt.xlabel("Incident Variety")
    plt.ylabel("# Incidents")
    plt.grid(True,axis='y')
    plt.show()

def loadJSON(filepath):
    f = open(filepath, 'r')
    data = json.loads(f.read())
    f.close()
    return data


if __name__ == "__main__":
    main()
