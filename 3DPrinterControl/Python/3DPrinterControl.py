from Printer import Printer

def run_points(printer,points_list):
    """Runs the given **printer** through the list of points **points_list**.

    printer: 3D printer defined as object **Printer**.
    points_list: List of points to traverse through. Each point defined as [x,y,z].
    """

    for point in points_list:
        printer.moveTo(point[0],point[1],point[2])

def get_scan_points_area(tArea,height,width):
    """Creates a list of [x,y,z] points with points centered in rectangles with area close to **tArea**.

        tArea: Desired area of each centered rectangle.
        height: Maximum height of scanning area.
        width: Maximum width of scanning area.
        """

    Hb_1st = sqrt(float(tArea))
    N_H = int(H/Hb_1st)
    Hb = float(H)/N_H

    Wb_1st = tArea/Hb
    N_W = int(W/Wb_1st)
    Wb = float(W)/N_W

    H_mid = Hb/2.0
    W_mid = Wb/2.0

    points_list = []
    
    for i_x in range(N_W):
        for i_z in range(N_H):
            points_list.append((i_x*Wb+W_mid,0.0,i_z*Hb+H_mid))

    print("Area: {} mm\n".format(Hb*Wb))
    print("Points: {} \n".format(N_W*N_H))
       
    return points_list
    

def get_scan_points_count(tCount,height,width):
    """Creates a list of [x,y,z] points with points equally spaced across given height and width.
        Total count of points will be close to tCount.

        tCount: Desired total count of points.
        height: Maximum height of scanning area.
        width: Maximum width of scanning area.
        """

    split_count = int(sqrt(tCount))
    
    N_H = split_count
    Hb = float(H)/N_H
    
    N_W = split_count
    Wb = float(W)/N_W

    H_mid = Hb/2.0
    W_mid = Wb/2.0

    points_list = []

    for i_x in range(N_W):
        for i_z in range(N_H):
            points_list.append((i_x*Wb+W_mid,0.0,i_z*Hb+H_mid))

    print("Area: {} mm\n".format(Hb*Wb))
    print("Points: {} \n".format(N_W*N_H))
       
    return points_list

if __name__ =="__main__":
    """The following example shows how a provided csv file of test points can be used to traverse a printer.
    
    """

    points_filename = "../test_points.csv"

    Ender3 = Printer(printerName="USB-SERIAL CH340") # This is the name that the computer sees the printer as.

    with open(points_filename) as points_file:
        # Required file format:
        # x(mm),y(mm),z(mm) {Header is not read. Can be anything, but is required.)
        # 0.0,0.0,0.0

        points_lines = points_file.readlines()

    points_lines = [line.strip().split(',') for line in points_lines]
    points = [(float(line[0]),float(line[1]),float(line[2]))for line in points_lines]

    run_points(Ender3,points)
