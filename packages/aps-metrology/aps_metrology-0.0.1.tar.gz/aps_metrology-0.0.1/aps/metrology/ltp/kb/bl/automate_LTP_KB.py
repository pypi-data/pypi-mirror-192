'''
@Time    	: 07 / 31 / 2022
@Author  	: Zhi Qiao
@Contact	: z.qiao1989@gmail.com
@File    	: automate_LTP_KB.py
@Software	: AutomateLTP
@Desc		: This script is used for automatically LTP data analysis
              It will automatically monitor the data folder and do the data processing
              The raw data is in mda format, to convert mda to readable ascii file, use the mda2ascii tool: 
              https://github.com/BCDA-APS/MDA_Utilities
              https://epics.anl.gov/bcda/mdautils/
              
              Since the mda2ascii tool is under /APSshare path, this data processing code will need to run on a APS computer. Or, install mda2ascii tool on the running computer as showed in https://epics.anl.gov/bcda/mdautils/
'''

import os
import sys
import numpy as np
import json
import glob
import csv
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import scipy.ndimage as snd
from scipy.optimize import curve_fit, minimize

from warnings import filterwarnings
filterwarnings("ignore")

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# Zhi Qiao's original code - DO NOT MODIFY

def check_LTP_status():
    """check if LTP instrument is running or not. This requires epics package and the accessible PV name to LTP

    Returns:
        status of LTP
    """
    from epics import PV
    LTP_status = PV('ltpu:scan1.SMSG')
    try:
        if LTP_status.get() == 'Scanning ...': return 'scanning'
        else:                                  return 'done'
    except:
        # if there's no accessible PV name to LTP instrument, ignore this
        return 'done'


def check_new_file(folder_path,
                   result_folder,
                   file_extension='*.mda',
                   force_process=False,
                   logger=None):
    """
        check if there's new data coming or not. And compare the data modification time and the LTP status, to see if it's ready to process or not
    Input:
        folder_path:    mda file's folder path
        result_folder:  the result folder path where mda file is processed.
        file_extension: mda or others
        force_process:  force to process the data or not
    Returns:
        mda_file: new mda file path
    """
    # get all mda file in this folder
    mda_file_list = glob.glob(os.path.join(folder_path, file_extension), recursive=False)
    subfolder_result = [ os.path.basename(f) for f in glob.glob(os.path.join(result_folder, '*')) ]

    mda_new_file = []
    for mda_file in mda_file_list:
        time_last_modified = os.path.getmtime(mda_file)
        file_name = os.path.basename(mda_file).split('.')[0]
        # uncomment this,if do not want to convert test measurement
        #if (file_name not in subfolder_result) and ('test' not in file_name):
        if force_process:
            mda_new_file.append(mda_file)
        else:
            if (file_name not in subfolder_result):
                if ((time.time() - time_last_modified) > 60):
                    mda_new_file.append(mda_file)
                else:
                    Flag_num = 0
                    for i in range(4):
                        if check_LTP_status() == 'done':
                            Flag_num += 1
                        time.sleep(1)
                    if (Flag_num > 3):
                        mda_new_file.append(mda_file)
            else:
                logger.print_message('skip...{}'.format(mda_file))
                continue

    return mda_new_file

from aps.metrology.ltp import MDA_DIRECTORY

def convert_mda(file_mda, logger):
    """convert mda to ascii files
    Args:
        file_mda ([file path]): file path of mda file
    """
    # use mda2ascii to convert the mda file to ascii file
    try:
        logger.print_warning('converting mda file: {}'.format(file_mda))
        if os.name == 'nt':      cmd = os.path.join(MDA_DIRECTORY, 'mda2ascii.exe') + ' {} -d {}'.format(file_mda, os.path.dirname(file_mda))
        elif os.name == 'posix': cmd = os.path.join(MDA_DIRECTORY, 'mda2ascii') + ' -d {} {} &> /dev/null'.format(os.path.dirname(file_mda), file_mda)
        else: cmd = os.path.join(MDA_DIRECTORY, 'mda2ascii') + ' {} -d {} &> /dev/null'.format(file_mda, os.path.dirname(file_mda))

        os.system(cmd)

        logger.print_warning('converting mda file: {} done'.format(file_mda))
    except Exception as e:
        logger.print_error('mda2ascii convert failed: {}'.format(file_mda))


