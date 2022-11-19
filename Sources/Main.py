from GMAT.Forces_models import Forces
from GMAT.load_gmat import *


# -----------------------------------------------------------
# Forces Model 
# -----------------------------------------------------------

fm = Forces()

fm.Help()



# -----------------------------------------------------------
# Our spacecraft 
# -----------------------------------------------------------

mysat = gmat.Construct("Spacecraft","Leosat")
mysat.SetField("DateFormat", "UTCGregorian")
mysat.SetField("Epoch", "12 Mar 2020 15:00:00.000")
mysat.SetField("CoordinateSystem", "EarthMJ2000Eq")
mysat.SetField("DisplayStateType", "Keplerian")
mysat.SetField("SMA", 7005)
mysat.SetField("ECC", 0.008)
mysat.SetField("INC", 28.5)
mysat.SetField("RAAN", 75)
mysat.SetField("AOP", 90)
mysat.SetField("TA", 45)

mysat.SetField("DryMass", 50)
mysat.SetField("Cd", 2.2)
mysat.SetField("Cr", 1.8)
mysat.SetField("DragArea", 1.5)
mysat.SetField("SRPArea", 1.2)


# -----------------------------------------------------------
# Import data DiscosWeb
# -----------------------------------------------------------




# Propagate



