class Device:
    '''
    Contrust a Device instance. This class is mainly used as the base class for other Smart Classes.

    Attributes:
        switchedOn (bool): The switchedOn status of the object; True if switched on, False otherwise. By default is False.

    Methods:
        toggleSwitch(): Toggles the value of the switchedOn attribute.
        getSwitchedOn(): Returns the value of the switchedOn attribute.
    '''
    def __init__(self) -> None:
        self.switchedOn = False

    def toggleSwitch(self) -> None:
        '''
        Toggles the switchedOn attribute of the object.
        If the object is switched-off, it will be switched-on, and vice versa.
        '''
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self) -> bool:
        '''
        Get the current switchedOn status of the object.
        Returns:
            bool: True if the object is switched on, False otherwise.
        '''
        return self.switchedOn
    


class SmartPlug(Device):
    '''
    Contrust a SmartPlug instance. Used in the SmartHome class, Inherits from Device class.

    Attributes:
        switchedOn (bool): The switchedOn status of the object; True if switched on, False otherwise.
        consumptionRate (int): The consumption rate (power usuage) that the SmartPlug uses.

    Methods:
        getConsumptionRate(): Returns the value of the consumptionRate attribute.
        getDeviceType(): Returns the device type ("Smart Plug").
        setConsuptionRate(): Sets the value of the consumptionRate attribute.
    '''
    def __init__(self, consumptionRate: int) -> None:
        super().__init__()
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self) -> int:
        '''
        Gets the value of the consumptionRate attribute.
        Returns int.
        '''
        return self.consumptionRate
    
    def getDeviceType(self) -> str:
        '''
        Gets the device type of the Smart Plug.
        Returns: "Smart Plug".
        '''
        return "Smart Plug"

    def setConsuptionRate(self, newConsumptionRate: int) -> None:
        '''
        Sets the consumption rate of the SmartPlug.
        Any int value from 0 - 150.
        '''
        self.consumptionRate = newConsumptionRate

    def __str__(self) -> str:
        '''
        Returns the device type, it's switchedOn attribute and the consumptionRate.
        '''
        output = "Smart Plug - "
        output += "On" if self.switchedOn else "Off"
        output += f", Consumption rate: {self.consumptionRate}"
        return output
    


class SmartOven(Device):
    '''
    Contrust a SmartOven instance. Used in the SmartHome class, Inherits from Device class.

    Attributes:
        switchedOn (bool): The switchedOn status of the object; True if switched on, False otherwise. By default is False.
        temperature (int): The consumption rate (power usuage) that the SmartPlug uses. By default is 0.

    Methods:
        getTemperature(): Returns the value of the temperature attribute.
        getDeviceType(): Returns the device type ("Smart Oven").
        setTemperature(): Sets the value of the temperature attribute.
    '''
    def __init__(self) -> None:
        super().__init__()
        self.switchedOn = False
        self.temperature = 0
    
    def getTemperature(self) -> int:
        '''
        Gets the value of the temperature attribute.
        Returns int.
        '''
        return self.temperature
    
    def getDeviceType(self) -> str:
        '''
        Gets the device type of the Smart Device.
        Returns: "Smart Oven".
        '''
        return "Smart Oven"
    
    def setTemperature(self, newTemperature: int) -> None:
        '''
        Sets the temperature of the SmartOven.
        Any int value from 0 - 260.
        '''
        if newTemperature in range(0, 261):
            self.temperature = newTemperature

    def __str__(self) -> str:
        '''
        Returns the device type, it's switchedOn attribute and the temperature.
        '''
        output = "Smart Oven - "
        output += "On" if self.switchedOn else "Off"
        output += f", Temperature: {self.temperature} Degrees Celcius"
        return output



class SmartHome:
    '''
    Contrust a SmartHome instance. 

    Attributes:

    Methods:
    '''
    def __init__(self) -> None:
        '''
        
        '''
        self.devices = []

    def getDevices(self) -> list:
        '''
        
        '''
        return self.devices
    
    def getDeviceAt(self, index: int) -> SmartOven | SmartPlug:
        '''
        
        '''
        return self.devices[index]
    
    def removeDeviceAt(self, index: int) -> None:
        '''
        
        '''
        self.devices.remove(self.devices[index])

    def removeAllDevices(self) -> None:
        '''
        
        '''
        self.devices = []
    
    def addDevice(self, device) -> None:
        '''
        
        '''
        self.devices.append(device)

    def toggleSwitchAt(self, index: int) -> None:
        '''
        
        '''
        self.devices[index].toggleSwitch()

    def turnOnAll(self) -> None:
        '''
        
        '''
        for device in self.devices:
            if not device.switchedOn:
                device.toggleSwitch()

    def turnOffAll(self) -> None:
        '''
        
        '''
        for device in self.devices:
            if device.switchedOn:
                device.toggleSwitch()

    def setConsumptionRateAtIndex(self, index, newConsumptionRate) -> None:
        '''
        
        '''
        self.devices[index].setConsuptionRate(newConsumptionRate)

    def setOvenTemperatureAtIndex(self, index, newTemperature) -> None:
        '''
        
        '''
        self.devices[index].setTemperature(newTemperature)

    def __str__(self)  -> str:
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