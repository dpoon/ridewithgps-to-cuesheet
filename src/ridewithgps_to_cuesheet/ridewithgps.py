from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Literal

import xlsxwriter
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

"""
    This program is designed to convert a RideWithGPS
    exported csv file, into a BC Randonneurs Routesheet

    TODO: direction legend
"""


# Excel formatting constants
DISTANCE_THRESHOLD_FOR_WIDE_COLUMN = 1000
FIRST_DATA_ROW = 6
CONTROL_ROW_HEIGHT: Literal[20] = 20
REGULAR_ROW_HEIGHT: Literal[15] = 15


@dataclass
class GenerationOptions:
    include_distance_from_last: bool = False
    hide_direction: bool = False
    verbose: bool = False
    control_cue_indicators = ["Food", "Control", "Start", "End", "Summit"]
    end_indicator = "Summit"
    start_text = "DÉPART"
    end_text = "ARRIVÉE"
    page_break_row_interval: int = 40


@dataclass
class _Formats:
    title_format: Format
    description_format: Format
    control_format: Format
    arial_12: Format
    arial_12_no_border: Format
    dist_format: Format
    dist_format2: Format
    cue_format: Format
    red_title: Format
    black_title: Format


@dataclass
class Cue:
    turn: Turn
    is_end: bool = False
    last_dist: Decimal = Decimal("0.0")


@dataclass
class Turn:
    turn: Literal["CO", "L", "BL", "R", "BR", "TA", ""] | str
    description: str
    dist: Decimal
    is_control: bool = False


logger = logging.getLogger(__name__)


def generate_excel(filename: str, csv_values: List[List[str]], opts: GenerationOptions):
    turns = _parse_to_turns(csv_values, opts)
    try:
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        formats = _create_excel_formats(workbook)
        col_num, last_col_letter = _setup_worksheet_headers(worksheet, formats, opts, turns)

        # Data processing variables
        row_num = FIRST_DATA_ROW
        ctrl_sum = Decimal("0.0")
        last_dist = Decimal("0.0")
        page_break_list = []
        last_was_control = False

        for i in range(len(turns)):
            turn = turns[i]
            curr_dist = turn.dist - last_dist
            last_dist = Decimal("0.0")
            curr_col = col_num

            if opts.verbose:
                tmp = "We're on row {0} at {1}kms".format(row_num - 6, turn.dist)
                if "onto" in turn.description:
                    tmp = "({0}) ".format(turn.description[turn.description.find("onto") + 5 :]) + tmp
                else:
                    tmp = turn.description + ": " + tmp
                logger.info(tmp)
                logger.info("\testimated distance is {0}kms since last".format(curr_dist))

            if i > 0:
                _write_data_row(
                    worksheet,
                    turn,
                    row_num,
                    curr_col,
                    last_col_letter,
                    last_was_control,
                    ctrl_sum,
                    curr_dist,
                    formats,
                    opts,
                )

            if turn.is_control:
                ctrl_sum = Decimal("0.0")
                last_was_control = True
                last_dist -= curr_dist
                page_break_list.append(row_num + 1)
            else:
                last_was_control = False
                ctrl_sum += curr_dist
                if page_break_list and (row_num - page_break_list[-1]) == opts.page_break_row_interval:
                    page_break_list.append(row_num)

            last_dist += turn.dist
            row_num += 1

        final_row = _add_footer_information(worksheet, row_num, last_col_letter, formats)

        # Printing setup
        worksheet.print_area("A1:{0}{1}".format(last_col_letter, final_row))
        if len(page_break_list) > 2:
            page_break_list = page_break_list[1:-1]
            worksheet.set_h_pagebreaks(page_break_list)

    finally:
        if workbook is not None:
            workbook.close()


