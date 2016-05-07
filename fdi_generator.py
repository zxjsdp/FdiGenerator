#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Modify Fdi files"""

from __future__ import (print_function, unicode_literals,
                        with_statement)

import sys
# Use zipimport to satisfy requirements
sys.path.insert(0, 'library.zip')

import os
import openpyxl
import logging

try:
    from PIL import Image, ImageFont, ImageDraw
    import colorsys
except ImportError:
    Image, ImageFont, ImageDraw = None, None, None
    colorsys = None

if sys.version[0] == '2':
    import Tkinter as tk
    import ttk
    import tkFileDialog
    from tkColorChooser import askcolor
    import tkMessageBox
elif sys.version[0] == '3':
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
    from tkinter.colorchooser import askcolor

IGNORE_LIMIT = 0
MIN_LIMIT = 1
MAX_LIMIT = 700
MIN_CIRC_RADIUS = '10'
MAX_CIRC_RADIUS = '100'
BORDER_COLOR = '0'
INFO_LINE_STYLE = "%4d / %4d |%18s |%20s"

OUT_DIR = os.path.abspath('./output')
IMAGE_DIR = os.path.abspath('./images')
INFO_DIR = os.path.abspath('./info')
for each_dir in [OUT_DIR, IMAGE_DIR, INFO_DIR]:
    if not os.path.isdir(each_dir):
        os.mkdir(each_dir)

PROCESSING_DATA_FILE = os.path.join(INFO_DIR, 'data.txt')
INFO_FILE = os.path.join(INFO_DIR, 'info.txt')

APP_TITLE = 'Fdi Generator'
DEFAULT_GEOMETRY = '1000x750'
CHOOSE_COLOR_BUTTON_TEXT = 'Browse Color...'
CHOOSE_EXCEL_LABEL_TEXT = 'Choose Excel file: '
CHOOSE_EXCEL_BUTTON_TEXT = 'Browse xlsx file...'
DEFALT_CHOOSE_EXCEL_LABEL_TEXT = '...'
CHOOSE_FDI_LABEL_TEXT = 'Choose fdi file: '
CHOOSE_FDI_BUTTON_TEXT = 'Browse fdi file...'
DEFALT_CHOOSE_FDI_LABEL_TEXT = '...'
IGNORE_LIMIT_LABEL_TEXT = 'Ignore Limit: '
MIN_LIMIT_LABEL_TEXT = 'Minimum Limit: '
MAX_LIMIT_LABEL_TEXT = 'Maximum Limit: '
MIN_CIRC_RADIUS_LABEL_TEXT = 'Minimum Circle Radius: '
MAX_CIRC_RADIUS_LABEL_TEXT = 'Maximum Circle Radius: '
BORDER_COLOR_LABEL_TEXT = 'Border Color: '
INFO_LINE_STYLE_LABEL_TEXT = 'Info Line Style (info.txt): '
OUTPUT_FILE_LABEL_TEXT = 'Output fdi filename: '
DEFAULT_OUTPUT_FILE = 'output.fdi'
EXECUTE_BUTTON_TEXT = 'Execute'

CHOOSED_XLSX_FILE = 'Selected xlsx file: '
CHOOSED_FDI_FILE = 'Selected fdi file: '

NO_XLSX_FILE_ERROR_TITLE = 'Excel error'
NO_XLSX_FILE_ERROR_MESSAGE = 'No xlsx file was selected'
NO_FDI_FILE_ERROR_TITLE = 'Fdi error'
NO_FDI_FILE_ERROR_MESSAGE = 'No Fdi file was selected!'
INVALID_XLSX_FILE_ERROR_TITLE = 'Execl error'
INVALID_XLSX_FILE_ERROR_MESSAGE = 'No Execl file was selected'
NOT_ALL_COLOR_CHOOSED_ERROR_TITLE = 'Color choose error'
NOT_ALL_COLOR_CHOOSED_ERROR_MESSAGE = 'Not all colors were choosed!'
NO_OUTFILE_ERROR_TITLE = 'Output file error'
NO_OUTFILE_ERROR_MESSAGE = 'No valid output file was specified!'
XLSX_FIRST_LINE_ERROR_TITLE = 'Xlsx content error'
XLSX_FIRST_LINE_ERROR_MESSAGE = ('First line of Xlsx file must be title '
                                 '(rather than digit)')
