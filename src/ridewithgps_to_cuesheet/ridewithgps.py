from decimal import Decimal

"""
    This program is designed to convert a RideWithGPS
    exported csv file, into a BC Randonneurs Routesheet

    TODO: direction legend
    cum sum for control
    align All rows to top
    align centre
"""

CONTROL_CUE_INDICATORS = ["Food", "Control", "Start", "End", "Summit"]
END_INDICATOR = "Summit"
START_TEXT = "DÉPART"
END_TEXT = "ARRIVÉE"

# Excel formatting constants
DISTANCE_THRESHOLD_FOR_WIDE_COLUMN = 1000
PAGE_BREAK_ROW_INTERVAL = 42
FIRST_DATA_ROW = 6
CONTROL_ROW_HEIGHT = 20
REGULAR_ROW_HEIGHT = 15


class argsobject:
    def __init__(self, d):
        self.__dict__ = d


def merge(dict1, *dicts):
    dict3 = dict1.copy()
    for dict in dicts:
        dict3.update(dict)
    return dict3


def read_csv_to_array(filename):
    import csv

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


def format_array(array, verbose=False):
    end_cue_present = False
    last = -1

    for i in range(len(array) - 1, -1, -1):
        parsed = _format_cue(array[i], i, last, verbose)
        array[i] = parsed["dict"]
        end_cue_present = end_cue_present or parsed["end"]
        last = parsed["last"]

    return array


def _map_direction(direction: str) -> str:
    cue_dir = direction.lower()
    if cue_dir == "straight":
        return "CO"
    elif cue_dir in ("left", "sharp left"):
        return "L"
    elif cue_dir == "slight left":
        return "BL"
    elif cue_dir in ("right", "sharp right"):
        return "R"
    elif cue_dir == "slight right":
        return "BR"
    elif cue_dir in ("generic", "food", "control"):
        return ""
    elif cue_dir == "uturn":
        return "TA"
    return direction


def _map_cue_description(description: str) -> str:
    import re

    if description == "Start of route":
        return START_TEXT
    elif description == "End of route":
        return END_TEXT
    elif description.startswith("Continue onto "):
        return description[len("Continue onto ") :]

    for direction in ["left", "right"]:
        if description.startswith(f"Turn {direction} onto "):
            return description[len(f"Turn {direction} onto ") :]
        elif re.match(f"Turn {direction} to ([^(stay)])", description):
            return description[len(f"Turn {direction} to ") :]

    description = description.replace("becomes", "b/c")
    description = description.replace("slightly ", "")
    return description


def _format_cue(row, idx, last_dist, verbose=False):
    has_end = False
    is_control = row[0] in CONTROL_CUE_INDICATORS
    this_dist = Decimal(row[2])

    if idx == 1 and this_dist <= 0.1:
        this_dist = Decimal("0")

    if row[0] == END_INDICATOR:
        has_end = True
        row[1] = END_TEXT + ": " + row[1]

    return {
        "dict": {
            "turn": _map_direction(row[0]),
            "descr": _map_cue_description(row[1]),
            "dist": last_dist,
            "control": is_control,
        },
        "end": has_end,
        "last": this_dist,
    }


def _create_excel_formats(workbook):
    defaults = {"font_size": 8, "font_name": "Arial"}
    a_12_opts = {"font_size": 12, "font_name": "Arial"}
    centered = {"align": "center", "valign": "vcenter"}
    float_top = {"valign": "top"}
    all_border = {"border": 1}

    return {
        "title_format": workbook.add_format(merge({"rotation": 90}, defaults, all_border)),
        "descr_format": workbook.add_format(merge(centered, defaults, all_border)),
        "control_format": workbook.add_format(
            merge(
                {"bold": True, "bg_color": "#C0C0C0", "text_wrap": True},
                centered,
                a_12_opts,
                all_border,
            )
        ),
        "arial_12": workbook.add_format(merge(a_12_opts, all_border)),
        "arial_12_no_border": workbook.add_format(
            merge(a_12_opts, all_border, {"left_color": "white", "right_color": "white"})
        ),
        "dist_format": workbook.add_format(merge({"num_format": "0.00"}, float_top, a_12_opts, all_border)),
        "dist_format2": workbook.add_format(merge({"num_format": "0.0"}, float_top, a_12_opts, all_border)),
        "cue_format": workbook.add_format(merge({"text_wrap": True}, float_top, a_12_opts, all_border)),
        "red_title": workbook.add_format(merge({"font_color": "red"}, a_12_opts, centered)),
        "black_title": workbook.add_format(merge({"font_color": "black"}, a_12_opts, centered)),
    }