def _create_excel_formats(workbook: xlsxwriter.Workbook) -> _Formats:
    defaults = {"font_size": 8, "font_name": "Arial"}
    a_12_opts = {"font_size": 12, "font_name": "Arial"}
    centered = {"align": "center", "valign": "vcenter"}
    float_top = {"valign": "top"}
    all_border = {"border": 1}

    return _Formats(
        title_format=workbook.add_format({**{"rotation": 90}, **defaults, **all_border}),
        description_format=workbook.add_format({**centered, **defaults, **all_border}),
        control_format=workbook.add_format(
            {
                **{"bold": True, "bg_color": "#C0C0C0", "text_wrap": True},
                **centered,
                **a_12_opts,
                **all_border,
            }
        ),
        arial_12=workbook.add_format({**a_12_opts, **float_top, **all_border}),
        arial_12_no_border=workbook.add_format(
            {**a_12_opts, **all_border, **{"left_color": "white", "right_color": "white"}}
        ),
        dist_format=workbook.add_format({**{"num_format": "0.00"}, **float_top, **a_12_opts, **all_border}),
        dist_format2=workbook.add_format({**{"num_format": "0.0"}, **float_top, **a_12_opts, **all_border}),
        cue_format=workbook.add_format({**{"text_wrap": True}, **float_top, **a_12_opts, **all_border}),
        red_title=workbook.add_format({**{"font_color": "red"}, **a_12_opts, **centered}),
        black_title=workbook.add_format({**{"font_color": "black"}, **a_12_opts, **centered}),
    )


def _setup_worksheet_headers(
    worksheet: Worksheet, formats: _Formats, opts: GenerationOptions, turns: List[Turn]
) -> tuple[int, str]:
    def as_letter(num_after: int) -> str:
        return chr(65 + num_after)

    curr_col = 0
    num_cols = 4
    if opts.include_distance_from_last:
        num_cols += 1
    if opts.hide_direction:
        num_cols -= 1

    last_col_letter = as_letter(num_cols)

    # Header rows
    worksheet.merge_range("A1:{0}1".format(last_col_letter), "INSERT NAME OF RIDE", formats.red_title)
    worksheet.merge_range("A2:{0}2".format(last_col_letter), "insert date of ride", formats.red_title)
    worksheet.merge_range("A3:{0}3".format(last_col_letter), "insert name of Ride Organizer", formats.red_title)
    worksheet.merge_range("A4:{0}4".format(last_col_letter), "insert Start location", formats.red_title)
    worksheet.merge_range("A5:{0}5".format(last_col_letter), "insert Finish location", formats.red_title)

    # Column headers
    worksheet.write("A6", "Dist.(cum.)", formats.title_format)
    curr_col += 1

    if opts.include_distance_from_last:
        worksheet.write(as_letter(curr_col) + "6", "Dist. Since", formats.title_format)
        curr_col += 1

    worksheet.write(as_letter(curr_col) + "6", "Turn", formats.title_format)
    curr_col += 1

    if not opts.hide_direction:
        worksheet.write(as_letter(curr_col) + "6", "Direction", formats.title_format)
        curr_col += 1

    # Column widths
    width = 7.5 if turns[len(turns) - 1].dist > DISTANCE_THRESHOLD_FOR_WIDE_COLUMN else 6.5
    worksheet.set_column("A:A", width)
    worksheet.set_column("B:" + as_letter(curr_col), 5.6)
    worksheet.write(as_letter(curr_col) + "6", "Route Description", formats.description_format)
    worksheet.set_column("{0}:{0}".format(as_letter(curr_col)), 39)
    curr_col += 1

    worksheet.write(as_letter(curr_col) + "6", "Dist.(int.)", formats.title_format)
    worksheet.set_column("{0}:{0}".format(as_letter(curr_col)), 5.6)

    return curr_col, last_col_letter


