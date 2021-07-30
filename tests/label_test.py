import unittest

from fcxref.rename.label import is_label, extract_label


class LabelTest(unittest.TestCase):

    def test_is_label(self):
        self.assertTrue(is_label('<<Main>>'))
        self.assertTrue(is_label('<<Master of Puppets>>'))
        self.assertFalse(is_label(' <<Main>>'))
        self.assertFalse(is_label('<<Main>> '))
        self.assertFalse(is_label('<Main>'))
        self.assertFalse(is_label(' <<Main>> '))
        self.assertFalse(is_label('Main'))
        self.assertFalse(is_label('Master_of_Puppets'))

    def test_extract_label(self):
        self.assertEqual(extract_label('<<Main>>'), 'Main')
        self.assertEqual(extract_label('<<Something with Spaces>>'), 'Something with Spaces')
        self.assertEqual(extract_label('Main'), 'Main')
        self.assertEqual(extract_label('<<<SurroundedByAngleBrackets>>>'), '<SurroundedByAngleBrackets>')

if __name__ == '__main__':
    unittest.main()
