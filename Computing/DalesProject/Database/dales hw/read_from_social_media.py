import sqlite3
from tabulate import tabulate

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return result


select_users = "SELECT * from users"
with sqlite3.connect("sm_app.sqlite") as conn:
    users = execute_read_query(conn, select_users)

for user in users:
    print(user)

select_user_posts = """
SELECT
    users.id,
    users.name,
    posts.description
FROM
    posts
    INNER JOIN users ON users.id = posts.user_id
"""

users_posts = execute_read_query(conn, select_user_posts)
print(tabulate(users_posts))
# for users_post in users_posts:
#     print(users_post)

select_posts_comments_users = """
SELECT
posts.description as post,
comments.comment as comment,
users.name as name
FROM
posts
INNER JOIN comments ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id
"""

posts_comments_users = execute_read_query(
    conn, select_posts_comments_users
)

print(posts_comments_users)

select_post_likes = """
SELECT
posts.description as post,
COUNT(likes.id) as likes
FROM
likes,
posts
WHERE
posts.id = likes.post_id
GROUP BY
likes.post_id
"""

post_likes = execute_read_query(conn, select_post_likes)

for post_like in post_likes:
    print(post_like)