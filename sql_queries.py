# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# Create fact table songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id serial PRIMARY KEY,
start_time time,
user_id varchar NOT NULL,
level varchar,
song_id varchar,
artist_id varchar,
session_id varchar,
location varchar,
user_agent varchar
);
""")
# Issue: it can be seen that you have created the songplay_id column with SERIAL datatype. Hence, you don't need to include that column name while inserting the values in that table. SERIAL is an auto-incremented integer column.

# Create dimension table users - users in the app
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id varchar PRIMARY KEY NOT NULL,
first_name varchar,
last_name varchar,
gender varchar,
level varchar
);
""")

# Create dimension table songs - songs in music database
song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id varchar PRIMARY KEY NOT NULL,
title varchar NOT NULL,
artist_id varchar NOT NULL,
year int,
duration float
);
""")

# Create dimension table artists - artists in music database
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id varchar PRIMARY KEY NOT NULL,
name varchar,
location varchar,
latitude varchar NOT NULL,
longitude varchar NOT NULL
);
""")

# Create dimension table artists - timestamps of records in songplays broken down into specific units
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time time PRIMARY KEY NOT NULL,
hour numeric NOT NULL,
day numeric NOT NULL,
week numeric NOT NULL,
month varchar NOT NULL,
year int NOT NULL,
weekday int NOT NULL
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    VALUES(to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s);
""")

# From code review: A user will be present even if he/she is a free tier user. 
# But what if the free tier user converts into a paid user. In that case we have to modify the level of the user as below:
user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (user_ID) DO UPDATE SET level = excluded.level    
    ;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING
    ;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING
    ;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING
    ;
""")

# FIND SONGS
# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.
song_select = ("""
SELECT songs.song_id, artists.artist_id
FROM songs
JOIN artists ON
songs.artist_id = artists.artist_id 
WHERE songs.title = (%s) AND artists.name = (%s) AND songs.duration = (%s)
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
