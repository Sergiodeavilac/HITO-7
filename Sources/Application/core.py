# Contains the application core logic.



from Application.gui import ApplicationGUI

from GMAT.Forces_models import Forces
from GMAT.load_gmat import gmat
from GMAT.Propagator import Prop

from kivy.app import App

from numpy import float64, sqrt, zeros

from pytwobodyorbit import TwoBodyOrbit

from typing import Tuple



class ApplicationCore(App):
    def __init__(self, **kwargs):
        # Application configuration.
        super(ApplicationCore, self).__init__(**kwargs)

        # Warning distance.
        self.warnDistance = 3000 # meters

        # Build the debris forces model.
        self.debrisFM = Forces(8, 8, "DebrisModel")
        self.payloadFM = Forces(1, 0, "PayloadModel")

        # Build the lists of other objects.
        self.payloads = []
        self.debris = []

        # Get an empty satellite orbit.
        self.satelliteOrbit = None

        # Build the default satellite.
        self.satellite = gmat.Construct("Spacecraft","Leosat")
        self.satellite.SetField("DateFormat", "UTCGregorian")
        self.satellite.SetField("Epoch", "12 Mar 2020 15:00:00.000")
        self.satellite.SetField("CoordinateSystem", "EarthMJ2000Eq")
        self.satellite.SetField("DisplayStateType", "Keplerian")
        self.satellite.SetField("SMA", 7005)
        self.satellite.SetField("ECC", 0.008)
        self.satellite.SetField("INC", 28.5)
        self.satellite.SetField("RAAN", 75)
        self.satellite.SetField("AOP", 90)
        self.satellite.SetField("TA", 45)

        self.satellite.SetField("DryMass", 50)
        self.satellite.SetField("Cd", 2.2)
        self.satellite.SetField("Cr", 1.8)
        self.satellite.SetField("DragArea", 1.5)
        self.satellite.SetField("SRPArea", 1.2)

    def build(self):
        return ApplicationGUI(self.checkCollisions)

    def checkCollisions(self, obj):
        print("Checking all collisions - ApplicationCore")

    def propagateAll(self):
        """Propagates all elements in the orbits"""

        # Propagate the target satellite.
        if self.satelliteOrbit is None:
            self.satelliteOrbit = self.propagatePayload(self.satellite)

        # Propagate all the conflict payloads.
        payloads = [self.propagatePayload(p) for p in self.payloads]

        # Propagate all the conflict debris.
        debris = [self.propagateDebris(d) for d in self.debris]

        # Process all the objects.
        self.process(payloads, debris)

    def process(self, payloads, debris):
        """Process all the recorded data and checks for warnings"""

        # List of all conflicting orbits.
        conflicts = []

        for p in payloads:
            if self.findConflicts(p):
                conflicts.append(p)

        for d in debris:
            if self.findConflicts(d):
                conflicts.append(d)

        # TODO : Pass this information to the polyastro.

    def findConflicts(self, orbit) -> bool:
        """Finds conflicting points in the orbit of the satellite"""

        def distance(X: Tuple[float, float, float], Y: Tuple[float, float, float]) -> float:
            (X0, Y0, Z0) = X
            (X1, Y1, Z1) = Y

            return sqrt( ((X0 - X1) ** 2.0) + ((Y0 - Y1) ** 2.0) + ((Z0 - Z1) ** 2.0) )
        
        return any( lambda X: X <= self.warnDistance, map( distance, zip( self.satelliteOrbit[0], orbit[0] ) ) )

    def propagatePayload(self, obj):
        """
        Propagates a payload for a week and returns its cartesian and
        keplerian coordinates
        """

        return self.propagateObject(obj, self.payloadFM)

    def propagateDebris(self, obj):
        """
        Propagates a debris object for a week and returns its cartesian and
        keplerian coordinates
        """

        return self.propagateObject(obj, self.debrisFM)

    def propagateObject(self, obj, fm):
        """
        Propagates a single object for a week and returns its cartesian and
        keplerian coordinates
        """

        # Time of propagation.
        T = 7 # days

        # mu of Earth.
        muEarth = float64(3.96e5)

        # Array to store the keplerian elements.
        kepl = zeros( (T * 24 * 60, 11) )

        # Orbit transformation.
        orbit = TwoBodyOrbit("Sat", mu=muEarth)

        # Perform the propagation.
        (r, v, t) = Prop(fm, obj, T)

        for j in range(T * 24 * 60):
            orbit.setOrbCart(t[j], r[j], v[j])
            kepl[j] = list( orbit.elmKepl().values() )

        return (r, kepl)
