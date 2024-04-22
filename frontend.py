from backend import *
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from csv import *

PADDING = 5
SMALL_ICON_SIZE = 30
LARGE_ICON_SIZE = 40
WHITE = "white"
BLACK = "black"
LIGHT_PRIMARY = "#ececec"
LIGHT_SECONDARY = "#ffffff"
DARK_PRIMARY = "#363636"
DARK_SECONDARY = "#007aff"
DEFAULT_FONT_SIZE = 10

def setUpHome():
    myHome = SmartHome()

    numberPositionDict = {
        0: "1st",
        1: "2nd",
        2: "3rd",
        3: "4th",
        4: "5th",
    }

    while len(myHome.devices) < 5:
        userInput = input(f"Enter the {numberPositionDict[len(myHome.devices)]}"
                            " smart device you'd like to add (Plug or Oven):\n")
        if "plug" in userInput.lower():
            while True:
                plugConsumption = input("Enter the consumption rate (0 - 150):\n")
                if not plugConsumption.isnumeric():
                    print(f"{plugConsumption} is not a integer, try a number (0 - 150)")
                elif int(plugConsumption) in range(0, 151):
                    myHome.addDevice(SmartPlug(plugConsumption))
                    break
                else:
                    print(f"{plugConsumption} is not within the consumption rate range (0 - 150)")
        elif "oven" in userInput.lower():
            myHome.addDevice(SmartOven())
        else:
            print(f"{userInput} is not recognised as a smart device, Try again")

    mySmartHomeSystem = SmartHomeSystem(myHome)
    mySmartHomeSystem.run()



