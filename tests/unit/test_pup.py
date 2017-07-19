import unittest

from sheepdog.pup import FsPup, GalaxyPup, GitPup, Pup, PupfileEntry

class PupTestCase(unittest.TestCase):
    def test_parse_text_into_entries(self):
        """Test we parse the pupfile into the appropriate data structures from
        which to create the `Pup` instances.
        """
        pupfile_contents = """
---
- { name: "sheepdog.pup-base", location: "fs+../../pups/pup-base" }
- { name: "sheepdog.pup-base", location: "git+https://github.com/mattjmcnaughton/pup-base.git" }
- { name: "sheepdog.pup-base", location: "galaxy+sheepdog.pup-base" }
        """

        expected_entries = [
            PupfileEntry(name='sheepdog.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='sheepdog.pup-base',
                         pup_type='galaxy')
        ]

        self.assertEqual(Pup.parse_text_into_entries(pupfile_contents),
                         expected_entries)

    def test_create_from_entries(self):
        """Test we transform the `PupfileEntry` instances into popular instances
        of `Pup` subclasses.
        """
        pupfile_entries = [
            PupfileEntry(name='sheepdog.pup-base', path='../../pups/pup-base',
                         pup_type='fs'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='https://github.com/mattjmcnaughton/pup-base.git',
                         pup_type='git'),
            PupfileEntry(name='sheepdog.pup-base',
                         path='sheepdog.pup-base',
                         pup_type='galaxy')
        ]

        expected_pups = [
            FsPup('../../pups/pup-base'),
            GitPup('https://github.com/mattjmcnaughton/pup-base.git'),
            GalaxyPup('sheepdog.pup-base')
        ]

        actual_pup_dicts = [pup.to_dict() for pup in Pup.create_from_entries(pupfile_entries)]
        expected_pup_dicts = [pup.to_dict() for pup in expected_pups]

        self.assertEqual(actual_pup_dicts, expected_pup_dicts)
