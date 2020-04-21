#from scipy.interpolate import spline
import os
import numpy as np

def lin_interp(indeps,deps,spec_indep):
    for ind,indep in enumerate(indeps):
        if spec_indep > indep and spec_indep < indeps[ind+1]:
            low_indep = indep
            high_indep = indeps[ind+1]
            return deps[ind] + (spec_indep-indep)*((deps[ind+1]-deps[ind])/(high_indep-low_indep))

class CalibPoint:

    def __init__(self,yaw,pitch,cp_yaw,cp_pitch,cp_static,cp_total):
        self.yaw = yaw
        self.pitch = pitch
        self.cp_yaw = cp_yaw
        self.cp_pitch = cp_pitch
        self.cp_static = cp_static
        self.cp_total = cp_total

class CalibData:

    def __init__(self,calib_filename):

        with open(calib_filename) as calib_file:
            cond_calib_lines = calib_file.readlines()
            cond_calib_lines.pop(0)  # Remove header line.
            cond_calib_lines = [line.split(',') for line in cond_calib_lines]

            calib_points = [CalibPoint(float(line[1]), float(line[0]), float(line[2]), float(line[3]), float(line[4]), \
                                       float(line[5])) for line in cond_calib_lines]

        yaws = [point.yaw for point in calib_points]
        pitches = [point.pitch for point in calib_points]

        yaws_u = list(set(yaws))
        yaws_u.sort()
        pitches_u = list(set(pitches))
        pitches_u.sort()

        yaw_lines = {}
        for yaw in yaws_u:
            yaw_lines[yaw] = {}
            for pitch in pitches_u:
                for point in calib_points:
                    if point.yaw == yaw and point.pitch == pitch:
                        yaw_lines[yaw][pitch] = point
        self.yaw_lines = yaw_lines

        pitch_lines = {}
        for pitch in pitches_u:
            pitch_lines[pitch] = {}
            for yaw in yaws_u:
                for point in calib_points:
                    if point.pitch == pitch and point.yaw == yaw:
                        pitch_lines[pitch][yaw] = point
        self.pitch_lines = pitch_lines

class TestPoint:

    def __init__(self, x, z, V1, V2, V3, V4, V5, P_ref, rho, calib_data):
        self.calib_data = calib_data

        self.x = x
        self.z = z
        self.V1 = V1
        self.V2 = V2
        self.V3 = V3
        self.V4 = V4
        self.V5 = V5

        self.P1 = self.get_pressure_30psi_sensor(V1) + P_ref
        self.P2 = self.get_pressure_30psi_sensor(V2) + P_ref
        self.P3 = self.get_pressure_30psi_sensor(V3) + P_ref
        self.P4 = self.get_pressure_30psi_sensor(V4) + P_ref
        self.P5 = self.get_pressure_30psi_sensor(V5) + P_ref
        self.Pavg = (self.P2 + self.P3 + self.P4 + self.P5) / 4.0
        self.Pref = Pref
        self.rho = rho

        self.cp_yaw = (self.P2 - self.P3) / (self.P1 - self.Pavg)
        self.cp_pitch = (self.P4 - self.P5) / (self.P1 - self.Pavg)
        try:
            angles = self.get_angles()
            self.yaw = angles[0]
            self.pitch = angles[1]
            self.cp_static = self.get_cp_static()
            self.cp_total = self.get_cp_total()

            self.Ptotal = self.get_Ptotal()
            self.Pstatic = self.get_Pstatic()

            self.vel = self.get_velocity()

        except:
            print("BAD POINT")
            self.yaw = 0.0
            self.pitch = 0.0
            self.cp_static = 0.0
            self.cp_total = 0.0
            self.vel = 0.0
            self.Pstatic = 0.0
            self.Ptotal = 0.0

    def get_pressure_30psi_sensor(self,voltage):
        return voltage*(30.0/5.0)

    def get_angles(self):
        yaw_lines = self.calib_data.yaw_lines
        pitch_lines = self.calib_data.pitch_lines
        new_lines = []
        for yaw in yaw_lines.keys():
            curr_cp_pitches = [yaw_lines[yaw][pitch].cp_pitch for pitch in yaw_lines[yaw].keys()]
            curr_cp_yaws = [yaw_lines[yaw][pitch].cp_yaw for pitch in yaw_lines[yaw].keys()]
            new_lines.append([self.cp_pitch, lin_interp(curr_cp_pitches, curr_cp_yaws, self.cp_pitch)])
        curr_cp_yaws = [line[1] for line in new_lines]
        yaw = lin_interp(curr_cp_yaws, list(yaw_lines.keys()), self.cp_yaw)

        new_lines = []
        for pitch in pitch_lines.keys():
            curr_cp_pitches = [pitch_lines[pitch][yaw].cp_pitch for yaw in pitch_lines[pitch].keys()]
            curr_cp_yaws = [pitch_lines[pitch][yaw].cp_yaw for yaw in pitch_lines[pitch].keys()]
            new_lines.append([self.cp_yaw, lin_interp(curr_cp_yaws, curr_cp_pitches, self.cp_yaw)])
        curr_cp_pitches = [line[1] for line in new_lines]
        pitch = lin_interp(curr_cp_pitches, list(pitch_lines.keys()), self.cp_pitch)

        return [yaw, pitch]

    def get_cp_static(self):
        yaw_lines = self.calib_data.yaw_lines
        for ind, yaw in enumerate(list(yaw_lines.keys())):
            if yaw < self.yaw and list(yaw_lines.keys())[ind + 1] > self.yaw:
                pitches_low = list(yaw_lines[yaw].keys())
                cp_statics_low = [yaw_lines[yaw][pitch].cp_static for pitch in yaw_lines[yaw].keys()]
                lower_int = lin_interp(pitches_low, cp_statics_low, self.pitch)

                pitches_high = list(yaw_lines[list(yaw_lines.keys())[ind + 1]].keys())
                cp_statics_high = [yaw_lines[list(yaw_lines.keys())[ind + 1]][pitch].cp_static for pitch in
                                   list(yaw_lines[list(yaw_lines.keys())[ind + 1]].keys())]
                higher_int = lin_interp(pitches_high, cp_statics_high, self.pitch)

                cp_static = (lower_int + higher_int) / 2.0
                return cp_static

    def get_cp_total(self):
        yaw_lines = self.calib_data.yaw_lines
        for ind, yaw in enumerate(list(yaw_lines.keys())):
            if yaw < self.yaw and list(yaw_lines.keys())[ind + 1] > self.yaw:
                pitches_low = list(yaw_lines[yaw].keys())
                cp_totals_low = [yaw_lines[yaw][pitch].cp_total for pitch in yaw_lines[yaw].keys()]
                lower_int = lin_interp(pitches_low, cp_totals_low, self.pitch)

                pitches_high = list(yaw_lines[list(yaw_lines.keys())[ind + 1]].keys())
                cp_totals_high = [yaw_lines[list(yaw_lines.keys())[ind + 1]][pitch].cp_total for pitch in
                                  list(yaw_lines[list(yaw_lines.keys())[ind + 1]].keys())]
                higher_int = lin_interp(pitches_high, cp_totals_high, self.pitch)

                cp_total = (lower_int + higher_int) / 2.0
                return cp_total

    def get_Ptotal(self):
        return self.Pref + (self.P1 - self.Pref) - self.cp_total * ((self.P1 - self.Pref) - (self.Pavg - self.Pref))

    def get_Pstatic(self):
        return self.Pref + (self.Pavg - self.Pref) - self.cp_static * ((self.P1 - self.Pref) - (self.Pavg - self.Pref))

    def get_velocity(self):
        return (2 / self.rho) * (self.Ptotal - self.Pstatic) ** 0.5