class AverageDataExtractor:

    #  class to extract data from the ascii files
    def __init__(self, mirror_parameters, logger):
        # calculation type: 1 for vertical, -Vx-Sy, 0 for horizontal, Hx - Sx
        self.mirror_parameters = mirror_parameters
        self.logger = logger

    def find_parameters(self, file_ascii):
        """find parameters in the ascii files

        Args:
            file_ascii (file path): file path to the ascii file
        """
        lines = []
        with open(file_ascii, 'r') as f: lines = f.readlines()

        # find the scanning mode, fly or step; find the column position of the Sx, Sy,...
        # scan the content to find the mode and position
        col_num = {}
        self.scan_mode = 'None'
        for line in lines[0:200]:
            # print(line)
            # find scanning mode
            if 'scan mode, "FLY"' in line:
                self.scan_mode = 'fly scan'
                self.logger.print_message('fly scan')
            if 'scan mode, "LINEAR"' in line:
                self.scan_mode = 'step scan'
                self.logger.print_message('step scan')
                self.col_T = []

            # for step scan, find the temperature line
            if self.scan_mode == 'step scan':
                # here use the PV name in the ascii file, if they are changed, modify them here.
                if 'ltpu2:D1Ch2_raw.VAL' in line or 'ltpu2:D1Ch3_raw.VAL' in line or 'ltpu2:D1Ch4_raw.VAL' in line or 'ltpu2:D1Ch5_raw.VAL' in line or 'ltpu2:D1Ch6_raw.VAL' in line:
                    n_col = int(line.split()[1])
                    self.col_T.append(n_col - 1)
                if 'ltpu:timer1:elapsedSecs' in line:
                    n_col = int(line.split()[1])
                    self.col_T_time = n_col - 1

            # find the position of X, Sx, Sy, Vx, Vy, Hx, Hy in the ascii file
            if 'S-AC X' in line:
                n_col = int(line.split()[1])
                col_num['Sx'] = n_col - 1
            if 'S-AC Y' in line:
                n_col = int(line.split()[1])
                col_num['Sy'] = n_col - 1
            if 'H-AC X' in line:
                n_col = int(line.split()[1])
                col_num['Hx'] = n_col - 1
            if 'H-AC Y' in line:
                n_col = int(line.split()[1])
                col_num['Hy'] = n_col - 1
            if 'V-AC X' in line:
                n_col = int(line.split()[1])
                col_num['Vx'] = n_col - 1
            if 'V-AC Y' in line:
                n_col = int(line.split()[1])
                col_num['Vy'] = n_col - 1
        self.col_num = col_num

        if len(self.col_num) < 6:
            self.logger.print_error('error finding the six value. Check file')

    def fitting_average(self, x, y1, y2):
        """average the data from each ascii file using interpolation
        Args:
            x (ndarray): x axis of each data
            y1 (ndarray): slope 1
            y2 (ndarray): slope 2

        Returns:
            x_axis: interpolated x axis
            averaged y1
            averaged y2
        """
        x_max = np.amin([np.amax(x, axis=1)])
        x_min = np.amax([np.amin(x, axis=1)])
        # print(x[:, 0], x[:, -1])
        # print(x_max, x_min)
        N_interp = 2000
        x_axis = np.linspace(x_min, x_max, N_interp)

        y1_avg = []
        y2_avg = []
        self.logger.print_message('Averaging {} data measurements'.format(x.shape[0]))
        for kk in range(x.shape[0]):
            temp_x, ind = np.unique(x[kk, :], return_index=True)

            f_1 = interp1d(x[kk, ind],
                           y1[kk, ind],
                           kind='linear',
                           fill_value='extrapolate')
            f_2 = interp1d(x[kk, ind],
                           y2[kk, ind],
                           kind='linear',
                           fill_value='extrapolate')

            y1_avg.append(f_1(x_axis))
            y2_avg.append(f_2(x_axis))

        y1_avg = np.array(y1_avg)
        y2_avg = np.array(y2_avg)

        return x_axis, np.mean(y1_avg, axis=0), np.mean(y2_avg, axis=0)

    def slope_extract(self, file_list):
        """extract slope data from each file

        Args:
            file_list (list of file path): file path list to the data

        Returns:
            x_fit: averaged x axis
            *_fit: averaged slope data
        """
        # extract slope profile from the files
        # load data from the ascfiles
        if self.mirror_parameters['mirror_direction'] == 1:
            self.logger.print('Vertical mirror')
            x_list = []
            Vx_list = []
            Sy_list = []

            for ascfile in file_list:
                data = np.genfromtxt(ascfile, dtype=None)
                x = []
                Vx = []
                Sy = []
                for d in data:
                    x.append(d[1])
                    Sy.append(d[self.col_num['Sy']])
                    Vx.append(d[self.col_num['Vx']])
                x = np.array(x)
                Sy = np.array(Sy)
                Vx = np.array(Vx)

            x_list = np.array(x_list)
            Sy_list = np.array(Sy_list)
            Vx_list = np.array(Vx_list)

            x_fit, Vx_fit, Sy_fit = self.fitting_average(
                x_list, Vx_list, Sy_list)
            return x_fit, Vx_fit, Sy_fit

        elif self.mirror_parameters['mirror_direction'] == 2:
            self.logger.print('Horizontal mirror')
            x_list = []
            Sx_list = []
            Hx_list = []
            for ascfile in file_list:
                data = np.genfromtxt(ascfile, dtype=None)
                x = []
                Sx = []
                Hx = []
                for d in data:
                    x.append(d[1])
                    Sx.append(d[self.col_num['Sx']])
                    Hx.append(d[self.col_num['Hx']])
                x = np.array(x)
                Sx = np.array(Sx)
                Hx = np.array(Hx)

                x_list.append(x)
                Sx_list.append(Sx)
                Hx_list.append(Hx)

            x_list = np.array(x_list)
            Sx_list = np.array(Sx_list)
            Hx_list = np.array(Hx_list)

            x_fit, Sx_fit, Hx_fit = self.fitting_average(
                x_list, Sx_list, Hx_list)
            return x_fit, Hx_fit, Sx_fit

        elif self.mirror_parameters['mirror_direction'] == 3:
            self.logger.print('data test')
            x_list = []
            Hy_list = []
            Hx_list = []
            Vy_list = []
            Vx_list = []
            Sy_list = []
            Sx_list = []
            for ascfile in file_list:
                data = np.genfromtxt(ascfile, dtype=None)
                x = []
                Hy = []
                Hx = []
                Vx = []
                Vy = []
                Sx = []
                Sy = []
                for d in data:
                    x.append(d[1])
                    Hy.append(d[self.col_num['Hy']])
                    Hx.append(d[self.col_num['Hx']])
                    Sy.append(d[self.col_num['Sy']])
                    Sx.append(d[self.col_num['Sx']])
                    Vy.append(d[self.col_num['Vy']])
                    Vx.append(d[self.col_num['Vx']])
                x = np.array(x)
                Hy = np.array(Hy)
                Hx = np.array(Hx)
                Sy = np.array(Sy)
                Sx = np.array(Sx)
                Vy = np.array(Vy)
                Vx = np.array(Vx)

                x_list.append(x)
                Hy_list.append(Hy)
                Hx_list.append(Hx)
                Sy_list.append(Sy)
                Sx_list.append(Sx)
                Vy_list.append(Vy)
                Vx_list.append(Vx)

            x_list = np.array(x_list)
            Hy_list = np.array(Hy_list)
            Hx_list = np.array(Hx_list)
            Sy_list = np.array(Sy_list)
            Sx_list = np.array(Sx_list)
            Vy_list = np.array(Vy_list)
            Vx_list = np.array(Vx_list)

            x_fit, Hy_fit, Hx_fit = self.fitting_average(
                x_list, Hy_list, Hx_list)
            x_fit, Sy_fit, Sx_fit = self.fitting_average(
                x_list, Sy_list, Sx_list)
            x_fit, Vy_fit, Vx_fit = self.fitting_average(
                x_list, Vy_list, Vx_list)
            return x_fit, Hx_fit, Hy_fit, Sx_fit, Sy_fit, Vx_fit, Vy_fit

    def noise_remove_filter(self, data, filter_size):
        """remove noise of slope profile by using uniform filter

        Args:
            data (ndarry): slope data
            filter_size (int): filter kernel size of uniform filter

        Returns:
            filtered slope data
        """
        if filter_size == 0:
            return data
        else:
            return snd.uniform_filter(data, filter_size)

    def noise_remove_poly(self, data, filter_order):
        """remove noise of slope profile by using polynomial fitting filter

        Args:
            data (ndarray): slope data
            filter_order (int): order of polynomial fitting

        Returns:
            filtered slope data
        """
        if filter_order == 0:
            return data
        else:
            x = np.arange(data.shape[0])
            return np.polyval(np.polyfit(x, data, filter_order), x)

    def load_T_flyscan(self, filename):
        """load temperature data from the flyscan ascii file

        Args:
            filename (str): filename of the ascii file

        Returns:
            x_time: x axis for time
            [T1, T2, T3, T4, T5]: temperature vs time from five sensors
        """
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        col_T = []
        for line in lines:
            # for step scan, find the temperature line
            if 'ltpu2:D1Ch2_raw.VAL' in line or 'ltpu2:D1Ch3_raw.VAL' in line or 'ltpu2:D1Ch4_raw.VAL' in line or 'ltpu2:D1Ch5_raw.VAL' in line or 'ltpu2:D1Ch6_raw.VAL' in line:
                n_col = int(line.split()[1])
                col_T.append(n_col - 1)
        T1_list = []
        T2_list = []
        T3_list = []
        T4_list = []
        T5_list = []
        time_list = []
        data = np.genfromtxt(filename, dtype=None)
        for d in data:
            time_list.append(d[0])
            # x.append(d[3])
            T1_list.append(d[col_T[0]])
            T2_list.append(d[col_T[1]])
            T3_list.append(d[col_T[2]])
            T4_list.append(d[col_T[3]])
            T5_list.append(d[col_T[4]])

        x_time = np.array(time_list)
        T1 = np.array(T1_list)
        T2 = np.array(T2_list)
        T3 = np.array(T3_list)
        T4 = np.array(T4_list)
        T5 = np.array(T5_list)

        return x_time, [T1, T2, T3, T4, T5]

    def load_T_stepscan(self, filelist):
        """load temperature data from the step-scan ascii file

        Args:
            filename (str): filename of the ascii file

        Returns:
            x_time: x axis for time
            [T1, T2, T3, T4, T5]: temperature vs time from five sensors
        """
        T1_list = []
        T2_list = []
        T3_list = []
        T4_list = []
        T5_list = []
        time_list = []
        for kk, ascfile in enumerate(filelist):
            data = np.genfromtxt(ascfile, dtype=None)
            x_time = []
            for d in data:
                x_time.append(d[self.col_T_time])
                # x.append(d[3])
                T1_list.append(d[self.col_T[0]])
                T2_list.append(d[self.col_T[1]])
                T3_list.append(d[self.col_T[2]])
                T4_list.append(d[self.col_T[3]])
                T5_list.append(d[self.col_T[4]])

            if kk == 0:
                time_list.append(x_time)
            else:
                temp = np.array(x_time) + time_list[-1]
                time_list.append(temp)

        x_time = np.arange(len(T1_list)) * np.mean(
            np.diff(np.array(time_list).flatten()))
        T1 = np.array(T1_list)
        T2 = np.array(T2_list)
        T3 = np.array(T3_list)
        T4 = np.array(T4_list)
        T5 = np.array(T5_list)

        return x_time, [T1, T2, T3, T4, T5]

    def data_extract(self, mda_file):
        """extract slope data from the ascii files converted from mda file

        Args:
            mda_file (str): mda file path

        Returns:
            slope data
        """
        dirname_path = os.path.dirname(mda_file)
        file_name = os.path.basename(mda_file).split('.')[0]

        ascfile_temperature = os.path.join(dirname_path, '{}.asc'.format(file_name))
        ascfile_list1       = glob.glob(os.path.join(dirname_path, '{}_*.asc'.format(file_name)))
        ascfile_list2       = glob.glob(os.path.join(dirname_path, '{}_*_*.asc'.format(file_name)))

        # test if it's step scan or fly scan
        if len(ascfile_list2) == 0: ascfile_list = ascfile_list1
        else:                       ascfile_list = ascfile_list2

        self.find_parameters(ascfile_list[0])
        self.logger.print('column number: {}'.format(self.col_num))

        # load temperature data
        if self.scan_mode == 'step scan':
            self.T_time, self.T_temp = self.load_T_stepscan(ascfile_list2)
        elif self.scan_mode == 'fly scan':
            self.T_time, self.T_temp = self.load_T_flyscan(ascfile_temperature)

        N_num = self.mirror_parameters['N_num']

        if self.mirror_parameters['mirror_direction'] == 1:
            # for vertical mirror
            if (len(ascfile_list) < N_num) or (N_num == -1):
                self.logger.print('use {} data files'.format(len(ascfile_list)))
                x, Vx, Sy = self.slope_extract(ascfile_list)

            else:
                self.logger.print('use {} data files'.format(N_num))
                x, Vx, Sy = self.slope_extract(ascfile_list[0:N_num])

            cut_pos = np.where(np.abs(x) <= self.mirror_parameters['mirror_length'])
            x = x[cut_pos]
            Vx = Vx[cut_pos]
            Sy = Sy[cut_pos]

            filter_size = self.mirror_parameters['filter_size']

            Sy = self.noise_remove_poly(Sy, filter_size[0])
            Vx = self.noise_remove_poly(Vx, filter_size[1])

            return {'X': x, 'Sy': Sy, 'Vx': Vx, 'slope': -(Vx - Sy)}
        elif self.mirror_parameters['mirror_direction'] == 2:
            # for horizontal mirror
            if (len(ascfile_list) < N_num) or (N_num == -1):
                self.logger.print('use {} data files'.format(len(ascfile_list)))
                x, Hx, Sx = self.slope_extract(ascfile_list)

            else:
                self.logger.print('use {} data files'.format(N_num))
                x, Hx, Sx = self.slope_extract(ascfile_list[0:N_num])

            cut_pos = np.where(np.abs(x) <= self.mirror_parameters['mirror_length'])
            x = x[cut_pos]
            Hx = Hx[cut_pos]
            Sx = Sx[cut_pos]

            filter_size = self.mirror_parameters['filter_size']
            Sx = self.noise_remove_poly(Sx, filter_size[0])
            Hx = self.noise_remove_poly(Hx, filter_size[1])

            return {'X': x, 'Sx': Sx, 'Hx': Hx, 'slope': Hx - Sx}

        elif self.mirror_parameters['mirror_direction'] == 3:
            # extract all the channels from LTP
            if (len(ascfile_list) < N_num) or (N_num == -1):
                self.logger.print('use {} data files'.format(len(ascfile_list)))
                x, Hx, Hy, Sx, Sy, Vx, Vy = self.slope_extract(ascfile_list)

            else:
                self.logger.print('use {} data files'.format(N_num))
                x, Hx, Hy, Sx, Sy, Vx, Vy = self.slope_extract(
                    ascfile_list[0:N_num])

            cut_pos = np.where((x <= self.mirror_parameters['mirror_length'])
                               & (x >= -self.mirror_parameters['mirror_length']))

            filter_size = self.mirror_parameters['filter_size']
            Hy = self.noise_remove_poly(Hy, filter_size[0])
            Hx = self.noise_remove_poly(Hx, filter_size[1])
            Sy = self.noise_remove_poly(Sy, filter_size[2])
            Sx = self.noise_remove_poly(Sx, filter_size[3])
            Vy = self.noise_remove_poly(Vy, filter_size[4])
            Vx = self.noise_remove_poly(Vx, filter_size[5])

            x = x[cut_pos]
            Hx = Hx[cut_pos]
            Hy = Hy[cut_pos]
            Sx = Sx[cut_pos]
            Sy = Sy[cut_pos]
            Vx = Vx[cut_pos]
            Vy = Vy[cut_pos]
            #for mirror up, vertical V-AC (Vx), reference Hx, using    -(Vx-(Hx));
            #for mirror up, vertical V-AC (Vx), reference Sy, using     Sy-Vx;
            #for mirror side, Horizontal H-AC (Hx), reference Sx, using Hx-Sx;
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': -Vx}
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': Sy-Vx}                  # USE THIS ONE FOR VERTICAL_SETUP
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': -Vx}
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': Hx-Sx}                    # USE THIS ONE FOR HORIZONTAL_SETUP
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': Hx}
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': -Hy-Vx}
            # return {'X': x, 'Hy': Hy, 'Hx': Hx, 'Sy': Sy, 'Sx': Sx, 'Vy': Vy, 'Vx': Vx, 'slope': (Sy-Hy)/2-(Vx)}

            slope_final = 0
            for slope_ch, sign in zip([Hy, Hx, Sy, Sx, Vy, Vx],
                                      self.mirror_parameters['slope_ch_sign']):
                slope_final += slope_ch * sign
            return {
                'X': x,
                'Hy': Hy,
                'Hx': Hx,
                'Sy': Sy,
                'Sx': Sx,
                'Vy': Vy,
                'Vx': Vx,
                'slope': slope_final
            }


