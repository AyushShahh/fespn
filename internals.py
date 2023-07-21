from csv import DictReader, DictWriter
from math import ceil

def score(m1, m2):
    i = (m1 + m2) / 4
    if i >= 12:
        i += 4
        if i > 30:
            i= 30
    return ceil(i)

# Calculate the required fields and write to the output CSV
with open('students_data.csv', 'r') as csvfile_in, open('internals.csv', 'w', newline='') as csvfile_out:
    reader = DictReader(csvfile_in)
    fieldnames = ['name', 'mat_i', 'bee_i', 'egd_i', 'pps_i', 'eng_i', 'bonus']
    writer = DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        full = 16 if row['full'] == '1' else 12
        bonus_marks = (float(row['attendance']) * full) / 100

        writer.writerow({
            'name': row['name'],
            'mat_i': score(int(row['mat2mse1']), int(row['mat2mse2'])),
            'bee_i': score(int(row['beemse1']), int(row['beemse2'])),
            'egd_i': score(int(row['egdmse1']), int(row['egdmse2'])),
            'pps_i': score(int(row['ppsmse1']), int(row['ppsmse2'])),
            'eng_i': score(int(row['engmse1']), int(row['engmse2'])), 
            'bonus': ceil(bonus_marks)
        })
