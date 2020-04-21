from serial import Serial
import serial.tools.list_ports
import sys
import time

class Printer(Serial):
    """Class that represents a 3D Printer using Serial connection. Can be used to intuitively control motion of printer.

        printerName: Provide serial name of printer. Required to locate printer.
        baudrate: Baud Rate of printer control board.
        xSpeed: Default speed of x-axis in mm/min. Can be set per-action also.
        ySpeed: Default speed of y-axis in mm/min. Can be set per-action also.
        zSpeed: Default speed of z-axis in mm/min. Can be set per-action also.
        bounds: Maximum limits of 3-axes in format: [xMax,yMax,zMax]
    """

    def __init__(self, printerName, baudrate=115200, xSpeed=6000, ySpeed=6000, zSpeed=200, bounds=None):
        
        if bounds is None:
            print("WARNING: NO BOUNDS SET FOR PRINTER\n")
            self.max_x = 1000000
            self.max_y = 1000000
            self.max_z = 1000000
        else:
            self.max_x = bounds[0]
            self.max_y = bounds[1]
            self.max_z = bounds[2]
        
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if printerName in port.description:
                self.p_port = port.device
                print("Printer found on port {}.\n".format(self.p_port))
                break
        else:
            print("Printer could not be found.")
            sys.exit()

        try:
            super(Printer, self).__init__(self.p_port, baudrate, timeout=3)
            time.sleep(3)
            print("PRINTER ECHO:\n\n\n")
            for line in self.readlines():
                print(line.decode('utf-8').replace("echo:",""))
        except:
            print("Serial connection could not be established.")
            sys.exit()
        
        self.home()
        
        self.x = 0
        self.y = 0
        self.z = 0

        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.zSpeed = zSpeed

    def write(self,string):
        """Encodes string then passes to Serial.write() super."""
        super(Printer, self).write(str.encode(string))

    # This function needs to be updated to intelligently wait for the end of the action.
    # Currently it only waits a set amount of time.
    def wait(self):
        """Function that sleeps program until printer has stopped moving."""
        time.sleep(0.5)
        # TODO: Update function to intelligently wait for command to finish.
    
    def home(self):
        """Function sends serial command for printer to move to home position."""
        print("Homing")
        self.write("G28 \r\n")
        self.wait()
    
    def moveX(self,dist,speed=None):
        """Move carriage in x-direction by amount *dist* at speed *speed*.

        dist: x-axis distance to move in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.

        """

        speed = self.xSpeed if speed is None else speed
        
        if self.x+dist > self.max_x:
            print("Cannot make move. End position is past maximum x position.")
            return
        
        try:
            dist = float(dist)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
        
        write_line = "G1 X{} F{} \r\n".format(dist,speed)
        
        self.write("G91 \r\n") #Set to relative motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        self.write("G90 \r\n") #Return to absolute motion.
        time.sleep(0.1)
        
        self.x = self.x + dist
        self.wait()
            
    def moveY(self,dist,speed=None):
        """Move carriage in y-direction by amount *dist* at speed *speed*.

        dist: y-axis distance to move in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.

        """

        speed = self.ySpeed if speed is None else speed
    
        if self.y+dist > self.max_y:
            print("Cannot make move. End position is past maximum y position.")
            return
    
        try:
            dist = float(dist)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
            
        write_line = "G1 Y{} F{} \r\n".format(dist,speed)
        
        self.write("G91 \r\n") #Set to relative motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        self.write("G90 \r\n") #Return to absolute motion.
        time.sleep(0.1)
        
        self.y = self.y + dist
        self.wait()
    
    def moveZ(self,dist,speed=None):
        """Move carriage in y-direction by amount *dist* at speed *speed*.

        dist: z-axis distance to move in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.

        """
        speed = self.zSpeed if speed is None else speed
    
        if self.z+dist > self.max_z:
            print("Cannot make move. End position is past maximum z position.")
            return
        
        try:
            dist = float(dist)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
            
        write_line = "G1 Z{} F{} \r\n".format(dist,speed)
        
        self.write("G91 \r\n") #Set to relative motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        self.write("G90 \r\n") #Return to absolute motion.
        time.sleep(0.1)
        
        self.z = self.z + dist
        self.wait()
    
    def moveToX(self,loc,speed=None):
        """Move carriage in x-direction to position **loc**.

        loc: x-axis location to move to in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.
        """

        speed = self.xSpeed if speed is None else speed
    
        if loc > self.max_x:
            print("Cannot make move. End position is past maximum x position.")
            return
        
        try:
            loc = float(loc)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
        
        write_line = "G1 X{} F{} \r\n".format(loc,speed)
        
        self.write("G90 \r\n") #Set to absolute motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        
        self.x = loc
        self.wait()
    
    def moveToY(self,loc,speed=None):
        """Move carriage in y-direction to position **loc**.

        loc: y-axis location to move to in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.
        """

        speed = self.ySpeed if speed is None else speed
    
        if loc > self.max_y:
            print("Cannot make move. End position is past maximum y position.")
            return
    
        try:
            loc = float(loc)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
            
        write_line = "G1 Y{} F{} \r\n".format(loc,speed)
        
        self.write("G90 \r\n") #Set to absolute motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        
        self.y = loc
        self.wait()
        
        
    
    def moveToZ(self,loc,speed=None):
        """Move carriage in z-direction to position **loc**.

        loc: z-axis location to move to in mm.
        speed: speed of movement in mm. If none given, defaults to default speed given at object initialization.
        """

        speed = self.zSpeed if speed is None else speed
    
        if loc > self.max_z:
            print("Cannot make move. End position is past maximum z position.")
            return
    
        try:
            loc = float(loc)
            speed = float(speed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
            
        write_line = "G1 Z{} F{} \r\n".format(loc,speed)
        
        self.write("G90 \r\n") #Set to absolute motion.
        time.sleep(0.1)
        self.write(write_line)
        time.sleep(0.1)
        
        self.z = loc
        self.wait()
    
    def moveTo(self,x=None,y=None,z=None, xSpeed=None, ySpeed=None, zSpeed=None):
        """Move carriage to position **x**,**y**,**z**.

        x: x-axis distance to move by in mm.
        y: y-axis distance to move by in mm.
        z: z-axis distance to move by in mm.
        xSpeed: speed of x-axis movement in mm. If none given, defaults to default x-speed given at object initialization.
        ySpeed: speed of y-axis movement in mm. If none given, defaults to default y-speed given at object initialization.
        zSpeed: speed of z-axis movement in mm. If none given, defaults to default z-speed given at object initialization.
        """
        
        if x > self.max_x:
            print("Cannot make move. End position is past maximum x position.")
            return
        
        if y > self.max_y:
            print("Cannot make move. End position is past maximum y position.")
            return
            
        if z > self.max_z:
            print("Cannot make move. End position is past maximum z position.")
            return

        xSpeed = self.xSpeed if xSpeed is None else xSpeed
        ySpeed = self.ySpeed if ySpeed is None else ySpeed
        zSpeed = self.zSpeed if zSpeed is None else zSpeed
        
    
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if z is None:
            z = self.z
        
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            xSpeed = float(xSpeed)
            ySpeed = float(ySpeed)
            zSpeed = float(zSpeed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
        
        
        write_line_x = "G1 X{} F{} \r\n".format(x,xSpeed)
        write_line_y = "G1 Y{} F{} \r\n".format(y,ySpeed)
        write_line_z = "G1 Z{} F{} \r\n".format(z,zSpeed)
        
        self.write("G90 \r\n") #Set to absolute motion.
        time.sleep(0.1)
        self.write(write_line_z)
        time.sleep(0.1)
        self.write(write_line_y)
        time.sleep(0.1)
        self.write(write_line_x)
        time.sleep(0.1)
        
        self.x = x
        self.y = y
        self.z = z
        self.wait()
    
    def move(self,x=0,y=0,z=0, xSpeed=None, ySpeed=None, zSpeed=None):
        """Move carriage to position **x**,**y**,**z**.

        x: x-axis distance to move by in mm.
        y: y-axis distance to move by in mm.
        z: z-axis distance to move by in mm.
        xSpeed: speed of x-axis movement in mm. If none given, defaults to default x-speed given at object initialization.
        ySpeed: speed of y-axis movement in mm. If none given, defaults to default y-speed given at object initialization.
        zSpeed: speed of z-axis movement in mm. If none given, defaults to default z-speed given at object initialization.
        """
    
        if self.x+x > self.max_x:
            print("Cannot make move. End position is past maximum x position.")
            return
        
        if self.y+y > self.max_y:
            print("Cannot make move. End position is past maximum y position.")
            return
            
        if self.z+z > self.max_z:
            print("Cannot make move. End position is past maximum z position.")
            return

        xSpeed = self.xSpeed if xSpeed is None else xSpeed
        ySpeed = self.ySpeed if ySpeed is None else ySpeed
        zSpeed = self.zSpeed if zSpeed is None else zSpeed
        
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            xSpeed = float(xSpeed)
            ySpeed = float(ySpeed)
            zSpeed = float(zSpeed)
        except ValueError:
            print("Invalid value(s) for movement")
            return
            
        write_line_x = "G1 X{} F{} \r\n".format(x,xSpeed)
        write_line_y = "G1 Y{} F{} \r\n".format(y,ySpeed)
        write_line_z = "G1 Z{} F{} \r\n".format(z,zSpeed)
        
        self.write("G91 \r\n") #Set to relative motion.
        time.sleep(0.1)
        self.write(write_line_x)
        time.sleep(0.1)
        self.write(write_line_y)
        time.sleep(0.1)
        self.write(write_line_z)
        time.sleep(0.1)
        self.write("G90 \r\n") #Return to absolute motion.
        time.sleep(0.1)
        
        self.x = self.x + x
        self.y = self.y + y
        self.z = self.z + z
        self.wait()

    def location(self):
        """Print current location of carriage."""

        print("x: {} y: {} z: {}".format(self.x,self.y,self.z))