class DataFitter:
    """
        process height and slope profile
    """
    def __init__(self, mirror_parameters={'mirror': 'flat'}, logger=None):
        self.mirror_parameters = mirror_parameters
        self.logger = logger

    def calc_radius_slope(self, x, y):
        """
        calculate radius from slope profile

        Args:
            x (ndarray): x axis
            y (ndarray): slope profile

        Returns:
            radius
        """
        p = np.polyfit(x, y, 1)
        radius = 1 / p[0]

        return radius

    def calc_radius_height(self, x, y):
        """
        calculate radius from height profile

        Args:
            x (ndarray): x axis
            y (ndarray): height profile

        Returns:
            radius
        """

        X_matrix = np.vstack([x**2, x, x * 0 + 1]).T

        beta_matrix = np.linalg.lstsq(X_matrix, y, rcond=-1)[0]

        radius = 1 / 2 / beta_matrix[0]
        return radius

    def get_integrate(self, x, y):
        """
        get integrated height profile from slope

        Args:
            x (ndarray): x axis
            y (ndarray): profile to be integrated

        Returns:
            integrated profile
        """
        dx = np.gradient(x)
        y_integ = np.cumsum((y - np.mean(y)) * dx)

        return y_integ

    def fitting_flat(self, data_profile):
        """
        fitting for flat mirror

        Args:
            data_profile (ndarray): line profile for flat mirror fitting

        Returns:
            result_dict
        """

        # get integrated height profile
        height_profile = self.get_integrate(data_profile['X'], data_profile['slope'])
        fitted_radius_slope = self.calc_radius_slope(data_profile['X'] * 1e-3, data_profile['slope'] * 1e-6)

        self.logger.print_message('fitted radius curvature: {}m'.format(fitted_radius_slope))

        fitted_radius_height = self.calc_radius_height(
            data_profile['X'] * 1e-3, height_profile * 1e-9)
        self.logger.print_message('fitted radius curvature: {}m'.format(fitted_radius_height))

        def flat_shape(x, y0):
            return y0 + x * 0

        x_axis = data_profile['X']

        param_bend, cov_bend = curve_fit(flat_shape,
                                         x_axis * 1e-3,
                                         height_profile * 1e-9,
                                         p0=[np.amin(height_profile * 1e-9)])
        curve_fit_height = flat_shape(x_axis * 1e-3, *param_bend) * 1e9

        error_height = height_profile - curve_fit_height

        PV_height = np.amax(error_height) - np.amin(error_height)
        rms_height = np.std(error_height)

        error_slope = np.gradient(error_height) / (x_axis[2] - x_axis[1])

        PV_slope = np.amax(error_slope) - np.amin(error_slope)
        rms_slope = np.std(error_slope)

        self.logger.print_message('slope error rms: {}\u03bcrad, PV: {}\u03bcrad'.format(rms_slope, PV_slope))
        self.logger.print_message('height error rms: {}nm, PV: {}nm'.format(rms_height, PV_height))

        # process slope and height with removing polynomial fit
        error_slope_polyfit = []
        error_height_polyfit = []
        statistics_polyfit = []
        poly_order = []
        if len(self.mirror_parameters['polyfit']) != 0:
            for polyfit_each in self.mirror_parameters['polyfit']:
                p = np.polyfit(x_axis, error_slope, polyfit_each)
                error_slope_polyfit.append(error_slope - np.polyval(p, x_axis))
                error_height_polyfit.append(
                    self.get_integrate(x_axis, error_slope_polyfit[-1]))

                PV_height_polyfit = np.amax(
                    error_height_polyfit[-1]) - np.amin(
                        error_height_polyfit[-1])
                rms_height_polyfit = np.std(error_height_polyfit[-1])

                PV_slope_polyfit = np.amax(error_slope_polyfit[-1]) - np.amin(
                    error_slope_polyfit[-1])
                rms_slope_polyfit = np.std(error_slope_polyfit[-1])

                statistics_polyfit.append({
                    'slope_rms': rms_slope_polyfit,
                    'slope_PV': PV_slope_polyfit,
                    'height_rms': rms_height_polyfit,
                    'height_PV': PV_height_polyfit
                })
                poly_order.append(polyfit_each)

        result_dict = {
            'x': x_axis,
            'height_profile': height_profile,
            'error_height': error_height,
            'error_slope': error_slope,
            'radius': [fitted_radius_height, fitted_radius_slope],
            'rms_height': rms_height,
            'PV_height': PV_height,
            'rms_slope': rms_slope,
            'PV_slope': PV_slope,
            'polyfit_results': {
                'slope': error_slope_polyfit,
                'height': error_height_polyfit,
                'statistics': statistics_polyfit,
                'polyorder': poly_order
            }
        }
        return result_dict

    def elipse_shape_shift_whole(self, x, xc, yc, tc):
        """
        equation for elliptical shape fitting using height profile

        Args:
            x (ndarray):    x axis
            xc (float):     x center offset
            yc (float):     y offset
            tc (float):     theta offset

        Returns:
            elliptical shape
        """
        p = self.mirror_parameters['P']
        q = self.mirror_parameters['Q']
        th = self.mirror_parameters['theta']

        return yc + (
            -(x - xc) * (2 * p * q +
                         (p**2 + q**2) * np.cos(2 * th)) * np.sin(2 * tc) +
            (p + q) *
            (4 * p * q * np.cos(tc) * np.sin(th) - 2 * np.sqrt(2) *
             np.sqrt(p * q * (p * q - 2 *
                              (x - xc)**2 + p * q * np.cos(2 * tc) + 2 * q *
                              (x - xc) * np.cos(tc - th) - 2 * p *
                              (x - xc) * np.cos(tc + th))) * np.sin(th) +
             (q - p) * (x - xc) * np.cos(2 * tc) * np.sin(2 * th))) / (
                 p**2 + 4 * p * q + q**2 + q *
                 (2 * p * np.cos(2 * tc) + q * np.cos(2 * tc - 2 * th) -
                  2 * p * np.cos(2 * th)) + p**2 * np.cos(2 * tc + 2 * th))

    def elipse_shape_shift_full(self, x, xc, yc, tc, p, q, th):
        """
        equation for elliptical shape fitting using height profile

        Args:
            x (ndarray):    x axis
            xc (float):     x center offset
            yc (float):     y offset
            tc (float):     theta offset
            p (float):      P value
            q (float):      Q
            th (float):     theta angle

        Returns:
            elliptical shape
        """
        return yc + (
            -(x - xc) * (2 * p * q +
                         (p**2 + q**2) * np.cos(2 * th)) * np.sin(2 * tc) +
            (p + q) *
            (4 * p * q * np.cos(tc) * np.sin(th) - 2 * np.sqrt(2) *
             np.sqrt(p * q * (p * q - 2 *
                              (x - xc)**2 + p * q * np.cos(2 * tc) + 2 * q *
                              (x - xc) * np.cos(tc - th) - 2 * p *
                              (x - xc) * np.cos(tc + th))) * np.sin(th) +
             (q - p) * (x - xc) * np.cos(2 * tc) * np.sin(2 * th))) / (
                 p**2 + 4 * p * q + q**2 + q *
                 (2 * p * np.cos(2 * tc) + q * np.cos(2 * tc - 2 * th) -
                  2 * p * np.cos(2 * th)) + p**2 * np.cos(2 * tc + 2 * th))

    def elipse_shape_slope(self, x, xc, yc, p, q, th):
        """
        equation for elliptical shape fitting using slope profile

        Args:
            x (ndarray):    x axis
            xc (float):     x center offset
            yc (float):     y offset
            p (float):      P value
            q (float):      Q
            th (float):     theta angle

        Returns:
            elliptical shape
        """
        alpha = np.pi / 2 - th
        up = (2 * (p + q) * np.cos(alpha) *
              ((p - q) * np.sin(alpha) - np.sqrt(p * q) *
               ((p - q) * np.sin(alpha) + 2 *
                (x - xc)) / np.sqrt(p * q - (x - xc) *
                                    (p - q) * np.sin(alpha) - (x - xc)**2)))
        down = p**2 + 6 * p * q + q**2 - (p - q)**2 * np.cos(2 * alpha)
        return -up / down + yc

    def fitting_ellipse(self, data_profile):
        """
        fitting for elliptical mirror

        Args:
            data_profile (ndarray): line profile

        Returns:
            result_dict    
        """
        # get target elliptical shape parameters
        P = self.mirror_parameters['P']
        Q = self.mirror_parameters['Q']
        theta = self.mirror_parameters['theta']

        self.logger.print_warning(
            'starting elliptical mirror process, P: {}m, Q:{}m, theta: {}rad'.
            format(P, Q, theta))
        fix_var = self.mirror_parameters['fix']
        if fix_var[0] == 0:
            p_up = 100
            p_down = 0.1
        else:
            p_up = self.mirror_parameters['P'] + 1e-6
            p_down = self.mirror_parameters['P'] - 1e-6
        if fix_var[1] == 0:
            q_up = 100
            q_down = 0.01
        else:
            q_up = self.mirror_parameters['Q'] + 1e-6
            q_down = self.mirror_parameters['Q'] - 1e-6
        if fix_var[2] == 0:
            th_up = 10e-3
            th_down = 0e-3
        else:
            th_up = self.mirror_parameters['theta'] + 1e-9
            th_down = self.mirror_parameters['theta'] - 1e-9

        if self.mirror_parameters['reverse']:
            x_axis = -data_profile['X']
            slope_profile = -data_profile['slope']
            height_profile = self.get_integrate(x_axis, slope_profile)
        else:
            x_axis = data_profile['X']
            slope_profile = data_profile['slope']
            height_profile = self.get_integrate(x_axis, slope_profile)

        fitted_radius_slope = self.calc_radius_slope(x_axis * 1e-3, slope_profile * 1e-6)
        self.logger.print_message('fitted radius curvature: {}m'.format(fitted_radius_slope))

        fitted_radius_height = self.calc_radius_height(x_axis * 1e-3, height_profile * 1e-9)
        self.logger.print_message('fitted radius curvature: {}m'.format(fitted_radius_height))

        if self.mirror_parameters['fitting_equation'] == 'slope':
            # fitting with slope equation
            bounds = [(-500e-3, 500e-3), (-1e10, 1e10), (p_down, p_up),
                      (q_down, q_up), (th_down, th_up)]

            # use minimization
            def cost_func(x):
                xc, yc, p, q, th = x
                return np.sum(
                    np.abs(
                        self.elipse_shape_slope(x_axis *
                                                1e-3, xc, yc, p, q, th) -
                        slope_profile * 1e-6))

            x0 = [
                0,
                np.mean(slope_profile * 1e-6), self.mirror_parameters['P'],
                self.mirror_parameters['Q'], self.mirror_parameters['theta']
            ]

            self.logger.print_warning(
                'initial guess xc: {}, yc: {}, P: {}, Q:{}, th:{}'.format(
                    x0[0], x0[1], x0[2], x0[3], x0[4]))

            res = minimize(cost_func,
                           x0,
                           method='nelder-mead',
                           options={
                               'xatol': 1e-9,
                               'disp': True
                           },
                           bounds=bounds)
            self.logger.print_warning(
                'fitted parameters\n xc: {:.6f}, yc: {:.6f}, P: {:.5f}, Q:{:.5f}, th:{}'
                .format(res.x[0], res.x[1], res.x[2], res.x[3],
                        res.x[4]))
            self.fitted_ellipse = {
                'xc': res.x[0],
                'yc': res.x[1],
                'P': res.x[2],
                'Q': res.x[3],
                'th': res.x[4],
            }

            slope_fit_target = self.elipse_shape_slope(x_axis * 1e-3, *
                                                       res.x) * 1e6
            height_fit_target = self.get_integrate(x_axis, slope_fit_target)

            error_slope = slope_profile - slope_fit_target
            error_height = self.get_integrate(x_axis, error_slope)

        else:
            # use height profile for elliptical fitting
            bounds = [(-100e-3, 100e-3), (-1e10, 1e10), (-1e-3, 1e-3),
                      (p_down, p_up), (q_down, q_up), (th_down, th_up)]

            # use minimization
            def cost_func(x):
                xc, yc, tc, p, q, th = x
                return np.sum(np.abs(self.elipse_shape_shift_full(x_axis * 1e-3, xc, yc, tc, p, q, th) - height_profile * 1e-9))

            x0 = [0, np.amin(height_profile * 1e-9), 0, self.mirror_parameters['P'], self.mirror_parameters['Q'], self.mirror_parameters['theta']]

            self.logger.print_warning('initial guess xc: {}, yc: {}, tc: {}, P: {}, Q:{}, th:{}'.format(x0[0], x0[1], x0[2], x0[3], x0[4], x0[5]))

            res = minimize(cost_func,
                           x0,
                           method='nelder-mead',
                           options={'xatol': 1e-10, 'disp': True},
                           bounds=bounds)
            self.logger.print_warning( 'fitted parameters\n xc: {:.6f}, yc: {:.6f}, tc: {}, P: {:.5f}, Q:{:.5f}, th:{}'.format(res.x[0], res.x[1], res.x[2], res.x[3], res.x[4], res.x[5]))

            self.fitted_ellipse = {
                'xc': res.x[0],
                'yc': res.x[1],
                'tc': res.x[2],
                'P': res.x[3],
                'Q': res.x[4],
                'th': res.x[5],
            }

            curve_fit_target = self.elipse_shape_shift_full(x_axis * 1e-3, *res.x) * 1e9

            error_height = height_profile - curve_fit_target
            error_slope = np.gradient(error_height) / (x_axis[2] - x_axis[1])

        PV_height = np.amax(error_height) - np.amin(error_height)
        rms_height = np.std(error_height)

        PV_slope = np.amax(error_slope) - np.amin(error_slope)
        rms_slope = np.std(error_slope)

        self.logger.print_message('slope error rms: {}\u03bcrad, PV: {}\u03bcrad'.format(rms_slope, PV_slope))
        self.logger.print_message('height error rms: {}nm, PV: {}nm'.format(rms_height, PV_height))

        # process slope and height with removing polynomial fit
        error_slope_polyfit = []
        error_height_polyfit = []
        statistics_polyfit = []
        poly_order = []
        if len(self.mirror_parameters['polyfit']) != 0:
            for polyfit_each in self.mirror_parameters['polyfit']:
                p = np.polyfit(x_axis, error_slope, polyfit_each)
                error_slope_polyfit.append(error_slope - np.polyval(p, x_axis))
                error_height_polyfit.append(
                    self.get_integrate(x_axis, error_slope_polyfit[-1]))

                PV_height_polyfit = np.amax(
                    error_height_polyfit[-1]) - np.amin(
                        error_height_polyfit[-1])
                rms_height_polyfit = np.std(error_height_polyfit[-1])

                PV_slope_polyfit = np.amax(error_slope_polyfit[-1]) - np.amin(
                    error_slope_polyfit[-1])
                rms_slope_polyfit = np.std(error_slope_polyfit[-1])

                statistics_polyfit.append({
                    'slope_rms': rms_slope_polyfit,
                    'slope_PV': PV_slope_polyfit,
                    'height_rms': rms_height_polyfit,
                    'height_PV': PV_height_polyfit
                })
                poly_order.append(polyfit_each)

        result_dict = {
            'x': x_axis,
            'height_profile': height_profile,
            'error_height': error_height,
            'error_slope': error_slope,
            'radius': [fitted_radius_height, fitted_radius_slope],
            'rms_height': rms_height,
            'PV_height': PV_height,
            'rms_slope': rms_slope,
            'PV_slope': PV_slope,
            'polyfit_results': {
                'slope': error_slope_polyfit,
                'height': error_height_polyfit,
                'statistics': statistics_polyfit,
                'polyorder': poly_order
            }
        }
        return result_dict

    def fitting(self, data_profile):
        if self.mirror_parameters['mirror'] == 'flat':      return self.fitting_flat(data_profile)
        elif self.mirror_parameters['mirror'] == 'ellipse': return self.fitting_ellipse(data_profile)

