# -*- coding: utf-8 -*-
from decimal import Decimal

"""
	This program is designed to convert a RideWithGPS
	exported csv file, into a BC Randonneurs Routesheet
"""

CONTROL_CUE_INDICATORS = ['Food','Start','End','Summit']
END_INDICATOR = "Summit"
START_TEXT = "DÉPART"
END_TEXT = "ARRIVÉE"

class argsobject(object):
    def __init__(self, d):
        self.__dict__ = d

def merge(dict1, *dicts):
	"""Merge two dicts. Used so we can preserve consistent styling"""
	dict3 = dict1.copy()
	for dict in dicts:
		dict3.update(dict)

	return dict3

def read_csv_to_array(filename):
	"""Basically import our csv file into an array"""
	import csv

	values = []
	try:
		with open(filename, 'rb') as csvfile:
			cuesheet = csv.reader(csvfile)
			next(cuesheet)
			for cue in cuesheet:
				values.append(cue)

	# TODO: make specific
	except IOError, ioe:
		if ioe.errno is 2:
			print ("Cannot find CSV file")
	except Exception, e:
		print ("Error in reading csv file")
		raise e
	finally:
		pass # should be uneeded using 'with'
	return values

def format_array(array, verbose=False):
	end_cue_present = False
	last = -1

	for i in range(len(array)-1, -1, -1):
		parsed = _format_cue(array[i], i, last, verbose)
		array[i] = parsed['dict']
		end_cue_present = end_cue_present or parsed['end']
		last = parsed['last']

	return array

def _format_cue(row, idx, last_dist, verbose=False):
	"""
	Parse the csv values into dictionaries so that they're easier to manipulate

	Return:
		Dict with 'dict': the dictionary for the row
				  'end': a boolean telling us if the cnotrol has an end value
				  'last': the distance of this control for use in interval calculationn
	"""
	import re

	has_end = False
	is_control = (row[0] in CONTROL_CUE_INDICATORS)
	this_dist = Decimal(row[2])

	if (idx is 1 and this_dist <= 0.1):
		this_dist = Decimal('0')

	# the summit cue is what tells us there's an end
	# (and that we will format the row cue with FINISH)
	if row[0] == END_INDICATOR:
		has_end = True
		row[1] = END_TEXT + ": " + row[1]


	# direction via Rando standards
	def map_dir(x):
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

	# more compact cues
	def map_cue(x):
		if x == 'Start of route':
			return START_TEXT
		elif x == 'End of route':
			return END_TEXT
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

	return { 'dict': {	'turn': map_dir(row[0]),
						'descr': map_cue(row[1]),
						'dist': last_dist,
						'control': is_control
						},
			'end': has_end,
			'last': this_dist
		}

