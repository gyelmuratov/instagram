import unittest
from unittest.mock import patch
from posts.crud import add_post


class TestAddPost(unittest.TestCase):
    """
    Tests for add_post function
    """

    @patch("posts.crud.execute_query")
    @patch("posts.crud.get_active_user")
    def test_add_post_success(self, mock_get_active_user, mock_execute_query):
        mock_get_active_user.return_value = {'id': 1, 'username': 'testuser'}
        mock_execute_query.return_value = True

        result = add_post('Hello World')

        self.assertTrue(result)
        mock_execute_query.assert_called_once()

    @patch("posts.crud.get_active_user")
    def test_add_post_no_active_user(self, mock_get_active_user):
        mock_get_active_user.return_value = None

        result = add_post("Hello world")

        self.assertFalse(result)

    @patch("posts.crud.execute_query")
    @patch("posts.crud.get_active_user")
    def test_add_post_db_error(self, mock_get_active_user, mock_execute_query):
        mock_get_active_user.return_value = {"id": 1}
        mock_execute_query.return_value = False

        result = add_post("Hello world")

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