def _setup_worksheet_headers(worksheet, formats, opts, values_array):
    def letter(num_after):
        return chr(65 + num_after)

    curr_col = 0
    num_cols = 4
    if opts.include_from_last:
        num_cols += 1
    if opts.hide_direction:
        num_cols -= 1

    last_col_letter = letter(num_cols)

    # Header rows
    worksheet.merge_range("A1:{0}1".format(last_col_letter), "INSERT NAME OF RIDE", formats["red_title"])
    worksheet.merge_range("A2:{0}2".format(last_col_letter), "insert date of ride", formats["red_title"])
    worksheet.merge_range("A3:{0}3".format(last_col_letter), "insert name of Ride Organizer", formats["red_title"])
    worksheet.merge_range("A4:{0}4".format(last_col_letter), "insert Start location", formats["red_title"])
    worksheet.merge_range("A5:{0}5".format(last_col_letter), "insert Finish location", formats["red_title"])

    # Column headers
    worksheet.write("A6", "Dist.(cum.)", formats["title_format"])
    curr_col += 1

    if opts.include_from_last:
        worksheet.write(letter(curr_col) + "6", "Dist. Since", formats["title_format"])
        curr_col += 1

    worksheet.write(letter(curr_col) + "6", "Turn", formats["title_format"])
    curr_col += 1

    if not opts.hide_direction:
        worksheet.write(letter(curr_col) + "6", "Direction", formats["title_format"])
        curr_col += 1

    # Column widths
    width = 7.5 if values_array[len(values_array) - 1]["dist"] > DISTANCE_THRESHOLD_FOR_WIDE_COLUMN else 6.5
    worksheet.set_column("A:A", width)
    worksheet.set_column("B:" + letter(curr_col), 5.6)
    worksheet.write(letter(curr_col) + "6", "Route Description", formats["descr_format"])
    worksheet.set_column("{0}:{0}".format(letter(curr_col)), 39)
    curr_col += 1

    worksheet.write(letter(curr_col) + "6", "Dist.(int.)", formats["title_format"])
    worksheet.set_column("{0}:{0}".format(letter(curr_col)), 5.6)

    return curr_col, last_col_letter


def _write_data_row(
    worksheet, row, row_num, curr_col, last_col_letter, last_was_control, ctrl_sum, curr_dist, formats, opts
):
    def letter(num_after):
        return chr(65 + num_after)

    # Distance columns
    if row_num == FIRST_DATA_ROW + 1:  # First data row after headers
        worksheet.write(row_num, curr_col, 0, formats["dist_format"])
    elif row_num > FIRST_DATA_ROW + 1:
        worksheet.write(
            row_num,
            curr_col,
            "=A{0}+{1}{0}".format(
                row_num if not last_was_control else row_num - 1,
                last_col_letter,
            ),
            formats["dist_format"],
        )
    curr_col += 1

    if opts.include_from_last:
        worksheet.write(row_num, curr_col, ctrl_sum, formats["dist_format2"])
        curr_col += 1

    # Handle control vs regular cue
    if row["control"]:
        worksheet.write_string(row_num, curr_col, "", formats["arial_12_no_border"])
        curr_col += 1

        if not opts.hide_direction:
            worksheet.write_string(row_num, curr_col, "", formats["arial_12"])
            curr_col += 1

        worksheet.write_string(row_num, curr_col, row["descr"], formats["control_format"])
        curr_col += 1
        worksheet.write_string(row_num, curr_col, "", formats["arial_12"])
        height = CONTROL_ROW_HEIGHT
    else:
        worksheet.write_string(row_num, curr_col, row["turn"], formats["arial_12"])
        curr_col += 1

        if not opts.hide_direction:
            worksheet.write_string(row_num, curr_col, "", formats["arial_12"])
            curr_col += 1

        worksheet.write_string(row_num, curr_col, row["descr"], formats["cue_format"])
        curr_col += 1
        worksheet.write_number(row_num, curr_col, curr_dist, formats["dist_format"])
        height = REGULAR_ROW_HEIGHT

    worksheet.set_row(row_num, height)
    return height


def _add_footer_information(worksheet, row_num, last_col_letter, formats):
    row_num += 1
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "IN CASE OF ABANDONMENT OR EMERGENCY",
        formats["black_title"],
    )
    row_num += 1
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "PHONE: ** ORGANIZER'S NUMBER **",
        formats["black_title"],
    )
    row_num += 2
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "ST=Turn Around, BL=Bear Left, BR=Bear Right, CO=Continue On, L/R=Left Immediate Right",
        formats["black_title"],
    )
    return row_num + 1


def generate_excel(filename, values_array, opts):
    import xlsxwriter

    try:
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        formats = _create_excel_formats(workbook)
        col_num, last_col_letter = _setup_worksheet_headers(worksheet, formats, opts, values_array)

        # Data processing variables
        row_num = FIRST_DATA_ROW
        ctrl_sum = 0
        last_dist = 0
        pbreak_list = []
        last_was_control = False

        for i in range(len(values_array)):
            row = values_array[i]
            curr_dist = row["dist"] - last_dist
            last_dist = 0
            curr_col = col_num

            if opts.verbose:
                tmp = "We're on row {0} at {1}kms".format(row_num - 6, row["dist"])
                if "onto" in row["descr"]:
                    tmp = "({0}) ".format(row["descr"][row["descr"].find("onto") + 5 :]) + tmp
                else:
                    tmp = row["descr"] + ": " + tmp
                print(tmp)
                print("\testimated distance is {0}kms since last".format(curr_dist))

            if i > 0:
                _write_data_row(
                    worksheet,
                    row,
                    row_num,
                    curr_col,
                    last_col_letter,
                    last_was_control,
                    ctrl_sum,
                    curr_dist,
                    formats,
                    opts,
                )

            if row["control"]:
                ctrl_sum = 0
                last_was_control = True
                last_dist -= curr_dist
                pbreak_list.append(row_num + 1)
            else:
                last_was_control = False
                ctrl_sum += curr_dist
                if pbreak_list and (row_num - pbreak_list[-1]) == PAGE_BREAK_ROW_INTERVAL:
                    pbreak_list.append(row_num)

            last_dist += row["dist"]
            row_num += 1

        final_row = _add_footer_information(worksheet, row_num, last_col_letter, formats)

        # Printing setup
        worksheet.print_area("A1:{0}{1}".format(last_col_letter, final_row))
        if len(pbreak_list) > 2:
            pbreak_list = pbreak_list[1:-1]
            worksheet.set_h_pagebreaks(pbreak_list)

    finally:
        if workbook is not None:
            workbook.close()


# our happy exports
__all__ = ["read_csv_to_array", "format_array", "generate_excel"]
