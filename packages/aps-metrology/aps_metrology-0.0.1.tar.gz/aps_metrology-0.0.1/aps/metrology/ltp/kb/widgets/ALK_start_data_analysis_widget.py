#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2023, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2023. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# ----------------------------------------------------------------------- #
from aps.common.initializer import get_registered_ini_instance
from aps.common.plot import gui
from aps.common.widgets.generic_widget import GenericWidget

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class ALKStartDataAnalysisWidget(GenericWidget):
    MIRRORS = ["flat", "ellipse"]
    FITTING_EQUATIONS = ["slope", "height"]

    def __init__(self, parent, application_name=None, **kwargs):
        super(ALKStartDataAnalysisWidget, self).__init__(parent=parent, application_name=application_name, **kwargs)

        self.__ini              = get_registered_ini_instance(application_name=application_name)

        self.__log_stream_widget         = kwargs["log_stream_widget"]
        self.__execute_method            = kwargs["execute_method"]
        self.__close_method              = kwargs["close_method"]
        self.__initialization_parameters = kwargs["initialization_parameters"]

        self.folder_monitor = self.__ini.get_string_from_ini("Folders", "monitor folder")
        self.folder_saving  = self.__ini.get_string_from_ini("Folders", "saving folder")

        self.force_process    = self.__initialization_parameters.get_parameter("force_process")
        self.mirror_direction = self.__initialization_parameters.get_parameter("mirror_direction") - 1

        slope_ch_sign = self.__initialization_parameters.get_parameter("slope_ch_sign")

        self.slope_ch_sign_1 = slope_ch_sign[0]
        self.slope_ch_sign_2 = slope_ch_sign[1]
        self.slope_ch_sign_3 = slope_ch_sign[2]
        self.slope_ch_sign_4 = slope_ch_sign[3]
        self.slope_ch_sign_5 = slope_ch_sign[4]
        self.slope_ch_sign_6 = slope_ch_sign[5]

        polyfit = self.__initialization_parameters.get_parameter("polyfit")

        self.polyfit = ""
        for i in range(len(polyfit)): self.polyfit += str(polyfit[i]) + (", " if (i < len(polyfit)-1) else "")

        mirror = self.__initialization_parameters.get_parameter("mirror")
        self.mirror = self.MIRRORS.index(mirror)

        self.P     = self.__initialization_parameters.get_parameter("P")
        self.Q     = self.__initialization_parameters.get_parameter("Q")
        self.theta = self.__initialization_parameters.get_parameter("theta")

        fix = self.__initialization_parameters.get_parameter("fix")
        self.fix_P     = fix[0]
        self.fix_Q     = fix[1]
        self.fix_theta = fix[2]

        self.fitting_equation = self.FITTING_EQUATIONS.index(self.__initialization_parameters.get_parameter("fitting_equation"))

        self.reverse          = self.__initialization_parameters.get_parameter("reverse")
        self.mirror_length    = self.__initialization_parameters.get_parameter("mirror_length")

        filter_size = self.__initialization_parameters.get_parameter("filter_size")

        self.filter_size_1 = filter_size[0]
        self.filter_size_2 = filter_size[1]
        self.filter_size_3 = filter_size[2]
        self.filter_size_4 = filter_size[3]
        self.filter_size_5 = filter_size[4]
        self.filter_size_6 = filter_size[5]

        self.N_num              = self.__initialization_parameters.get_parameter("N_num")
        self.check_time         = self.__initialization_parameters.get_parameter("check_time")
        self.max_waiting_cycles = self.__initialization_parameters.get_parameter("max_waiting_cycles")
        self.display_results    = self.__initialization_parameters.get_parameter("display_results")

        self.height_profile_scale_1 , self.height_profile_scale_2  = self.__initialization_parameters.get_parameter("height_profile_scale")
        self.height_error_scale_1   , self.height_error_scale_2    = self.__initialization_parameters.get_parameter("height_error_scale")
        self.height_error_p1_scale_1, self.height_error_p1_scale_2 = self.__initialization_parameters.get_parameter("height_error_p1_scale")
        self.height_error_p3_scale_1, self.height_error_p3_scale_2 = self.__initialization_parameters.get_parameter("height_error_p3_scale")
        self.height_error_p5_scale_1, self.height_error_p5_scale_2 = self.__initialization_parameters.get_parameter("height_error_p5_scale")
        self.slope_profile_scale_1  , self.slope_profile_scale_2   = self.__initialization_parameters.get_parameter("slope_profile_scale")
        self.slope_error_scale_1    , self.slope_error_scale_2     = self.__initialization_parameters.get_parameter("slope_error_scale")
        self.slope_error_p1_scale_1 , self.slope_error_p1_scale_2  = self.__initialization_parameters.get_parameter("slope_error_p1_scale")
        self.slope_error_p3_scale_1 , self.slope_error_p3_scale_2  = self.__initialization_parameters.get_parameter("slope_error_p3_scale")
        self.slope_error_p5_scale_1 , self.slope_error_p5_scale_2  = self.__initialization_parameters.get_parameter("slope_error_p5_scale")

    def get_plot_tab_name(self): return "Automated LTP-KB Data Analysis"

    def build_widget(self, **kwargs):
        geom = QApplication.desktop().availableGeometry()

        try:    widget_width = kwargs["widget_width"]
        except: widget_width = min(1450, geom.width()*0.98)
        try:    widget_height = kwargs["widget_height"]
        except: widget_height = min(750, geom.height()*0.95)

        self.setGeometry(QRect(10,
                               10,
                               widget_width,
                               widget_height))

        self.setFixedWidth(widget_width)
        self.setFixedHeight(widget_height)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)


        main_box = gui.widgetBox(self, "", width=450, height=self.height()-20)
        log_box  = gui.widgetBox(self, "", width=self.width()-470, height=self.height()-15)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        log_box.setLayout(layout)
        log_box.layout().addWidget(self.__log_stream_widget.get_widget())
        self.__log_stream_widget.set_widget_size(width=log_box.width(), height=log_box.height())

        button_box = gui.widgetBox(main_box, "", width=main_box.width(), orientation='horizontal')
        button_box.layout().setAlignment(Qt.AlignCenter)

        gui.button(button_box, None, "Execute Analysis", callback=self.__execute_callback, width=220, height=35)
        button = gui.button(button_box, None, "Exit Program", callback=self.__close_callback, width=210, height=35)
        font = QFont(button.font())
        font.setBold(True)
        font.setItalic(True)
        button.setFont(font)
        palette = QPalette(button.palette())  # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('Red'))
        button.setPalette(palette)  # assign new palette

        gui.separator(main_box)

        tab_widget = gui.tabWidget(main_box)

        tab_0 = gui.createTabPage(tab_widget, "Folders")
        tab_1 = gui.createTabPage(tab_widget, "Analysis")
        tab_2 = gui.createTabPage(tab_widget, "Graphics")

        select_folder_monitor_box = gui.widgetBox(tab_0, orientation="horizontal")
        self.le_folder_monitor = gui.lineEdit(select_folder_monitor_box, self, "folder_monitor", label="Folder Monitor", labelWidth=150, valueType=str, orientation="vertical")
        gui.button(select_folder_monitor_box, self, "...", width=30, callback=self.selectFolderMonitor)

        select_folder_saving_box = gui.widgetBox(tab_0, orientation="horizontal")
        self.le_folder_saving = gui.lineEdit(select_folder_saving_box, self, "folder_saving", label="Folder Saving", labelWidth=150, valueType=str, orientation="vertical")
        gui.button(select_folder_saving_box, self, "...", width=30, callback=self.selectFolderSaving)

        input_box =  gui.widgetBox(tab_1, "Input Parameters", width=main_box.width()-20, height=460, orientation='vertical')

        label_width = 200
        spaces = "                                                          "

        gui.checkBox(input_box, self, "force_process", "Force process")
        gui.comboBox(input_box, self, "mirror_direction", label="Mirror direction", orientation='horizontal', items=["Vertical", "Horizontal", "All Six Channels"])

        gui.separator(input_box)

        def set_mirror_type():
            if self.mirror == 0: ellipse_box.setEnabled(False)
            else: ellipse_box.setEnabled(True)

        gui.comboBox(input_box, self, "mirror", label="Mirror type", orientation='horizontal', items=self.MIRRORS, callback=set_mirror_type)

        ellipse_box = gui.widgetBox(input_box, "", width=input_box.width()-20, orientation='vertical')

        box = gui.widgetBox(ellipse_box, "", orientation='horizontal')
        gui.lineEdit(box, self, "P", "P [mm]", labelWidth=label_width, orientation='horizontal', controlWidth=130, valueType=float)
        gui.checkBox(box, self, "fix_P", "fixed")
        box = gui.widgetBox(ellipse_box, "", orientation='horizontal')
        gui.lineEdit(box, self, "Q", "Q [mm]", labelWidth=label_width, orientation='horizontal', controlWidth=130, valueType=float)
        gui.checkBox(box, self, "fix_Q", "fixed")
        box = gui.widgetBox(ellipse_box, "", orientation='horizontal')
        gui.lineEdit(box, self, "theta", "\u03b8 [rad]", labelWidth=label_width, orientation='horizontal', controlWidth=130, valueType=float)
        gui.checkBox(box, self, "fix_theta", "fixed")

        set_mirror_type()

        gui.lineEdit(input_box, self, "mirror_length", "mirror length [mm]", labelWidth=label_width, controlWidth=130, orientation='horizontal', valueType=float)

        gui.separator(input_box)

        gui.widgetLabel(input_box, spaces + "Hy    Hx    Sy    Sx    Vy    Vx")

        slope_ch_sign_box = gui.widgetBox(input_box, "", width=input_box.width()-55, orientation='horizontal')
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_1", "Sign of slopes from channels", labelWidth=label_width, orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_2", "",                             labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_3", "",                             labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_4", "",                             labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_5", "",                             labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(slope_ch_sign_box, self, "slope_ch_sign_6", "",                             labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)

        gui.lineEdit(input_box, self, "polyfit", "Polynomial order to remove", labelWidth=label_width, orientation='horizontal', controlWidth=130, valueType=str)

        gui.comboBox(input_box, self, "fitting_equation", label="Fitting equation", orientation='horizontal', items=self.FITTING_EQUATIONS)
        gui.checkBox(input_box, self, "reverse", "Reverse (False is left is upstream)")

        gui.widgetLabel(input_box, spaces + "Hy    Hx    Sy    Sx    Vy    Vx")

        filter_size_box = gui.widgetBox(input_box, "", width=input_box.width()-55, orientation='horizontal')
        gui.lineEdit(filter_size_box, self, "filter_size_1", "Polynomial fit filter", labelWidth=label_width, orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(filter_size_box, self, "filter_size_2", "",                      labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(filter_size_box, self, "filter_size_3", "",                      labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(filter_size_box, self, "filter_size_4", "",                      labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(filter_size_box, self, "filter_size_5", "",                      labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)
        gui.lineEdit(filter_size_box, self, "filter_size_6", "",                      labelWidth=2,   orientation='horizontal', controlWidth=25, valueType=int)

        gui.separator(input_box)

        gui.lineEdit(input_box, self, "N_num", "Use how many passes (-1 all)", labelWidth=label_width, orientation='horizontal', controlWidth=40, valueType=int)

        monitor_box =  gui.widgetBox(tab_1, "Monitor Parameters", width=main_box.width()-20, orientation='vertical')

        gui.lineEdit(monitor_box, self, "check_time", "Time interval between cycles (s)", labelWidth=label_width, orientation='horizontal', controlWidth=40, valueType=int)
        gui.lineEdit(monitor_box, self, "max_waiting_cycles", "Max # of cycles (-1 = no limit)", labelWidth=label_width, orientation='horizontal', controlWidth=40, valueType=int)

        output_box =  gui.widgetBox(tab_1, "Output Parameters", width=main_box.width()-20, orientation='vertical')

        gui.checkBox(output_box, self, "display_results", "Display figures after completion")

        # TAB 2 --------------------------------------------------------------

        input_box =  gui.widgetBox(tab_2, "Graphic Parameters", width=main_box.width()-20, height=460, orientation='vertical')

        gui.widgetLabel(input_box, "Scale                                        Min                     Max")

        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "height_profile_scale_1", "Height Profile",   labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "height_profile_scale_2", "",                 labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "height_error_scale_1", "Height Error",       labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "height_error_scale_2", "",                   labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "height_error_p1_scale_1", "Height Error P1", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "height_error_p1_scale_2", "",                labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "height_error_p3_scale_1", "Height Error P3", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "height_error_p3_scale_2", "",                labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "height_error_p5_scale_1", "Height Error P4", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "height_error_p5_scale_2", "",                labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        
        gui.separator(input_box)

        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "slope_profile_scale_1", "Slope Profile",   labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "slope_profile_scale_2", "",                labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "slope_error_scale_1", "Slope Error",       labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "slope_error_scale_2", "",                  labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "slope_error_p1_scale_1", "Slope Error P1", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "slope_error_p1_scale_2", "",               labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "slope_error_p3_scale_1", "Slope Error P3", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "slope_error_p3_scale_2", "",               labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)
        graphics_box = gui.widgetBox(input_box, "", width=360, orientation='horizontal')
        gui.lineEdit(graphics_box, self, "slope_error_p5_scale_1", "Slope Error P4", labelWidth=label_width, orientation='horizontal', controlWidth=90, valueType=float)
        gui.lineEdit(graphics_box, self, "slope_error_p5_scale_2", "",               labelWidth=2,   orientation='horizontal', controlWidth=90, valueType=float)


    def selectFolderMonitor(self):
        self.le_folder_monitor.setText(gui.selectDirectoryFromDialog(self, self.folder_monitor, "Select Folder Monitor"))

    def selectFolderSaving(self):
        self.le_folder_saving.setText(gui.selectDirectoryFromDialog(self, self.folder_saving, "Select Folder Saving"))

    def __execute_callback(self, **kwargs):
        self.__initialization_parameters.set_parameter("folder_monitor", self.folder_monitor)
        self.__initialization_parameters.set_parameter("folder_saving",  self.folder_saving)

        slope_ch_sign = [self.slope_ch_sign_1, self.slope_ch_sign_2, self.slope_ch_sign_3, self.slope_ch_sign_4, self.slope_ch_sign_5, self.slope_ch_sign_6]
        filter_size   = [self.filter_size_1, self.filter_size_2, self.filter_size_3, self.filter_size_4, self.filter_size_5, self.filter_size_6]

        polyfit = []
        for token in self.polyfit.split(sep=","):
            if token.strip() != '': polyfit.append(int(token))
        fix = [self.fix_P, self.fix_Q, self.fix_theta]

        self.__initialization_parameters.set_parameter("force_process", self.force_process)
        self.__initialization_parameters.set_parameter("mirror_direction", self.mirror_direction+1)
        self.__initialization_parameters.set_parameter("slope_ch_sign", slope_ch_sign)
        self.__initialization_parameters.set_parameter("polyfit", polyfit)
        self.__initialization_parameters.set_parameter("mirror", self.MIRRORS[self.mirror])
        self.__initialization_parameters.set_parameter("P", self.P)
        self.__initialization_parameters.set_parameter("Q", self.Q)
        self.__initialization_parameters.set_parameter("theta", self.theta)
        self.__initialization_parameters.set_parameter("fix", fix)
        self.__initialization_parameters.set_parameter("fitting_equation", self.FITTING_EQUATIONS[self.fitting_equation])
        self.__initialization_parameters.set_parameter("reverse", self.reverse)
        self.__initialization_parameters.set_parameter("mirror_length", self.mirror_length)
        self.__initialization_parameters.set_parameter("filter_size", filter_size)
        self.__initialization_parameters.set_parameter("N_num", self.N_num)
        self.__initialization_parameters.set_parameter("check_time", self.check_time)
        self.__initialization_parameters.set_parameter("max_waiting_cycles", self.max_waiting_cycles)
        self.__initialization_parameters.set_parameter("display_results", self.display_results)

        self.__initialization_parameters.set_parameter("height_profile_scale",  [self.height_profile_scale_1 , self.height_profile_scale_2 ])
        self.__initialization_parameters.set_parameter("height_error_scale",    [self.height_error_scale_1   , self.height_error_scale_2   ])
        self.__initialization_parameters.set_parameter("height_error_p1_scale", [self.height_error_p1_scale_1, self.height_error_p1_scale_2])
        self.__initialization_parameters.set_parameter("height_error_p3_scale", [self.height_error_p3_scale_1, self.height_error_p3_scale_2])
        self.__initialization_parameters.set_parameter("height_error_p5_scale", [self.height_error_p5_scale_1, self.height_error_p5_scale_2])
        self.__initialization_parameters.set_parameter("slope_profile_scale",   [self.slope_profile_scale_1  , self.slope_profile_scale_2  ])
        self.__initialization_parameters.set_parameter("slope_error_scale",     [self.slope_error_scale_1    , self.slope_error_scale_2    ])
        self.__initialization_parameters.set_parameter("slope_error_p1_scale",  [self.slope_error_p1_scale_1 , self.slope_error_p1_scale_2 ])
        self.__initialization_parameters.set_parameter("slope_error_p3_scale",  [self.slope_error_p3_scale_1 , self.slope_error_p3_scale_2 ])
        self.__initialization_parameters.set_parameter("slope_error_p5_scale",  [self.slope_error_p5_scale_1 , self.slope_error_p5_scale_2 ])

        self.__execute_method(self.__initialization_parameters, **kwargs)

    def __close_callback(self, **kwargs):
        if gui.ConfirmDialog.confirmed(self, "Confirm Exit?"): self.__close_method(self.__initialization_parameters, **kwargs)
