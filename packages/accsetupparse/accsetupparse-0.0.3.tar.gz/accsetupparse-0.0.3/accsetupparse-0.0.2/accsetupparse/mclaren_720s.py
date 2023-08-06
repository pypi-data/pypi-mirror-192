# This file is part of ACC Setup Parse.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# For more information contact
# jurs.slovinac2@gmail.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

import json

class McLaren720S:
    """
    Class for converting and storing McLaren 720S GT3 setup from json file
    Use McLaren720S("<path to setup file>")
    """
    def __init__(self, setup):
        #Loading setup from json file
        self.s = open(setup) 
        self.data = json.load(self.s)
        self.s.close()

        #Saving setup into real values
        self.car = self.data["carName"]
        #Tyres
        self.tyreType = self._getTyreType()
        self.tyrePressure = self._getTyrePressure()
        self.tyreToe = self._getTyreToe()
        self.tyreCamber = self._getTyreCamber()
        self.tyreCaster = self._getTyreCaster()
        #Electronics
        self.tc = self.data['basicSetup']['electronics']['tC1']
        self.abs = self.data['basicSetup']['electronics']['abs']
        self.ecu = self.data['basicSetup']['electronics']['eCUMap'] + 1
        #Strategy
        self.fuel = self.data['basicSetup']['strategy']['fuel']
        self.tyreSet = self.data['basicSetup']['strategy']['tyreSet']
        self.frontBrakePad = self.data['basicSetup']['strategy']['frontBrakePadCompound'] + 1
        self.rearBrakePad = self.data['basicSetup']['strategy']['rearBrakePadCompound'] + 1
        #Mecanical settings
        self.frontARB = self.data['advancedSetup']['mechanicalBalance']['aRBFront']
        self.rearARB = self.data['advancedSetup']['mechanicalBalance']['aRBRear']
        self.wheelRate = self._getWheelRate()
        self.bumpStopRate = self._getBumpStopRate()
        self.bumpStopRange = self.data['advancedSetup']['mechanicalBalance']['bumpStopWindow']
        self.brakePower = self.data['advancedSetup']['mechanicalBalance']['brakeTorque'] + 80
        self.brakeBias = self._getBrakeBias()
        self.preload = 20 + self.data['advancedSetup']['drivetrain']['preload'] * 10
        #Dampers
        self.bumpSlow = self.data['advancedSetup']['dampers']['bumpSlow']
        self.bumpFast = self.data['advancedSetup']['dampers']['bumpFast']
        self.reboundSlow = self.data['advancedSetup']['dampers']['reboundSlow']
        self.reboundFast = self.data['advancedSetup']['dampers']['reboundFast']
        #Aero
        self.rideHeight = self._getRideHeight()
        self.frontSpliter = 0
        self.rearWing = self.data['advancedSetup']['aeroBalance']['rearWing'] + 1
        self.brakeDucts = self.data['advancedSetup']['aeroBalance']['brakeDuct']


    def _getTyreType(self): #Function for returning tyre compound
        if self.data['basicSetup']['tyres']['tyreCompound'] == 0:
            return "Dry"
        else:
            return "Wet"
        
    def _getTyrePressure(self): #Function returns real tyre pressure numbers
        pressures = []
        for p in self.data['basicSetup']['tyres']['tyrePressure']:
            pressures.append(round(20.3 + p * 0.1, 1))

        return pressures
        
    def _getTyreToe(self): #Function returns list of real toe vaules
        toe = []
        for t in range(0, 2): #Front toe
            toe.append(round(-0.48 + self.data['basicSetup']['alignment']['toe'][t] * 0.01, 2))

        for t in range(2, 4): #Front toe
            toe.append(round(-0.1 + self.data['basicSetup']['alignment']['toe'][t] * 0.01, 2))

        return toe
    
    def _getTyreCamber(self): #Function return list of real camber values
        camber = []
        for c in range(0, 2): #Front camber
            camber.append(round(-4 + self.data['basicSetup']['alignment']['camber'][c] * 0.1, 1))

        for c in range(2, 4): #Rear camber
            camber.append(round(-3.5 + self.data['basicSetup']['alignment']['camber'][c] * 0.1, 1))

        return camber

    def _getTyreCaster(self): #Function returns list of real caster values
        casterValues = [5.3, 5.6, 5.8, 6.0, 6.3, 6.5, 6.8, 7.0, 7.3, 7.5, 7.8, 8.0] #Possible vaules in-game
        caster = []
        caster.append(casterValues[self.data['basicSetup']['alignment']['casterLF']])
        caster.append(casterValues[self.data['basicSetup']['alignment']['casterRF']])

        return caster
    
    def _getWheelRate(self): #Returns list of real wheel rate vaules
        rates = []
        for r in range(0, 2): #Front springs
            rates.append(118000 + self.data['advancedSetup']['mechanicalBalance']['wheelRate'][r] * 16000)

        for r in range(2, 4): #Rear springs
            rates.append(114000 + self.data['advancedSetup']['mechanicalBalance']['wheelRate'][r] * 14000)

        return rates
    
    def _getBumpStopRate(self): #Returns list of real bumpstop rates
        rates = []
        for r in self.data['advancedSetup']['mechanicalBalance']['bumpStopRateUp']:
            rates.append(300 + r * 100)

        return rates
    
    def _getBrakeBias(self): #Returns real brake bias value in %
        return (47.0 + self.data['advancedSetup']['mechanicalBalance']['brakeBias'] * 0.2)
    
    def _getRideHeight(self): #Returns list of real ride height values [front, rear]
        height = []
        height.append(50 + self.data['advancedSetup']['aeroBalance']['rideHeight'][0]) #Front
        height.append(64 + self.data['advancedSetup']['aeroBalance']['rideHeight'][2]) #Rear

        return height