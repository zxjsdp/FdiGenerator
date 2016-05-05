#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Modify Fdi files"""

from __future__ import (print_function, unicode_literals,
                        with_statement)

import os
import sys

import openpyxl
import logging

if sys.version[0] == '2':
    import Tkinter as tk
    import ttk
    import tkFileDialog
    import ScrolledText as st
    from tkColorChooser import askcolor
elif sys.version[0] == '3':
    import tkinter as tk
    from tkinter import ttk
    import tkinter.scrolledtext as st
    from tkinter import filedialog as tkFileDialog
    from tkinter.colorchooser import askcolor

APP_TITLE = 'Fdi Generator'
CHOOSE_COLOR_BUTTON_TEXT = 'Choose Color'
CHOOSE_EXCEL_BUTTON_TEXT = 'Choose Excel File'
DEFALT_CHOOSE_EXCEL_LABEL_TEXT = 'Please choose excel file'
CHOOSE_FDI_BUTTON_TEXT = 'Choose Fdi file'
DEFALT_CHOOSE_FDI_LABEL_TEXT = 'Please choose fdi file'
OUTPUT_FILE_LABEL_TEXT = 'Output fdi file'
DEFAULT_OUTPUT_FILE = 'output.fdi'
EXECUTE_BUTTON_TEXT = 'Execute'


class XlsxFile(object):
    """
    Handel xlsx files and return a matrix of content.
    """
    def __init__(self, excel_file):
        try:
            self.wb = openpyxl.load_workbook(excel_file)
        # Invalid xlsx format
        except openpyxl.utils.exceptions.InvalidFileException as e:
            logging.error("Invalid xlsx format.\n%s" % e)
            sys.exit(1)
        except IOError as e:
            logging.error("No such xlsx file: %s. (%s)" % (excel_file, e))
            sys.exit(1)
        except BaseException as e:
            logging.error(e)
            sys.exit(1)

        # self.ws = self.wb.get_active_sheet()
        self.ws = self.wb.active
        self.ws_title = self.ws.title
        self.matrix = []
        self._get_matrix()

    def _get_matrix(self):
        """Get a two dimensional matrix from the xlsx file."""
        for i, row in enumerate(self.ws.rows):
            row_container = []
            for i, cell in enumerate(row):
                row_container.append(cell.value)
            self.matrix.append(tuple(row_container))


