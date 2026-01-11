from core.db_settings import execute_query
from auth.login import get_active_user


def like_post(post_id: int):
    """
    Like a tweet (only once per user)
    """
    user = get_active_user()
    if not user:
        print("No active user")
        return False

    # oldin like bosilganmi tekshiramiz
    check_query = """
    SELECT id FROM likes
    WHERE user_id=%s AND post_id=%s
    """
    if execute_query(
        query=check_query,
        params=(user['id'], post_id),
        fetch="one"
    ):
        print("You already liked this post") # allaqchon like bosgansiz
        return False

    query = "INSERT INTO likes(user_id, post_id) VALUES (%s, %s)"
    params = (user['id'], post_id)

    if execute_query(query=query, params=params):
        print("Post liked")
        return True

    return False


def unlike_post(post_id: int):
    """
    Remove like from tweet
    """
    user = get_active_user()
    if not user:
        print("No active user")
        return False

    query = "DELETE FROM likes WHERE user_id=%s AND post_id=%s"
    params = (user['id'], post_id)

    if execute_query(query=query, params=params):
        print("Post unliked")
        return True

    print("Like not found")
    return False


def show_liked_posts(page: int = 1, page_size: int = 10):
    """
    Get tweets liked by active user
    """
    user = get_active_user()
    if not user:
        print("No active user")
        return []

    offset = (page - 1) * page_size

    query = f"""
    SELECT posts.id,
           users.username,
           posts.post
    FROM likes
    JOIN posts ON likes.post_id = posts.id
    JOIN users ON posts.user_id = users.id
    WHERE likes.user_id = %s
    ORDER BY likes.id DESC
    LIMIT {page_size} OFFSET {offset}
    """

    return execute_query(query=query, params=(user['id'],), fetch="all")