class TestData:

    def __init__(self,results_filename,calib_data,Pref,density):

        with open(results_filename) as results_file:
            results_lines = results_file.readlines()
            results_lines = [line.strip().replace('(', '').replace(')', '').split(';') for line in results_lines]
        self.results_filename = results_filename
        self.test_points = [
            TestPoint(float(line[0].split(',')[0]), float(line[0].split(',')[1]), float(line[1].split(',')[0]), \
                      float(line[1].split(',')[1]), float(line[1].split(',')[2]), float(line[1].split(',')[3]), \
                      float(line[1].split(',')[4]), Pref, density, calib_data) for line in results_lines]

    def write(self):
        out_filename = os.path.splitext(self.results_filename)[0] + "_Results.csv"
        with open(out_filename, 'w') as results_out:
            results_out.write("X(mm),Z(mm),Vx(mm/s),Vy(mm/s),Vz(mm/s),P(Pa),P0(Pa),T(K)\n")

            for point in self.test_points:

                Vx = np.sin(point.yaw * (np.pi / 180.0)) * np.cos(point.pitch * (np.pi / 180.0)) * point.vel
                Vy = np.cos(point.yaw * (np.pi / 180.0)) * np.cos(point.pitch * (np.pi / 180.0)) * point.vel
                Vz = np.sin(point.pitch * (np.pi / 180.0)) * point.vel

                if np.iscomplex(Vx):
                    Vx = 0.0
                if np.iscomplex(Vy):
                    Vy = 0.0
                if np.iscomplex(Vz):
                    Vz = 0.0

                results_out.write(
                    "{},{},{},{},{},{},{},{}\n".format(point.x, point.z, Vx * 304.8, Vy * 304.8, Vz * 304.8,
                                                       point.Pstatic * 6894.76, point.Ptotal * 6894.76, 293.0))


if __name__ =="__main__":

    calibration_filename = r"C:\Users\jjbet\Desktop\CalibrationCurves\Condensed_FCalibData.csv"
    results_filename = r"E:\Results\CenterFlap_30Deg_TEUP.csv"

    sample_calibration = CalibData(calibration_filename)

    Pref = 14.5  # psia
    density = 0.002297145 # slugs/ft^3
    sample_test = TestData(results_filename,sample_calibration,Pref,density)
    sample_test.write()







