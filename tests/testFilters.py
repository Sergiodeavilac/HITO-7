# Test module for the API filters.



import unittest
from Sources.DISCOSWeb.filters import ObjectClassFilter, ObjectClassType,\
    OrbitAttribute, OrbitFilter, FilterOperation



class TestObjectClass(unittest.TestCase):
    def test_EmptyClass(self):
        """Tests correctness for an empty Object Class filter"""
        self.assertEqual( ObjectClassFilter().apistring(), None)

    def test_SingleClass(self):
        """Tests correctness for a single item Object Class filter"""

        filter = ObjectClassFilter()
        filter.add( ObjectClassType.Payload )

        print( filter.apistring() )

        self.assertEqual( filter.apistring(), "eq(objectClass,Payload)" )

    def test_MultipleClasses(self):
        """Tests correctness for a multiple item Object Class filter"""

        filter = ObjectClassFilter()
        filter.add( ObjectClassType.Payload )
        filter.add( ObjectClassType.RocketDebris )

        self.assertEqual( filter.apistring(), "in(objectClass,('Payload','Rocket Debris'))" )



class TestOrbit(unittest.TestCase):
    def test_Operations(self):
        """Tests correctness of all orbit filter attributtes"""

        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.Equal,        7100).apistring(), "eq(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.GreaterThan,  7100).apistring(), "gt(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.GreaterEqual, 7100).apistring(), "ge(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.LessThan,     7100).apistring(), "lt(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.LessEqual,    7100).apistring(), "le(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.NotEqual,     7100).apistring(), "ne(destinationOrbits.sma,7100)")

    def test_ValueFormatting(self):
        """Test correctness of value formatting"""

        # Test SMA.
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.Equal, 7100.0).apistring(), "eq(destinationOrbits.sma,7100)")
        self.assertEqual( OrbitFilter(OrbitAttribute.SemimajorAxis, FilterOperation.Equal, 7100  ).apistring(), "eq(destinationOrbits.sma,7100)")

        # Test inclination.
        self.assertEqual( OrbitFilter(OrbitAttribute.Inclination, FilterOperation.Equal, 53.04).apistring(), "eq(destinationOrbits.inc,53.04)")
        self.assertEqual( OrbitFilter(OrbitAttribute.Inclination, FilterOperation.Equal, 53   ).apistring(), "eq(destinationOrbits.inc,53.00)")

        # Test periapsis argument.
        self.assertEqual( OrbitFilter(OrbitAttribute.PeriapsisArg, FilterOperation.Equal, 310).apistring(), "eq(destinationOrbits.aPer,310)")

        # Test epoch.
        self.assertEqual( OrbitFilter(OrbitAttribute.Epoch, FilterOperation.Equal, "2020-31-01").apistring(), "eq(destinationOrbits.epoch,2020-31-01)")

if __name__ == "__main__":
    unittest.main()
