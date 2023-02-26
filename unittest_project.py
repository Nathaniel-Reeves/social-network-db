"""Unit test module for main.py and models.py"""

import unittest
from freezegun import freeze_time
import main
import init_db
import models


# class TestMain(unittest.TestCase):

#     def setUp(self):
#         init_db.main()

#     def test_add_user(self):
#         self.assertEqual(main.add_user(1, 2), 3)
    
#     def test_remove_user(self):
#         self.assertEqual(main.remove_user(1), 2)
    
#     def test_list_users(self):
#         self.assertEqual(main.list_users(), 3)

class TestModel(unittest.TestCase):

    def setUp(self):
        init_db.main()

    def test_valid_user(self):
        self.assertEqual(models.valid_user("johnsmith", "p@ssw0rd"), True)
        self.assertEqual(models.valid_user("",""), False)
        self.assertEqual(models.valid_user("bobjohnson", ""), False)
        self.assertEqual(models.valid_user("", "abc123"), False)
        self.assertEqual(models.valid_user("bobjohnson", "wrong_password"), False)
    
    def test_user_exists(self):
        self.assertEqual(models.user_exists("johnsmith"), True)
        self.assertEqual(models.user_exists("bobjohnson"), True)
        self.assertEqual(models.user_exists(""), False)
        self.assertEqual(models.user_exists("fake_user"), False)

    def test_create_user(self):
        self.assertEqual(models.create_user("new_user", "new_username", "new_password"), 11)

    def test_delete_user(self):
        self.assertEqual(models.delete_user("johnsmith", "p@ssw0rd"), True)
        self.assertEqual(models.delete_user("bobjohnson", ""), False)

    def test_get_users(self):
        expected_result = [
            (10, "amandarodriguez", "Amanda Rodriguez"),
            (3, "bobjohnson", "Bob Johnson"),
            (9, "chriswilson", "Chris Wilson"),
            (5, "davidlee", "David Lee"),
            (4, "emilydavis", "Emily Davis"),
            (2, "janedoe", "Jane Doe"),
            (1, "johnsmith", "John Smith"),
            (8, "laurataylor", "Laura Taylor"),
            (7, "michaelbrown", "Michael Brown"),
            (6, "samanthajones", "Samantha Jones")
        ]
        self.assertEqual(models.get_users(), expected_result)

    def test_get_user_id(self):
        self.assertEqual(models.get_user_id("johnsmith"), 1)
        self.assertEqual(models.get_user_id("janedoe"), 2)
        self.assertEqual(models.get_user_id("bobjohnson"), 3)
        self.assertEqual(models.get_user_id("emilydavis"), 4)
        self.assertEqual(models.get_user_id("davidlee"), 5)
        self.assertEqual(models.get_user_id("samanthajones"), 6)
        self.assertEqual(models.get_user_id("michaelbrown"), 7)
        self.assertEqual(models.get_user_id("laurataylor"), 8)
        self.assertEqual(models.get_user_id("chriswilson"), 9)
        self.assertEqual(models.get_user_id("fake_user"), None)

    def test_get_username_by_id(self):
        self.assertEqual(models.get_username_by_id(1), "johnsmith")
        self.assertEqual(models.get_username_by_id(2), "janedoe")
        self.assertEqual(models.get_username_by_id(3), "bobjohnson")
        self.assertEqual(models.get_username_by_id(4), "emilydavis")
        self.assertEqual(models.get_username_by_id(5), "davidlee")
        self.assertEqual(models.get_username_by_id(6), "samanthajones")
        self.assertEqual(models.get_username_by_id(7), "michaelbrown")
        self.assertEqual(models.get_username_by_id(8), "laurataylor")
        self.assertEqual(models.get_username_by_id(20), None)

    def test_get_comments_by_post_id(self):
        expected_result = [
            (4, 2, 9, "Wow, the deep sea looks absolutely mesmerizing. I'm so jealous you got to see it in person!", "2022-08-04 10:09:37"),
            (5, 2, 2, "Swimming with sharks? That sounds so cool and terrifying at the same time!",
             "2022-08-05 14:26:18"),
            (6, 2, 4, "I've always been fascinated by the ocean. Your post made me want to book a diving trip ASAP.", "2022-08-06 11:05:42")
        ]
        self.assertEqual(models.get_comments_by_post_id(2), expected_result)
        self.assertEqual(models.get_comments_by_post_id(20), [])

    def test_add_comment(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        self.assertEqual(models.add_comment(2, 2, "this is content"),
                         (25, 2, 2, "this is content", "2012-01-14 12:00:01"))

        self.assertEqual(models.add_comment(50, 2, "invalid post"), None)
        self.assertEqual(models.add_comment(2, 50, "invalid author"), None)
        freezer.stop()

    def test_remove_comment(self):
        self.assertEqual(models.remove_comment(5), True)
        self.assertEqual(models.remove_comment(500), False)

    @unittest.skip("not implemented")
    def test_get_feed_with_comments(self):
        #TODO: implement this test.
        self.assertEqual(models.get_feed_with_comments(2), 25)
        self.assertEqual(models.get_feed_with_comments(20), None)

    def test_create_post(self):
        freezer = freeze_time("2012-01-14 12:00:01")
        freezer.start()
        self.assertEqual(models.create_post(
            2, "this is title", "this is content"), 9)
        freezer.stop()
    
    def test_delete_post(self):
        self.assertEqual(models.delete_post(9), True)
        self.assertEqual(models.delete_post(20), True)

    @unittest.skip("not implemented")
    def test_fetch_post_feed(self):
        #TODO: implement this test.
        self.assertEqual(models.fetch_post_feed(2), 25)
        self.assertEqual(models.fetch_post_feed(20), None)


if __name__ == '__main__':

    unittest.main()