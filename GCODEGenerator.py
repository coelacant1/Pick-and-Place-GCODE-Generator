import csv

inputFilename = "PickPlaceKV4_Top.csv"
outputFilename = "PickPlaceOutput.gcode"

feederRotationOffset = -180.0 #forward or backward rotation depending on feeder location
feederMMPerComponent = -13.33 #requires additional 0.05 every 15 to normalize rotation
fAxisMMPerDegree = 200.0/360.0 #200MM movement is 360 degree rotation
fAxisInvertRotation = 1.0 #Multiplies by input rotation to flip direction

xyFastMove = 15000
zFastMove = 12000
zSlowMove = 3000
feederFastMove = 3000
nozzleFastMove = 12000
nozzleSlowMove = 3000

xyTravelZAxisHeight = 98.0 # Height for traveling with xy moves

feederXPosition = 478.0
feederYPosition = 761.9
feederZPosition = 87.0
feederSlowDownOffset = 2.0 #offset from z position where movement is slowed down
feederSynchronization = -40.0 + (13.33 * 3.0) # for syncrhonizing offset every 5 components
feederSyncCounter = 0 # Current Sync Counter
feederSyncMax = 4 # Once counter is at max add synchronization to mm per component
feederForwardPark = 80.0 # Park in front of feeder prior to picking up

pcbXPosition = 258.10 - 21.5
pcbYPosition = 554.50 - 2.5
pcbZPosition = 52.0
pcbSlowDownOffset = 6.0 # Offset from z position where movement is slowed down

def S(value):
    return str(round(value, 3))

def GetAcceleration():
    output = "M201 X2500 Y2500 Z2500\n"
    output += "M204 P1000 T1000\n"
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
    return "M400\nM42 P36 S255\nM42 P24 S255\nG4 P250\n" # Vacuum on, valve open, pause
    
def GetAirOffLine():
    return "M400\nM42 P36 S0\nM42 P24 S0\nG4 P250\n" # Vacuum off, valve closed, pause

def GetComponentLine(xPosition, yPosition, rotation):
    global feederSyncCounter
    output = ""

    feederDistance = feederMMPerComponent

    if feederSyncCounter < feederSyncMax:
        feederSyncCounter += 1
    else:
        feederSyncCounter = 0
        feederDistance += feederSynchronization # Add syncrhonization distance to feeder if out of sync


    output += "M400\n" # Wait until finished then continue
    output += "T1\n" # Switch to feeder spin
    output += "G92 E0\n" # Set relative e position

    output += "G0 X" + S(feederXPosition - feederForwardPark / 2.0) + " Y" + S(feederYPosition - feederForwardPark) + " Z" + S(xyTravelZAxisHeight) + " E" + S(feederDistance) + " F" + S(xyFastMove) + "\n" # Move to Feeder offset XY
    output += "G0 X" + S(feederXPosition) + " Y" + S(feederYPosition) + " F" + S(xyFastMove) + "\n" # Move to Feeder XY

    output += "G0 Z" + S(feederZPosition + feederSlowDownOffset) + " F" + S(nozzleFastMove) + "\n" # Nozzle drop fast move
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

    output += "G0 Z" + S(pcbZPosition + pcbSlowDownOffset) + " F" + S(xyFastMove) + "\n" # Move to clearance height for Z move
 
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

    

    