def generate_excel(filename, values_array, opts):
	"""
	This is pretty much the meat. We take the array of dicts and spit out the values

	Arguments:

		filename: to write to
		values_array: as read in above
		opts.include_from_last: to show distance since the last control
		opts.hide_direction: hide direction column
		opts.verbose: periodic printiouts
	"""
	import xlsxwriter

	try:
		workbook = xlsxwriter.Workbook(filename)
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
												   centered, a_12_opts,
												   all_border))
		# default font
		arial_12 = workbook.add_format(merge(a_12_opts, all_border))
		arial_12_no_border = workbook.add_format(merge(a_12_opts, all_border,
												{'left_color':'white',
												 'right_color':'white'}))
		# Add a number format for cells with distances
		dist_format = workbook.add_format(merge({'num_format': '0.00'},
												a_12_opts, all_border))
		dist_format2 = workbook.add_format(merge({'num_format': '0.0'},
												a_12_opts, all_border))
		cue_format = workbook.add_format(merge({'text_wrap': True},
												a_12_opts, all_border))
		red_title = workbook.add_format(merge({'font_color':'red'
											  }, a_12_opts, centered))
		black_title = workbook.add_format(merge({'font_color':'black'
											  }, a_12_opts, centered))

		# Add an Excel date format.

		# Adjust the column width.
		#     Cell width is (8.43/16.83) * XXmm
		#     worksheet.set_column(1, 1, 15)

		# helper function to allow us to get the colum letters
		def letter(num_after):
			return chr(65 + num_after)

		col_num = 0
		curr_col = col_num # init
		num_cols = 4
		if opts.include_from_last:
			num_cols += 1

		if opts.hide_direction:
			num_cols -= 1

		last_col_letter = letter(num_cols)

		worksheet.merge_range('A1:{0}1'.format(last_col_letter), 'INSERT NAME OF RIDE', red_title)
		worksheet.merge_range('A2:{0}2'.format(last_col_letter), 'insert date of ride', red_title)
		worksheet.merge_range('A3:{0}3'.format(last_col_letter), 'insert name of Ride Organizer', red_title)
		worksheet.merge_range('A4:{0}4'.format(last_col_letter), 'insert Start location', red_title)
		worksheet.merge_range('A5:{0}5'.format(last_col_letter), 'insert Finish location', red_title)

		# Write some data headers.
		worksheet.write('A6', 'Dist.(cum.)', title_format)
		curr_col += 1

		if opts.include_from_last:
			worksheet.write(letter(curr_col)+'6', 'Dist. Since', title_format)
			curr_col += 1

		worksheet.write(letter(curr_col)+'6', 'Turn', title_format)
		curr_col += 1

		if not opts.hide_direction:
			worksheet.write(letter(curr_col)+'6', 'Direction', title_format)
			curr_col += 1

		# on long rides, we need wider columns
		worksheet.set_column('A:A', 7.5
									if values_array[ len(values_array)-1 ]['dist'] > 1000 
									else 6.5)  # width
		worksheet.set_column('B:'+letter(curr_col), 5.6)  # width
		worksheet.write( letter(curr_col)+'6' , 'Route Description', descr_format)
		worksheet.set_column( '{0}:{0}'.format(letter(curr_col)) , 39)  # width
		curr_col += 1

		worksheet.write( letter(curr_col)+'6', 'Dist.(int.)' , title_format)
		worksheet.set_column( '{0}:{0}'.format(letter(curr_col)) , 5.6)  # width

		# Start from the first cell below the headers.
		row_num = 6
		ctrl_sum = 0
		last_dist = 0
		pbreak_list = []
		last_was_control = False # for calculations

		# now we get to loop through each row
		for i in range(len(values_array)):
			row = values_array[i]

			# interval distance
			curr_dist = row['dist'] - last_dist
			# for the next loop
			last_dist = 0
			curr_col = col_num

			if opts.verbose:
				tmp = "We're on row {0} at {1}kms".format(row_num-6, row['dist']);
				if 'onto' in row['descr']:
					tmp = '({0}) '.format(row['descr'][ row['descr'].find('onto')+5 : ]) + tmp
				else:
					tmp = row['descr'] + ': ' + tmp
				print (tmp)
				print ('\testimated distance is {0}kms since last'.format(curr_dist))

			if i is 0:
				pass
			elif i is 1:
				worksheet.write(row_num, curr_col, 0, dist_format)
			else:
				# On those ones after a control, we'll simply repeat the previous sum
				worksheet.write(row_num, curr_col, '=A{0}+{1}{0}'.format(row_num if not last_was_control
																		  else row_num-1, last_col_letter),
													dist_format)
			curr_col += 1

			# write out the include from last distances in the second column
			if opts.include_from_last:
				worksheet.write(row_num, curr_col, ctrl_sum, dist_format2)
				curr_col += 1
				
			if row['control']:
				worksheet.write_string(row_num, curr_col, '', arial_12_no_border)
				curr_col += 1

				if not opts.hide_direction:
					worksheet.write_string(row_num, curr_col, '', arial_12)
					curr_col += 1

				worksheet.write_string(row_num, curr_col, row['descr'].decode('utf-8'), control_format)
				curr_col += 1
				worksheet.write_string(row_num, curr_col, '', arial_12)
				height = 20

				# reset the control accumulator
				ctrl_sum = 0
				last_was_control = True

				# make a note of the distance so we can accumulate on the next cue
				last_dist -= curr_dist
				# for easier printing configuration
				pbreak_list.append(row_num)
			else:
				last_was_control = False
				worksheet.write_string(row_num, curr_col, row['turn'].decode('utf-8'), arial_12)
				curr_col += 1

				if not opts.hide_direction:
					worksheet.write_string(row_num, curr_col, '', arial_12)
					curr_col += 1

				worksheet.write_string(row_num, curr_col, row['descr'].decode('utf-8'), cue_format)
				curr_col += 1
				worksheet.write_number(row_num, curr_col, curr_dist, dist_format)

				height = 15
				ctrl_sum += curr_dist
				if (row_num - pbreak_list[-1]) is 42:
					pbreak_list.append(row_num)
				

			# set the row_num formatting
			worksheet.set_row(row_num, height)
			last_dist += row['dist']
			row_num += 1

		row_num += 1
		worksheet.merge_range('A{0}:{1}{0}'.format(row_num, last_col_letter), 'IN CASE OF ABANDONMENT OR EMERGENCY', black_title)
		row_num += 1
		worksheet.merge_range('A{0}:{1}{0}'.format(row_num, last_col_letter), "PHONE: ** ORGANIZER'S NUMBER **", black_title)

		row_num += 1

		# for printing
		worksheet.print_area('A1:{0}{1}'.format(last_col_letter, row_num))
		# chop off finish and start
		pbreak_list = pbreak_list[1:-1]
		worksheet.set_h_pagebreaks(pbreak_list)

		workbook.close()

	finally:
		if workbook is not None:
			workbook.close()


# our happy exports
__all__ = [ 'read_csv_to_array', 'format_array', 'generate_excel' ]
