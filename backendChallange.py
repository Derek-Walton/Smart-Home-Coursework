class Device:
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn
    


class SmartPlug(Device):
    def __init__(self, consumptionRate: int):
        super().__init__()
        self.consumptionRate = 150
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self):
        return self.consumptionRate
    
    def getDeviceType(self):
        return "Smart Plug"

    def setConsuptionRate(self, newConsumptionRate: int):
        self.consumptionRate = newConsumptionRate

    def __str__(self):
        output = "Smart Plug - "
        output += "On" if self.switchedOn else "Off"
        output += f", Consumption rate: {self.consumptionRate}"
        return output
    


class SmartOven(Device):
    def __init__(self):
        super().__init__()
        self.switchedOn = False
        self.temperature = 0
    
    def getTemperature(self):
        return self.temperature
    
    def getDeviceType(self):
        return "Smart Oven"
    
    def setTemperature(self, newTemperature: int):
        if newTemperature in range(0, 261):
            self.temperature = newTemperature

    def __str__(self):
        output = "Smart Oven - "
        output += "On" if self.switchedOn else "Off"
        output += f", Temperature: {self.temperature} Degrees Celcius"
        return output



class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices
    
    def getDeviceAt(self, index: int):
        return self.devices[index]
    
    def removeDeviceAt(self, index: int):
        self.devices.remove(self.devices[index])

    def removeAllDevices(self):
        self.devices = []
    
    def addDevice(self, device):
        self.devices.append(device)

    def toggleSwitchAt(self, index: int):
        self.devices[index].toggleSwitch()

    def turnOnAll(self):
        for device in self.devices:
            if not device.switchedOn:
                device.toggleSwitch()

    def turnOffAll(self):
        for device in self.devices:
            if device.switchedOn:
                device.toggleSwitch()

    def setConsumptionRateAtIndex(self, index, newConsumptionRate):
        self.devices[index].setConsuptionRate(newConsumptionRate)

    def setOvenTemperatureAtIndex(self, index, newTemperature):
        self.devices[index].setTemperature(newTemperature)

    def __str__(self):
        output = f"Smart Home has {len(self.devices)} devices:\n"
        for device in self.devices:
            output += f"{device}\n"
        return output
    
# Testing

def testSmartPlug():
    mySmartPlug = SmartPlug(45)
    mySmartPlug.toggleSwitch()
    print(mySmartPlug.getSwitchedOn())
    print(mySmartPlug.getConsumptionRate())
    mySmartPlug.setConsuptionRate(100)
    print(mySmartPlug.getConsumptionRate())
    print(mySmartPlug)
# testSmartPlug()
    
def testSmartOven():
    mySmartOven = SmartOven()
    mySmartOven.toggleSwitch()
    mySmartOven.getSwitchedOn()
    print(mySmartOven.getTemperature())
    mySmartOven.setTemperature(200)
    print(mySmartOven.getTemperature())
    print(mySmartOven)
# testSmartOven()

def testSmartHome():
    myHome = SmartHome()

    plug1 = SmartPlug(100)
    plug2 = SmartPlug(50)
    oven = SmartOven()

    plug1.toggleSwitch()
    plug1.setConsuptionRate(150)
    plug2.setConsuptionRate(25)
    oven.setTemperature(195)

    myHome.addDevice(plug1)
    myHome.addDevice(plug2)
    myHome.addDevice(oven)

    myHome.toggleSwitchAt(1)
    print(myHome)
    myHome.turnOnAll()
    print(myHome)
    myHome.removeDeviceAt(1)
    print(myHome)
# testSmartHome()