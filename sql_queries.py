# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_table
(songplay_id serial primary key, start_time timestamp, user_id varchar, level varchar, song_id varchar, artist_id varchar,
session_id varchar, location varchar, user_agent varchar);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_table
(user_id int primary key, first_name varchar, last_name varchar, gender varchar, level varchar);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS song_table
(song_id varchar primary key, title varchar, artist_id varchar, year int, duration decimal);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS
artist_table (artist_id varchar primary key, artist_name varchar, artist_latitude decimal, artist_longitude decimal);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_table
(start_time int primary key, hour int, day int, week int, month int, year int, weekday int);
""")


# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplay_table
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT songplay_table_pkey DO NOTHING;
""")

user_table_insert = ("""INSERT INTO user_table
(user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT user_table_pkey DO UPDATE SET level=EXCLUDED.level;
""")

song_table_insert = ("""INSERT INTO song_table
(song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT song_table_pkey DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artist_table
(artist_id, artist_name, artist_latitude, artist_longitude)
VALUES (%s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT artist_table_pkey DO NOTHING;
""")


time_table_insert = ("""INSERT INTO time_table
(start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT time_table_pkey DO NOTHING;
""")

# FIND SONGS
# find song_id and artist_id based on title, artist_name, duration
song_select = ("""
 SELECT s.song_id, a.artist_id FROM song_table as s
 JOIN artist_table as a ON s.artist_id = a.artist_id
 WHERE s.title = %s AND a.artist_name = %s AND s.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
