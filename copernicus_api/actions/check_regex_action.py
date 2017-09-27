import re


def check_iso_string(timestamp):
    """
    Checks if the timestamp matches the ISO Date format. Source for the regex: https://stackoverflow.com/a/6709493/1496040
    :param timestamp: string timestamp
    :return: true if it matches the iso format | false if not
    """
    regular_exp = re.compile(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
    return bool(regular_exp.search(timestamp))



def check_iso_date_string(timestamp):
    """
    Checks if the timestamp matches the ISO Date format. Source for the regex: https://stackoverflow.com/a/6709493/1496040, shortened to verify yyyy-mm-dd strings.
    :param timestamp: string timestamp
    :return: true if it matches the iso format | false if not
    """
    regular_exp = re.compile(r'^\d{4}-\d{2}-\d{2}')
    return bool(regular_exp.search(timestamp))