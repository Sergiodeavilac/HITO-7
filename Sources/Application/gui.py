# Contains the application GUI.



from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput



class ApplicationGUI(BoxLayout):
    def __init__(self, checkCollisions, **kwargs):
        # Box Layout configuration.
        super(ApplicationGUI, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Add the orbit parameters GUI.
        self.orbitParameters = OrbitParameters()
        self.add_widget(self.orbitParameters)

        # Add the Check button.
        self.checkbtn = Button(text="Check collisions")
        self.checkbtn.bind(on_press=checkCollisions)
        self.add_widget(self.checkbtn)



class OrbitParameters(GridLayout):
    def __init__(self, **kwargs):
        # Grid Layout configuration.
        super(OrbitParameters, self).__init__(**kwargs)
        self.cols = 2

        # Add the SMA parameter.
        self.smainput = TextInput(multiline=False)
        self.add_widget(Label(text="Semi-major axis"))
        self.add_widget(self.smainput)

        # Add the ECC parameter.
        self.eccinput = TextInput(multiline=False)
        self.add_widget(Label(text="Eccentricity"))
        self.add_widget(self.eccinput)

        # Add the INC parameter.
        self.incinput = TextInput(multiline=False)
        self.add_widget(Label(text="Inclination"))
        self.add_widget(self.incinput)

        # Add the RAAN parameter.
        self.raaninput = TextInput(multiline=False)
        self.add_widget(Label(text="RAAN"))
        self.add_widget(self.raaninput)

        # Add the AOP parameter.
        self.aopinput = TextInput(multiline=False)
        self.add_widget(Label(text="Argument of Periapsis"))
        self.add_widget(self.aopinput)

        # Add the TA parameter.
        self.tainput = TextInput(multiline=False)
        self.add_widget(Label(text="True Anomaly"))
        self.add_widget(self.tainput)

        # Add the minimum distance for check.
        self.mindistance = TextInput(multiline=False)
        self.add_widget(Label(text="Collision Warning Distance"))
        self.add_widget(self.mindistance)
