import unittest

import src.aws_keypair_manager as key_m


class UnitTestAwsKeypairManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.name = 'skeletonkey'
        self.keys_manager = key_m.AwsKeypairManager()

    def test_create_keypair(self):
        """
        Create a keypair
        @return: none
        """
        key_pair = self.keys_manager.create(self.name)
        keyname = key_pair['KeyName']
        self.assertTrue((keyname == self.name))

    def test_create_keypair_already_exists(self):
        """
        try to create a keypair who already exist
        @return: none
        @raise: exception when the keypair already exists
        """

    def test_exists_keypair(self):
        self.keys_manager.create(self.name)
        response = self.keys_manager.exists(self.name)
        self.assertTrue(response)

    def asyncTearDown(self):
        if self.keys_manager.exists(self.name):
            self.keys_manager.delete(self.name)

if __name__ == '__main__':
    unittest.main()