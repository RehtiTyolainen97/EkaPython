#Luokkien rakentelu Hue-laitteille (KESKEN), yläluokka HueDevice
class HueDevice():
    def __init__(self, productId, productName, deviceName):
        self.productId = productId
        self.productName = productName
        self.deviceName = deviceName

# Aliluokka HueLamp, joka perii HueDeviceltä
class HueLamp(HueDevice):
    def __init__(self, productId, productName, deviceName, lightId, onOff, brighteness, color):
        super().__init__(productId, productName, deviceName)
        self.lightId = lightId
        self.onOff = onOff
        self.brighteness = brighteness
        self.color = color

# Aliluokka HueSwitch, joka perii HueDeviceltä
class HueSwitch(HueDevice):
    def __init__(self, productId, productName, deviceName, button1, button2, button3, button4):
        super().__init__(productId, productName, deviceName)
        self.button1 = button1
        self.button2 = button2
        self.button3 = button3
        self.button4 = button4

# Aliluokka HueBridge, joka perii HueDeviceltä
class HueBridge(HueDevice):
    def __init__(self, productId, productName, deviceName, bridgeIP):
        super().__init__(productId, productName, deviceName)
        self.bridgeIP = bridgeIP
