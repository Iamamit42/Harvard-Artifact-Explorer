import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


# Connect to MySQL

def get_connection():

    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    return conn


# Create Tables

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata (
        id INT PRIMARY KEY,
        title TEXT,
        culture TEXT,
        period TEXT,
        century TEXT,
        medium TEXT,
        dimensions TEXT,
        description TEXT,
        department TEXT,
        classification TEXT,
        accessionyear INT,
        accessionmethod TEXT
    )
    """)

    # Media Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media (
        objectid INT,
        imagecount INT,
        mediacount INT,
        colorcount INT,
        `rank` INT,
        datebegin INT,
        dateend INT,
        FOREIGN KEY (objectid)
        REFERENCES artifact_metadata(id)
    )
    """)

    # Colors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors (
        objectid INT,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent FLOAT,
        css3 TEXT,
        FOREIGN KEY (objectid)
        REFERENCES artifact_metadata(id)
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Tables Created Successfully")

# Insertion of Data into SQL

def insert_metadata(records):

    conn = get_connection()
    cursor = conn.cursor()

    for record in records:

        cursor.execute("""
        INSERT IGNORE INTO artifact_metadata
        (
            id,
            title,
            culture,
            period,
            century,
            medium,
            dimensions,
            description,
            department,
            classification,
            accessionyear,
            accessionmethod
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,

        (

            record.get("objectid"),
            record.get("title"),
            record.get("culture"),
            record.get("period"),
            record.get("century"),
            record.get("medium"),
            record.get("dimensions"),
            record.get("description"),
            record.get("department"),
            record.get("classification"),
            record.get("accessionyear"),
            record.get("accessionmethod")

        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Metadata Inserted")

def insert_media(records):

    conn = get_connection()
    cursor = conn.cursor()

    for record in records:

        cursor.execute("""

        INSERT IGNORE INTO artifact_media

        (
        objectid,
        imagecount,
        mediacount,
        colorcount,
        `rank`,
        datebegin,
        dateend
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s)

        """,

        (

            record.get("objectid"),
            record.get("imagecount"),
            record.get("mediacount"),
            record.get("colorcount"),
            record.get("rank"),
            record.get("datebegin"),
            record.get("dateend")

        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Media Inserted")

def insert_colors(records):

    conn = get_connection()
    cursor = conn.cursor()

    for record in records:

        colors = record.get("colors", [])

        for color in colors:

            cursor.execute("""

            INSERT IGNORE INTO artifact_colors

            (
            objectid,
            color,
            spectrum,
            hue,
            percent,
            css3
            )

            VALUES
            (%s,%s,%s,%s,%s,%s)

            """,

            (

                record.get("objectid"),
                color.get("color"),
                color.get("spectrum"),
                color.get("hue"),
                color.get("percent"),
                color.get("css3")

            ))

    conn.commit()

    cursor.close()
    conn.close()

    print("Colors Inserted")

def insert_all(records):

    create_tables()

    insert_metadata(records)

    insert_media(records)

    insert_colors(records)

    print("All Data Inserted Successfully")

import pandas as pd

# Run SQL Query

def run_query(query):

    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df