from .load_gmat import *

# -----------------------------------------------------------
# Forces Model 
# -----------------------------------------------------------
def Forces(degree, order, name):
    # Build an empty force model.
    fm = gmat.Construct("ForceModel", name)

    # An 8x8 JGM-3 Gravity Model
    earthgrav = gmat.Construct("GravityField")
    earthgrav.SetField("BodyName","Earth")
    earthgrav.SetField("Degree",degree)
    earthgrav.SetField("Order",order)
    earthgrav.SetField("PotentialFile","JGM2.cof")
    
    # Add forces into the ODEModel container
    fm.AddForce(earthgrav)

    # The Point Masses
    moongrav = gmat.Construct("PointMassForce")
    moongrav.SetField("BodyName","Luna")
    sungrav = gmat.Construct("PointMassForce")
    sungrav.SetField("BodyName","Sun")

    # Drag using Jacchia-Roberts
    jrdrag = gmat.Construct("DragForce")
    jrdrag.SetField("AtmosphereModel","JacchiaRoberts")

    # Build and set the atmosphere for the model
    atmos = gmat.Construct("JacchiaRoberts")
    jrdrag.SetReference(atmos)

    # Add all of the forces into the ODEModel container
    fm.AddForce(moongrav)
    fm.AddForce(sungrav)
    fm.AddForce(jrdrag)
    
    return(fm)
