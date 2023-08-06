import os
import glob
import win32com.client as win32


def remove_meta():
    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.DisplayAlerts = False

    filetypes = ["**/*.xlsx", "**/*.xls", "**/*.xlsm"]

    for filetype in filetypes:
        for file in glob.iglob(filetype, recursive=True):
            absolute_path = os.path.abspath(file)
            print("Working with file:", absolute_path)
            wb = excel.Workbooks.Open(absolute_path)
            wb.RemovePersonalInformation = True
            wb.Save()
            wb.Close()

    excel.Quit()
