class DOF:
    def __init__(self, values):
        self.value = values[0]
        self.controlled = values[1]
        self.control_ratio = None
        if self.controlled:
            self.control_ratio = values[2]

    def __str__(self):
        return "Value:"+str(self.value)+", Controlled:"+self.controlled + ", Controll ratio:"+self.control_ratio
