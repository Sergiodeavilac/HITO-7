# Common attribute filter operations.



from enum import Enum



class FilterOperation(Enum):
    """Enumeration of all filters supported by the DISCOSWeb API"""

    Equal        = 1
    GreaterThan  = 2
    GreaterEqual = 3
    LessThan     = 4
    LessEqual    = 5
    NotEqual     = 6

    def __str__(self) -> str:
        if self == FilterOperation.Equal:
            return "Equal"
        elif self == FilterOperation.GreaterThan:
            return "Greater Than"
        elif self == FilterOperation.GreaterEqual:
            return "Greater or Equal"
        elif self == FilterOperation.LessThan:
            return "Less Than"
        elif self == FilterOperation.LessEqual:
            return "Less or Equal"
        elif self == FilterOperation.NotEqual:
            return "Not Equal"

    def apistring(self) -> str:
        if self == FilterOperation.Equal:
            return "eq"
        elif self == FilterOperation.GreaterThan:
            return "gt"
        elif self == FilterOperation.GreaterEqual:
            return "ge"
        elif self == FilterOperation.LessThan:
            return "lt"
        elif self == FilterOperation.LessEqual:
            return "le"
        elif self == FilterOperation.NotEqual:
            return "ne"



