import csv
from math import ceil


grade_mapping = {
    'AA': 0,
    'AB': 10,
    'BB': 20,
    'BC': 30,
    'CC': 40,
    'CD': 45,
    'DD': 50
}


def final():
    sem1 = []
    with open('final_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            final = []
            final.append(score(row['mat_g'], int(row['mat_i'])))
            final.append(score(row['be_g'], int(row['be_i'])))
            final.append(score(row['bme_g'], int(row['bme_i'])))
            final.append(score(row['phy_g'], int(row['phy_i'])))
            final.append(score(row['es_g'], int(row['es_i'])))
            sem1.append(final)
    return sem1


def score(grade, internal):
    r = grade_mapping[grade]
    mark = 85 - r - internal

    if r == 0:
        mark = (mark + 70) / 2
    elif r <= 40 and r >= 10:
        mark = (mark * 2 + 9) / 2
    elif r > 40 and r <= 50:
        mark = (mark * 2 + 4) / 2
    return ceil(mark)


if __name__ == "__main__":
    final()