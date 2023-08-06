#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------- #
# Copyright (c) 2022, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2022. UChicago Argonne, LLC. This software was produced       #
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

'''
        if not script_logger_mode == LoggerMode.NONE: stream = open(self.__plotter.get_save_file_prefix() + "_" + datetime_now_str() + ".log", "wt")
        else: stream = None

'''

from aps.metrology.ltp.kb.bl.automate_LTP_KB import create_automate_ltp_kb_manager, APPLICATION_NAME, START_DATA_ANALYSIS

from aps.common.initializer import get_registered_ini_instance
from aps.common.logger import register_logger_pool_instance, register_logger_single_instance
from aps.common.plotter import get_registered_plotter_instance
from aps.common.plot.qt_application import get_registered_qt_application_instance
from aps.common.scripts.generic_qt_script import GenericQTScript
from aps.common.io.printout import datetime_now_str
from aps.common.widgets.log_stream_widget import LogStreamWidget


class MainAutomateLTPKB(GenericQTScript):
    SCRIPT_ID = "automate-ltp-kb"

    def _get_script_id(self): return MainAutomateLTPKB.SCRIPT_ID
    def _get_ini_file_name(self): return ".automate_ltp_kb.ini"
    def _get_application_name(self): return APPLICATION_NAME
    def _get_script_package(self): return "aps.metrology"

    def _run_script(self, **args):
        automate_ltp_kb_manager = create_automate_ltp_kb_manager(log_stream_widget=self._log_stream_widget)

        # ==========================================================================
        # %% Initialization parameters
        # ==========================================================================

        automate_ltp_kb_manager.start_data_analysis()

        # ==========================================================================
        # %% Final Operations
        # ==========================================================================

        get_registered_ini_instance(self._get_application_name()).push()

        # ==========================================================================
        plotter = get_registered_plotter_instance(APPLICATION_NAME)

        get_registered_qt_application_instance().show_application_closer()

        plotter.raise_context_window(context_key=START_DATA_ANALYSIS)

        get_registered_qt_application_instance().run_qt_application()

    def _parse_additional_sys_argument(self, sys_argument, args):
        if "-m" == sys_argument[:2]: args["LOG_POOL"] = int(sys_argument[2:])
        else: args["LOG_POOL"] = 0

    def _help_additional_parameters(self):
        help = "  -m<use multiple loggers>\n"
        help += "   use multiple loggers:\n" + \
                "     0 No (on GUI only) - Default value\n" + \
                "     1 on GUI and on File\n"
        return help

    def _register_logger_instance(self, logger_mode, application_name, **args):
        self._log_stream_widget = LogStreamWidget(width=850, height=400, color='\'light grey\'')

        if args.get("LOG_POOL") == 0 or args.get("LOG_POOL") is None:
            register_logger_single_instance(stream=self._log_stream_widget, logger_mode=logger_mode, application_name=application_name)
        else:
            self._log_stream_file   = open("automate_ltp_kb" + "_" + datetime_now_str() + ".log", "wt")

            register_logger_pool_instance(stream_list=[self._log_stream_widget, self._log_stream_file], logger_mode=logger_mode, application_name=application_name)

import os, sys
if __name__=="__main__":
    if os.getenv('LTP_DEBUG', "0") == "1": MainAutomateLTPKB(sys_argv=sys.argv).run_script()
    else: MainAutomateLTPKB().show_help()