class SmartHomeSystem:
    def __init__(self, smartHome):
        self.smartHome = smartHome

        self.win = Tk()
        self.win.title("Smart Home System")

        # Image Set Up
        plugImageSetup = PhotoImage(file="images/plug.png")
        self.plugImage = plugImageSetup.subsample(plugImageSetup.width() // LARGE_ICON_SIZE)

        ovenImageSetup = PhotoImage(file="images/oven.png")
        self.ovenImage = ovenImageSetup.subsample(ovenImageSetup.width() // LARGE_ICON_SIZE)

        powerImageSetup = PhotoImage(file="images/powerButton.png")
        self.powerButtonImage = powerImageSetup.subsample(powerImageSetup.width() // SMALL_ICON_SIZE)

        binImageSetup = PhotoImage(file="images/bin.png")
        self.binButtonImage = binImageSetup.subsample(binImageSetup.width() // LARGE_ICON_SIZE)

        settingImageSetup = PhotoImage(file="images/setting.png")
        self.settingButtonImage = settingImageSetup.subsample(settingImageSetup.width() // SMALL_ICON_SIZE)
        
        editImageSetup = PhotoImage(file="images/edit.png")
        self.editButtonImage = editImageSetup.subsample(editImageSetup.width() // LARGE_ICON_SIZE)
        
        saveImageSetup = PhotoImage(file="images/save.png")
        self.saveButtonImage = saveImageSetup.subsample(saveImageSetup.width() // LARGE_ICON_SIZE)


        # Main Window
        self.mainframe = Frame(self.win)
        self.mainframe.grid(
            padx=PADDING,
            pady=PADDING
        )
        self.deviceWidgets = []         # destroy main widgets

        self.powerButtonList = []      # destroy submit button for new devices

        self.deviceSchedule = []    # List of schedules

        self.sliderValues = []    # used to create the value for the slider and update later

        for index in range(len(self.smartHome.getDevices())):
            sliderValue = StringVar()
            sliderValue.set(self.smartHome.getDeviceAt(index).getConsumptionRate() 
                          if self.smartHome.getDeviceAt(index).getDeviceType() == "Smart Plug" 
                          else self.smartHome.getDeviceAt(index).getTemperature())
            self.sliderValues.append(sliderValue)

            # Creates the Schedule on and off Var's
            deviceScheduleOn = StringVar()
            deviceScheduleOff = StringVar()
            deviceScheduleOn.set("None")
            deviceScheduleOff.set("None")
            self.deviceSchedule.append([deviceScheduleOn, deviceScheduleOff])

        # Edit Window
        self.newConsumptionRate = IntVar()
        self.newTemperature = IntVar()
        self.errorMessage = StringVar()

        # New Device Window
        self.newDevice = StringVar()
        self.newDeviceSetting = IntVar()
        self.newErrorMessage = StringVar()
        self.newDevice.set("Smart Plug")
        self.newDeviceSubmitWidget = []

        # List of Widgets used to Change Colour
        self.primaryColourList = []
        self.secondaryColourList = []

        # Colour Picker
        self.primaryColour = StringVar()
        self.secondaryColour = StringVar()
        self.fontColour = StringVar()

        self.radioButtonIndex = 0

        # Font size
        self.fontSize = DoubleVar()
        self.fontSize.set(1)

        # Storage
        self.storageErrorText = StringVar()

        # Clock
        self.clock = StringVar()
        self.clock.set("12:00")

        
        
    # Create Main Window

    def createWidgets(self):
        self.deleteAllWidgets()
        self.primaryColourList.append(self.mainframe)

        turnOnAllButton = Button(
            self.mainframe,
            text="Turn on all",
            command=self.turnOnAllDevices,
            relief="flat"
        )
        turnOnAllButton.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.deviceWidgets.append(turnOnAllButton)
        self.secondaryColourList.append(turnOnAllButton)

        turnOffAllButton = Button(
            self.mainframe,
            text="Turn off all",
            command=self.turnOffAllDevices,
            relief="flat"
        )
        turnOffAllButton.grid(
            column=1,
            row=0,
            padx=PADDING,
            pady=PADDING,
            columnspan=2,
            sticky=W
        )
        self.deviceWidgets.append(turnOffAllButton)
        self.secondaryColourList.append(turnOffAllButton)

        clockLabel = Label(
            self.mainframe,
            textvariable=self.clock
        )
        clockLabel.grid(
            column=3,
            row=0,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(clockLabel)

        storageButton = Button(
            self.mainframe,
            image=self.saveButtonImage,
            command=self.storageMenu,
            relief="flat"
        )
        storageButton.grid(
            column=4,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=E,
            columnspan=2
        )
        self.deviceWidgets.append(storageButton)
        self.secondaryColourList.append(storageButton)

        index = 0 # Won't break the buttons reliant on the index if there's no devices

        for index, device in enumerate(self.smartHome.getDevices()):

            devicePowerButton = self.createPowerButton(index)
            self.powerButtonList.append(devicePowerButton)

            deviceIcon = Label(
                self.mainframe,
                image=self.plugImage if device.getDeviceType() == "Smart Plug" else self.ovenImage
            )
            deviceIcon.grid(
                column=1,
                row=index + 1,
                padx=PADDING,
                pady=PADDING
            )
            self.deviceWidgets.append(deviceIcon)
            self.primaryColourList.append(deviceIcon)

            deviceEditScale = Scale(
                self.mainframe,
                orient="horizontal",
                from_=0,
                to=150 if device.getDeviceType() == "Smart Plug" else 260,
                variable=self.sliderValues[index],
                command=lambda value, i = index : self.updateDeviceAtIndex(i),
                length=260,
                sliderrelief="solid",
                troughcolor="grey",
                width=10,
                border=0,
                highlightthickness=0
            )
            deviceEditScale.grid(
                column=2,
                row=index + 1,
                padx=PADDING,
                pady=PADDING
            )
            deviceEditScale.set(self.sliderValues[index].get())
            self.deviceWidgets.append(deviceEditScale)
            self.primaryColourList.append(deviceEditScale)

            deviceEditButton = Button(
                self.mainframe,
                image=self.editButtonImage,
                command=lambda i = index: self.editWindow(i),
                relief="flat"
            )
            deviceEditButton.grid(
                column=3,
                row=index + 1,
                padx=PADDING,
                pady=PADDING
            )
            self.deviceWidgets.append(deviceEditButton)
            self.secondaryColourList.append(deviceEditButton)


            deviceDeleteButton = Button(
                self.mainframe,
                image=self.binButtonImage,
                command=lambda i = index: self.removeDeviceAtIndex(i),
                width=50,
                relief="flat"
            )
            deviceDeleteButton.grid(
                column=4,
                row=index + 1,
                padx=PADDING,
                pady=PADDING
            )
            self.deviceWidgets.append(deviceDeleteButton)
            self.secondaryColourList.append(deviceDeleteButton)

        addDeviceButton = Button(
            self.mainframe,
            text="Add",
            command= self.addNewDeviceWindow,
            relief="flat"
        )
        addDeviceButton.grid(
            column=0,
            row=index + 2,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.deviceWidgets.append(addDeviceButton)
        self.secondaryColourList.append(addDeviceButton)

        settingsButton = Button(
            self.mainframe,
            image=self.settingButtonImage,
            command=self.createSettingsMenu,
            width=50,
            relief="flat"
        )
        settingsButton.grid(
            column=3,
            row=index + 2,
            ipady=2,
            padx=PADDING,
            pady=PADDING,
            columnspan=2,
            sticky=E
        )
        self.deviceWidgets.append(settingsButton)
        self.secondaryColourList.append(settingsButton)

        self.setColoursForWindow()
        self.updateFontSize()

    def updateDeviceAtIndex(self, index):
        if self.smartHome.getDeviceAt(index).getDeviceType() == "Smart Plug":
            self.updatePlugConsumptionAtIndex(index)
        elif self.smartHome.getDeviceAt(index).getDeviceType() == "Smart Oven":
            self.updateOvenTempAtIndex(index)

    def updateSubmitButton(self, index):
        self.powerButtonList[index].destroy()
        self.createPowerButton(index)
        
    def createPowerButton(self, index):
        devicePowerButton = Button(
            self.mainframe,
            image=self.powerButtonImage,
            command=lambda i = index: self.toggleDeviceAtIndex(i),
            bg="#00d000" if self.smartHome.getDeviceAt(index).getSwitchedOn() else "#ff0000",
            border=0,
            borderwidth=0,
            width=40,
            relief="flat"
        )
        devicePowerButton.grid(
            column=0,
            row=index + 1,
            padx=PADDING,
            pady=PADDING
        )
        self.deviceWidgets.append(devicePowerButton)
        return devicePowerButton
    
    def updatePlugConsumptionAtIndex(self, index):
        self.smartHome.setConsumptionRateAtIndex(index, self.sliderValues[index].get())

    def updateOvenTempAtIndex(self, index):
        self.smartHome.setOvenTemperatureAtIndex(index, int(self.sliderValues[index].get()))

    def deleteAllWidgets(self):
        for widget in self.deviceWidgets:
            widget.destroy()
        self.deviceWidgets = []
        self.primaryColourList = []
        self.secondaryColourList = []
        
    def toggleDeviceAtIndex(self, index):
        self.smartHome.toggleSwitchAt(index)
        self.updateSubmitButton(index)

    def turnOnAllDevices(self):
        self.smartHome.turnOnAll()
        for index in range(len(self.smartHome.getDevices())):
            self.updateSubmitButton(index)

    def turnOffAllDevices(self):
        self.smartHome.turnOffAll()
        for index in range(len(self.smartHome.getDevices())):
            self.updateSubmitButton(index)

    def removeDeviceAtIndex(self, index):
        self.sliderValues.remove(self.sliderValues[index])
        self.powerButtonList.remove(self.powerButtonList[index])
        self.deviceSchedule.remove(self.deviceSchedule[index])
        self.smartHome.removeDeviceAt(index)
        self.createWidgets()

# Edit Window

    def editWindow(self, index):
        self.editWin = Toplevel(self.win)
        self.editWin.title("Edit Device")
        self.editWin.grid()
        self.primaryColourList.append(self.editWin)

        deviceType = self.smartHome.getDeviceAt(index).getDeviceType()

        deviceLabel = Label(
            self.editWin,
            text=f"{deviceType} "
                 f"{'Consumption rate: ' if deviceType =='Smart Plug' else 'Cemperature: '}"
        )
        deviceLabel.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(deviceLabel)

        if deviceType == "Smart Plug":
            self.newConsumptionRate.set(int(self.sliderValues[index].get()))
            plugEntry = Entry(
                self.editWin,
                textvariable=self.newConsumptionRate
            )
            plugEntry.grid(
                column=1,
                row=0,
                padx=PADDING,
                pady=PADDING
            )
            self.secondaryColourList.append(plugEntry)
        else:
            self.newTemperature.set(int(self.sliderValues[index].get()))
            ovenEntry = Entry(
                self.editWin,
                textvariable=self.newTemperature
            )
            ovenEntry.grid(
                column=1,
                row=0,
                padx=PADDING,
                pady=PADDING
            )
            self.secondaryColourList.append(ovenEntry)

        scheduleOnLabel = Label(
            self.editWin,
            text="Schedule On: "
        )
        scheduleOnLabel.grid(
            column=0,
            row=1,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(scheduleOnLabel)

        optionMenu = [
            "None","00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00",
            "08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00",
            "17:00","18:00","19:00","20:00","21:00","22:00","23:00","24:00"
        ]

        scheduleOnOptionMenu = OptionMenu(
            self.editWin,
            self.deviceSchedule[index][0],
            *optionMenu
        )
        scheduleOnOptionMenu.grid(
            column=1,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(scheduleOnOptionMenu)

        scheduleOffLabel = Label(
            self.editWin,
            text="Schedule Off: "
        )
        scheduleOffLabel.grid(
            column=0,
            row=2,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(scheduleOffLabel)

        scheduleOffOptionMenu = OptionMenu(
            self.editWin,
            self.deviceSchedule[index][1],
            *optionMenu
        )
        scheduleOffOptionMenu.grid(
            column=1,
            row=2,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(scheduleOffOptionMenu)

        errorLabel = Label(
            self.editWin,
            textvariable=self.errorMessage,
            fg="red"
        )
        errorLabel.grid(
            column=0,
            row=3,
            padx=PADDING,
            pady=PADDING,
            columnspan=3
        )
        self.primaryColourList.append(errorLabel)

        submitButton = Button(
            self.editWin,
            text="Submit",
            command= lambda i = index:self.consumptionRateChecker(i) if deviceType == 
                                        "Smart Plug" else self.temperatureChecker(i),
            relief="flat"
        )
        submitButton.grid(
            column=1,
            row=4,
            padx=PADDING,
            pady=PADDING,
            sticky=E
        )
        self.secondaryColourList.append(submitButton)
        
        self.setColoursForWindow()
        self.updateFontSize()
    
    def consumptionRateChecker(self, index):
        try:
            if self.newConsumptionRate.get() in range(0, 151):
                self.setConsuptionRateAtIndexFunc(index)
                self.closeEditWindow()
            else:
                self.errorMessage.set(f"{self.newConsumptionRate.get()}"
                                    " is outside of the Smart Plug range (0 - 150)")
        except TclError:
                self.errorMessage.set("Please use an integer within the range 0 - 150")

    def temperatureChecker(self, index):
        try:
            if self.newTemperature.get() in range(0, 261):
                self.setOvenTemperatureAtIndexFunc(index)
                self.closeEditWindow()
            else:
                self.errorMessage.set(f"{self.newTemperature.get()}"
                                    " is outside of the Smart Oven range (0 - 260)")
        except TclError:
                self.errorMessage.set("Please use an integer within the range 0 - 260")

    def setOvenTemperatureAtIndexFunc(self, index):
        self.smartHome.setOvenTemperatureAtIndex(index, self.newTemperature.get())
        self.sliderValues[index].set(self.newTemperature.get())

    def setConsuptionRateAtIndexFunc(self, index):
        self.smartHome.setConsumptionRateAtIndex(index, self.newConsumptionRate.get())
        self.sliderValues[index].set(self.newConsumptionRate.get())
            
    def closeEditWindow(self):
        self.editWin.destroy()
  
# Add New Device Window

    def addNewDeviceWindow(self):
        self.addNewDeviceWin = Toplevel(self.win)
        self.addNewDeviceWin.title("New Device")
        self.addNewDeviceWin.grid()
        self.primaryColourList.append(self.addNewDeviceWin)

        selectDeviceLabel = Label(
            self.addNewDeviceWin,
            text="Device:"
        )
        selectDeviceLabel.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(selectDeviceLabel)

        # Creates the submit button for the option menu command 
        self.createSubmitButton()

        newDeviceOption = OptionMenu(
            self.addNewDeviceWin,
            self.newDevice,
            "Smart Plug",
            "Smart Oven",
            command= lambda _: self.createSubmitButton()
        )
        newDeviceOption.grid(
            column=0,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(newDeviceOption)
        
        self.setColoursForWindow()
        self.updateFontSize()

    def createSubmitButton(self):
        self.newErrorMessage.set("")
        self.newDeviceSetting.set(0)
        if self.newDevice.get() == "Smart Plug":
            self.createPlugSubmitButton()
        else:
            self.createOvenSubmitButton()

    def createPlugSubmitButton(self):
        self.deleteSubmitWidget()

        plugLabel = Label(
            self.addNewDeviceWin,
            text="Consumption Rate: "
        )
        plugLabel.grid(
            column=1,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(plugLabel)
        self.newDeviceSubmitWidget.append(plugLabel)

        newDeviceEntry = Entry(
            self.addNewDeviceWin,
            textvariable=self.newDeviceSetting
        )
        newDeviceEntry.grid(
            column=1,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(newDeviceEntry)
        self.newDeviceSubmitWidget.append(newDeviceEntry)

        newErrorMessage = Label(
            self.addNewDeviceWin,
            textvariable=self.newErrorMessage,
            fg="red"
        )
        newErrorMessage.grid(
            column=0,
            row=2,
            padx=PADDING,
            pady=PADDING,
            columnspan=3
        )
        self.primaryColourList.append(newErrorMessage)
        self.newDeviceSubmitWidget.append(newErrorMessage)

        submitButton = Button(
            self.addNewDeviceWin,
            text="Submit",
            command=self.newConsumptionRateChecker,
            relief="flat"
        )
        submitButton.grid(
            column=2,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.newDeviceSubmitWidget.append(submitButton)
        self.secondaryColourList.append(submitButton)
        self.setColoursForWindow()
        self.updateFontSize()

    def createOvenSubmitButton(self):
        self.deleteSubmitWidget()

        submitButton = Button(
            self.addNewDeviceWin,
            text="Submit",
            command=self.createNewOven,
            relief="flat"
        )
        submitButton.grid(
            column=2,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.newDeviceSubmitWidget.append(submitButton)
        self.secondaryColourList.append(submitButton)
        self.setColoursForWindow()
        self.updateFontSize()

    def newConsumptionRateChecker(self):
        try:
            if self.newDeviceSetting.get() in range(0, 151):
                self.createNewPlug()
                self.closeNewDeviceWin()
            else:
                self.newErrorMessage.set(f"{self.newDeviceSetting.get()}"
                                        " is outside of the Smart Plug range (0 - 150)")
        except TclError:
            self.newErrorMessage.set("Please use an integer within the range 0 - 150")

    def createNewPlug(self):
        newPlug = SmartPlug(self.newDeviceSetting.get())

        scaleText = StringVar()
        scaleText.set(self.newDeviceSetting.get())
        deviceScheduleOn = StringVar()
        deviceScheduleOff = StringVar()
        deviceScheduleOn.set("None")
        deviceScheduleOff.set("None")
        self.deviceSchedule.append([deviceScheduleOn, deviceScheduleOff])
           

        deviceScheduleOn = StringVar()
        deviceScheduleOff = StringVar()
        deviceScheduleOn.set("None")
        deviceScheduleOff.set("None")
        self.deviceSchedule.append([deviceScheduleOn, deviceScheduleOff])

        self.smartHome.addDevice(newPlug)
        self.sliderValues.append(scaleText)
        self.closeNewDeviceWin()


    def createNewOven(self):
        newOven = SmartOven()

        scaleText = StringVar()
        scaleText.set(self.newDeviceSetting.get())
        deviceScheduleOn = StringVar()
        deviceScheduleOff = StringVar()
        deviceScheduleOn.set("None")
        deviceScheduleOff.set("None")
        self.deviceSchedule.append([deviceScheduleOn, deviceScheduleOff])

        self.smartHome.addDevice(newOven)
        self.sliderValues.append(scaleText)
        self.closeNewDeviceWin()

    def closeNewDeviceWin(self):
        self.createWidgets()
        self.addNewDeviceWin.destroy()

    def deleteSubmitWidget(self):
        for widget in self.newDeviceSubmitWidget:
            widget.destroy()
        self.newDeviceSubmitWidget = []

    # Settings Menu
        
    def createSettingsMenu(self):
        settingWin = Toplevel(self.win)
        settingWin.title("Setting Menu")
        settingWin.grid()
        self.primaryColourList.append(settingWin)

        colourSchemeList = [
            ["Light Mode", "The default scheme with dark text on a white background"],
            ["Dark Mode", "Alternative scheme with light text on a dark background"],
            ["Custom Colour", "Set your own colour scheme"]
        ]

        colourSchemeLabel = Label(
            settingWin,
            text="Colour Scheme: "
        )
        colourSchemeLabel.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(colourSchemeLabel)

        for index, colour in enumerate(colourSchemeList):
            colourSchemeRadio = Radiobutton(
                settingWin,
                text=colour[0],
                value=colour[0],
                command=lambda i = index:self.colourSelector(i)
            )
            colourSchemeRadio.grid(
                column=0,
                row= index + 1,
                padx=PADDING,
                pady=PADDING,
                sticky=W
            )
            self.primaryColourList.append(colourSchemeRadio)

            colourSchemeDescription = Label(
                settingWin,
                text=colour[1]
            )
            colourSchemeDescription.grid(
                column=1,
                row= index + 1,
                padx=PADDING,
                pady=PADDING,
                sticky=W
            )
            self.primaryColourList.append(colourSchemeDescription)
        
        fontLabel = Label(
            settingWin,
            text="Text size: "
        )
        fontLabel.grid(
            column=0,
            row=index + 2,
            padx=PADDING,
            pady=PADDING,
            columnspan=2,
            sticky=W
        )
        self.primaryColourList.append(fontLabel)

        fontScale = Scale(
            settingWin,
            orient="horizontal",
            from_=0.5,
            to=1.5,
            resolution=0.01,
            variable=self.fontSize,
            command=lambda value: self.updateFontSize(),
            length=260,
            sliderrelief="flat",
            troughcolor="grey",
            width=10,
            highlightthickness=0
        )
        fontScale.grid(
            column=0,
            row= index + 3,
            padx=PADDING,
            pady=PADDING,
            sticky=W,
            columnspan=2
        )
        fontScale.set(self.fontSize.get())
        self.primaryColourList.append(fontScale)

        self.setColoursForWindow()
        self.updateFontSize()

    def updateFontSize(self):
        fontSize = int(self.fontSize.get() * DEFAULT_FONT_SIZE)
        for widget in self.primaryColourList:
            try:
                widget.configure(font=("", fontSize))
            except TclError:
                pass
        for widget in self.secondaryColourList:
            try:
                widget.configure(font=("", fontSize))
            except TclError:
                pass

    # used to change colours

    def colourSelector(self, index):

        oldIndex = self.radioButtonIndex
        self.radioButtonIndex = index

        if index < 1:
            self.setLightMode()
        elif index < 2:
            self.setDarkMode()
        else:
            self.colourPicker(oldIndex)

    # used to set colours when creating / updating the window

    def setColoursForWindow(self): 

        index = self.radioButtonIndex

        if index < 1:
            self.setLightMode()
        elif index < 2:
            self.setDarkMode()
        else:
            self.setColours()

    # colour selector window

    def colourPicker(self, oldColourIndex):
        self.colourPickerWin = Toplevel(self.win)
        self.colourPickerWin.title("Custom Colour Picker")
        self.colourPickerWin.grid()
        self.primaryColourList.append(self.colourPickerWin)

        primaryColourLabel = Label(
            self.colourPickerWin,
            text="Primary Colour"
        )
        primaryColourLabel.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(primaryColourLabel)
        primaryColourMenu = Button(
            self.colourPickerWin,
            text="Choose Colour",
            command=self.choosePrimaryColour
        )
        primaryColourMenu.grid(
            column=1,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.secondaryColourList.append(primaryColourMenu)
        primaryColourHex = Label(
            self.colourPickerWin,
            textvariable=self.primaryColour
        )
        primaryColourHex.grid(
            column=2,
            row=0,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(primaryColourHex)

        secondaryColourLabel = Label(
            self.colourPickerWin,
            text="Secondary Colour"
        )
        secondaryColourLabel.grid(
            column=0,
            row=1,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(secondaryColourLabel)
        secondaryColourMenu = Button(
            self.colourPickerWin,
            text="Choose Colour",
            command=self.choosesecondaryColour
        )
        secondaryColourMenu.grid(
            column=1,
            row=1,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.secondaryColourList.append(secondaryColourMenu)
        secondaryColourHex = Label(
            self.colourPickerWin,
            textvariable=self.secondaryColour
        )
        secondaryColourHex.grid(
            column=2,
            row=1,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(secondaryColourHex)

        fontColourLabel = Label(
            self.colourPickerWin,
            text="Font Colour"
        )
        fontColourLabel.grid(
            column=0,
            row=2,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(fontColourLabel)
        fontColourMenu = Button(
            self.colourPickerWin,
            text="Choose Colour",
            command=self.choosefontColour
        )
        fontColourMenu.grid(
            column=1,
            row=2,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.secondaryColourList.append(fontColourMenu)
        fontColourHex = Label(
            self.colourPickerWin,
            textvariable=self.fontColour
        )
        fontColourHex.grid(
            column=2,
            row=2,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.primaryColourList.append(fontColourHex)

        submitColourButton = Button(
            self.colourPickerWin,
            text="Submit",
            command=self.checkColours
        )
        submitColourButton.grid(
            column=0,
            row=3,
            padx=PADDING,
            pady=PADDING,
            sticky=W
        )
        self.secondaryColourList.append(submitColourButton)
        self.colourSelectorForPicker(oldColourIndex)

    # used to colour the colour picker menu it's old colour before submitting
    def colourSelectorForPicker(self, oldIndex):

        index = oldIndex

        if index < 1:
            self.setLightMode()

        elif index < 2:
            self.setDarkMode()
        else:
            self.setColours()

    def setLightMode(self):
        self.win.configure(bg=LIGHT_PRIMARY)
        for widget in self.primaryColourList:
            try:      # no errors when trying to change fg or bg for something with no attribute
                widget.configure(bg=LIGHT_PRIMARY)
                widget.configure(fg=BLACK)
            except TclError:
                pass
        for widget in self.secondaryColourList:
            try:
                widget.configure(bg=LIGHT_SECONDARY)
                widget.configure(highlightbackground=LIGHT_PRIMARY)   # used for entry's
                widget.configure(fg=BLACK)
            except TclError:
                pass

    def setDarkMode(self):
        self.win.configure(bg=DARK_PRIMARY)
        for widget in self.primaryColourList:
            try:
                widget.configure(bg=DARK_PRIMARY)
                widget.configure(fg=WHITE)
            except TclError:
                pass
        for widget in self.secondaryColourList:
            try:
                widget.configure(bg=DARK_SECONDARY)
                widget.configure(highlightbackground=DARK_PRIMARY)
                widget.configure(fg=WHITE)
            except TclError:
                pass
    
    # Sets custom colours

    def setColours(self):
        try:                        # doesn't throw error if submitting before choosing a colour
            self.win.configure(bg=self.primaryColour.get())
            for widget in self.primaryColourList:
                try:
                    widget.configure(bg=self.primaryColour.get())
                    widget.configure(fg=self.fontColour.get())
                except TclError:
                    pass
            for widget in self.secondaryColourList:
                try:
                    widget.configure(bg=self.secondaryColour.get())
                    widget.configure(highlightbackground=self.primaryColour.get())
                    widget.configure(fg=self.fontColour.get())
                except TclError:
                    pass
        except TclError:
            pass

    def choosePrimaryColour(self):
        primaryColour = colorchooser.askcolor(title="Choose Primary Colour")
        self.primaryColour.set(primaryColour[1])

    def choosesecondaryColour(self):
        secondaryColour = colorchooser.askcolor(title="Choose secondary Colour")
        self.secondaryColour.set(secondaryColour[1])

    def choosefontColour(self):
        fontColour = colorchooser.askcolor(title="Choose font Colour")
        self.fontColour.set(fontColour[1])

    def checkColours(self):
        if self.primaryColour.get() == "" or self.primaryColour.get() == "None":
            self.primaryColour.set("Choose an option before submitting")
        if self.secondaryColour.get() == "" or self.secondaryColour.get() == "None":
            self.secondaryColour.set("Choose an option before submitting")
        if self.fontColour.get() == "" or self.fontColour.get() == "None":
            self.fontColour.set("Choose an option before submitting")

        if self.primaryColour.get()[0] == "#" \
            and self.secondaryColour.get()[0] == "#" \
            and self.fontColour.get()[0] == "#":

            self.setColours()
            self.colourPickerWin.destroy()

    # Permanent storage

    def storageMenu(self):
        self.storageWin = Toplevel(self.win)
        self.storageWin.title("Smart Home Settings")
        self.storageWin.grid()
        self.primaryColourList.append(self.storageWin)

        storgaeLabel = Label(
            self.storageWin,
            text="Save / Open a Smart Home"
        )
        storgaeLabel.grid(
            column=0,
            row=0,
            padx=PADDING,
            pady=PADDING,
            columnspan=2
        )
        self.primaryColourList.append(storgaeLabel)

        saveFileLabel = Label(
            self.storageWin,
            text="Save current Smart Home: "
        )
        saveFileLabel.grid(
            column=0,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(saveFileLabel)
        saveFileButton = Button(
            self.storageWin,
            text="Choose Save File",
            command=self.openSaveFile
        )
        saveFileButton.grid(
            column=1,
            row=1,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(saveFileButton)

        openFileLabel = Label(
            self.storageWin,
            text="Open an existing Smart Home: "
        )
        openFileLabel.grid(
            column=0,
            row=2,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(openFileLabel)
        openFileButton = Button(
            self.storageWin,
            text="Choose File",
            command=self.openFile
        )
        openFileButton.grid(
            column=1,
            row=2,
            padx=PADDING,
            pady=PADDING
        )
        self.secondaryColourList.append(openFileButton)

        errorLabel = Label(
            self.storageWin,
            textvariable=self.storageErrorText
        )
        errorLabel.grid(
            column=0,
            row=3,
            padx=PADDING,
            pady=PADDING
        )
        self.primaryColourList.append(errorLabel)

        self.setColoursForWindow()
        self.updateFontSize()

    def getFilePath(self):
        storageFileName = filedialog.askopenfilename(initialdir="/", title="Select a Save", 
            filetypes=(
                ("csv Files", "*.csv"), 
                ("Text Files", "*.txt"), 
                ("All Files", "*.*")
            )
        )
        return storageFileName

    def openFile(self):
        storageFileName = self.getFilePath()
        if storageFileName == "":
            self.storageErrorText.set("Please choose a file.")
        else:
            try:
                storageFileOpen = open(storageFileName, "r")
                storageFile = reader(storageFileOpen)
                self.createNewSmartHome(storageFile)
                storageFileOpen.close()
                self.storageWin.destroy()
            except UnicodeDecodeError:
                self.storageErrorText.set("This file is not correctly formatted. Try another file.")
        
    def createNewSmartHome(self, storageFile):
        self.smartHome.removeAllDevices()
        self.sliderValues = []
        self.powerButtonList = []
        self.deviceSchedule = []

        for line in storageFile:
            scaleText = StringVar()
            deviceScheduleOn = StringVar()
            deviceScheduleOff = StringVar()
            deviceScheduleOn.set("None")
            deviceScheduleOff.set("None")

            if line[0] == "Plug":
                newDevice = SmartPlug(int(line[2]))
                scaleText.set(line[2])
            else:
                newDevice = SmartOven()
                newDevice.setTemperature(line[2])
                scaleText.set(line[2])
            try:
                deviceScheduleOn.set(line[3])
                deviceScheduleOff.set(line[4])
            except IndexError:
                pass
            
            self.deviceSchedule.append([deviceScheduleOn, deviceScheduleOff])
            self.sliderValues.append(scaleText)
            if line[1] == "On":
                newDevice.toggleSwitch()
            self.smartHome.addDevice(newDevice)
        self.createWidgets()

    def openSaveFile(self):
        storageFileName = self.getFilePath()
        if storageFileName == "":
            self.storageErrorText.set("Please choose a file.")
        else:
            storageFileOpen = open(storageFileName, "w", newline="")
            storageFile = writer(storageFileOpen)
            self.saveSmartHome(storageFile)
            storageFileOpen.close()
            self.storageWin.destroy()
        
    def saveSmartHome(self, storageFile):
        
        devices = self.smartHome.getDevices()
        for index, device in enumerate(devices):
            deviceType = device.getDeviceType()[-4:]
            deviceState = "On" if device.getSwitchedOn() else "Off"
            deviceSetting = device.getConsumptionRate() if deviceType == "Plug" else device.getTemperature()

            deviceScheduleOn = self.deviceSchedule[index][0].get()
            deviceScheduleOff = self.deviceSchedule[index][1].get()

            storageFile.writerow((deviceType, deviceState, deviceSetting, deviceScheduleOn, deviceScheduleOff))

    # Clock 
            
    def clockTick(self):
        self.win.after(3000, self.addSecond)

    def addSecond(self):
        time = int(self.clock.get()[:2])
        if time < 9:
            self.clock.set(f"0{time + 1}:00")
        elif time < 23:
            self.clock.set(f"{time + 1}:00")
        else:
            self.clock.set(f"00:00")

        self.checkSchedule()
        self.clockTick()

    def checkSchedule(self):
        for index, schedule in enumerate(self.deviceSchedule):
            scheduleOn = schedule[0].get()
            scheduleOff = schedule[1].get()

            if scheduleOn == "None":
                pass
            else:
                if not self.smartHome.getDeviceAt(index).getSwitchedOn():
                    if scheduleOn == self.clock.get():
                        self.toggleDeviceAtIndex(index)

            if scheduleOff == "None":
                pass
            else:
                if self.smartHome.getDeviceAt(index).getSwitchedOn():
                    if scheduleOff == self.clock.get():
                        self.toggleDeviceAtIndex(index)

    def run(self):
        self.createWidgets()
        self.clockTick()
        self.win.mainloop()


def main():
    setUpHome()
main()


# Testing Main

def testMain():
    myHome = SmartHome()

    plug1 = SmartPlug(100)
    plug2 = SmartPlug(50)
    plug3 = SmartPlug(50)
    plug4 = SmartPlug(50)

    oven = SmartOven()

    plug1.toggleSwitch()
    plug1.setConsuptionRate(150)

    plug2.setConsuptionRate(25)
    oven.setTemperature(195)
    oven.toggleSwitch()

    myHome.addDevice(plug1)
    myHome.addDevice(plug2)
    myHome.addDevice(plug3)
    myHome.addDevice(plug4)
    myHome.addDevice(oven)

    myApp = SmartHomeSystem(myHome)
    myApp.run()
# testMain()