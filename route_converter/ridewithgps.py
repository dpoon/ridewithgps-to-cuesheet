"""
	This program is designed to convert a RideWithGPS
	exported csv file, into a BC Randonneurs Routesheet
"""
# TODO: throw errors in this program, make someone else handle?

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
	except Exception, e:
		print ("Error in reading csv file")
	finally:
		pass # should be uneeded using 'with'
	return values

def format_array(array, verbose=False):
	end_cue_present = False

	for i in range(len(array)):
		parsed = _format_cue(array[i], verbose)
		array[i] = parsed['dict']
		end_cue_present = end_cue_present or parsed['end']

	return array

def _format_cue(row, verbose=False):
	"""
	Parse the csv values into dictionaries so that they're easier to manipulate

	Return:
		Dict with 'dict': the dictionary for the row
				  'end': a boolean telling us if the cnotrol has an end value
	"""
	import re

	has_end = False
	is_control = (row[0] in ['Food','Start','End','Summit'])

	# the summit cue is what tells us there's an end
	# (and that we will format the row cue with FINISH)
	if row[0] == 'Summit':
		has_end = True
		row[1] = "FINISH: " + row[1]

	# print (row[2])

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

	return { 'dict': {	'turn': map_dir(row[0]),
						'descr': map_cue(row[1]),
						'dist': float(row[2]),
						'control': is_control
						},
			'end': has_end
		}

def generate_excel(filename, values_array, verbose=False):
	"""This is pretty much the meat. We take the array of dicts and spit out the values"""
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
		row_num = 6
		col_num = 0
		ctrl_sum = 0
		last_dist = 0
		pbreak_list = []

		# now we get to loop through each row
		for i in range(len(values_array)):
			row = values_array[i]

			if verbose:
				print("We're on row %s at %s" % ((row_num-6), row['dist']))
			curr_dist = row['dist']-last_dist

			if ctrl_sum != 0:
				worksheet.write(row_num, col_num, '=SUM(A{0}+E{0})'.format(row_num), dist_format)
			else:
				worksheet.write(row_num, col_num, '', arial_12)
			if row['control']:
				worksheet.write_string(row_num, col_num + 1, '', arial_12_no_border)
				worksheet.write_string(row_num, col_num + 3, row['descr'].decode('utf-8'), control_format)
				worksheet.write_number(row_num, col_num + 4,     0, dist_format)
				height = 20
				pbreak_list.append(row_num)
			else:
				worksheet.write_string(row_num, col_num + 1, row['turn'].decode('utf-8'), arial_12)
				worksheet.write_string(row_num, col_num + 2, '', arial_12)
				worksheet.write_string(row_num, col_num + 3, row['descr'].decode('utf-8'), cue_format)
				worksheet.write_number(row_num, col_num + 4, round(curr_dist, 1), dist_format)
				height = 15
				ctrl_sum += curr_dist
				if (row_num - pbreak_list[-1]) == 42:
					pbreak_list.append(row_num)

			# set the row_num formatting
			worksheet.set_row(row_num, height)
			last_dist = row['dist']
			row_num += 1

		# Write last notes
		worksheet.write(row_num, col_num + 2, '', workbook.add_format({'top':1}))
		only_center = workbook.add_format(merge(defaults, centered))
		worksheet.write(row_num, col_num + 3, 'IN CASE OF ABANDONMENT OR EMERGENCY', only_center)
		row_num += 1
		worksheet.write(row_num, col_num + 3, "PHONE: ** ORGANIZER'S NUMBER **", only_center)

		# for printing
		worksheet.print_area('A1:E%d' % (row_num+1))
		# chop off finish and start
		pbreak_list = pbreak_list[1:-1]
		worksheet.set_h_pagebreaks(pbreak_list)

		workbook.close()

	# TODO: make specific
	except Exception, e:
		raise e
	finally:
		if workbook is not None:
			workbook.close()


# our happy exports
__all__ = [ 'read_csv_to_array', 'format_array', 'generate_excel' ]
