# Test module for the API filters.


import unittest

from .ObjectClass import ObjectClassFilter, ObjectClassType


class TestObjectClass(unittest.TestCase):
    def empty(self):
        """Tests correctness for an empty Object Class filter"""
        self.assertEqual( ObjectClassFilter().apistring(), None )

    def single(self):
        """Tests correctness for a single item Object Class filter"""

        filter = ObjectClassFilter()
        filter.add( ObjectClassType.Payload )

        self.assertEqual( filter.apistring(), "eq(objectClass,Payload)" )

    def multiple(self):
        """Tests correctness for a multiple item Object Class filter"""

        filter = ObjectClassFilter()
        filter.add( ObjectClassType.Payload )
        filter.add( ObjectClassType.RocketDebris )

        self.assertEqual( filter.apistring(), "in(objectClass,('Payload','RocketDebris'))" )


if __name__ == "__main__":
    unittest.main()