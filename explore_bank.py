# -*- coding: utf-8 -*-
#
# Class and values used to maintain current value estimate
#
import os, json


#Indices
DETAILED_INDEX = 0
BASIC_INDEX = 1
#Stars
T_TTauri = (2895, 1208)
WolfRaynet = (2931, 1221)
Carbon = (2930, 1222)
WhiteDwarf = (34294, 14289)
BlackHole = (60589, 25819)
GiantStar = (3122, 1301)
#Planets
WaterGiant = (1824, 760)
HeGiant = (2095, 986)
IcyBody = (1246, 535)
BODIES = { 
# Stars
           "O" : (6135, 2556),
           "B" : (3012, 1255),
           "A" : (2949, 1226),
           "F" : (2932, 1222),
           "G" : (2919, 1216),
           "K" : (2916, 1216),
           "M" : (2903, 1208),
           "L" : (2889, 1204),
           "T" : T_TTauri,
           "Y" : (2881, 1200),
           "TTS" : T_TTauri,
           "AeBe" : (3077, 1282),
           "W" : WolfRaynet,
           "WN" : WolfRaynet,
           "WNC" : WolfRaynet,
           "WC" : WolfRaynet,
           "WO" : WolfRaynet,
           "CS" : Carbon,
           "C" : Carbon,
           "CN" : Carbon,
           "CJ" : Carbon,
           "CH" : Carbon,
           "CHd" : Carbon,
# I don't know about MS and S but I'm guessing similar to carbon so
# thats what I'm going with
           "MS" : Carbon,
           "S" : Carbon,
           "D" : WhiteDwarf,
           "DA" : WhiteDwarf,
           "DAB" : WhiteDwarf,
           "DAO" : WhiteDwarf,
           "DAZ" : WhiteDwarf,
           "DAV" : WhiteDwarf,
           "DB" : WhiteDwarf,
           "DBZ" : WhiteDwarf,
           "DBV" : WhiteDwarf,
           "DO" : WhiteDwarf,
           "DOV" : WhiteDwarf,
           "DQ" : WhiteDwarf,
           "DC" : WhiteDwarf,
           "DCV" : WhiteDwarf,
           "DX" : WhiteDwarf,
           "N" : (54782, 22814),
           "H" : BlackHole,
           "SupermassiveBlackHole" : BlackHole,
           "A_BlueWhiteSuperGiant" : GiantStar,
           "F_WhiteSuperGiant" : GiantStar,
           "M_RedSuperGiant" : GiantStar,
           "M_RedGiant" : GiantStar,
           "K_OrangeGiant" : GiantStar,
# Planets
           "Metal rich body" : (65045, 27102),
           "High metal content body" : (34310, 13866),
           "Terraformable High metal content body" : (412249, 171770),
           "Rocky body" : (928, 500),
           "Terraformable Rocky body" : (181104, 75460),
           "Icy body" : IcyBody,
           "Rocky ice body" : IcyBody,
           "Earthlike body" : (627885, 261619),
           "Water world" : (301410, 125587),
           "Terraformable Water world" : (694971, 289587),
           "Ammonia world" : (320203, 133418),
           "Water giant" : WaterGiant,
           "Water giant with life" : WaterGiant,
           "Gas giant with water based life" : (2314, 964),
           "Gas giant with ammonia based life" : (1721, 717),
           "Sudarsky class I class giant" : (7013, 2922),
           "Sudarsky class II class giant" : (53663, 22360),
           "Sudarsky class III class giant" : (2693, 1122),
           "Sudarsky class IV class giant" : (2799, 1166),
           "Sudarsky class V class giant" : (2761, 1150),
           "Helium gas giant" : HeGiant,
           "Helium rich gas giant" : HeGiant
}