class FigureScales:
    height_profile_scale  = [0.0, 3000.0]
    height_error_scale    = [-3500.0, 1500.0]
    height_error_p1_scale = [-30.0, 30.0]
    height_error_p3_scale = [-0.5, 0.5]
    height_error_p5_scale = [-0.5, 0.5]
    slope_profile_scale   = [-150.0, 100.0]
    slope_error_scale     = [-150.0, 100.0]
    slope_error_p1_scale  = [-3.0, 1.5]
    slope_error_p3_scale  = [-0.3, 0.3]
    slope_error_p5_scale  = [-0.3, 0.3]

    @classmethod
    def __check_scale(cls, scale):
        if not scale is None:
            if scale[0] == 0.0 and scale[1] == 0.0: return None
            else: return scale
        else: return scale

    def check_scales(self):
        self.height_profile_scale  = FigureScales.__check_scale(self.height_profile_scale)
        self.height_error_scale    = FigureScales.__check_scale(self.height_error_scale)
        self.height_error_p1_scale = FigureScales.__check_scale(self.height_error_p1_scale)
        self.height_error_p3_scale = FigureScales.__check_scale(self.height_error_p3_scale)
        self.height_error_p5_scale = FigureScales.__check_scale(self.height_error_p5_scale)
        self.slope_profile_scale   = FigureScales.__check_scale(self.slope_profile_scale)
        self.slope_error_scale     = FigureScales.__check_scale(self.slope_error_scale)
        self.slope_error_p1_scale  = FigureScales.__check_scale(self.slope_error_p1_scale)
        self.slope_error_p3_scale  = FigureScales.__check_scale(self.slope_error_p3_scale)
        self.slope_error_p5_scale  = FigureScales.__check_scale(self.slope_error_p5_scale)

