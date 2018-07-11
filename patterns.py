import sys
import argparse
import re

def get_data():
    """
    Reads data in stdin and returns a mapping of patterns and paths
    """

    data = sys.stdin.readlines()
    try:
        pat_len = int(data[0])
    except ValueError:
        print('Error: The first input should be an integer')

    patterns = []
    for d in data[1:pat_len+1]:
        d = d.strip()
        patterns.append(d.split(','))

    try:
        url_len = int(data[pat_len + 1])
    except ValueError:
        print('Error: The value in this position should be an integer')

    paths = []
    for p in data[pat_len+2:]:
        p = p.strip()
        path = [value for value in p.split('/') if not value == '']
        paths.append(path)

    results = {
        'patterns': patterns,
        'paths': paths
    }

    return results

def build_regex_pattern(string, case=False):
    """
    For a given pattern(string) returns its regex compatible pattern that
    matches all of its instances and for a single '*', returns a regex that
    matches any sequence of ASCII characters
    """

    wild_card = '*'
    case_regex = '(?i)'
    ascii_regex = '[ -~]+'
    special_regex = re.compile(r'[^\w]+|_+')
    backslash = '\\'
    if not string == wild_card:
        pos = 0
        last_pos = 0
        rebuilt_string = ''
        #In case a pattern is a string containing special characters, we rebuild
        # its regex compatible version with '\' in front of @,!,~,* etc...
        while pos < len(string):
            if special_regex.match(string[pos]):
                if pos == 0:
                    rebuilt_string += backslash + string[pos]
                else:
                    rebuilt_string += string[last_pos:pos] + backslash + string[pos]
                last_pos = pos + 1
            pos += 1
        rebuilt_string += string[last_pos:]
        string = rebuilt_string
    else:
        string = string.replace(wild_card, ascii_regex)
    regex_string = '^' + string + '$'

    if case:
        regex_string = '{}'.format(case_regex) + regex_string

    return re.compile(regex_string, re.A)

def path_match(list_pattern, list_path, case=False):
    """
    Give a pattern and a path, broken down in list respectively by ',' and '/',
    the path cleaned of eventual leading and trailing '/',
    return True if the pattern matches the path, False otherwise
    """

    if not len(list_pattern) == len(list_path):
        return False

    index = 0
    match = True
    while index < len(list_path) and match:
        pattern = build_regex_pattern(list_pattern[index], case=case)
        if not pattern.match(list_path[index]):
            match = False
        index += 1
    return match

def count_wildcards(pattern):
    """
    Returns the number n of wildcards in a given pattern
    The given pattern should be a string ex. 'g,*,ab,*,mg'
    """

    wild_card = '*'
    patt_list = pattern.split(',')
    count = 0
    for p in patt_list:
        if p == wild_card:
            count += 1
    return count


def best_patterns(patt1, patt2):
    """
    Given two patterns, returns the one for which the leftmost wildcard appears
    further to the righ recursively, giving priority to the one with less
    wildcards
    patt1, patt2 -> string
    """

    wild_card = '*'
    #We return the pattern with less wildcards
    if count_wildcards(patt1) < count_wildcards(patt2):
        return patt1
    elif count_wildcards(patt1) > count_wildcards(patt2):
        return patt2

    #Of the two patterns, we return the one for which a non wildcard character
    #appears first recursively without necessarely going through
    #the entire pattern.
    else:
        match = patt1
        i = 0
        found = False
        while i < len(patt1) and not found:
            if not patt1[i] == wild_card and not patt2[i] == wild_card:
                i += 1
            elif patt1[i] == wild_card and patt2[i] == wild_card:
                i += 1
            elif patt1[i] == wild_card and not patt2[i] == wild_card:
                match = patt2
                found = True
            else:
                match = patt1
                found = True

    return match


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', help='True or False for case sensitive match',
        dest= 'case', default=False
    )
    args = parser.parse_args()

    data = get_data()
    for path in data['paths']:
        match = 'NO MATCH'
        match_len_path = [p for p in data['patterns'] if len(p) == len(path)]
        #We restrict the search on patterns of the same length as the path
        for patt in match_len_path:
            if path_match(patt, path, case=args.case):
                #If we previously found a match we update it with the best of
                #of the two.
                if not match == 'NO MATCH':
                    match2 = ','.join(p for p in patt)
                    match = best_patterns(match, match2)
                else:
                    match = ','.join(p for p in patt)
        print(match)
