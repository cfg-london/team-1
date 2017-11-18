import csv
from survey import Survey
import collections
import json

CSV_PATH = './Code-for-Good-EM2030_data.csv'

def complete_indicator_line(table):
    last_indicator = ''
    for index, indicator in enumerate(table[0]):
        if indicator == '':
            table[0][index] = last_indicator
        else:
            last_indicator = indicator

def read_data(file):
    table = []

    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            table.append(row)

    return table

def extract_surveys(table):
    surveys = []

    for row_id, row in enumerate(table):
        # Ignore header
        if (row_id < 4):
            continue

        # Ignore empty rows
        if len(row) is 0:
            continue

        country = row[0]
        survey = Survey(table[0], table[3])

        # Ignore blank lines
        if country is '':
            continue

        for index, value in enumerate(row):
            crt_indicator = table[0][index]
            crt_category = table[3][index]

            if index < 2:
                survey.indicators[crt_indicator][crt_category] = value
                continue
            elif value is not '':
                survey.indicators[crt_indicator][crt_category] += float(value)

        surveys.append(survey)

    return surveys

def parse_data(file):
    table = read_data(file)
    complete_indicator_line(table)

    surveys = extract_surveys(table)
    return surveys

def horizontal_chart(countries, surveys_by_country):
    # dataset = [
    #     {label: "Men", "Not Satisfied": 20, "Not Much Satisfied": 10, "Satisfied": 50, "Very Satisfied": 20},
    #     {label: "Women", "Not Satisfied": 15, "Not Much Satisfied": 30, "Satisfied": 40, "Very Satisfied": 15}
    # ];

    answer = []

    for c in surveys_by_country.keys():
        crt_pairs = {}
        crt_pairs['label'] = c
        print(surveys_by_country[c].indicators)
        for indicator in surveys_by_country[c].indicators:
            if 'Total' in surveys_by_country[c].indicators[indicator]:
                crt_pairs[indicator] = surveys_by_country[c].indicators[indicator]['Total']
                print('adsdasdasdasdasd')
        ordered_dict = collections.OrderedDict(sorted(crt_pairs.items()))
        answer.append(ordered_dict)

    return json.dumps(answer)

if __name__ == "__main__":
    surveys = parse_data(CSV_PATH)

    surveys_by_country = {}
    for s in surveys:
        if s.indicators['Indicator']['Country'].startswith('Colombia') and s.indicators['Indicator']['Survey'].startswith('2015 DHS'):
            surveys_by_country['Colombia'] = s
        if s.indicators['Indicator']['Country'].startswith('India') and s.indicators['Indicator']['Survey'].startswith('2005-06 DHS'):
            surveys_by_country['India'] = s
        if s.indicators['Indicator']['Country'].startswith('Indonesia') and s.indicators['Indicator']['Survey'].startswith('2012 DHS'):
            surveys_by_country['Indonesia'] = s
        if s.indicators['Indicator']['Country'].startswith('Kenya') and s.indicators['Indicator']['Survey'].startswith('2015 MIS'):
            surveys_by_country['Kenya'] = s
        if s.indicators['Indicator']['Country'].startswith('Senegal') and s.indicators['Indicator']['Survey'].startswith('2016 DHS'):
            surveys_by_country['Senegal'] = s

    print(horizontal_chart(['Indonesia', 'India'], surveys_by_country))