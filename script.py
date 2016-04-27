
import argparse, sys, os
from subprocess import call

# our code
import route_converter.ridewithgps as Converter

TMP_CURL_FILE='_curl_file.csv'
CSV_DIR='files'
XLSX_DIR='outputs'

def output_exists(string):
	"""Use this to validate the output filename"""
	return string

def valid_url(string):
	"""
	Ensure that our string starts with the proper url, and return the last
	"""

	rw_url_prefix = 'https://ridewithgps.com/routes/'
	if not string.startswith(rw_url_prefix) or string[len(rw_url_prefix):] is "":
		msg = "Not a valid URL from RideWithGPS: '{0}'.".format(string)
		raise argparse.ArgumentTypeError(msg)

	return { 'url': string,
			'slug': string[len(rw_url_prefix):]
			}

def csv_file(string):
	if not string.endswith('.csv'):
		msg = "Not a valid css file: '{0}'.".format(string)
		raise argparse.ArgumentTypeError(msg)

	return string

def curl_route(url, do_printing):
	"""
	Handle the good ole' curl, and grab the handle

	Args:
		url: http string
		do_printing: for verbosity

	Raises:
		nothing at the moment...
	"""
	# TODO: fix me in terms of the latest versions
	print ("Grabbing '{}' ...".format(url))

	args = ['curl', url+'.csv', "-H Content-Type:text/csv",
					'-o', TMP_CURL_FILE, 
					'--silent'] # keep me last

	if do_printing:
		print ("\t" + " ".join(args))
		# args.pop()

	call(args)

def create_directories():
	"""Because we want a clear output structure"""
	if not os.path.exists(CSV_DIR):
		os.makedirs(CSV_DIR)
	if not os.path.exists(XLSX_DIR):
		os.makedirs(XLSX_DIR)

def run_generation(input_csv, output_xlsx, do_printing):
	"""Basically do the generation part, calling our ridewithgps.py module functions"""

	print ("Beginning file read...")
	values_array = Converter.read_csv_to_array(input_csv)
	values_array = Converter.format_array(values_array, do_printing)

	print ("Beginning file generation...")
	Converter.generate_excel(output_xlsx, values_array, do_printing)

	print ("Generation complete!")


def main():
	parser = argparse.ArgumentParser(description='Convert a RWGPS Map to a BC Rando style cuesheet')
	
	parser.add_argument("-v", "--verbose", help="Output all statuses",
						action="store_true")

	parser.add_argument("-o", "--output", help="Override output filename",
						type=output_exists)
	parser.add_argument("-u", "--url", help="URL if pulling from the web directly, like https://ridewithgps.com/routes/1234",
						type=valid_url)
	parser.add_argument("-f", "--filename", help="CSV if converting locally",
						type=csv_file)

	args = parser.parse_args()

	# Okay, we know at least one is required
	if args.url is None and args.filename is None:
		sys.exit ("You have to supply either a filename or a URL!")

	# obligatory warning
	if args.url is not None:
		# let them know they screwed up
		if args.filename is not None:
			print ("Ignoring filename with URL specified")

		print ("URL grabbing is experimental. Currently non-functional with updated routes due to API restrictions")

	if args.verbose:
		print ("Running converter in verbose mode")

	# set where we output to
	if args.output is not None:
		excel_filename = args.output
	elif args.url:
		excel_filename = '{0}_cues.xlsx'.format(args.url['slug'])
	else:
		excel_filename = args.filename.replace('.csv', '_cues.xlsx')

	print ("We will output to '{0}'".format(excel_filename))

	try:
		create_directories()
	# TODO: make specific
	except Exception, e:
		print (e)
		print ("Unable to output to the proper directories")

	# set the filename
	csv_filename = args.filename

	# start the actions
	if args.url is not None:
		try:
			curl_route(args.url['url'], args.verbose)
			csv_filename = TMP_CURL_FILE
		except Exception, e:
			print "Unable to retrieve url!"
			sys.exit (e)

	# do the generation
	run_generation(csv_filename, excel_filename, args.verbose)

	# move the files
	os.rename(excel_filename, "outputs/"+excel_filename)

	if args.url is not None:
		os.remove(TMP_CURL_FILE)
	else:
		os.rename(csv_filename, "files/"+csv_filename)

	print ("Your cues file is now located at {0}/outputs/{1}".format(os.getcwd(),
																	excel_filename))
	# success!
	sys.exit(0)

if __name__ == "__main__":
	main()