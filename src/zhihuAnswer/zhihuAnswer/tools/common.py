import re


def extract_num(text):
    match_pattern = re.match('.*?(\d+).*', text)
    if match_pattern:
        nums = int(match_pattern.group(1))
    else:
        nums = 0
    return nums