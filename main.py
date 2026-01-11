from auth import login
from posts.crud import add_post, show_all_posts, show_my_posts, delete_post
from posts.likes import like_post, unlike_post, show_liked_posts
from utils import menus
from core.db_settings import execute_query
from core import models


def main_loop():
    """Auth menu loop"""
    while True:
        print(menus.auth_menu)
        option = input("Enter your option: ")

        if option == "1":
            if login.login():
                print("Welcome to main menu")
                main_menu_loop()
            else:
                print("Username or password is incorrect")

        elif option == "2":
            if login.register():
                print("Please login now")

        elif option == "3":
            if login.validate():
                print("Welcome to main menu")
                main_menu_loop()

        elif option == "4":
            print("Good bye")
            break

        else:
            print("Invalid option")


def main_menu_loop():
    """Main menu loop"""
    while True:
        print(menus.main_menu)
        option = input("Enter your option: ")

        if option == "1":
            show_all_posts()
        elif option == "2":
            page = 1
            posts = show_my_posts(page)
            print("\n--- MY TWEETS ---")
            for p in posts:
                print(f"[{p['id']}] {p['like_count']} likes")
                print(p['post'])
                print("-" * 30)
            post_id = input("Delete post id (Enter to skip): ")
            if post_id:
                delete_post(int(post_id))
        elif option == "3":
            posts = show_liked_posts()
            print("\n--- LIKED TWEETS ---")
            for p in posts:
                print(f"[{p['id']}] @{p['username']}")
                print(p['post'])
                print("-" * 30)
        elif option == "4":
            content = input("Post text: ")
            add_post(content)
        else:
            print("Invalid option")


def show_posts_menu():
    """All tweets submenu with pagination and like/unlike"""
    current_page = 1
    order_by_likes = False

    while True:
        posts = show_all_posts(page=current_page, order_by_likes=order_by_likes)
        if not posts:
            print("No tweets on this page")
        for p in posts:
            print(f"{p['id']}: @{p['username']} - {p['post']} ({p['like_count']} likes)")

        print(menus.show_posts_menu)
        option = input("Enter your option: ")

        if option == "0":  # Back
            break
        elif option == "1":  # Next
            current_page += 1
        elif option == "2":  # Prev
            if current_page > 1:
                current_page -= 1
            else:
                print("This is the first page")
        elif option == "3":
            post_id = int(input("Post id to like: "))
            like_post(post_id)
        elif option == "4":
            post_id = int(input("Post id to unlike: "))
            unlike_post(post_id)
        elif option == "5":
            order_by_likes = True
            current_page = 1
        else:
            print("Invalid option")


if __name__ == "__main__":

    # create tables if needed
      execute_query(query=models.users)
      execute_query(query=models.posts)
      execute_query(query=models.likes)
      execute_query(query=models.codes)
      main_loop()

