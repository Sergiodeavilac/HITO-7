# This module contains the orbit filter attributes of the DISCOSWeb API.



from enum import Enum
from functools import reduce
from typing import Optional

from .Operations import FilterOperation



class OrbitAttribute(Enum):
    """Enumeration of all orbit attributes defined in the DISCOSWeb API"""

    Epoch         = 1
    SemimajorAxis = 2
    Inclination   = 3
    Eccentricity  = 4
    RAAN          = 5
    PeriapsisArg  = 6
    MeanAnomaly   = 7


    def __str__(self) -> str:
        if self == OrbitAttribute.Epoch:
            return "Epoch"
        elif self == OrbitAttribute.SemimajorAxis:
            return "Semimajor Axis"
        elif self == OrbitAttribute.Inclination:
            return "Inclination"
        elif self == OrbitAttribute.Eccentricity:
            return "Eccentricity"
        elif self == OrbitAttribute.RAAN:
            return "RAAN"
        elif self == OrbitAttribute.PeriapsisArg:
            return "Argument of Peripapsis"
        elif self == OrbitAttribute.MeanAnomaly:
            return "Mean Anomaly"

    def apistring(self) -> str:
        if self == OrbitAttribute.Epoch:
            return "epoch"
        elif self == OrbitAttribute.SemimajorAxis:
            return "sma"
        elif self == OrbitAttribute.Inclination:
            return "inc"
        elif self == OrbitAttribute.Eccentricity:
            return "ecc"
        elif self == OrbitAttribute.RAAN:
            return "raan"
        elif self == OrbitAttribute.PeriapsisArg:
            return "aPer"
        elif self == OrbitAttribute.MeanAnomaly:
            return "mAno"
        else:
            raise ValueError



class OrbitFilter:
    """Abstracts a single DISCOSWeb API orbit filter"""

    def __init__(self, attribute: OrbitAttribute, operation: FilterOperation, value: float):
        self.attribute = attribute
        self.operation = operation
        self.value     = value

    def display(self) -> str:
        """Displays the filter in a human readable way"""

        return f"{self.attribute} {self.operation} {self.value}"

    def apistring(self) -> str:
        """Returns the DISCOSWeb API compliant filter string"""

        if self.attribute in [OrbitAttribute.Inclination, OrbitAttribute.RAAN, OrbitAttribute.MeanAnomaly]:
            value = "{:2.2f}".format( float(self.value) )
        elif self.attribute in [OrbitAttribute.SemimajorAxis, OrbitAttribute.PeriapsisArg]:
            value = f"{int(self.value)}"
        #elif self.attribute in [OrbitAttribute.PeriapsisArg]:
        #    value = "{:3.0f}".format( float(self.value) )
        else:
            value = str( self.value )

        return f"{self.operation.apistring()}({self.attribute.apistring()},{value})"
