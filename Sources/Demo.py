# PyGMAT demo file.


from DISCOSWeb.connection import APIConnection
from DISCOSWeb.filters import ObjectClassType,\
    OrbitAttribute, OrbitFilter, FilterOperation
from DISCOSWeb.filtering import APIFilter



if __name__ == "__main__":
    # Build the filter.
    filter = APIFilter()

    # Add object classes.
    filter.addObjectClass( ObjectClassType.Payload )
    filter.addObjectClass( ObjectClassType.Debris  )

    # Build the Orbit requirements.
    sma  = OrbitFilter( OrbitAttribute.SemimajorAxis, FilterOperation.GreaterEqual, 9000 )
    incs = OrbitFilter( OrbitAttribute.Inclination,   FilterOperation.GreaterEqual, 45.0 )
    incm = OrbitFilter( OrbitAttribute.Inclination,   FilterOperation.LessEqual,    65.0 )

    # Add orbit requirements.
    filter.addOrbitFilter(sma)
    filter.addOrbitFilter(incs)
    filter.addOrbitFilter(incm)

    # Create the API connection
    conn = APIConnection("")

    print( f"Generated API string:\n{conn.url( filter )}" )

