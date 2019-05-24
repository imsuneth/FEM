class DOF:
    def __init__(self, values):
        self.value = values[0]
        self.controlled = values[1]
        if self.controlled:
            self.control_ratio = values[2]
        else:
            self.control_ratio = 0

    def __str__(self):
        return "Value:"+str(self.value)+", Controlled:"+str(self.controlled) + ", Controll ratio:"+str(self.control_ratio)