XLSX_NOT_FIRST_LINE_ERROR_TITLE = 'Xlsx content error'
XLSX_NOT_FIRST_LINE_ERROR_MESSAGE = ('All cells from second line in xlsx files '
                                     'must be digit (rather than alpha)')
STARTING_VALIDATING_DATA_INFO = 'Start validating data...'
FINISHED_VALIDATING_DATA_INFO = 'Finished data validation'
RAW_DATA_PROCESSED_INFO = 'Raw data processed!'
INFO_FILE_PROCESSED_INFO = 'Info file generated'
FDI_FILE_GENERATED_INFO = 'New fdf file generated'


def save_color_image(color_rgb_tuple_str, color_name):
    """Draw an image with specied color."""
    color_rgb_tuple = tuple([
        int(float(x)) for x in
        color_rgb_tuple_str.replace('(', '').replace(')', '').split(',')])
    if Image:
        image = Image.new('RGB', (200, 200), color_rgb_tuple)
        draw = ImageDraw.Draw(image)
        image_file = os.path.join(IMAGE_DIR, '%s.png' % color_name)
        image.save(image_file)


def rgb_to_rgb_value(rgb_tuple_str):
    """
    Convert RGB to single RGB integer value.

    [Parameters]
        rgb_tuple_str: This kind of format: '(147,112,219)'

    [Return]
        rgb_value:  14381203
                    (
                        147
                        + (112 * 256)
                        + (219 * 256 * 256)
                    )

        RGB value= Red + (Green*256) + (Blue*256*256)
        (https://msdn.microsoft.com/en-us/library/dd355244.aspx)
    """
    r_value, g_value, b_value = [
        float(x) for x in
        rgb_tuple_str.replace('(', '').replace(')', '').split(',')]
    return int(r_value + (g_value * 256) + (b_value * 256 * 256))


def processing_raw_data(raw_matrix_without_title, data_file):
    """Processing raw data, apply [MIN_LIMIT, MAX_LIMIT] rule.
    Title line was already removed.
    """
    out_list = []

    for each_tuple in raw_matrix_without_title:
        number_list = [float(x) for x in each_tuple]
        for i, number in enumerate(number_list):
            if number <= IGNORE_LIMIT:
                number_list[i] = 0
            elif IGNORE_LIMIT < number < MIN_LIMIT:
                number_list[i] = int(round(MIN_LIMIT))
            elif number > MAX_LIMIT:
                number_list[i] = int(round(MAX_LIMIT))
            else:
                number_list[i] = int(round(number))
        out_list.append(', '.join([str(x) for x in number_list]))

    with open(data_file, 'w') as f_out:
        f_out.write('\n'.join(out_list))


def generate_info_file(data_file, info_file, name_list, color_dict):
    """Generate info_file."""
    out_list = []
    with open(data_file, 'r') as f_in:
        lines = [x.strip() for x in f_in.readlines() if x.strip()]

    for i, line in enumerate(lines):
        out_list.append('Hap_%d:\n\n' % (i+1))
        num_list = [int(x) for x in line.split(',')]
        num_sum = sum(num_list)
        for j, num in enumerate(num_list):
            if num:
                out_list.append(INFO_LINE_STYLE % (num, num_sum,
                                                   name_list[j],
                                                   str(color_dict.get(name_list[j]))))
        out_list.append('\n')

    with open(info_file, 'w') as f_out:
        f_out.write('\n'.join(out_list))


