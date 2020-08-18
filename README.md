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

### Justification for database schema design

### Fact Table
1. Songplays - records in log data associated with song plays i.e. records with page `NextSong`

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
2. users - the users in the app

user_id, first_name, last_name, gender, level

3. songs - songs in music database

song_id, title, artist_id, year, duration

4. artists - artists in music database

artist_id, name, location, latitude, longitude

5. time - timestamps of records in songplays broken down into specific units

start_time, hour, day, week, month, year, weekday

## Project File Structure
1. `data` folder - contains the song and log datasets
2. `sql_queries.py` contains all sql queries, and is imported into `create_tables.py`, `etl.ipynb`, and `etl.py`
3. `create_tables.py` drops and creates your tables. Run this file to reset your tables before each time you run your ETL scripts.
4. `test.ipynb` displays the first few rows of each table to let you check your database
5. `etl.ipynb` reads and processes a single file from `song_data` and `log_data` and loads the data into your tables. This notebook contains detailed instructions on the ETL process for each of the tables.
6. `etl.py` reads and processes files from `song_data` and `log_data` and loads them into your tables. You can fill this out based on your work in the ETL notebook.
7. `README.md` provides discussion on the project.

## Steps to Follow
### A. Creating Tables
1. Write `DROP` and `CREATE` table statements in `sql_queries.py`.
2. Ran `!python create_tables.py` in the console.
3. Ran `create_tables.py` to create the database and tables.
4. Ran `test.ipynb` to confirm the creation of tables with the correct columns. __Note: Make sure to click "Restart kernel" to close the connection to the database after running this notebook.__

### B. Build and Implement the ETL Pipeline
1. Followed the instructions in `etl.ipynb` to develop the ETL process for each table before completing the `etl.py` file to load the whole datasets.
2. Transferred these steps into `etl.py`.
3. Ran `!python etl.py` in the console.
4. Verify the data was inserted into the tables with `test.ipynb`.

## ETL Pipeline Overview
1. Connect to the Sparkify database.
2. Process song data. Use the `get_files` function to get a list of all song JSON files in data/song_data.
2a. Extract data for the `Songs` table and `Artists` table from the `song_data` file.
3. Process log data. Use the `get_files` function to get a list of all song JSON files in data/log_data.
3a. Extract data for the `time` table, `users` table, and `songplays` table from the `log` file.
__Note: `time` table is in milliseconds. Since the log file does not specify an ID for either the song or the artist, you'll need to get the song ID and artist ID by querying the songs and artists tables to find matches based on song title, artist name, and song duration time.__
4. Insert the extracted data using `etl.py`.
4a. def process_song_file(cur, filepath): Extracts the song files.
4b. def process_log_file(cur, filepath): Extracts the log files.
4c. def process_data(cur, conn, filepath, func): Processes the data extracted from 4a. and 4b.
4d. def main(): Calls the process_data function using process_song_file() and process_log_file().
5. Close connection to the Sparkify database.

## Challenges faced
1. Conflicting values for user_ID and artist_ID when inserting data.
Solution: Add `ON CONFLICT (artist_id) DO NOTHING`.
For example:
artist_table_insert = ("""
`INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING
    ;
""")`
2. Convert the ts timestamp column to datetime
Solution found here: https://datascience.stackexchange.com/questions/14645/convert-a-pandas-column-of-int-to-timestamp-datatype