class ColorChooseFrame(tk.Frame):
    """Inner frame used for generating buttons and labels dynamically.

    Usage:
        >>> app = ColorChooseFrame(name_list=['SpeciesA', 'SpeciesB',
        >>>                                   'SpeciesC'])
        >>> app.mainloop()
    """
    def __init__(self, master=None, name_list=[]):
        tk.Frame.__init__(self, master)
        self.name_list = name_list
        # {'name_1': (0, 255, 64), 'name_2': (10, 255, 64)}
        self.choosed_color_dict = {}

        # Create widgets
        self.name_lebels = []
        self.buttons = []
        self.colored_bg_labels = []

        # Create GUI
        self.set_style()
        self.create_widgets()
        self.grid_config()
        self.row_and_column_config()
        self.bind_function()

    def set_style(self):
        """Set custom style for widget."""
        pass

    def create_widgets(self):
        """
        +------------------------------------------------+
        |                                                |
        |                                                |
        +------------------------------------------------+
        |   NAME_1    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_2    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_3    BUTTON    COLORED_BACKGROUND_LABEL |
        |   ...       ...       ...                      |
        |   NAME_n    BUTTON    COLORED_BACKGROUND_LABEL |
        +------------------------------------------------+
        |                                                |
        +------------------------------------------------+
        """
        for name in self.name_list:
            self.name_lebels.append(ttk.Label(self.master, text=name))
            self.buttons.append(ttk.Button(self.master,
                                           text=CHOOSE_COLOR_BUTTON_TEXT))
            self.colored_bg_labels.append(ttk.Label(self.master,
                                                    background='grey'))

    def grid_config(self):
        self.master.grid()
        for i, name in enumerate(self.name_lebels):
            name.grid(row=i, column=0, sticky='we')
            self.buttons[i].grid(row=i, column=1, sticky='e')
            self.colored_bg_labels[i].grid(row=i, column=2, sticky='we')

    def row_and_column_config(self):
        for i, name in enumerate(self.name_lebels):
            self.master.rowconfigure(i, weight=0)
        for i in range(6):
            self.master.columnconfigure(i, weight=1)

    def bind_function(self):
        for i, label in enumerate(self.name_lebels):
            button = self.buttons[i]
            button['command'] = lambda i=i: self._ask_color(i)

    def _ask_color(self, i):
        # ((0, 255, 64), '#00ff40')
        color = askcolor()
        if not color[0]:
            return
        self.choosed_color_dict[self.name_list[i]] = color[0]
        self.colored_bg_labels[i].config(text=str(color[0]) + '\t' +
                                              str(color[1]),
                                         background=color[1],)


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Data
        self.name_list = ['Please select excel file first!!']
        self.excel_matrix = []
        self.fdi_content = ''

        # Create GUI
        self.master.geometry('1200x800')
        self.master.title(APP_TITLE)
        self.set_style()
        self.create_widgets()
        self.grid_config()
        self.row_and_column_config()
        self.bind_functions()

    def set_style(self):
        """Set custom style for widget."""
        s = ttk.Style()
        # Configure button style
        s.configure('TButton', padding=5)
        s.configure('TLable', padding=5)
        s.configure('TEntry', padding=5)

    def create_widgets(self):
        """
        +------------------------------------------------+
        |                                                |
        |                                                |
        +------------------------------------------------+
        |   NAME_1    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_2    BUTTON    COLORED_BACKGROUND_LABEL |
        |   NAME_3    BUTTON    COLORED_BACKGROUND_LABEL |
        |   ...       ...       ...                      |
        |   NAME_n    BUTTON    COLORED_BACKGROUND_LABEL |
        +------------------------------------------------+
        |                                                |
        +------------------------------------------------+
        """
        self.config_pane = ttk.Frame(self.master, padding=8)
        self.color_choose_pane = ttk.Frame(self.master, padding=8)
        self.execute_pane = ttk.Frame(self.master, padding=8)

        # Excel file related lable and button
        self.choose_excel_button = ttk.Button(self.config_pane,
                                              text=CHOOSE_EXCEL_BUTTON_TEXT)
        self.display_excel_var = tk.StringVar()
        self.display_excel_label = ttk.Label(self.config_pane,
                                             textvariable=self.display_excel_var,
                                             style='config.TLabel')
        self.display_excel_var.set(DEFALT_CHOOSE_EXCEL_LABEL_TEXT)

        # Fdi file related lable and button
        self.choose_fdi_button = ttk.Button(self.config_pane,
                                            text=CHOOSE_FDI_BUTTON_TEXT)
        self.display_fdi_var = tk.StringVar()
        self.display_fdi_label = ttk.Label(self.config_pane,
                                           textvariable=self.display_fdi_var)
        self.display_fdi_var.set(DEFALT_CHOOSE_FDI_LABEL_TEXT)

        # Output file line
        self.output_file_label = ttk.Label(self.config_pane,
                                           text=OUTPUT_FILE_LABEL_TEXT)
        self.output_file_entry = ttk.Entry(self.config_pane, )

        self.output_file_entry.insert('0', DEFAULT_OUTPUT_FILE)

        # Dynamically allocated area
        self.dynamic_area = ColorChooseFrame(self.color_choose_pane,
                                             name_list=self.name_list)

        # Execute button
        self.execute_button = ttk.Button(self.execute_pane, text=EXECUTE_BUTTON_TEXT)


    def grid_config(self):
        self.master.grid()

        self.config_pane.grid(row=0, column=0, sticky='wens')
        self.color_choose_pane.grid(row=1, column=0, sticky='wens')
        self.execute_pane.grid(row=2, column=0, sticky='wens')

        self.choose_excel_button.grid(row=0, column=0, sticky='we')
        self.display_excel_label.grid(row=0, column=1, sticky='we')

        self.choose_fdi_button.grid(row=1, column=0, sticky='we')
        self.display_fdi_label.grid(row=1, column=1, sticky='we')

        self.output_file_label.grid(row=2, column=0, sticky='we')
        self.output_file_entry.grid(row=2, column=1, sticky='we')

        self.dynamic_area.grid(row=0, column=0, columnspan=6, sticky='wens')

        self.execute_button.grid(row=0, column=0, sticky='we')


    def row_and_column_config(self):
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=0)
        self.master.rowconfigure(0, weight=0)
        for i in range(6):
            self.master.columnconfigure(0, weight=1)

        # config_pane
        for i in range(3):
            self.config_pane.rowconfigure(i, weight=0)
        for i in range(6):
            self.config_pane.columnconfigure(i, weight=1)

        # color choose pane
        for i, name in enumerate(self.name_list):
            self.color_choose_pane.rowconfigure(i, weight=0)
        for i in range(6):
            self.color_choose_pane.columnconfigure(i, weight=1)

        # execute pane
        self.execute_pane.rowconfigure(0, weight=0)
        for i in range(6):
            self.execute_pane.columnconfigure(i, weight=1)

    def bind_functions(self):
        self.choose_excel_button['command'] = self._read_excel_file
        self.choose_fdi_button['command'] = self._read_fdi_file

    def _read_excel_file(self):
        c = tkFileDialog.askopenfile(mode='rb')
        if c is None:
            # No file selected
            return
        excel_name = c.name
        self.display_excel_var.set(os.path.basename(excel_name))
        self.excel_matrix = XlsxFile(excel_name).matrix
        self.refresh_dynamic_area(self.excel_matrix[0])

    def _read_fdi_file(self):
        c = tkFileDialog.askopenfile(mode='rb')
        if c is None:
            # No file selected
            return
        fdi_name = c.name
        self.display_fdi_var.set(os.path.basename(fdi_name))
        with open(fdi_name, 'r') as f:
            self.fdi_content = f.read()

    def refresh_dynamic_area(self, new_name_list):
        if self.dynamic_area is not None:
            self.dynamic_area.destroy()
        self.dynamic_area = ColorChooseFrame(self.color_choose_pane, new_name_list)
        self.dynamic_area.grid(row=0, column=0, columnspan=6, sticky='wens')


def main():
    # app = ColorChooseFrame(name_list=['SpeciesA', 'SpeciesB', 'SpeciesC'])
    # app.mainloop()

    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
