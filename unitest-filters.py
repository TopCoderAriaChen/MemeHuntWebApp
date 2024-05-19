
import unittest
import hashlib

from filters import email_hash

class FiltersTest(unittest.TestCase):

    def test_email_hash(self):
        email = "yggl1889@163.com"
        expected_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()
        self.assertEqual(email_hash(email), expected_hash)

if __name__ == "__main__":
    unittest.main()
