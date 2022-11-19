# This module contains the functions that generate the filters for a given orbit.
# This filter is then passed to the DISCOSWeb API.



from enum import Enum
from functools import reduce
from typing import Optional

from .filters import ObjectClassFilter, ObjectClassType, OrbitFilter



class APIFilter:
    """Abstracts a list of filters to pass to the DISCOSWeb API"""

    def __init__(self):
        self.objclass = ObjectClassFilter()
        self.orbitfilter = set()

    def addOrbitFilter(self, filter: OrbitFilter):
        """Adds an orbit filter"""
        self.orbitfilter.add(filter)

    def addObjectClass(self, classtype: ObjectClassType):
        """Adds an ObjectClass to the filter"""
        self.objclass.add(classtype)

    def removeObjectClass(self, classtype: ObjectClassType):
        """Removes an ObjectClass from the filter"""
        self.objclass.remove(classtype)

    def clearObjectClass(self):
        """Clears the object class filter"""
        self.objclass.clear()

    def display(self):
        """Displays all the filters in a human readable way"""

        # If there are object classes, 


    def apistring(self) -> str:
        """Generates the API filter string to use in the DISCOSWeb API"""

        # Create an empty string.
        string = ""

        # If there are object classes, add them.
        objclass = self.objclass.apistring()

        if objclass is not None:
            string += objclass

        if len(self.orbitfilter) > 0:
            string += '&'.join( map( self.orbitfilter, lambda X: f"{X}" ) )

        return string