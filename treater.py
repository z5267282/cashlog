#!/usr/bin/env python3

import datetime
import json
import re

import keys

# constants

year = 2022
file_name = f'years/{year}.txt'

target = f'json/{year}.json'
indent = 4

shorthands = { 'cr' : 'chiclen roll', 'cpr' : 'crispy pork roll', 'pr' : 'pork roll', 'gc' : 'glass coke', 'mr' : 'mixed roll' }

# logic

def get_date(date_str):
    match = re.fullmatch(date_re, date_str)
    day, month = int(match.group(1)), int(match.group(2))
    return datetime.date(year, month, day).strftime('%d/%m/%Y')

date_re = re.compile(r'([0-9]{1,2})/([0-9]{1,2})(?:/.*)?')
def parse_record(record):
    result = list()
    date_str = record.pop(0)
    date = get_date(date_str)
    while record:
        name = record.pop(0).lower()
        if name in shorthands:
            name = shorthands[name]
        price = record.pop(0).replace('$', '')
        curr = { keys.DATE : date, keys.NAME : name, keys.PRICE : price }
        while record:
            next = record[0]
            mappings = { '@': keys.LOC , 'x': keys.QTY, '+': keys.WITH, '(': keys.SIZE }
            letter = next[0]
            if letter in mappings:
                match letter:
                    case 'x' | '@' | '+':
                        next = next[1:].lower().title()
                    case '(':
                        next = next[1:-1]
                curr[ mappings[letter] ] = next
                record.pop(0)
            else:
                break
        result.append(curr)
    return result

entries = list()
with open(file_name) as f:
    records = f.read().split('\n\n')
    for r in records:
        record = r.split('\n')
        parsed = parse_record(record)
        for p in parsed:
            entries.append(p)

with open(target, 'w') as f:
    json.dump(entries, f, indent=indent)
