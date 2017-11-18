import csv
from survey import Survey

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
    print(len(surveys))

if __name__ == "__main__":
    parse_data(CSV_PATH)