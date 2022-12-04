from astropy import units as u

from poliastro.bodies import Earth, Mars, Sun
from poliastro.twobody import Orbit
from poliastro.plotting.static import StaticOrbitPlotter
from poliastro.plotting.interactive import OrbitPlotter3D, OrbitPlotter2D

def Orbit_Param(): #Para el programa final, la función tiene como input un diccionario
    long = 5
    #long = len(diccionario)
    interac = OrbitPlotter3D() #Sólo se define aquí y vale para todas las órbitas
    for i in range (long):
        #Definición de parámetros orbitales de cada órbita
        a = 7500+100*i << u.km
        ecc = 0.093315 << u.one
        inc = 1.85+5*i << u.deg
        raan = 49.562-2*i << u.deg
        argp = 286.537+45*i << u.deg
        nu = 23.33+30*i << u.deg
        #Definición de la órbita y su plot
        orb = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu)
        interac.plot(orb)
    #Plot de todas las órbitas
    D = interac.plot(orb)
    D.show()

if __name__ == "__main__":
    Orbit_Param()