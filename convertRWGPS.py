import csv
import sys
import re
import os
from subprocess import call

"""
    This program is designed to convert a RideWithGPS
    exported csv file, into a BC Randonneurs Routesheet
"""
import xlsxwriter
has_end = False

# for dicts


def merge(dict1, *dicts):
    dict3 = dict1.copy()
    for dict in dicts:
        dict3.update(dict)

    return dict3


def format_cue(row):

    global has_end

    is_control = (row[0] == 'Food') or (row[0] == 'Start') or (row[0] == 'End')
    if row[0] == 'Summit':
        is_control = True
        has_end = True
        row[1] = "FINISH: " + row[1]

    print (row[2])

    # direction
    def dir(x):
        if x == 'Straight':
            return 'CO'
        elif x == 'Left':
            return 'L'
        elif x == 'Right':
            return 'R'
        elif x == 'Generic' or x == 'Food':
            return ''
        else:
            return x

    # direction
    def cue(x):
        if x == 'Start of route':
            return 'START'
        elif x == 'End of route':
            return 'FINISH CONTROL'
        elif x.startswith('Continue onto '):
            return x[len('Continue onto '):]
        else:
            for direction in ['left', 'right']:
                if x.startswith('Turn ' + direction + ' onto '):
                    return x[len('Turn ' + direction + ' onto '):]
                elif re.match('Turn ' + direction + ' to ([^(stay)])',
                              x):
                    return x[len('Turn ' + direction + ' to '):]
            x.replace('becomes', 'b/c')
            return x

    return [
        dir(row[0]),
        cue(row[1]),
        float(row[2]),
        is_control
    ]

if len(sys.argv) < 2:
    print ("Missing arguments!")
    print ("Either enter a filename.csv, or a ridewithgps url slug")
    sys.exit(1)

# And begin!
title = sys.argv[1]
    
if title.endswith('.csv'):
    # loading from file
    filename = title
    title = title.split('.')[0]
    curl = False
else:
    curl = True
    filename = title + '.csv'

if curl:
    rwgs_url = "http://ridewithgps.com/routes/%s" % filename
    print("Grabbing '%s' ..." % rwgs_url)

    call(['curl', '-O', rwgs_url, "-H Content-Type:text/csv", '--silent'])

values = []

with open(filename, 'rb') as csvfile:
    cuesheet = csv.reader(csvfile)
    next(cuesheet)
    for cue in cuesheet:
        values.append(format_cue(cue))

if has_end:
    values = values[:-1]

print("Cues read, generating excel")

workbook = xlsxwriter.Workbook(title + '_cues.xlsx')
worksheet = workbook.add_worksheet()

defaults = {'font_size': 8,
            'font_name': 'Arial'}
a_12_opts = {'font_size': 12,
            'font_name': 'Arial'}
centered = {'align': 'center',
            'valign': 'vcenter'}
all_border = {'border':1}

# for the titles
title_format = workbook.add_format(merge({'rotation': 90
                                          }, defaults,
                                          all_border))

descr_format = workbook.add_format(merge(centered, defaults, all_border))
control_format = workbook.add_format(merge({'bold': True,
                                            'bg_color': '#C0C0C0',
                                            'text_wrap': True
                                            },
                                           centered, defaults,
                                           all_border))
# default font
arial_12 = workbook.add_format(merge(a_12_opts, all_border))
arial_12_no_border = workbook.add_format(merge(a_12_opts, all_border,
                                        {'left_color':'white',
                                         'right_color':'white'}))
# Add a number format for cells with distances
dist_format = workbook.add_format(merge({'num_format': '0.0'},
                                        a_12_opts, all_border))
cue_format = workbook.add_format(merge({'text_wrap': True},
                                        a_12_opts, all_border))
red_title = workbook.add_format(merge({'font_color':'red'
                                      }, a_12_opts, centered))

# Add an Excel date format.
# date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})


# Adjust the column width.
#     Cell width is (8.43/16.83) * XXmm
#     worksheet.set_column(1, 1, 15)

worksheet.merge_range('A1:E1', 'INSERT NAME OF RIDE', red_title)
worksheet.merge_range('A2:E2', 'insert date of ride', red_title)
worksheet.merge_range('A3:E3', 'insert name of Ride Organizer', red_title)
worksheet.merge_range('A4:E4', 'insert Start location', red_title)
worksheet.merge_range('A5:E5', 'insert Finish location', red_title)

# Write some data headers.
worksheet.write('A6', 'Dist.(cum.)', title_format)
worksheet.write('B6', 'Turn', title_format)
worksheet.write('C6', 'Direction', title_format)
worksheet.set_column('A:D', 5.6)  # width
worksheet.write('D6', 'Route Description', descr_format)
worksheet.set_column('D:D', 39)  # width
worksheet.write('E6', 'Dist.(int.)', title_format)
worksheet.set_column('E:E', 5.6)  # width

# Start from the first cell below the headers.
row = 6
col = 0
ctrl_sum = 0
last_dist = 0
pbreak_list = []

for turn, descr, dist, control in (values):
    print("We're on row %s at %s" % ((row-6), dist))
    curr_dist = dist-last_dist

    if ctrl_sum != 0:
        worksheet.write(row, col, '=SUM(A' +
                        str(row) +
                        '+E' +
                        str(row) +
                        ')', dist_format)
    else:
        worksheet.write(row, col, '', arial_12)
    if control:
        worksheet.write_string(row, col + 1, '', arial_12_no_border)
        worksheet.write_string(row, col + 3, descr, control_format)
        worksheet.write_number(row, col + 4,     0, dist_format)
        height = 20
        pbreak_list.append(row)
    else:
        worksheet.write_string(row, col + 1, turn, arial_12)
        worksheet.write_string(row, col + 2, '', arial_12)
        worksheet.write_string(row, col + 3, descr, cue_format)
        worksheet.write_number(row, col + 4, round(curr_dist, 1), dist_format)
        height = 15
        ctrl_sum += curr_dist
        if (row - pbreak_list[-1]) == 42:
            pbreak_list.append(row)

    # set the row formatting
    worksheet.set_row(row, height)
    last_dist = dist
    row += 1

# Write last notes
worksheet.write(row, col + 2, '', workbook.add_format({'top':1}))
only_center = workbook.add_format(merge(defaults, centered))
worksheet.write(row, col + 3, 'IN CASE OF ABANDONMENT OR EMERGENCY', only_center)
row += 1
worksheet.write(row, col + 3, "PHONE: ** ORGANIZER'S NUMBER **", only_center)

# for printing
worksheet.print_area('A1:E%d' % (row+1))
# chop off finish and start
pbreak_list = pbreak_list[1:-1]
worksheet.set_h_pagebreaks(pbreak_list)

workbook.close()

if curl:
    os.remove(filename)

print("Done!")
