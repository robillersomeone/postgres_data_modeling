# postgres_data_modeling


## Overview
Design a Postgres database and ETL pipeline for analyzing song play, based on song data and user logs, for a music streaming startup Sparkify in Python and Postgres.

The data is stored in JSON in two directories which can be found nested in
- data/song_data
  - this is a subset of the million song dataset
- data/log_data
  - from an event simulator

## Database Schema

The schema follows the star format with fact and dimension tables.

fact table
- songplay

dimension tables
- users
- artists
- time
- songs

<img src="./imgs/updated_database_schema.png" height="400px" width="600px">

## ETL pipeline

requirements?

### to create an instance of the database

From the project directory in the terminal run

`$ python create_tables.py`

this script connects to a postgreSQL database to make a Sparkify database and create the tables defined in the schema. It assumes there is a database `studentdb` to initially connect to.


### to populate the database

`$ python etl.py`

this script loads the JSON data from 'data/song_data' and 'data/log_data' to populate the tables.
