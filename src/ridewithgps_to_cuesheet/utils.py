import csv


def read_csv_to_array(filename):
    values = []
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            cuesheet = csv.reader(csvfile)
            next(cuesheet)
            for cue in cuesheet:
                values.append(cue)

    except IOError as ioe:
        if ioe.errno == 2:
            print("Cannot find CSV file")
            raise ioe
    except Exception as e:
        print("Error in reading csv file")
        raise e
    return values


def merge_dicts(dict1, *dicts):
    copied = dict1.copy()
    for dict in dicts:
        copied.update(dict)
    return copied
