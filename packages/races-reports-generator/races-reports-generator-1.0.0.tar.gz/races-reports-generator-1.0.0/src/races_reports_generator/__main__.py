import os
import argparse
from main import check_abbreviations, check_log, get_results, print_report


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", required=True, help="Path to folder with log files")
    parser.add_argument("--asc", action="store_true", help="Sort results in ascending order")
    parser.add_argument("--desc", action="store_true", help="Sort results in descending order")
    parser.add_argument("--driver", help="Show statistics for a specific driver")
    return parser.parse_args()

def main():
    args = parse_arguments()
    folder_path = args.files
    is_rev_order = args.desc
    if args.driver:
        r_name = args.driver
    else:
        r_name = ""

    races = {}
    abbrevs_file_path = os.path.join(folder_path, "abbreviations.txt")
    races.update(check_abbreviations(abbrevs_file_path))
    start_log_path = os.path.join(folder_path, "start.log")
    races.update(check_log(start_log_path, "start_logs"))
    end_log_path = os.path.join(folder_path, "end.log")
    races.update(check_log(end_log_path, "end_logs"))
    results = get_results(races, r_name, is_rev_order)
    print_report(results)


if __name__ == "__main__":
    main()