class HandleFdi(object):
    """
    Modify fdi file to draw color.

    info_file was generated after HandleColorInfo()

    >>> hf = HandleFdi(fdi_file, info_file, out_file)
    >>> hf.parse_info_file()
    >>> hf.parse_fdi_file()
    >>> hf.write_to_file()
    """
    def __init__(self, fdi_file, info_file, out_file):
        self.info_file = info_file
        self.out_file = out_file
        self.info_dict = {}
        self.fdi_file = fdi_file
        self.final_list = []

    def parse_info_file(self):
        """
        Parse infomation file and extract TAXON_PIE_FREQUENCY and RGB color.

        [Return]
            {
                'Hap_1': [['1 /  1:', 17919]],
                ...,
                'Hap_5': [
                             ['1 /  3:', 11394815],
                             ['1 /  3:', 2763429],
                             ['1 /  3:', 16776960]
                         ],
                ...
            }
        """
        temp_hap_name = ''
        exists_color_set = set()
        with open(self.info_file, 'r') as f_in:
            lines = [x.strip() for x in f_in.readlines() if x.strip()]

        for line in lines:
            if line.startswith("Hap_"):
                temp_hap_name = line.rstrip(':')
                self.info_dict[temp_hap_name] = []
            else:
                num_raw, name, rgb_tuple_str = \
                    [x.strip() for x in line.strip().split("|")
                     if x.strip()]

                # Save a image with name and color
                if name not in exists_color_set:
                    save_color_image(rgb_tuple_str, name)
                    exists_color_set.add(name)

                self.info_dict[temp_hap_name].append(
                    [num_raw, rgb_to_rgb_value(rgb_tuple_str)])

    def parse_fdi_file(self):
        """
        Parse fdi file and save modified lines to final list.
        """
        with open(self.fdi_file, 'r') as f_in:
            lines = f_in.readlines()

        for line in lines:
            if line.startswith("MIN_CIRC_RADIUS"):
                line = line.replace('4', MIN_CIRC_RADIUS)
                self.final_list.append(line)
            elif line.startswith("MAX_CIRC_RADIUS"):
                line = line.replace('50', MAX_CIRC_RADIUS)
                self.final_list.append(line)
            elif line.startswith("TAXON_NAME;H_"):
                # keep_part, throw_part
                keep_part, _ = line.split("TAXON_COLOR_PIE1")
                hap_num = line.split(";")[1].replace("H", "Hap").strip()
                # Infomation list
                # Example:
                #     [['8 /  8:', 16760576]],
                # or:
                #     [['7 / 27:', 11394815], ['5 / 27:', 2763429]]
                info_list = self.info_dict[hap_num]
                modified_line = ''
                modified_line += keep_part.rstrip("TAXON_COLOR_PIE1")
                for i, (num_raw, rgb_value) in enumerate(info_list):
                    frequency = num_raw.split("/")[0].strip()
                    modified_line += (
                        "TAXON_COLOR_PIE%d;%s;" % (i + 1, rgb_value) +
                        "TAXON_PIE_FREQUENCY%d;%s;" % (i + 1, frequency) +
                        "TAXON_STYLE_PIE%d;SOLID;" % (i + 1))
                modified_line += ("TAXON_LINE_WIDTH;1;" +
                                  "TAXON_LINE_COLOR;%s;" % BORDER_COLOR +
                                  "TAXON_LINE_STYLE;SOLID;" +
                                  "TAXON_ACTIVE;TRUE\n")
                self.final_list.append(modified_line)
            else:
                self.final_list.append(line)

    def write_to_file(self):
        """Write new fdi lines to file."""
        out_file = os.path.join(OUT_DIR, self.out_file)
        with open(out_file, 'w') as f_out:
            f_out.write(''.join(self.final_list))


