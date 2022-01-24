import csv
with open('food-scores.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    with open('../src/food-scores.js', 'w') as outfile:
        outfile.write('let foods; export const foods = [\n')
        for row in reader:
            outfile.write(f'\t{{"name": "{row[0]}", "score": {row[1]}}},\n')
        outfile.write(']')