class DataManager:
    # save results and figures
    def __init__(self, saving_path, mirror_parameters, logger, figure_scales=FigureScales()):
        self.saving_path = saving_path
        self.mirror_parameters = mirror_parameters
        self.logger = logger
        self.figure_scales = figure_scales

    def save_data(self, subfolder, Rawdata_dict, data_dict, data_fit):
        """
        save fitted data and figures

        Args:
            subfolder (str): saving subfolder name
            Rawdata_dict (dict): raw data dict
            data_dict (dict): extracted data dict
            data_fit (dict): fitted data dict
        """
        result_path = os.path.join(self.saving_path, subfolder)
        if not os.path.exists(result_path):
            os.makedirs(result_path)

        # save json setting file
        with open(os.path.join(result_path, 'setting.json'), 'w') as f:
            json.dump(self.mirror_parameters, f)

        if self.mirror_parameters['mirror'] == 'ellipse':
            with open(os.path.join(result_path, 'fitted_param.json'),
                      'w') as f:
                json.dump(data_fit.fitted_ellipse, f)

        key_Rawdata = list(Rawdata_dict.keys())
        polyfit_results = data_dict['polyfit_results']

        with open(os.path.join(result_path,
                               '{}_LTP_measurement.csv'.format(subfolder)),
                  mode='w',
                  newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')

            line = [
                'radius: {}m'.format(data_dict['radius'][0]),
                'Height error: {:0.2f}nm RMS, {:0.2f}nm PV'.format(
                    data_dict['rms_height'], data_dict['PV_height']),
                'slope error: {:0.2f}nrad, {:0.2f}\u03bcrad'.format(
                    data_dict['rms_slope'] * 1e3, data_dict['PV_slope'])
            ]
            if len(polyfit_results['slope']) != 0:
                for stat, polyorder in zip(polyfit_results['statistics'], polyfit_results['polyorder']):
                    line.append(
                        'remove {} order polyfit: {:0.2f}nrad RMS, {:0.2f}\u03bcrad PV, {:0.2f}nm RMS, {:0.2f}nm PV'
                        .format(polyorder, stat['slope_rms'] * 1e3,
                                stat['slope_PV'], stat['height_rms'],
                                stat['height_PV']))
            csv_writer.writerow(line)

            line = [
                'X [mm]', '{} [\u03bcrad]'.format(key_Rawdata[1]),
                '{} [\u03bcrad]'.format(key_Rawdata[2]),
                '{} [\u03bcrad]'.format(key_Rawdata[3]),
                '{} [\u03bcrad]'.format(key_Rawdata[4]),
                '{} [\u03bcrad]'.format(key_Rawdata[5]),
                '{} [\u03bcrad]'.format(key_Rawdata[6]),
                'slope [\u03bcrad]',
                'height',
                'height error',
                'slope error'
            ]

            if len(polyfit_results['slope']) != 0:
                for polyorder in polyfit_results['polyorder']:
                    line.append('slope error after removing {} order polyfit [\u03bcrad]'. format(polyorder))
                    line.append( 'height error after removing {} order polyfit [nm]'. format(polyorder))

            csv_writer.writerow(line)

            for k in range(Rawdata_dict['X'].shape[0]):
                line = [
                    Rawdata_dict['X'][k],
                    Rawdata_dict[key_Rawdata[1]][k],
                    Rawdata_dict[key_Rawdata[2]][k],
                    Rawdata_dict[key_Rawdata[3]][k],
                    Rawdata_dict[key_Rawdata[4]][k],
                    Rawdata_dict[key_Rawdata[5]][k],
                    Rawdata_dict[key_Rawdata[6]][k],
                    Rawdata_dict['slope'][k],
                    data_dict['height_profile'][k],
                    data_dict['error_height'][k],
                    data_dict['error_slope'][k]
                ]

                if len(polyfit_results['slope']) != 0:
                    for slope, height in zip(polyfit_results['slope'], polyfit_results['height']):
                        line.append(slope[k])
                        line.append(height[k])

                csv_writer.writerow(line)

    def save_figure(self, x, y, x_label, y_label, title, filename, scale=None):
        """
            save the data in visible figure
        Args:
            x:              x axis
            y:              y axis
            x_label:        label for x axis
            y_label:        label for y axis
            title:          figure title
            filename:       saved filename
        """
        fig = plt.figure()
        plt.plot(x, y, '-k')
        plt.xlabel(x_label, fontsize=22)
        plt.ylabel(y_label, fontsize=22)
        if not scale is None: plt.ylim(scale[0], scale[1])
        fig.gca().tick_params(axis='both', which='major', labelsize=18)
        fig.gca().tick_params(axis='both', which='minor', labelsize=16)
        plt.grid()
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()

    def save_figure_temperature(self, x_time, T_temp, x_label, filename):
        """
            save the temperature data in visible figure
        Args:
            x_time:                 x axis
            T_temp:                 y axis
            x_label:                label for x axis
            filename:               saved filename
        """

        fig = plt.figure()
        for T in T_temp:
            plt.plot(x_time, T)
        plt.xlabel(x_label, fontsize=22)
        plt.ylabel('Temperature [\u00b0C]', fontsize=22)
        fig.gca().tick_params(axis='both', which='major', labelsize=18)
        fig.gca().tick_params(axis='both', which='minor', labelsize=16)
        plt.grid()
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()

    def save_psd(self, x, y, x_label, y_label, title, filename):
        """
        save psd figures

        Args:
            x:              x axis
            y:              y axis
            x_label:        label for x axis
            y_label:        label for y axis
            title:          figure title
            filename:       saved filename
        """
        dx = x[2] - x[1]
        plt.figure(figsize=(10, 4))
        plt.psd(y, 1024, 1 / dx)
        plt.xlabel(x_label, fontsize=22)
        plt.ylabel(y_label, fontsize=22)
        # plt.grid()
        plt.title(title)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()

    def save_figures(self, subfolder, Rawdata_dict, data_dict, data_extractor):
        """
        save figures from the processed data

        Args:
            subfolder (str): subfolder where to save figures
            Rawdata_dict (dict): raw data
            data_dict (dict): extracted data
            data_extractor (class): class to extract data from raw data file, here used to check the measurement parameters
        """
        result_path = os.path.join(self.saving_path, subfolder)
        if not os.path.exists(result_path): os.makedirs(result_path)

        # save temperature figures
        if data_extractor.scan_mode == 'fly scan': x_temp_label = 'scan pass'
        else:                                      x_temp_label = 'time [s]'

        saved_figures = [os.path.join(result_path, '{}_temperature.png'.format(subfolder)),
                         os.path.join(result_path, '{}_slope_profile.png'.format(subfolder)),
                         os.path.join(result_path, '{}_height_profile.png'.format(subfolder)),
                         os.path.join(result_path, '{}_slope_error_profile.png'.format(subfolder)),
                         os.path.join(result_path, '{}_height_error_profile.png'.format(subfolder))]


        self.save_figure_temperature(data_extractor.T_time, data_extractor.T_temp, x_temp_label, saved_figures[0])
        self.save_figure(Rawdata_dict['X'], Rawdata_dict['slope'], 'x [mm]', 'slope [\u03bcrad]', 'slope profile', saved_figures[1],
                         scale=self.figure_scales.slope_profile_scale)
        self.save_figure(data_dict['x'], data_dict['height_profile'], 'x [mm]', 'height [nm]', 'height profile', saved_figures[2],
                         scale=self.figure_scales.height_profile_scale)

        self.save_figure(data_dict['x'], data_dict['error_slope'], 'x [mm]', 'slope error [\u03bcrad]',
                         'slope error profile, {:.2f}nrad RMS, {:.2f}\u03bcrad PV'.format(data_dict['rms_slope'] * 1e3, data_dict['PV_slope']), saved_figures[3],
                         scale=self.figure_scales.slope_error_scale)
        self.save_figure(data_dict['x'], data_dict['error_height'], 'x [mm]', 'height error [nm]',
                         'height error profile, {:.2f}nm RMS, {:.2f}nm PV'.format(data_dict['rms_height'], data_dict['PV_height']), saved_figures[4],
                         scale=self.figure_scales.height_error_scale)

        polyfit_results = data_dict['polyfit_results']

        if len(polyfit_results['slope']) != 0:
            for slope, height, stat, polyorder in zip(
                    polyfit_results['slope'], polyfit_results['height'],
                    polyfit_results['statistics'],
                    polyfit_results['polyorder']):

                if polyorder == 1:
                    slope_scale = self.figure_scales.slope_error_p1_scale
                    height_scale = self.figure_scales.height_error_p1_scale
                elif polyorder == 3:
                    slope_scale = self.figure_scales.slope_error_p3_scale
                    height_scale = self.figure_scales.height_error_p3_scale
                elif polyorder == 5:
                    slope_scale = self.figure_scales.slope_error_p5_scale
                    height_scale = self.figure_scales.height_error_p5_scale

                saved_figures_tmp = [os.path.join(result_path, '{}_slope_error_profile_removing_{}_order_polyfit.png'.format(subfolder, polyorder)),
                                     os.path.join(result_path, '{}_height_error_profile_removing_{}_order_polyfit.png'.format(subfolder, polyorder))]

                self.save_figure(data_dict['x'], slope, 'x [mm]', 'slope error [\u03bcrad]',
                                 'slope error profile removing {} order polyfit,\n{:.2f}nrad RMS, {:.2f}\u03bcrad PV' .format(polyorder, stat['slope_rms'] * 1e3, stat['slope_PV']),
                                 saved_figures_tmp[0], scale=slope_scale)

                self.save_figure(data_dict['x'], height, 'x [mm]', 'height error [nm]',
                                 'height error profile {} order polyfit,\n{:.2f}nm RMS, {:.2f}nm PV'.format(polyorder, stat['height_rms'], stat['height_PV']),
                                 saved_figures_tmp[1], scale=height_scale)

                saved_figures.extend(saved_figures_tmp)

        saved_figures_tmp = [os.path.join(result_path, '{}_slope_profile_psd.png'.format(subfolder)),
                             os.path.join(result_path, '{}_height_profile_psd.png'.format(subfolder))]

        # save psd figures
        self.save_psd(Rawdata_dict['X'], Rawdata_dict['slope'], 'Frequency [mm$^{-1}$]', 'Spectrum [a.u.]', 'slope profile PSD', saved_figures_tmp[0])
        self.save_psd(Rawdata_dict['X'], data_dict['height_profile'], 'Frequency [mm$^{-1}$]', 'Spectrum [a.u.]', 'height profile PSD', saved_figures_tmp[0])

        saved_figures.extend(saved_figures_tmp)

        return saved_figures

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

from aps.common.scripts.generic_process_manager import GenericProcessManager
from aps.common.widgets.context_widget import PlottingProperties
from aps.common.plotter import get_registered_plotter_instance
from aps.common.initializer import get_registered_ini_instance
from aps.common.logger import get_registered_logger_instance
from aps.common.scripts.script_data import ScriptData

from aps.metrology.ltp.kb.widgets.ALK_start_data_analysis_widget import ALKStartDataAnalysisWidget
from aps.metrology.ltp.kb.widgets.ALK_display_results_widget import ALKDisplayResultDialog

APPLICATION_NAME = "Automate LTP - KB"

INITIALIZATION_PARAMETERS_KEY  = "Automate LTP - KB Initialization"
START_DATA_ANALYSIS            = "Start Data Analysis"
DISPLAY_RESULTS                = "Display Results"

class AutomateLTPKBFacade(GenericProcessManager):
    def start_data_analysis(self, initialization_parameters, plotting_properties=PlottingProperties(), **kwargs): raise NotImplementedError()
    def display_results(self, data_analysis_parameters, plotting_properties=PlottingProperties(), **kwargs): raise NotImplementedError()

def create_automate_ltp_kb_manager(**kwargs): return _AutomateLTPKB(**kwargs)


def generate_initialization_parameters_alk(folder_monitor,
                                           folder_saving,
                                           force_process,
                                           mirror_direction,
                                           slope_ch_sign,
                                           polyfit,
                                           mirror,
                                           P,
                                           Q,
                                           theta,
                                           fix,
                                           fitting_equation,
                                           reverse,
                                           mirror_length,
                                           filter_size,
                                           N_num,
                                           check_time,
                                           max_waiting_cycles,
                                           display_results,
                                           height_profile_scale,
                                           height_error_scale,
                                           height_error_p1_scale,
                                           height_error_p3_scale,
                                           height_error_p5_scale,
                                           slope_profile_scale,
                                           slope_error_scale,
                                           slope_error_p1_scale,
                                           slope_error_p3_scale,
                                           slope_error_p5_scale):
    if not os.path.exists(folder_monitor): raise ValueError("Folder Monitor does not exist")
    if not os.path.exists(folder_saving): os.mkdir(folder_saving)

    return ScriptData(folder_monitor=folder_monitor,
                      folder_saving=folder_saving,
                      force_process=force_process,
                      mirror_direction=mirror_direction,
                      slope_ch_sign=slope_ch_sign,
                      polyfit=polyfit,
                      mirror=mirror,
                      P=P,
                      Q=Q,
                      theta=theta,
                      fix=fix,
                      fitting_equation=fitting_equation,
                      reverse=reverse,
                      mirror_length=mirror_length,
                      filter_size=filter_size,
                      N_num=N_num,
                      check_time=check_time,
                      max_waiting_cycles=max_waiting_cycles,
                      display_results=display_results,
                      height_profile_scale=height_profile_scale,
                      height_error_scale=height_error_scale,
                      height_error_p1_scale=height_error_p1_scale,
                      height_error_p3_scale=height_error_p3_scale,
                      height_error_p5_scale=height_error_p5_scale,
                      slope_profile_scale=slope_profile_scale,
                      slope_error_scale=slope_error_scale,
                      slope_error_p1_scale=slope_error_p1_scale,
                      slope_error_p3_scale=slope_error_p3_scale,
                      slope_error_p5_scale=slope_error_p5_scale,
                      file_prefix="automate_ltp,_kb")


class _AutomateLTPKB(AutomateLTPKBFacade):
    def __init__(self, **kwargs):
        self.reload_utils()

        self.__log_stream_widget = kwargs.get("log_stream_widget")

    def reload_utils(self):
        self.__plotter = get_registered_plotter_instance(application_name=APPLICATION_NAME)
        self.__logger  = get_registered_logger_instance(application_name=APPLICATION_NAME)
        self.__ini     = get_registered_ini_instance(application_name=APPLICATION_NAME)

    # %% ==================================================================================================

    def manage_initialization(self, initialization_parameters):
        self.__plotter.register_save_file_prefix(initialization_parameters.get_parameter("file_prefix"))

        return initialization_parameters

    def start_data_analysis(self, plotting_properties=PlottingProperties(), **kwargs):
        add_context_label = plotting_properties.get_parameter("add_context_label", True)
        use_unique_id     = plotting_properties.get_parameter("use_unique_id", False)

        initialization_parameters = generate_initialization_parameters_alk(folder_monitor=self.__ini.get_string_from_ini("Folders", "monitor folder"),
                                                                           folder_saving=self.__ini.get_string_from_ini("Folders", "saving folder"),
                                                                           force_process=self.__ini.get_boolean_from_ini("Input", "force process", default=False),
                                                                           mirror_direction=self.__ini.get_int_from_ini("Input", "mirror direction", default=3),
                                                                           slope_ch_sign=self.__ini.get_list_from_ini("Input", "sign of slopes", default=[0, 0, -1, 0, 0, 1], type=int),
                                                                           polyfit=self.__ini.get_list_from_ini("Input", "polynomial order to remove", default=[1, 3, 5], type=int),
                                                                           mirror=self.__ini.get_string_from_ini("Input", "mirror type", default="flat"),
                                                                           P=self.__ini.get_float_from_ini("Input", "p", default=67.02633),
                                                                           Q=self.__ini.get_float_from_ini("Input", "q", default=0.17367),
                                                                           theta=self.__ini.get_float_from_ini("Input", "theta", default=0.003),
                                                                           fix=self.__ini.get_list_from_ini("Input", "fixed parameters", default=[1, 1, 0], type=int),
                                                                           fitting_equation=self.__ini.get_string_from_ini("Input", "fitting equation", default="height"),
                                                                           reverse=self.__ini.get_boolean_from_ini("Input", "reverse", default=False),
                                                                           mirror_length=self.__ini.get_float_from_ini("Input", "mirror length", default=63.5),
                                                                           filter_size=self.__ini.get_list_from_ini("Input", "polynomial fit filter", default=[0, 0, 0, 8, 0, 0], type=int),
                                                                           N_num=self.__ini.get_int_from_ini("Input", "Nr of scan passes", default=-1),
                                                                           check_time=self.__ini.get_int_from_ini("Monitor", "check time", default=15),
                                                                           max_waiting_cycles=self.__ini.get_int_from_ini("Monitor", "max waiting cycles", default=10),
                                                                           display_results=self.__ini.get_boolean_from_ini("Output", "display results", default=True),
                                                                           height_profile_scale=self.__ini.get_list_from_ini("Graphics", "height profile range", default=[0.0, 3000.0], type=float),
                                                                           height_error_scale=self.__ini.get_list_from_ini("Graphics", "height error range", default=[-3500.0, 1500.0], type=float),
                                                                           height_error_p1_scale=self.__ini.get_list_from_ini("Graphics", "height error p1 range", default=[-30.0, 30.0], type=float),
                                                                           height_error_p3_scale=self.__ini.get_list_from_ini("Graphics", "height error p3 range", default=[-0.5, 0.5], type=float),
                                                                           height_error_p5_scale=self.__ini.get_list_from_ini("Graphics", "height error p5 range", default=[-0.5, 0.5], type=float),
                                                                           slope_profile_scale=self.__ini.get_list_from_ini("Graphics", "slope profile range", default=[-150.0, 150.0], type=float),
                                                                           slope_error_scale=self.__ini.get_list_from_ini("Graphics", "slope error range", default=[-150.0, 150.0], type=float),
                                                                           slope_error_p1_scale=self.__ini.get_list_from_ini("Graphics", "slope error p1 range", default=[-3.0, 1.5], type=float),
                                                                           slope_error_p3_scale=self.__ini.get_list_from_ini("Graphics", "slope error p3 range", default=[-0.3, 0.3], type=float),
                                                                           slope_error_p5_scale=self.__ini.get_list_from_ini("Graphics", "slope error p5 range", default=[-0.3, 0.3], type=float))

        self.__plotter.register_context_window(START_DATA_ANALYSIS,
                                               context_window=plotting_properties.get_context_widget(),
                                               use_unique_id=use_unique_id)

        self.__plotter.push_plot_on_context(START_DATA_ANALYSIS, ALKStartDataAnalysisWidget, None,
                                            log_stream_widget=self.__log_stream_widget,
                                            initialization_parameters=initialization_parameters,
                                            execute_method=self.execute_analysis,
                                            close_method=self.close_analysis,
                                            allows_saving=False,
                                            **kwargs)

        self.__plotter.draw_context(START_DATA_ANALYSIS, add_context_label=add_context_label, unique_id=None, **kwargs)
        self.__plotter.show_context_window(START_DATA_ANALYSIS)

    def execute_analysis(self, initialization_parameters, **kwargs):
        self.__ini.set_value_at_ini("Input",  "force process",              value=initialization_parameters.get_parameter("force_process"))
        self.__ini.set_value_at_ini("Input",  "mirror direction",           value=initialization_parameters.get_parameter("mirror_direction"))
        self.__ini.set_list_at_ini( "Input",  "sign of slopes",             values_list=initialization_parameters.get_parameter("slope_ch_sign"))
        self.__ini.set_list_at_ini( "Input",  "polynomial order to remove", values_list=initialization_parameters.get_parameter("polyfit"))
        self.__ini.set_value_at_ini("Input",  "mirror type",                value=initialization_parameters.get_parameter("mirror"))
        self.__ini.set_value_at_ini("Input",  "p",                          value=initialization_parameters.get_parameter("P"))
        self.__ini.set_value_at_ini("Input",  "q",                          value=initialization_parameters.get_parameter("Q"))
        self.__ini.set_value_at_ini("Input",  "theta",                      value=initialization_parameters.get_parameter("theta"))
        self.__ini.set_list_at_ini( "Input",  "fixed parameters",           values_list=initialization_parameters.get_parameter("fix"))
        self.__ini.set_value_at_ini("Input",  "fitting equation",           value=initialization_parameters.get_parameter("fitting_equation"))
        self.__ini.set_value_at_ini("Input",  "reverse",                    value=initialization_parameters.get_parameter("reverse"))
        self.__ini.set_value_at_ini("Input", "mirror length",               value=initialization_parameters.get_parameter("mirror_length"))
        self.__ini.set_list_at_ini( "Input", "polynomial fit filter",       values_list=initialization_parameters.get_parameter("filter_size"))
        self.__ini.set_value_at_ini("Input", "Nr of scan passes",           value=initialization_parameters.get_parameter("N_num"))
        self.__ini.set_value_at_ini("Monitor", "check time",                value=initialization_parameters.get_parameter("check_time"))
        self.__ini.set_value_at_ini("Monitor", "max waiting cycles",        value=initialization_parameters.get_parameter("max_waiting_cycles"))
        self.__ini.set_value_at_ini("Output", "display results",            value=initialization_parameters.get_parameter("display_results"))
        self.__ini.set_list_at_ini( "Graphics",  "height profile range",    values_list=initialization_parameters.get_parameter("height_profile_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "height error range",      values_list=initialization_parameters.get_parameter("height_error_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "height error p1 range",   values_list=initialization_parameters.get_parameter("height_error_p1_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "height error p3 range",   values_list=initialization_parameters.get_parameter("height_error_p3_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "height error p5 range",   values_list=initialization_parameters.get_parameter("height_error_p5_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "slope profile range",     values_list=initialization_parameters.get_parameter("slope_profile_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "slope error range",       values_list=initialization_parameters.get_parameter("slope_error_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "slope error p1 range",    values_list=initialization_parameters.get_parameter("slope_error_p1_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "slope error p3 range",    values_list=initialization_parameters.get_parameter("slope_error_p3_scale"))
        self.__ini.set_list_at_ini( "Graphics",  "slope error p5 range",    values_list=initialization_parameters.get_parameter("slope_error_p5_scale"))

        self.__ini.push()

        try:
            self.data_analysis_thread = DataAnalysisThread(self.__log_stream_widget.get_widget(), initialization_parameters)
            self.data_analysis_thread.begin.connect(self.__data_analysis_begin)
            self.data_analysis_thread.print_signal.connect(self.__print)
            self.data_analysis_thread.print_message_signal.connect(self.__print_message)
            self.data_analysis_thread.print_warning_signal.connect(self.__print_warning)
            self.data_analysis_thread.print_error_signal.connect(self.__print_error)
            self.data_analysis_thread.update.connect(self.__data_analysis_update)
            self.data_analysis_thread.finish.connect(self.__data_analysis_completed)
            self.data_analysis_thread.start()
        except Exception as e:
            raise e

    def close_analysis(self, initialization_parameters, **kwargs):
        self.__plotter.get_context_container_widget(context_key=START_DATA_ANALYSIS).parent().close()
        sys.exit(0)

    def __data_analysis_begin(self):
        self.__logger.print_message("Begin Data Analysis")

    def __print(self, text):
        self.__logger.print(text)

    def __print_message(self, text):
        self.__logger.print_message(text)

    def __print_warning(self, text):
        self.__logger.print_warning(text)

    def __print_error(self, text):
        self.__logger.print_error(text)

    def __data_analysis_update(self):
        self.__logger.print_message("Data Analysis: new waiting cycle")

    def __data_analysis_completed(self, saved_figures, initialization_parameters):
        self.__logger.print_message("Data Analysis Completed")

        if len(saved_figures) > 0 and initialization_parameters.get_parameter("display_results") == True:
            self.display_results(data_analysis_parameters=ScriptData(saved_figures=saved_figures))

    def display_results(self, data_analysis_parameters, plotting_properties=PlottingProperties(), **kwargs):
        if self.__plotter.is_active():
            self.__plotter.show_interactive_plot(ALKDisplayResultDialog,
                                                 container_widget=plotting_properties.get_container_widget(),
                                                 saved_figures=data_analysis_parameters.get_parameter("saved_figures"),
                                                 **kwargs)

import time
from PyQt5.QtCore import QThread, pyqtSignal

class DataAnalysisThread(QThread):

    begin                = pyqtSignal()
    update               = pyqtSignal()
    print_signal = pyqtSignal(str)
    print_message_signal = pyqtSignal(str)
    print_warning_signal = pyqtSignal(str)
    print_error_signal   = pyqtSignal(str)
    finish               = pyqtSignal(list, object)
    
    def __init__(self, logger_widget, initialization_parameters):
        super(DataAnalysisThread, self).__init__(logger_widget)
        self.__initialization_parameters = initialization_parameters

    def run(self):
        try:
            self.begin.emit()

            folder_monitor = self.__initialization_parameters.get_parameter("folder_monitor")
            folder_saving  = self.__initialization_parameters.get_parameter("folder_saving")

            mirror_parameters = {
                'force_process': self.__initialization_parameters.get_parameter("force_process"),
                'mirror_direction': self.__initialization_parameters.get_parameter("mirror_direction"),
                'slope_ch_sign': self.__initialization_parameters.get_parameter("slope_ch_sign"),
                'polyfit': self.__initialization_parameters.get_parameter("polyfit"),  
                'mirror': self.__initialization_parameters.get_parameter("mirror"),
                'P': self.__initialization_parameters.get_parameter("P"),  
                'Q': self.__initialization_parameters.get_parameter("Q"),  
                'theta': self.__initialization_parameters.get_parameter("theta"),  
                'fix': self.__initialization_parameters.get_parameter("fix"), 
                'fitting_equation': self.__initialization_parameters.get_parameter("fitting_equation"),  
                'reverse': self.__initialization_parameters.get_parameter("reverse"), 
                'mirror_length': self.__initialization_parameters.get_parameter("mirror_length"),  
                'filter_size': self.__initialization_parameters.get_parameter("filter_size"), 
                'N_num': self.__initialization_parameters.get_parameter("N_num")
            }

            figure_scales = FigureScales()
            figure_scales.height_profile_scale  = self.__initialization_parameters.get_parameter("height_profile_scale")
            figure_scales.height_error_scale    = self.__initialization_parameters.get_parameter("height_error_scale")
            figure_scales.height_error_p1_scale = self.__initialization_parameters.get_parameter("height_error_p1_scale")
            figure_scales.height_error_p3_scale = self.__initialization_parameters.get_parameter("height_error_p3_scale")
            figure_scales.height_error_p5_scale = self.__initialization_parameters.get_parameter("height_error_p5_scale")
            figure_scales.slope_profile_scale   = self.__initialization_parameters.get_parameter("slope_profile_scale")
            figure_scales.slope_error_scale     = self.__initialization_parameters.get_parameter("slope_error_scale")
            figure_scales.slope_error_p1_scale  = self.__initialization_parameters.get_parameter("slope_error_p1_scale")
            figure_scales.slope_error_p3_scale  = self.__initialization_parameters.get_parameter("slope_error_p3_scale")
            figure_scales.slope_error_p5_scale  = self.__initialization_parameters.get_parameter("slope_error_p5_scale")
            figure_scales.check_scales()

            data_extractor = AverageDataExtractor(mirror_parameters=mirror_parameters, logger=self)
            data_fit       = DataFitter(mirror_parameters=mirror_parameters, logger=self)
            data_save      = DataManager(saving_path=folder_saving, mirror_parameters=mirror_parameters, logger=self, figure_scales=figure_scales)

            check_time = self.__initialization_parameters.get_parameter("check_time")
            max_waiting_cycles = self.__initialization_parameters.get_parameter("max_waiting_cycles")

            skip_file      = []
            n_waiting_cycles = 0

            saved_figures = []

            while (n_waiting_cycles < max_waiting_cycles if max_waiting_cycles > 0 else True):
                mda_file_list = check_new_file(folder_monitor,
                                               folder_saving,
                                               force_process=mirror_parameters['force_process'],
                                               file_extension='*.mda',
                                               logger=self)

                if len(mda_file_list) != 0:
                    for mda_file in mda_file_list:
                        if mda_file in skip_file: continue
                        # convert mda to ascii file
                        convert_mda(mda_file, self)
                        try:
                            Rawdata_dict = data_extractor.data_extract(mda_file)
                            fitting_dict = data_fit.fitting(Rawdata_dict)
                            file_name = os.path.basename(mda_file).split('.')[0]
                            data_save.save_data(file_name, Rawdata_dict, fitting_dict, data_fit)
                            saved_figures.extend(data_save.save_figures(file_name, Rawdata_dict, fitting_dict, data_extractor))
                        except Exception as e:
                            raise e
                            self.print_error('error in file: {}'.format(mda_file))
                            skip_file.append(mda_file)

                self.print_message('waiting {}s for new data...'.format(check_time))

                time.sleep(check_time)

                n_waiting_cycles += 1

                self.update.emit()

            self.finish.emit(saved_figures, self.__initialization_parameters)
        except Exception as exception:
            self.print_error('Exception occured: {}'.format(str(exception)))

            self.finish.emit([], self.__initialization_parameters)

    def print(self, text):
        self.print_signal.emit(text)

    def print_message(self, text):
        self.print_message_signal.emit(text)

    def print_warning(self, text):
        self.print_warning_signal.emit(text)

    def print_error(self, text):
        self.print_error_signal.emit(text)
