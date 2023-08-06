import tempfile
import os
from datetime import timedelta
from main import check_abbreviations, check_log, get_results


def test_check_abbreviations():
    log_msgs = "TES_Test Este_Sets Test\n" \
               "SWF_Ssss Wwwwwww_Ffffffffff Tournament"
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(log_msgs)
    expected_result = {
        "abbreviations": [
            {"short_name": "TES", "racer_name": "Test Este", "race_name": "Sets Test"},
            {"short_name": "SWF", "racer_name": "Ssss Wwwwwww", "race_name": "Ffffffffff Tournament"}
        ]
    }
    abbreviations = check_abbreviations(f.name)
    assert abbreviations == expected_result
    os.unlink(f.name)

def test_check_log():
    expected_result = {
        "start_logs": {
            "TES": ["2018-05-24", "12:05:58.778"],
            "RG": ["2018-05-24", "12:06:27.441"]
        }
    }
    log_msgs = "TES2018-05-24_12:05:58.778\n"\
               "RG2018-05-24_12:06:27.441"
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(log_msgs)
    log = check_log(f.name, "start_logs")
    assert log == expected_result
    os.unlink(f.name)

def test_get_results():
    races = {
        "abbreviations": [
            {"short_name": "ABC", "racer_name": "Alice", "race_name": "Tournament1"},
            {"short_name": "DEF", "racer_name": "Bob", "race_name": "Tournament2"}
        ],
        "start_logs": {
            "ABC": ["2022-01-01", "00:00:00.000"],
            "DEF": ["2022-01-01", "01:00:00.000"]
        },
        "end_logs": {
            "ABC": ["2022-01-01", "00:01:00.000"],
            "DEF": ["2022-01-01", "01:01:00.000"]
        }
    }
    results = get_results(races)
    expected_result = [("Alice", "Tournament1", timedelta(minutes=1)), ("Bob", "Tournament2", timedelta(minutes=1))]
    assert results == expected_result
