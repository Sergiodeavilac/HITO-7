from .load_gmat import *

# -----------------------------------------------------------
# Propagator
# -----------------------------------------------------------
def Prop(fm, sat, T):
    
    N = T * 24*60 #iteations
    
    # Build the propagation container that connect the integrator, force model, and spacecraft together
    pdprop = gmat.Construct("Propagator","PDProp")

    # Create and assign a numerical integrator for use in the propagation
    gator = gmat.Construct("PrinceDormand78", "Gator")
    pdprop.SetReference(gator)

    # Set some of the fields for the integration
    pdprop.SetField("InitialStepSize", 60.0)
    pdprop.SetField("Accuracy", 1.0e-12)
    pdprop.SetField("MinStep", 0.0)
    
    # Assign the force model and sat to the propagator
    pdprop.SetReference(fm) 
    pdprop.AddPropObject(sat)
    
    # Perform top level initialization
    gmat.Initialize()
    # Perform the integation subsysem initialization
    pdprop.PrepareInternals()

    # Refresh the integrator reference
    gator = pdprop.GetPropagator()
    
    # Initial list
    time = []
    pos = []
    vel = []
    gatorstate = gator.GetState()
    t = 0.0
    r = []
    v = []
    
    #Propagate
    for i in range(N):
    # Take a step and buffer it
        gator.Step(60.0)
        gatorstate = gator.GetState()
        t = t + 60.0
        r = []
        v = []
        for j in range(3):
            r.append(gatorstate[j])
            v.append(gatorstate[j+3])
        time.append(t)
        pos.append(r)
        vel.append(v)

    return (pos, vel, time)

    
    