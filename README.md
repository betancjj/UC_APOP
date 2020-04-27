# University of Cincinnati APOP 2020

This project was done as part of the United States Air Force Research Laboratory's Aerospace Propulsion Outreach Program (APOP).
It was performed by the following University of Cincinnati students:

Jorge Betancourt (betancjj@mail.uc.edu)

Chris Feldman (feldmacc@mail.uc.edu)

Alec Gaetano (gaetanac@mail.uc.edu)

Logan Neiheisel (neiheila@mail.uc.edu)

under the direction of Mark Turner (turnermr@ucmail.uc.edu).

This code consists of 2 sections:
- 3D Printer Traversing
  - This section of code allows for the control of a generic 3D printer with serial control. This code is provided in either LabVIEW or Python programming. The LabView code is built to traverse the 3D printer through a given set of points. The Python code does the same, but also provides multiple functions for finer intuitive control of the 3D printer.

- Five Hole Probe Calibration and Use
  - Five Hole Probe Calibration
    - Using an Arduino and LabVIEW, a motorized calibration rig can be controlled to collect calibration data of a 5-hole probe.
  - Test Result Processing
    - Given calibration data and test data, this code can calculate pitch/yaw angles, total/static pressures, and velocity for each given point.