class ExploreBank(object):
   
   def __init__(self, readLater=False):
      self.honkValue = 500

      self.currentSystemName = ""
      self.currentSystemAddress = ""

      self.hardBankName = os.path.join(os.path.dirname(__file__), "ExploreBank.json")
      self.exploreBank = {}
      self.notif_string = ""
      if not readLater:
         self.readHardBank()

      self.eventLogName = os.path.join(os.path.dirname(__file__), "EventLog.txt")
      self.logging = False

   def willLog(self, logItems):
      self.logging = logItems
      
   def log(self, item):
      if self.logging:
         try:
            with open(self.eventLogName, "a") as logFile:
               line = str(item)
               line += "\n"
               logFile.write(line)
         except IOError:
            pass

   def readHardBank(self):
      try:
         with open(self.hardBankName, "r") as hardBank:
            self.exploreBank = json.load(hardBank)
            self.notif_string = "Read saved bank."
      except IOError:
         self.notif_string = "No saved bank, starting over."

   def writeHardBank(self):
      try:
         with open(self.hardBankName, "w") as hardBank:
            json.dump(self.exploreBank, hardBank)
            self.notif_string = "Saved Bank"
      except IOError:
         self.notif_string = "Could not save bank."

   def clearBank(self):
      self.exploreBank = {}
#Go ahead and write the clear out
      self.writeHardBank()

   def getTotalValue(self):
      return sum(self.exploreBank.values())

   def setLocation(self, event):
      ''' This event MUST have the 'StarSystem' and 'SystemAddress' keys present '''
      self.currentSystemName = event['StarSystem']
      self.currentSystemAddress = event['SystemAddress']
      self.notif_string = "New system, {}, entered.".format(self.currentSystemName)
      self.log(self.notif_string)
      return True

   def honk(self, event):
      ''' This event MUST have the 'SystemAddress' and 'Bodies' keys present '''
      self.log(event)
      if event['SystemAddress'] == self.currentSystemAddress:
         systemValue = self.exploreBank.get(self.currentSystemName, 0)
         systemValue += event['Bodies'] * self.honkValue
         self.exploreBank[self.currentSystemName] = systemValue
         self.notif_string = "Discovery scan in {}".format(self.currentSystemName)
         self.log(self.notif_string)
         return True
      else:
         self.notif_string = "This scan is not in our current system, no value added."
         self.log(self.notif_string)
         return False

   def sellData(self, event):
      ''' This event MUST have the 'Systems', and 'BaseValue' keys present '''
      self.log(event)
      output = []
      ourValue = 0
      for system in event['Systems']:
         if system in self.exploreBank:
            ourValue += self.exploreBank[system]
            del self.exploreBank[system]
         else:
            output.append('System "{}" not in bank'.format(system))

      percentage = (float(ourValue)/event['BaseValue']) * 100
      output.append('Banked value is {:.2f}% of reported base value.'.format(percentage))
      self.notif_string = "\n".join(output)
      self.log(self.notif_string)

   def scanBody(self, event):
      ''' This event MUST have the 'ScanType' and 'BodyName' keys present and at least one of 
          'StarType' or 'PlanetClass' defined. 'TerraformState' will also be checked '''
      self.log(event)
      bodyType = ""
      if 'StarType' in event:
         bodyType = event['StarType']
      elif 'PlanetClass' in event:
         bodyType = event['PlanetClass']
      else:
         self.notif_string = 'Body "{}" unidentifiable'.format(event['BodyName'])
         self.log(self.notif_string)
         return False

      terraformVal = "Terraformable"
      if ('TerraformState' in event) and (event['TerraformState'] == terraformVal):
         bodyType = terraformVal + " " + bodyType

      scanTypeIndex = BASIC_INDEX
      if event['ScanType'] == "Detailed":
         scanTypeIndex = DETAILED_INDEX

      # Check BodyName again currentSystemName?

      try:
         systemValue = self.exploreBank.get(self.currentSystemName, 0)
         # We remove the value that probably added during the honk, that seems to be the most likely scenario
         systemValue += (BODIES[bodyType][scanTypeIndex] - self.honkValue)
         self.exploreBank[self.currentSystemName] = systemValue
         self.notif_string = 'Added {} to bank for "{}"'.format(BODIES[bodyType][scanTypeIndex], event['BodyName'])
         self.log(self.notif_string)
         return True
      except KeyError:
         self.notif_string = 'No value for "{}"'.format(bodyType)
         self.log(self.notif_string)
         return False

   def surfaceScan(self, event):
      ''' This event MUST have ***** '''
      self.log(event)
      return True

