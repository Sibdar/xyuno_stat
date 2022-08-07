import pandas as pd
from functions import get_xyuno_data,\
                      process_xyuno_data_and_get_lol_struct,\
                      save_to_excel
from structures import ST_XYUNO_TAB

# get data from huiyuno logs file
log_lines = get_xyuno_data("../Data/xyuno_Log.txt")
print(log_lines)

# form LOL data struct for excel tab
excel_lol_tab = process_xyuno_data_and_get_lol_struct(log_lines, ST_XYUNO_TAB)

# save to excel
save_to_excel(excel_lol_tab, '../Data/xyuno DataSet.xlsx', save=True)
