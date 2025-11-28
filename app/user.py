class CTSSUser:
    def __init__(self, credentials, role):
        self.username = credentials[0] 
        self.__password = credentials[1]
        self.role = role