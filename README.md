# CareFlow Clinical Pathway Process Mining

## Project Overview

CareFlow is a process mining project that analyses simulated hospital event logs to understand patient journeys, identify process inefficiencies, and investigate potential bottlenecks.

## Project Objectives

* Generate simulated hospital event logs using Python.
* Prepare and clean event data.
* Discover hospital workflows using process mining.
* Analyse activity sequences and waiting times.
* Develop a dashboard to present findings.
* Perform conformance checking and document the results.

## Technologies

* Python
* CSV
* Google BigQuery
* dbt
* PM4Py
* Power BI or Looker

## Current Progress

* [x] Generated simulated hospital event logs using Python.
* [x] Created the CSV file containing case IDs, activity names, and timestamps.
* [ ] Load raw data into BigQuery.
* [ ] Configure dbt and clean the data.
* [ ] Discover processes using PM4Py.
* [ ] Analyse waiting times and bottlenecks.
* [ ] Build the dashboard.
* [ ] Complete conformance checking and final documentation.

## Data Fields

* `Case_ID`: Identifier for a simulated patient case.
* `Activity_Name`: Hospital activity performed.
* `Timestamp`: Date and time of the activity.

## Data Privacy

This initial dataset contains simulated data, not real patient records.

