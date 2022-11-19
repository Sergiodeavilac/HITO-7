# This module contains the 'objectClass' attribute filter of the DISCOSWeb API.



from enum import Enum
from functools import reduce
from typing import Optional



class ObjectClassType(Enum):
    """Enumeration of all Object Classes supported by the DISCOSWeb API"""

    Payload              = 1
    PayloadDebris        = 2
    PayloadFragmentation = 3

    RocketBody          = 4
    RocketDebris        = 5
    RocketFragmentation = 6

    Debris = 7

    def __str__(self) -> str:
        if self == ObjectClassType.Payload:
            return "Payload"
        elif self == ObjectClassType.PayloadDebris:
            return "Payload Debris"
        elif self == ObjectClassType.PayloadFragmentation:
            return "Payload Fragmentation Debris"
        elif self == ObjectClassType.RocketBody:
            return "Rocket Body"
        elif self == ObjectClassType.RocketDebris:
            return "Rocket Debris"
        elif self == ObjectClassType.RocketFragmentation:
            return "Rocket Fragmentation Debris"
        elif self == ObjectClassType.Debris:
            return "Other Debris"



class ObjectClassFilter:
    """A filter for the class of an object as defined by the DISCOSWeb API"""

    def __init__(self):
        self.filter = set()

    def __str__(self):
        """Displays the ObjectClassType filter in a human readable way"""

        # Add each element from 'self.filter' to the initial description string.
        return reduce( lambda string, element: string + f"| {element} ", self.filter, "ObjectClassType must be one of -> " )

    def apistring(self) -> Optional[str]:
        """Returns the equivalent API string to this ObjectClassType filter"""

        # Get the size of the set.
        size = len( self.filter )

        # If there are no filters, return nothing.
        if size == 0:
            return None

        # If there is 1 (one) filter return an equality check.
        elif size == 1:
            return f"eq(objectClass,{list(self.filter)[0]})"

        # If there are more than 1 (one) filters, perform a containing check.
        else:
            classes = list( map(lambda t: f"'{t}'", self.filter) )
            classes.sort()

            return  f"in(objectClass,({','.join( classes )}))"

    def add(self, t: ObjectClassType):
        """Adds the given ObjectClassType to the filter"""
        self.filter.add(t)

    def remove(self, t: ObjectClassType):
        """Removes the given ObjectClassType from the filter"""
        self.filter.remove(t)

    def clear(self):
        """Clears all the elements from this filter"""
        self.filter = set()
