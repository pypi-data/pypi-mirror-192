import re
from datetime import datetime

def check_abbreviations(abbrevs_file_path: str) -> dict:
    """
        Reads in a file of race abbreviations and returns a dictionary containing the race
        abbreviations as well as the corresponding racer and team names.

        Parameters:
            - abbrevs_file_path (str): the path to the file containing the race abbreviations.

        Returns:
            - races (dict): a dictionary containing the race abbreviations as well as the
                            corresponding racer and team names. The dictionary has the following
                            structure:
                            {
                                "abbreviations": [
                                    {
                                        "short_name": <str>,
                                        "racer_name": <str>,
                                        "race_name": <str>
                                    },
                                    ...
                                ]
                            }
        """
    races = {}
    races_abbrevs = []
    with open(abbrevs_file_path, "r") as file:
        for line_num, line in enumerate(file):
            line = line.replace("\n", "")
            race = {}
            for i, part in enumerate(line.split("_", maxsplit=2)):
                match(i):
                    case 0:
                        race["short_name"] = part
                    case 1:
                        race["racer_name"] = part
                    case 2:
                        race["race_name"] = part
            races_abbrevs.append(race)
    races["abbreviations"] = races_abbrevs
    return races

def check_log(log_path: str, res_key: str) -> dict:
    """Parses a log file to retrieve start times for each race abbreviation and saves them in a dictionary.

        Args:
            log_path (str): The path to the log file to be parsed.
            res_key (str): The key used to store the resulting dictionary in the main dictionary.

        Returns:
            dict: A dictionary containing the start times for each race abbreviation found in the log file, with the race abbreviation as the key and the start time as the value.
        """
    races = {}
    races_start = {}
    with open(log_path, "r") as file:
        for i, line in enumerate(file):
            line = line.replace("\n", "")
            race_abbreviation = re.match("^[A-Z]+", line)
            if race_abbreviation is None:
                continue
            race_abbreviation = race_abbreviation.group(0)
            date = re.search("\d{4}-\d{2}-\d{2}", line)
            if date is None:
                continue
            date = date.group(0)
            time = re.search("\d{2}:\d{2}:\d{2}\.\d{3}$", line)
            if time is None:
                continue
            time = time.group(0)
            races_start[str(race_abbreviation)] = [date, time]
    races[res_key] = races_start
    return races

def get_results(races: dict, r_name: str = "", is_rev_order: bool = False):
    """
        Given a dictionary of races data containing abbreviations, start logs, and end logs,
        computes the duration of each race and returns the sorted list of results.

        Args:
            races: a dictionary with the following keys:
                - "abbreviations": a list of dictionaries, each containing the following keys:
                    - "racer_name": the name of the racer
                    - "race_name": the name of the race
                    - "short_name": the abbreviation of the race
                - "start_logs": a dictionary with the short name of each race as key, and a list with
                    two elements as value, representing the date and time when the race started
                - "end_logs": a dictionary with the short name of each race as key, and a list with
                    two elements as value, representing the date and time when the race ended
            r_name: (str) optional racer name to filter results only for that racer
            is_rev_order: (bool) optional flag to sort the results in reverse order

        Returns:
            A list of tuples, where each tuple contains the racer name, the team name, and the duration
            of the race, sorted by descending order of duration.
    """
    all_abbrevs = races["abbreviations"]
    results = []
    for abbrev in all_abbrevs:
        if r_name and abbrev["racer_name"] != r_name:
            continue
        racer_name = abbrev["racer_name"]
        team_name = abbrev["race_name"]
        short_name = abbrev["short_name"]
        if short_name in races["start_logs"] and short_name in races["end_logs"]:
            start_log = races["start_logs"][short_name]
            end_log = races["end_logs"][short_name]
            start_time = datetime.strptime(f"{start_log[0]} {start_log[1]}", "%Y-%m-%d %H:%M:%S.%f")
            end_time = datetime.strptime(f"{end_log[0]} {end_log[1]}", "%Y-%m-%d %H:%M:%S.%f")
            delta_time = end_time - start_time
            results.append((racer_name, team_name, delta_time))

    results.sort(key=lambda x: x[2], reverse=is_rev_order)
    return results

def print_report(results):
    """
        Prints the race results report to the console.

        Args:
            results (list): A list of tuples containing the racer name, team name, and the time delta of each race.

        Returns:
            None.
            1. John Doe            | Team A                                   | 0:00:25
            2. Jane Smith          | Team B                                   | 0:00:30

        """
    for i, result in enumerate(results):
        racer_name, team_name, delta_time = result
        print(f"{i + 1}. {racer_name:<20} | {team_name:<40} | {delta_time if delta_time.days > -1 else f'{delta_time} [INCORRECT]'}")