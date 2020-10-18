# It is important to note that this script will include your PTH components as well as your SMT components.
# You will need to later select which parts are skipped or not.
# Copyright 2018 Michael Moskie
# mod 2020 to Python3
# modded from altium to circuit studio output
import sys
from decimal import Decimal
class component:
    ##just a structure to represent a physical component
    def __init__(self, line):
        #Designator,Footprint,Mid X,Mid Y,Ref X,RefY,Pad X,PadY,Layer,Rotation,Comment
        self.Designator = line.split(',')[0]
        self.Footprint = line.split(',')[1].replace("\"", "")
        self.X = line.split(',')[2].replace("\"", "").replace("mm", "")
        self.Y = line.split(',')[3].replace("\"", "").replace("mm", "")
        self.Layer = line.split(',')[8]
        self.Rotation = line.split(',')[9]
        self.Comment = line.split(',')[10]

class NeoDenConverter:
    def MakeComponentList(self):
        counter = 0
        for line in self.AltiumOutputFile:
            if(counter < 2):
                #throw away the header.
                pass
            else:
                self.components.append(component(line))
            counter += 1
            #print(counter,line)

    def getDistancesFromFirstChip(self):
        FirstChipX = 0
        FirstChipY = 0
        counter = 0
        for comp in self.components:
                if(counter == 0):
                    #this is the first component
                    FirstChipX = comp.X
                    FirstChipY = comp.Y
                    comp.X = 0
                    comp.Y = 0
                else:
                    comp.X = float(comp.X) - float(FirstChipX)
                    comp.Y = float(comp.Y) - float(FirstChipY)
                counter += 1

    def ApplyMachinePositionsToComponents(self):
        for comp in self.components:
            comp.X += self.firstChipPhysicalX
            comp.Y += self.firstChipPhysicalY

    def createOutputFile(self):
        outputFile = open(self.AltiumOutputFile.name.replace(".csv", "-NEODEN.csv"), "w")
        outputFile.write("Designator,Footprint,Mid X,Mid Y,Layer,Rotation,Comment\n")
        outputFile.write(",,,,,,\n")
        for comp in self.components:
            outLine = str(comp.Designator).replace("\"","") + "," + str(comp.Footprint).replace("\"","") + "," + str(round(Decimal(comp.X),2))+"mm" + "," + str(round(Decimal(comp.Y),2))+"mm" + "," + "T," + str(comp.Rotation).replace("\"","") + "," + comp.Comment.replace("\"","")
            outputFile.write(outLine + "\n")

    def __init__(self, fileName):
        self.AltiumOutputFile = open(fileName, "r")
        self.components = list()
        self.MakeComponentList()
        self.getDistancesFromFirstChip();
        self.firstChipPhysicalX = float(input("Enter the machine X coordinate of component " + self.components[0].Designator + " : "))
        self.firstChipPhysicalY = float(input("Enter the machine Y coordinate of component " + self.components[0].Designator + " : "))
        self.ApplyMachinePositionsToComponents()
        self.createOutputFile()

if(sys.argv[1]):
    Converter = NeoDenConverter(sys.argv[1])