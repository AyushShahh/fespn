from csv import DictReader, DictWriter
from math import ceil


# Calculate the required fields and write to the output CSV
with open('students_data.csv', 'r') as csvfile_in, open('internals.csv', 'w', newline='') as csvfile_out:
    reader = DictReader(csvfile_in)
    fieldnames = ['name', 'mat_i', 'bee_i', 'egd_i', 'pps_i', 'eng_i', 'bonus']
    writer = DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:

        maths_internal = (int(row['mat2mse1']) + int(row['mat2mse2'])) / 4
        if maths_internal >= 12:
            maths_internal += 4
            if maths_internal > 30:
                maths_internal = 30
        

        bee_internal = (int(row['beemse1']) + int(row['beemse2'])) / 4
        if bee_internal >= 12:
            bee_internal += 4
            if bee_internal > 30:
                bee_internal = 30
        
        egd_internal = (int(row['egdmse1']) + int(row['egdmse2'])) / 4
        if egd_internal >= 12:
            egd_internal += 4
            if egd_internal > 30:
                egd_internal = 30
        
        pps_internal = (int(row['ppsmse1']) + int(row['ppsmse2'])) / 4
        if pps_internal >= 12:
            pps_internal += 4
            if pps_internal > 30:
                pps_internal = 30

        eng_internal = (int(row['engmse1']) + int(row['engmse2'])) / 4
        if eng_internal >= 12:
            eng_internal += 4
            if eng_internal > 30:
                eng_internal = 30

        full = 16 if row['full'] == '1' else 12
        bonus_marks = (float(row['attendance']) * full) / 100

        writer.writerow({
            'name': row['name'],
            'mat_i': ceil(maths_internal),
            'bee_i': ceil(bee_internal),
            'egd_i': ceil(egd_internal),
            'pps_i': ceil(pps_internal),
            'eng_i': ceil(eng_internal), 
            'bonus': ceil(bonus_marks)
        })
