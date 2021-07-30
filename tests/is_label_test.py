import unittest

from fcxref.rename.is_label import is_label


class IsLabelTest(unittest.TestCase):

    def test_is_label(self):
        self.assertTrue(is_label('<<Main>>'))
        self.assertTrue(is_label('<<Master of Puppets>>'))
        self.assertFalse(is_label(' <<Main>>'))
        self.assertFalse(is_label('<<Main>> '))
        self.assertFalse(is_label('<Main>'))
        self.assertFalse(is_label(' <<Main>> '))
        self.assertFalse(is_label('Main'))
        self.assertFalse(is_label('Master_of_Puppets'))


if __name__ == '__main__':
    unittest.main()
