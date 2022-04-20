import csv

inputFilename = "PickPlaceKV4_Bottom.csv"
outputFilename = "PickPlaceOutput.gcode"

feederRotationOffset = -180.0 #forward or backward rotation depending on feeder location
feederMMPerComponent = 10.00 #requires additional 0.05 every 15 to normalize rotation
fAxisMMPerDegree = 200.0/360.0 #200MM movement is 360 degree rotation
fAxisInvertRotation = 1.0 #Multiplies by input rotation to flip direction

xyFastMove = 15000
zFastMove = 12000
zSlowMove = 3000
feederFastMove = 3000
nozzleFastMove = 12000
nozzleSlowMove = 3000

xyTravelZAxisHeight = 98.0 # Height for traveling with xy moves

feederXPosition = 480.6
feederYPosition = 763.6
feederZPosition = 87.0
feederSlowDownOffset = 2.0 #offset from z position where movement is slowed down
feederForwardPark = 80.0 # Park in front of feeder prior to picking up

#VERTICAL
#pcbXPosition = 258.40 - 21.5 - 0.55
#pcbYPosition = 554.90 - 2.5 - 0.225
#HORIZONTAL
pcbXPosition = 397.4 + 21.5 - 0.55
pcbYPosition = 554.90 - 2.5 - 0.225

pcbZPosition = 52.0
pcbSlowDownOffset = 6.0 # Offset from z position where movement is slowed down

def S(value):
    return str(round(value, 3))

def GetAcceleration():
    output = "M201 X2500 Y1500 Z1000\n"
    output += "M204 P3000 T3000\n"
    return output

def GetTrammingLine():
    output =  "G0 Y415 F" + S(xyFastMove) + "\n"
    output += "G0 Y405 F" + S(xyFastMove / 30.0) + "\n"
    output += "G0 Y980 F" + S(xyFastMove) + "\n"
    output += "G28 Y\n"
    return output

def GetHomingLine():
    return "G28 XYZ\n"

def GetAirOnLine():
    return "M42 P36 S255\nM42 P24 S255\nM400\n" # Vacuum on, valve open, pause
    
def GetAirOffLine():
    return "M400\nM42 P24 S0\nM42 P36 S0\nG4 P500\n" # Vacuum off, valve closed, pause

def GetComponentLine(xPosition, yPosition, rotation):
    output = ""

    feederDistance = feederMMPerComponent

    output += "T1\n" # Switch to feeder spin
    output += "G92 E0\n" # Set relative e position

    output += "G0 X" + S(feederXPosition - feederForwardPark / 2.0) + " Y" + S(feederYPosition - feederForwardPark) + " Z" + S(xyTravelZAxisHeight) + " E" + S(feederDistance) + " F" + S(xyFastMove) + "\n" # Move to Feeder offset XY
    output += "G0 X" + S(feederXPosition) + " Y" + S(feederYPosition) + " F" + S(xyFastMove) + "\n" # Move to Feeder XY

    output += "G0 Z" + S(feederZPosition + feederSlowDownOffset) + " F" + S(nozzleFastMove) + "\n" # Nozzle drop fast move
    
    output += "M400\n" # Wait until finished then continue
    output += "G0 Z" + S(feederZPosition) + " F" + S(nozzleSlowMove) + "\n" # Nozzle drop finishing move slow
    output += GetAirOnLine()
    
    output += "G0 Z" + S(xyTravelZAxisHeight) + " F" + S(zFastMove) + "\n" # Move z up for travel
    output += "G0 X" + S(feederXPosition - feederForwardPark / 2.0) + " Y" + S(feederYPosition - feederForwardPark) + " Z" + S(xyTravelZAxisHeight) + " F" + S(xyFastMove) + "\n" # Move to Feeder offset XY

    output += "M400\n" # Wait until finished then continue
    output += "T0\n" # Switch to nozzle spin
    output += "G92 E0\n" # Set relative e position
    output += "G0 X" + S(pcbXPosition + xPosition) + " Y" + S(pcbYPosition + yPosition) + " Z" + S(pcbZPosition + pcbSlowDownOffset) + " E" + S(fAxisMMPerDegree * (rotation + feederRotationOffset) * fAxisInvertRotation) + " F" + S(xyFastMove) + "\n" # Move to PCB coordinate
   
    output += "G0 Z" + S(pcbZPosition) + " F" + S(zSlowMove) + "\n" # Z Axis slow move to drop component
    output += GetAirOffLine()

    output += "G0 Z" + S(pcbZPosition + pcbSlowDownOffset) + " F" + S(zSlowMove) + "\n" # Move to clearance height for Z move
 
    return output

with open(inputFilename, 'r') as file:
    writer = open(outputFilename, "w")
    reader = csv.reader(file)

    print("Parsing CSV file...")

    #start
    writer.write(GetAcceleration())
    writer.write(GetHomingLine())
    writer.write(GetTrammingLine())

    #loop here
    for row in reader:
        if row[0] != "Designator":
            xIn = float(row[1])
            yIn = float(row[2])
            rIn = float(row[4])
            writer.write(GetComponentLine(xIn, yIn, rIn))

    #end loop
    writer.write(GetHomingLine())
    writer.close()

    num_lines = sum(1 for line in open(outputFilename))

    print("Wrote " + str(num_lines) + " lines to " + outputFilename)

    

    



