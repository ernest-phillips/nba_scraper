import sys
import linecache

def LogException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

# function for adding keys to list of dictionaries
def add_keys(data, date, is_regular_season):
    for line in data:
        line['DATE'] = date
        line['IS_REGULAR_SEASON'] = is_regular_season
    return data
