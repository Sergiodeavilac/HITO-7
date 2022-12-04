# Contains the application core logic.



from Application.gui import ApplicationGUI
from Application.token import token

from DISCOSWeb.connection import APIConnection
from DISCOSWeb.filtering import APIFilter

from GMAT.Forces_models import Forces
from GMAT.load_gmat import gmat
from GMAT.Propagator import Prop

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar

from numba import njit, prange

import numpy as np
from numpy import float64, sqrt, array, zeros, subtract, power, sum

from pytwobodyorbit import TwoBodyOrbit

from typing import Tuple



class ApplicationCore(App):
    def __init__(self, **kwargs):
        # Application configuration.
        super(ApplicationCore, self).__init__(**kwargs)

        # DISCOSWeb connection.
        self.connection = APIConnection(token)

        # Warning distance.
        self.warnDistance = 3000 # meters

        # Get an empty satellite orbit.
        self.satelliteOrbit = None

        # Build the debris forces model.
        self.debrisFM = Forces(8, 8, "DebrisModel")
        self.payloadFM = Forces(1, 0, "PayloadModel")

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

        # Get the objects to match against.
        response, pointed = self.connection.orbits("2016-01-01 12:00")
        orbits = response['data']
        self.objects = {}
        self.objectOrbits = {}

        for (i, object) in enumerate( orbits ):
            # Get attributes.
            attributes = object['attributes']

            ecc  = attributes['ecc']
            sma  = attributes['sma']
            raan = attributes['raan']
            aPer = attributes['aPer']
            mAno = attributes['mAno']
            inc  = attributes['inc']

            # Build the object.
            sat = gmat.Construct("Spacecraft", f"Satellite{i}")
            sat.SetField("DateFormat", "UTCGregorian")
            # TODO : Change the Epoch
            sat.SetField("Epoch", "12 Mar 2020 15:00:00.000")
            sat.SetField("CoordinateSystem", "EarthMJ2000Eq")
            sat.SetField("DisplayStateType", "Keplerian")
            sat.SetField("SMA", sma if sma is not None else 0)
            sat.SetField("ECC", ecc if ecc is not None else 0)
            sat.SetField("INC", inc if inc is not None else 0)
            sat.SetField("RAAN", raan if raan is not None else 0)
            sat.SetField("AOP", aPer if aPer is not None else 0)
            # TODO : Change this into true anomaly.
            sat.SetField("TA", mAno if mAno is not None else 0)

            self.objects[object['id']] = sat

    def build(self):
        self.gui = ApplicationGUI(self.checkCollisions, len(self.objects))
        return self.gui

    def checkCollisions(self, obj):
        print("Checking all collisions - ApplicationCore")

        # Get the values of the GUI.
        guisma = self.gui.orbitParameters.smainput.text
        self.satellite.SetField("SMA", float( guisma ) if guisma is not None else 14000)

        guiecc = self.gui.orbitParameters.eccinput.text
        self.satellite.SetField("ECC", float( guiecc ) if guiecc is not None else 0)

        guiinc = self.gui.orbitParameters.incinput.text
        self.satellite.SetField("INC", float( guiinc ) if guiinc is not None else 0)

        guiraan = self.gui.orbitParameters.raaninput.text
        self.satellite.SetField("RAAN", float( guiraan ) if guiraan is not None else 0)

        guiaop = self.gui.orbitParameters.aopinput.text
        self.satellite.SetField("AOP", float( guiaop ) if guiaop is not None else 0)

        guita = self.gui.orbitParameters.tainput.text
        self.satellite.SetField("TA", float( guita ) if guita is not None else 0)

        if self.gui.orbitParameters.mindistance.text is not None:
            self.warnDistance = int( self.gui.orbitParameters.mindistance.text )

        # Propagate all the objects.
        self.propagateAll()

        # Filter the conflicting orbits.
        par = array( list( map( lambda X: array( X[1][0] ), self.objectOrbits.items() ) ) )
        sat = array( list( map( lambda X: array(X)        , self.satelliteOrbit[0]    ) ) )
        conflicts = findConflicts(sat, par, self.warnDistance)

        print("Done saerching for conflicts")

        # TODO : Send the conflic orbits to Polyastro.

    def propagateAll(self):
        """Propagates all elements in the orbits"""

        # Open the progress popup
        pb = ProgressBar( max=len(self.objects) )
        pb.value = 1

        popup = Popup(
            title='Propagation progress',
            content=pb,
            size=(200,200),
            auto_dismiss=False
        )

        popup.open(animation=False)

        # Propagate the target satellite.
        self.satelliteOrbit = self.propagatePayload(self.satellite)
        print("Propagated the satellite orbit")

        # Propagate all the conflict payloads.
        for (i, (id, p)) in enumerate( self.objects.items() ):
            self.objectOrbits[id] = self.propagatePayload(p)
            print(f'Propagated object {id} | {i} total objects')
            pb.value += 1

        popup.dismiss()

    def processConflicts(self):
        """Process all the recorded data and checks for warnings"""

        # List of all conflicting orbits.
        conflicts = {}

        if len(self.objectOrbits.items()) == 0:
            print("No objects were propagated")

        for (id, orbit) in self.objectOrbits.items():
            # Check if the orbit is valid and if it conflicts with the satellite.
            if orbit is None:
                print(f"[WARN]: Propagated orbit not found for object {id}")

            elif self.findConflicts(orbit):
                print(f"Found conflict with object {id}")
                conflicts[id] = orbit

        return conflicts

    def findConflicts(self, orbit) -> bool:
        """Finds conflicting points in the orbit of the satellite"""

        def distance(X: Tuple[float, float, float], Y: Tuple[float, float, float]) -> float:
            (X0, Y0, Z0) = X
            (X1, Y1, Z1) = Y

            return sqrt( ((X0 - X1) ** 2.0) + ((Y0 - Y1) ** 2.0) + ((Z0 - Z1) ** 2.0) )

        for otherPoint in orbit[0]:
            for thisPoint in self.satelliteOrbit[0]:
                if distance(otherPoint, thisPoint) < self.warnDistance:
                    return True

        return False

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
        T = 1 # days

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
            kepl[j] = array( list( orbit.elmKepl().values() ) )

        return (r, kepl)



@njit(parallel=True)
def findConflicts(sat, objects, warnDistance):
    bools = array( [False for _ in range(len(objects))] )

    for o in prange(len(objects)):

        object = objects[o]

        for i in range(len(object[0])):
            if bools[o]:
                break

            for j in range(len(sat)):
                if bools[o]:
                    break

                distance = np.sqrt( np.sum( np.power( np.subtract(object[i], sat[j]), 2.0 ) ) )

                if distance < warnDistance:
                    bools[o] = True
                    print(f"Object {o} conflicts with the satellite\n")

    return bools