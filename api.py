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

def horizontal_chart(countries, surveys_by_indicator):
    # dataset = [
    #     {label: "Men", "Not Satisfied": 20, "Not Much Satisfied": 10, "Satisfied": 50, "Very Satisfied": 20},
    #     {label: "Women", "Not Satisfied": 15, "Not Much Satisfied": 30, "Satisfied": 40, "Very Satisfied": 15}
    # ];

    answer = []

    print(surveys_by_indicator)

    for indicator in surveys_by_indicator.keys():
        crt_pairs = {}
        crt_pairs['label'] = indicator
        # print(surveys_by_country[c].indicators)
        for c in surveys_by_indicator[indicator]:
            # print(c)
            if 'Total' in surveys_by_indicator[indicator][c]:
                print('yes')
                # print(surveys_by_indicator[indicator][c].indicators[indicator])
                crt_pairs[c] = surveys_by_indicator[indicator][c]['Total']
                # print('adsdasdasdasdasd')
                # print(crt_pairs)
        ordered_dict = collections.OrderedDict(sorted(crt_pairs.items()))
        answer.append(ordered_dict)

    return json.dumps(answer)

def hisogram(countries, indicator, surveys_by_country):
    answer = []

    pairs_by_country = {}
    for country in surveys_by_country.keys():
        pairs_by_country[country] = surveys_by_country[country].indicators[indicator]

    print('asdasdasdas')
    print(pairs_by_country)

    for category in pairs_by_country[list(pairs_by_country.keys())[0]]:
        crt_bars = {}
        crt_bars["categorie"] = category

        values = []
        for country in pairs_by_country.keys():
            print(pairs_by_country[country][category])
            values.append({'value': pairs_by_country[country][category], 'rate': country})

        crt_bars["values"] = values

        answer.append(crt_bars)

        # print(c)
        # print(surveys_by_country[c].indicators[indicator])
        # for category in surveys_by_country[c].indicators[indicator]:


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

    print('sbc')
    print(surveys_by_country)

    surveys_by_indicator = {}
    for c in surveys_by_country.keys():
        for i in surveys_by_country[c].indicators:
            if i not in surveys_by_indicator:
                surveys_by_indicator[i] = {}
            surveys_by_indicator[i][c] = surveys_by_country[c].indicators[i]

    print(len(surveys_by_indicator.keys()))

    # print(horizontal_chart(['Indonesia', 'India'], surveys_by_indicator))
    # print(hisogram(['Indonesia', 'India'], 'Wife beating justified for at least one specific reason [Women]', surveys_by_country))

    print(horizontal_chart(['Indonesia', 'India'], surveys_by_indicator))