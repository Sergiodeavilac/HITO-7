from astropy import units as u

from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.plotting.interactive import OrbitPlotter3D, OrbitPlotter2D

import sys

def OrbitParam(sat, obj): #Para el programa final, la función tiene como input un diccionario
    # Orbit plotter.
    interac = OrbitPlotter3D()

    # Display the objects orbits.
    for o in obj:
        sma, ecc, inc, raan, aop, ta = extract(o)
        interac.plot( Orbit.from_classical(Earth, sma, ecc, inc, raan, aop, ta) )

    # Display the satellite.
    sma, ecc, inc, raan, aop, ta = extract(sat)
    D = interac.plot( Orbit.from_classical(Earth, sma, ecc, inc, raan, aop, ta) )

    # Display the orbit.
    D.show()

def extract(obj):
    return obj[4] << u.m, obj[2] << u.one, obj[3] << u.deg, obj[5] << u.deg, obj[1] << u.deg, obj[0] << u.deg

if __name__ == "__main__":
    #Orbit_Param()

    # Command line arguments.
    if len(sys.argv) < 2:
        print(f"Expected 2 command line argument, found {len(sys.argv)}")

    # Get the first arg.
    path = sys.argv[1]

    # Open the file.
    with open(path, "r") as file:
        # Read the file.
        orbitdata = file.readlines()

        # Get the satellite data.
        sat = list( map( float, orbitdata[0].split(' ') ) )

        # Get the object data.
        obj = []

        for j in range(1, len(orbitdata)):
            obj.append( list( map(float, orbitdata[j].split(' ')) ) )

        # Send the arguments to the display function.
        OrbitParam(sat, obj)