def generate_new_fdi(fdi_file, info_file, out_file):
    """Generate a new fdi with new proportions, new colors and new size limit.
    """
    fdi = HandleFdi(fdi_file, info_file, out_file)
    fdi.parse_info_file()
    fdi.parse_fdi_file()
    fdi.write_to_file()


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
        s = ttk.Style()
        s.configure('color.TButton', padding=0)

    def create_widgets(self):
        """Create widgets for dynamically color choose pane
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
                                           text=CHOOSE_COLOR_BUTTON_TEXT,
                                           style='color.TButton'))
            self.colored_bg_labels.append(ttk.Label(self.master,
                                                    background='#FFFFFF'))

    def grid_config(self):
        """Grid configurations

        Three columns.
        """
        for i, name in enumerate(self.name_lebels):
            name.grid(row=i, column=0, sticky='we')
            self.buttons[i].grid(row=i, column=1, sticky='we')
            self.colored_bg_labels[i].grid(row=i, column=2, sticky='we')

    def row_and_column_config(self):
        """Row and column configurations"""
        # Row configs
        for i, name in enumerate(self.name_lebels):
            self.master.rowconfigure(i, weight=0)

        # Column configs
        for i in range(3):
            self.master.columnconfigure(i, weight=1)

    def bind_function(self):
        """Bind functions to each button.

        Use defualt parameter in lambda function to avoid variable bug:
        If no default paramter, value of i will always be value of the last i
        button['command'] = lambda i=i: self._ask_color(i)
        """
        for i, label in enumerate(self.name_lebels):
            button = self.buttons[i]
            button['command'] = lambda i=i: self._ask_color(i)

    def _ask_color(self, i):
        """Popup a color pane to choose color"""
        # ((0, 255, 64), '#00ff40')
        color = askcolor()
        if not color[0]:
            return
        self.choosed_color_dict[self.name_list[i]] = color[0]
        self.colored_bg_labels[i].config(
            text='%17s %8s' % (str(color[0]), str(color[1])),
            background=color[1],
            font='Monospace'
        )

    def destroy_all_inner_widgets(self):
        """Destroy all name_labels, buttons and color_labels to show new ones.
        """
        for name_label in self.name_lebels:
            name_label.destroy()
        for button in self.buttons:
            button.destroy()
        for color_label in self.colored_bg_labels:
            color_label.destroy()


class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Data
        self.name_list = []
        self.excel_matrix = []
        self.excel_name = ''
        self.fdi_name = ''
        self.dynamic_area = None

        # Create GUI
        self.master.geometry(DEFAULT_GEOMETRY)
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
        s.configure('TButton', padding=(3, 10))
        s.configure(
            'execute.TButton',
            foreground='red',
        )

        s.configure('TLable', padding=(3, 10))
        s.configure(
            'status.TLabel',
            padding=10,
            foreground='#2E64FE'
        )

        s.configure('TEntry', padding=(3, 10))

    def create_widgets(self):
        """Create GUI widgets.
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
        self.choose_excel_label = ttk.Label(self.config_pane,
                                            text=CHOOSE_EXCEL_LABEL_TEXT)
        self.choose_excel_button = ttk.Button(self.config_pane,
                                              text=CHOOSE_EXCEL_BUTTON_TEXT)
        self.display_excel_var = tk.StringVar()
        self.display_excel_label = ttk.Label(self.config_pane,
                                             textvariable=self.display_excel_var,
                                             style='config.TLabel')
        self.display_excel_var.set(DEFALT_CHOOSE_EXCEL_LABEL_TEXT)

        # Fdi file related lable and button
        self.choose_fdi_label = ttk.Label(self.config_pane,
                                          text=CHOOSE_FDI_LABEL_TEXT)
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

        # IGNORE_LIMIT
        self.ignore_limit_label = ttk.Label(
            self.config_pane, text=IGNORE_LIMIT_LABEL_TEXT)
        self.ignore_limit_entry = ttk.Entry(self.config_pane)

        # MIN_LIMIT
        self.min_limit_label = ttk.Label(
            self.config_pane, text=MIN_LIMIT_LABEL_TEXT)
        self.min_limit_entry = ttk.Entry(self.config_pane)

        # MAX_LIMIT
        self.max_limit_label = ttk.Label(
            self.config_pane, text=MAX_LIMIT_LABEL_TEXT)
        self.max_limit_entry = ttk.Entry(self.config_pane)

        # MIN_CIRC_RADIUS
        self.min_circ_radius_label = ttk.Label(
            self.config_pane, text=MIN_CIRC_RADIUS_LABEL_TEXT)
        self.min_circ_radius_entry = ttk.Entry(self.config_pane)

        # MAX_CIRC_RADIUS
        self.max_circ_radius_label = ttk.Label(
            self.config_pane, text=MAX_CIRC_RADIUS_LABEL_TEXT)
        self.max_circ_radius_entry = ttk.Entry(self.config_pane)

        # BORDER_COLOR
        self.border_color_label = ttk.Label(
            self.config_pane, text=BORDER_COLOR_LABEL_TEXT)
        self.border_color_entry = ttk.Entry(self.config_pane)

        # INFO_LINE_STYLE
        self.info_line_style_label = ttk.Label(
            self.config_pane, text=INFO_LINE_STYLE_LABEL_TEXT)
        self.info_line_style_entry = ttk.Entry(self.config_pane)

        # Insert default values
        self.output_file_entry.insert('0', DEFAULT_OUTPUT_FILE)
        self.ignore_limit_entry.insert('0', IGNORE_LIMIT)
        self.min_limit_entry.insert('0', MIN_LIMIT)
        self.max_limit_entry.insert('0', MAX_LIMIT)
        self.min_circ_radius_entry.insert('0', MIN_CIRC_RADIUS)
        self.max_circ_radius_entry.insert('0', MAX_CIRC_RADIUS)
        self.border_color_entry.insert('0', BORDER_COLOR)
        self.info_line_style_entry.insert('0', INFO_LINE_STYLE)

        # Dynamic Area
        self.dynamic_area = ColorChooseFrame(self.color_choose_pane,
                                             name_list=self.name_list)

        # Execute button
        self.execute_button = ttk.Button(self.execute_pane,
                                         text=EXECUTE_BUTTON_TEXT,
                                         style='execute.TButton')
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.execute_pane,
                                      textvariable=self.status_var,
                                      style='status.TLabel')

    def grid_config(self):
        """Grid configurations"""
        self.master.grid()

        self.config_pane.grid(row=0, column=0, sticky='wens')
        self.color_choose_pane.grid(row=1, column=0, sticky='wens')
        self.execute_pane.grid(row=2, column=0, sticky='wens')

        # config_pane
        self.choose_excel_label.grid(row=0, column=0, sticky='we')
        self.choose_excel_button.grid(row=0, column=1, sticky='we')
        self.display_excel_label.grid(row=0, column=2, sticky='we')

        self.choose_fdi_label.grid(row=1, column=0, sticky='we')
        self.choose_fdi_button.grid(row=1, column=1, sticky='we')
        self.display_fdi_label.grid(row=1, column=2, sticky='we')

        # Output filename
        self.output_file_label.grid(row=2, column=0, sticky='we')
        self.output_file_entry.grid(row=2, column=1, sticky='we')

        # Other configs
        self.ignore_limit_label.grid(row=3, column=0, sticky='we')
        self.ignore_limit_entry.grid(row=3, column=1, sticky='we')

        self.min_limit_label.grid(row=4, column=0, sticky='we')
        self.min_limit_entry.grid(row=4, column=1, sticky='we')

        self.max_limit_label.grid(row=5, column=0, sticky='we')
        self.max_limit_entry.grid(row=5, column=1, sticky='we')

        self.min_circ_radius_label.grid(row=6, column=0, sticky='we')
        self.min_circ_radius_entry.grid(row=6, column=1, sticky='we')

        self.max_circ_radius_label.grid(row=7, column=0, sticky='we')
        self.max_circ_radius_entry.grid(row=7, column=1, sticky='we')

        self.border_color_label.grid(row=8, column=0, sticky='we')
        self.border_color_entry.grid(row=8, column=1, sticky='we')

        self.info_line_style_label.grid(row=9, column=0, sticky='we')
        self.info_line_style_entry.grid(row=9, column=1, sticky='we')

        # color_choose_pane
        self.dynamic_area.grid(row=0, column=0, columnspan=3, sticky='wens')

        # execute_pane
        self.execute_button.grid(row=0, column=0, columnspan=3, sticky='we')
        self.status_label.grid(row=1, column=0, columnspan=3, sticky='we')

    def row_and_column_config(self):
        """Row and column configurations"""
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=0)
        self.master.rowconfigure(2, weight=0)
        self.master.columnconfigure(0, weight=1)

        # config_pane
        for i in range(3):
            self.config_pane.rowconfigure(i, weight=0)
        for i in range(3):
            self.config_pane.columnconfigure(i, weight=1, uniform='fred')

        # color choose pane
        for i, name in enumerate(self.name_list):
            self.color_choose_pane.rowconfigure(i, weight=0)
        for i in range(3):
            self.color_choose_pane.columnconfigure(i, weight=1, uniform='fred')

        # execute pane
        self.execute_pane.rowconfigure(0, weight=0)
        self.execute_pane.rowconfigure(1, weight=0)
        for i in range(3):
            self.execute_pane.columnconfigure(i, weight=1, uniform='fred')

    def bind_functions(self):
        """Bind functions to buttons"""
        self.choose_excel_button['command'] = self._read_excel_file
        self.choose_fdi_button['command'] = self._read_fdi_file
        self.execute_button['command'] = self._execute

    def _read_excel_file(self):
        """Select and read excel file"""
        self.excel_name = tkFileDialog.askopenfilename(
            filetypes=[("Xlsx files", "xlsx")])
        if not self.excel_name:
            # No file selected
            return
        self.display_excel_var.set(os.path.basename(self.excel_name))
        self._set_status_var_text(CHOOSED_XLSX_FILE +
                                  os.path.basename(self.excel_name))
        self.excel_matrix = XlsxFile(self.excel_name).matrix
        if self._validate_excel_matrix():
            self.name_list = list(self.excel_matrix[0])
            self.refresh_dynamic_area(self.excel_matrix[0])

    def _read_fdi_file(self):
        """Select and read fdi file"""
        filename = tkFileDialog.askopenfilename(
            filetypes=[("Fdi files", "fdi")])
        if not filename:
            # No file selected
            return
        self.fdi_name = filename
        self.display_fdi_var.set(os.path.basename(self.fdi_name))
        self._set_status_var_text(CHOOSED_FDI_FILE +
                                  os.path.basename(self.fdi_name))
        self.output_file_entry.delete('0', 'end')
        self.output_file_entry.insert('0', os.path.basename(self.fdi_name))

    def _read_configs(self):
        global IGNORE_LIMIT
        global MIN_LIMIT
        global MAX_LIMIT
        global MIN_CIRC_RADIUS
        global MAX_CIRC_RADIUS
        global BORDER_COLOR
        global INFO_LINE_STYLE

        IGNORE_LIMIT = float(self.ignore_limit_entry.get())
        MIN_LIMIT = float(self.min_limit_entry.get())
        MAX_LIMIT = float(self.max_limit_entry.get())
        MIN_CIRC_RADIUS = str(self.min_circ_radius_entry.get())
        MAX_CIRC_RADIUS = str(self.max_circ_radius_entry.get())
        BORDER_COLOR = str(self.border_color_entry.get())
        INFO_LINE_STYLE = str(self.info_line_style_entry.get())

    def _execute(self):
        """Do validation and execution"""
        # Check parameters
        if self._check_params():
            try:
                self._read_configs()
                # Remove title line from matrix
                processing_raw_data(self.excel_matrix[1:], PROCESSING_DATA_FILE)
                self._set_status_var_text(RAW_DATA_PROCESSED_INFO)

                generate_info_file(PROCESSING_DATA_FILE,
                                   INFO_FILE,
                                   self.name_list,
                                   self.dynamic_area.choosed_color_dict)
                self._set_status_var_text(INFO_FILE_PROCESSED_INFO)

                out_file = self.output_file_entry.get().strip()
                generate_new_fdi(self.fdi_name, INFO_FILE, out_file)
                self._set_status_var_text(FDI_FILE_GENERATED_INFO)

                self._set_status_var_text('Done!  Output file:  ./output/%s' %
                                    os.path.basename(out_file))
            except Exception as e:
                self._display_error("ERROR: %s" % e)

    def _check_params(self):
        """Validate files and contents before running"""
        self._set_status_var_text(STARTING_VALIDATING_DATA_INFO)

        # Check if excel file already choosed
        if not self.excel_name:
            self._display_error(
                NO_XLSX_FILE_ERROR_TITLE,
                NO_XLSX_FILE_ERROR_MESSAGE
            )
            return False

        # Check if fdi file was choosed
        if not self.fdi_name:
            self._display_error(
                NO_FDI_FILE_ERROR_TITLE,
                NO_FDI_FILE_ERROR_MESSAGE
            )
            return False

        # Check if data was successfully extracted from excel file
        if not self.excel_matrix:
            self._display_error(
                INVALID_XLSX_FILE_ERROR_TITLE,
                INVALID_XLSX_FILE_ERROR_MESSAGE
            )
            return False

        # Check if all categories have colors
        if len(self.name_list) != len(self.dynamic_area.choosed_color_dict):
            self._display_error(
                NOT_ALL_COLOR_CHOOSED_ERROR_TITLE,
                NOT_ALL_COLOR_CHOOSED_ERROR_MESSAGE
            )
            return False

        # Check if no output file name in output file name entry
        out_file = self.output_file_entry.get().strip()
        if not out_file:
            self._display_error(
                NO_OUTFILE_ERROR_TITLE,
                NO_OUTFILE_ERROR_MESSAGE
            )
            return False

        self._set_status_var_text(FINISHED_VALIDATING_DATA_INFO)

        # All check passed
        return True

    def _validate_excel_matrix(self):
        """Validate content of xlsx file"""
        # Check if number of elements of excel lines are the same
        each_tuple_len_list = [len(each_tuple) for each_tuple
                               in self.excel_matrix]
        if len(set(each_tuple_len_list)) != 1:
            self._display_error(
                INVALID_XLSX_FILE_ERROR_TITLE,
                INVALID_XLSX_FILE_ERROR_MESSAGE
            )
            return False

        # Check if first line is title
        # MUST startswith alpha rather than digit
        for cell in self.excel_matrix[0]:
            try:
                float(cell)
            except ValueError:
                continue
            else:
                self._display_error(
                    XLSX_FIRST_LINE_ERROR_TITLE,
                    XLSX_FIRST_LINE_ERROR_MESSAGE
                )
                return False

        # Check if all cells (except those in first line) is digit
        for each_tuple in self.excel_matrix[1:]:
            for cell in each_tuple:
                try:
                    float(cell)
                except ValueError:
                    self._display_error(
                        XLSX_NOT_FIRST_LINE_ERROR_TITLE,
                        XLSX_NOT_FIRST_LINE_ERROR_MESSAGE
                    )
                    return False

        # All xlsx checks passed
        return True

    def _set_status_var_text(self, text):
        """Display information on status label"""
        self.status_var.set(text)
        self.status_label.update_idletasks()

    def _display_error(self, title, message):
        """Display information on status label and messagebox"""
        message = 'ERROR: ' + message
        self._set_status_var_text(message)
        tkMessageBox.showerror(title, message)

    def refresh_dynamic_area(self, new_name_list):
        """Dynamically refresh color choose area.
        Generate new buttons and labels according to number of categories.
        """
        self.dynamic_area.destroy_all_inner_widgets()
        self.dynamic_area.destroy()
        self.dynamic_area = ColorChooseFrame(self.color_choose_pane,
                                             new_name_list)
        for i, name in enumerate(new_name_list):
            self.dynamic_area.grid(row=i, column=0, columnspan=3,
                                   sticky='wens')
        self.dynamic_area.update_idletasks()


def main():
    """Main GUI function"""
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
