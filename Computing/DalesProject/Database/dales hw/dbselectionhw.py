import sqlite3

with sqlite3.connect('sm_app.sqlite') as conn:
    cursor = conn.cursor()

    question1 = """    
    SELECT comment
    FROM comments
    WHERE comment LIKE '%?'
    """

    print(cursor.execute(question1).fetchall())

    quesiton2="""
    UPDATE users
    SET name = 'Lizzy'
    WHERE name = 'Elizabeth'
    """

    cursor.execute(quesiton2)

    question3="""
    SELECT users.name, count(posts.id)
    FROM users inner join posts on users.id = posts.user_id
    GROUP BY posts.id;
    """
    print(cursor.execute(question3).fetchall())

    conn.commit()