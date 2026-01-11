from core.db_settings import execute_query
from auth.login import get_active_user

PAGE_SIZE = 10 # Results are paginated with 10 items per page

def add_post(content: str) -> bool:
    """Add a new post"""
    user = get_active_user()
    if not user:
        print("No active user!")
        return False

    query = "INSERT INTO posts (user_id, post) VALUES (%s, %s)"
    params = (user['id'], content)

    if execute_query(query=query, params=params):
        print("Added post!")
        return True

    return False


def show_all_posts(page: int = 1, order_by_likes: bool = True ) -> list[dict] | None:
    """
    Return a paginated list of posts with username and like count.
    Can be ordered by likes or creation date.
    :param page: int or default 1
    :param order_by_likes: Parameter order_by_likes, boolean, default True; indicates whether to sort by likes
    :return:list of dicts with post info (id, username, post, like_count);
         empty list if no posts; None if a DB error occurs
    """
    offset = (page - 1)*PAGE_SIZE  # Variable, used for SQL OFFSET, indicates how many posts to skip
    if order_by_likes:
        order = "like_count DESC"  # order_by_likes = True -> like_count DESC
    else:
        order = "posts_created_at DESC"  # order_by_likes = False -> posts_created_at DESC

    query = f"""
    SELECT posts.id,
    users.username,
    posts.post,
    COUNT(likes.id) AS like_count
    FROM posts 
    JOIN users ON posts.user_id = users.id
    LEFT JOIN likes ON posts.id = likes.post_id
    GROUP BY posts.id, users.username, posts.post
    ORDER BY {order}
    LIMIT {PAGE_SIZE} OFFSET {offset}
"""
    return execute_query(query=query, fetch="all")


def show_my_posts(page: int = 1):
    """
    Get posts of active user
    """
    user = get_active_user()
    if not user:
        print("No active user")
        return []

    offset = (page - 1) * PAGE_SIZE

    query = f"""
    SELECT posts.id,
           posts.post,
           COUNT(likes.id) AS like_count
    FROM posts
    LEFT JOIN likes ON posts.id = likes.post_id
    WHERE posts.user_id = %s
    GROUP BY posts.id, posts.post
    ORDER BY posts.created_at DESC
    LIMIT {PAGE_SIZE} OFFSET {offset}
    """

    posts = execute_query(query=query, params=(user['id'],), fetch="all")
    return posts or []  # None bo'lsa ham bo'sh list qaytaradi

def delete_post(post_id: int):
    """
    Delete tweet by id (only owner can delete)
    """
    user = get_active_user()
    if not user:
        print("No active user")
        return False

    query = "DELETE FROM posts WHERE id=%s AND user_id=%s"
    params = (post_id, user['id'])

    if execute_query(query=query, params=params):
        print("Deleted post")
        return True

    print("Post not found or not yours")
    return False


