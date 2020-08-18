# postgreSQL_data_modeling
Data modeling a Spotify-like music database using postgreSQL within a Python wrapper.

## Background
This project creates an ETL pipeline that makes song data available for the analytics team at the startup Sparkify to understand what songs users are listening to.
Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. This project creates a Postgres database with tables designed to optimize queries on song play analysis.

## Data
1. **Song Dataset** - Each file is in JSON format and contains metadata about a song and the artist of that song. 
The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset:
`song_data/A/B/C/TRABCEI128F424C983.json`
`song_data/A/A/B/TRAABJL12903CDCF1A.json`

Below is an example of a single song file:
`{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`

2. **Log Dataset** - This data is based on simulated activity logs from a music streaming app based on specified configurations.

The log files in this dataset partitioned by year and month. For example, here are filepaths to two files in this dataset:
`log_data/2018/11/2018-11-12-events.json`
`log_data/2018/11/2018-11-13-events.json`

To read one of these json files into a Pandas DataFrame, use a query such as this:
`df = pd.read_json('data/log_data/2018/11/2018-11-01-events.json', lines=True)`

## Database Schema - The schema consists of one fact table and four dimension tables.

### Fact Table
1. Songplays - records in log data associated with song plays i.e. records with page `NextSong`
- songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
2. users - the users in the app
user_id, first_name, last_name, gender, level

3. songs - songs in music database
song_id, title, artist_id, year, duration

4. artists - artists in music database
artist_id, name, location, latitude, longitude

5. time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

