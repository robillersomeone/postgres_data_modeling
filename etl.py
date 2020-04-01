import os
import glob
import config
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    instance of the cursor, filepath for song data

    inserts song data into the song and artist tables in the sparkifydb database
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title','artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    instance of the cursor, filepath for log data

    inserts log data into the time, user, and songplay tables in the sparkifydb database
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong'].reset_index()

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    df['ts'] = t
    timestamp = df['ts'] # .apply(lambda x: x.timestamp()).values
    hour = df['ts'].apply(lambda x: x.hour).values
    day = df['ts'].apply(lambda x: x.day).values
    weekofyear = df['ts'].apply(lambda x: x.weekofyear).values
    month = df['ts'].apply(lambda x: x.month).values
    year = df['ts'].apply(lambda x: x.year).values
    weekday = df['ts'].apply(lambda x: x.weekday()).values

    # insert time data records
    time_data = [timestamp, hour, day, weekofyear, month, year, weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']] #.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    instance of the cursor, connection to database,
    filepath for song or log data
    function to process ong or log data

    inserts song data into the song and artist tables in the sparkifydb tables
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(f"host=127.0.0.1 dbname=sparkifydb user={config.user}")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
