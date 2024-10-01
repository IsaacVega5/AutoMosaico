import xlsxwriter
import tkinter.filedialog

EXCEL_COLUMN_ORDER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def create_workbook() -> object:
    destiny_path = tkinter.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
    if destiny_path == '': return None, None
    
    workbook = xlsxwriter.Workbook(destiny_path, {'nan_inf_to_errors': True})
    
    return workbook, destiny_path

def add_worksheet(workbook, name) -> object:
    worksheet_all = workbook.worksheets()
    worksheet_len = str(len(worksheet_all))
    if len(name) > ( 31 - ( len(worksheet_len) + 2 ) ):
        fixed_name_len = 31 - ( len(worksheet_len) + 5 )
        name = name[0:fixed_name_len]
        name = name + '... #' + worksheet_len
    else :
        fixed_name_len = 31 - ( len(worksheet_len) + 2 )
        name = name[0:fixed_name_len]
        name = name + ' #' + worksheet_len
    worksheet = workbook.add_worksheet(name[0:31])
    return worksheet

def add_table_headers(worksheet, headers) -> None:
    for i in range(len(headers)):
        worksheet.write(EXCEL_COLUMN_ORDER[i] + '1', headers[i])

def add_table_row(worksheet, row, data) -> None:
    for i in range(len(data)):
      worksheet.write(EXCEL_COLUMN_ORDER[i] + str(row), data[i])

def add_table_column(worksheet, column, header,  data) -> None:
    worksheet.write(0, column, header)
    for i in range(len(data)):
        worksheet.write(i+1, column,  data[i])

def save_workbook(workbook) -> None:
    workbook.close()