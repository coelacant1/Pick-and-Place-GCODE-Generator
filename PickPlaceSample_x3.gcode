G28 XYZ; Home all axes

T0; Switch to spin axis
G0 X478.0 Y761.90 F12000; Move to feeder

M400; Wait until finished then continue
;Nozzle pickup
G0 Z89.0 F12000; Drop nozzle
G0 Z87.0 F1500; Drop nozzle
M42 P36 S255; Turn on vacuum
G4 P250; Dwell for 500ms
M42 P24 S255; Open air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G92 E0; Set relative e position
G0 Z98.0 F12000; Pick up nozzle
G0 E50 F12000; Rotate part

M400; Wait until finished then continue
T1; Switch to feeder
G92 E0; Set relative e position
G0 E-13.33 F3000; Move feeder
; Every fifteen rotations, rotate 0.05 to compensate

G0 X378.0 Y580.40 F12000; Move to pcb
G0 Z55.0 F12000; Drop Nozzle
G0 Z52.0 F1500; Drop Nozzle

M400; Wait until finished then continue
M42 P36 S0; Turn off vacuum
G4 P250; Dwell for 500ms
M42 P24 S0; Close air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G0 Z98.0 F12000; Pick up nozzle

; LOOOOP 
T0; Switch to spin axis
G0 X478.0 Y761.90 F12000; Move to feeder

M400; Wait until finished then continue
;Nozzle pickup
G0 Z89.0 F12000; Drop nozzle
G0 Z87.0 F1500; Drop nozzle
M42 P36 S255; Turn on vacuum
G4 P250; Dwell for 500ms
M42 P24 S255; Open air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G92 E0; Set relative e position
G0 Z98.0 F12000; Pick up nozzle
G0 E50 F12000; Rotate part

M400; Wait until finished then continue
T1; Switch to feeder
G92 E0; Set relative e position
G0 E-13.33 F3000; Move feeder
; Every fifteen rotations, rotate 0.05 to compensate

G0 X373.0 Y580.40 F12000; Move to pcb
G0 Z55.0 F12000; Drop Nozzle
G0 Z52.0 F1500; Drop Nozzle

M400; Wait until finished then continue
M42 P36 S0; Turn off vacuum
G4 P250; Dwell for 500ms
M42 P24 S0; Close air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G0 Z98.0 F12000; Pick up nozzle

; LOOOOP 
T0; Switch to spin axis
G0 X478.0 Y761.90 F12000; Move to feeder

M400; Wait until finished then continue
;Nozzle pickup
G0 Z89.0 F12000; Drop nozzle
G0 Z87.0 F1500; Drop nozzle
M42 P36 S255; Turn on vacuum
G4 P250; Dwell for 500ms
M42 P24 S255; Open air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G92 E0; Set relative e position
G0 Z98.0 F12000; Pick up nozzle
G0 E50 F12000; Rotate part

M400; Wait until finished then continue
T1; Switch to feeder
G92 E0; Set relative e position
G0 E-13.33 F3000; Move feeder
; Every fifteen rotations, rotate 0.05 to compensate

G0 X368.0 Y580.40 F12000; Move to pcb
G0 Z55.0 F12000; Drop Nozzle
G0 Z52.0 F1500; Drop Nozzle

M400; Wait until finished then continue
M42 P36 S0; Turn off vacuum
G4 P250; Dwell for 500ms
M42 P24 S0; Close air valve
G4 P250; Dwell for 500ms

M400; Wait until finished then continue
G0 Z98.0 F12000; Pick up nozzle

G28 XYZ;