def _write_data_row(
    worksheet: Worksheet,
    row: Turn,
    row_num: int,
    curr_col: int,
    last_col_letter: str,
    last_was_control: bool,
    ctrl_sum: Decimal,
    curr_dist: Decimal,
    formats: _Formats,
    opts: GenerationOptions,
) -> None:
    # Distance columns
    if row_num == FIRST_DATA_ROW + 1:  # First data row after headers
        worksheet.write(row_num, curr_col, 0, formats.dist_format)
    elif row_num > FIRST_DATA_ROW + 1:
        worksheet.write(
            row_num,
            curr_col,
            "=A{0}+{1}{0}".format(
                row_num if not last_was_control else row_num - 1,
                last_col_letter,
            ),
            formats.dist_format,
        )
    curr_col += 1

    if opts.include_distance_from_last:
        worksheet.write(row_num, curr_col, ctrl_sum, formats.dist_format2)
        curr_col += 1

    row_height: int = REGULAR_ROW_HEIGHT

    # Handle control vs regular cue
    if row.is_control:
        worksheet.write_string(row_num, curr_col, "", formats.arial_12_no_border)
        curr_col += 1

        if not opts.hide_direction:
            worksheet.write_string(row_num, curr_col, "", formats.arial_12)
            curr_col += 1

        worksheet.write_string(row_num, curr_col, row.description, formats.control_format)
        curr_col += 1
        worksheet.write_string(row_num, curr_col, "", formats.arial_12)
        row_height = CONTROL_ROW_HEIGHT
    else:
        worksheet.write_string(row_num, curr_col, row.turn, formats.arial_12)
        curr_col += 1

        if not opts.hide_direction:
            worksheet.write_string(row_num, curr_col, "", formats.arial_12)
            curr_col += 1

        worksheet.write_string(row_num, curr_col, row.description, formats.cue_format)
        curr_col += 1
        worksheet.write_number(row_num, curr_col, curr_dist, formats.dist_format)

    worksheet.set_row(row_num, row_height)


def _map_direction(direction: str) -> Literal["CO", "L", "BL", "R", "BR", "TA", ""] | str:
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
    logger.warning(f"Unknown direction '{direction}' encountered, defaulting to empty string.")
    return direction


def _map_cue_description(opts: GenerationOptions, description: str) -> str:
    if description == "Start of route":
        return opts.start_text
    elif description == "End of route":
        return opts.end_text
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


def _add_footer_information(worksheet, row_num, last_col_letter, formats):
    row_num += 1
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "IN CASE OF ABANDONMENT OR EMERGENCY",
        formats.black_title,
    )
    row_num += 1
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "PHONE: ** ORGANIZER'S NUMBER **",
        formats.black_title,
    )
    row_num += 2
    worksheet.merge_range(
        "A{0}:{1}{0}".format(row_num, last_col_letter),
        "ST=Turn Around, BL=Bear Left, BR=Bear Right, CO=Continue On, L/R=Left Immediate Right",
        formats.black_title,
    )
    return row_num + 1


def _parse_to_turns(array: List[List[str]], opts: GenerationOptions) -> List[Turn]:
    end_cue_present = False
    last = Decimal("-1.0")
    turns: List[Turn] = []

    for i in range(len(array) - 1, -1, -1):
        parsed = _read_as_cue(array[i], i, last, opts)
        turns[i] = parsed.turn
        end_cue_present = end_cue_present or parsed.is_end
        last = parsed.last_dist

    return turns


def _read_as_cue(row: List[str], idx: int, last_dist: Decimal, opts: GenerationOptions) -> Cue:
    has_end = False
    is_control = row[0] in opts.control_cue_indicators
    this_dist = Decimal(row[2])

    if idx == 1 and this_dist <= 0.1:
        this_dist = Decimal("0")

    if row[0] == opts.end_indicator:
        has_end = True
        row[1] = opts.end_text + ": " + row[1]

    return Cue(
        turn=Turn(
            turn=_map_direction(row[0]),
            description=_map_cue_description(opts, row[1]),
            dist=last_dist,
            is_control=is_control,
        ),
        is_end=has_end,
        last_dist=this_dist,
    )
