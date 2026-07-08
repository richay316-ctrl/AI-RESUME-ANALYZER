import mysql.connector


# MySQL Connection

def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="KHUSHI_9827",
        database="resume_match"
    )

    return conn



# Table create

def create_table():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis
    (
        id INT AUTO_INCREMENT PRIMARY KEY,

        resume_name VARCHAR(255),

        job_description TEXT,

        match_score FLOAT,

        skills TEXT,

        missing_keywords TEXT
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    cursor.close()
    conn.close()



# Save Analysis Data

def save_analysis(
        resume_name,
        job_description,
        score,
        skills,
        missing_keywords
):

    conn = get_connection()

    cursor = conn.cursor()


    query = """
    INSERT INTO resume_analysis
    (
        resume_name,
        job_description,
        match_score,
        skills,
        missing_keywords
    )

    VALUES (%s,%s,%s,%s,%s)
    """


    values = (

        resume_name,

        job_description,

        score,

        ", ".join(skills),

        ", ".join(missing_keywords)

    )


    cursor.execute(
        query,
        values
    )


    conn.commit()

    cursor.close()
    conn.close()



# Fetch Data

def get_analysis():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM resume_analysis"
    )


    data = cursor.fetchall()


    cursor.close()
    conn.close()


    return data