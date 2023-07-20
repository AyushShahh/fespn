import pandas as pd
from finalcal import final
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from math import ceil
from csv import DictWriter


# maths, be, bme, phy, es
subject_difficulty_sem1 = [3, 4, 5, 4, 1]
# maths, bee, egd, pps, eng
subject_difficulty_sem2 = [4, 3, 4, 3, 2]

credits = [5, 4, 4, 4, 3]


# Data preparation
data = pd.read_csv('students_data.csv')
internal = pd.read_csv('internals.csv')

names = data['name']
rating1 = 1000 - 5 * (data['roll no 1'] - 1)
rating2 = 1000 - 5 * (data['roll no 2'] - 1)

s1m1_c = ['mat1mse1', 'bemse1', 'bmemse1', 'phymse1', 'esmse1']
s1m2_c = ['mat1mse2', 'bemse2', 'bmemse2', 'phymse2', 'esmse2']
s2m1_c = ['mat2mse1', 'beemse1', 'egdmse1', 'ppsmse1', 'engmse1']
s2m2_c = ['mat2mse2', 'beemse2', 'egdmse2', 'ppsmse2', 'engmse2']
int_c = ['mat_i', 'bee_i', 'egd_i', 'pps_i', 'eng_i']

sem1_mse1 = data[s1m1_c].values.tolist()
sem1_mse2 = data[s1m2_c].values.tolist()
sem2_mse1 = data[s2m1_c].values.tolist()
sem2_mse2 = data[s2m2_c].values.tolist()
internals = internal[int_c].values.tolist()

final_sem1 = final()


# Get data ready for training
X = []
y = []
for i in range(len(names)):
    s1m1 = np.array(sem1_mse1[i]) * 0.45
    s1m2 = np.array(sem1_mse2[i]) * 0.80
    final1 = final_sem1[i]
    
    for i in range(len(s1m1)):
        X.append([s1m1[i], s1m2[i], subject_difficulty_sem1[i], rating1[i]])
        y.append(final1[i])

X = np.array(X)
y = np.array(y)


# Train the neural network
model = MLPRegressor(hidden_layer_sizes=(5, 4), activation='relu', solver='sgd', random_state=43, max_iter=500)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model.fit(X_scaled, y)


# Prepare unseen data for prediction
X_new = []
for i in range(len(names)):
    s2m1 = np.array(sem2_mse1[i]) * 0.45
    s2m2 = np.array(sem2_mse2[i]) * 0.80
    
    for i in range(len(s2m1)):
        X_new.append([s2m1[i], s2m2[i], subject_difficulty_sem2[i], rating2[i]])


# Predict sem 2 final scors
X_new = np.array(X_new)
X_new_scaled = scaler.transform(X_new)
y_pred = model.predict(X_new_scaled)
predicted_final_sem2 = np.reshape(y_pred, (len(y_pred) // 5, 5))


with open('prediction.csv', 'w', newline='') as f:
    fieldnames = ['name', 'spi', 'maths', 'bee', 'egd', 'pps', 'eng']
    writer = DictWriter(f, fieldnames = fieldnames)
    writer.writeheader()

    for i in range(len(names)):
        final_score = np.array(internals[i]) + np.array(predicted_final_sem2[i])
        spi = 0
        for j, k in enumerate(final_score):
            if ceil(k) >= 85: # AA
                spi += credits[j] * 10
            elif ceil(k) >= 75: # AB
                spi += credits[j] * 9
            elif ceil(k) >= 65: # BB
                spi += credits[j] * 8
            elif ceil(k) >= 55: # BC
                spi += credits[j] * 7
            elif ceil(k) >= 45: # CC
                spi += credits[j] * 6
            elif ceil(k) >= 40: # CD
                spi += credits[j] * 5
            elif ceil(k) >= 35: # DD
                spi += credits[j] * 4
            else:
                spi += 0 # FF

        writer.writerow({
            'name': names[i],
            'spi': round(spi / 20, 2),
            'maths': ceil(predicted_final_sem2[i][0]),
            'bee': ceil(predicted_final_sem2[i][1]),
            'egd': ceil(predicted_final_sem2[i][2]),
            'pps': ceil(predicted_final_sem2[i][3]),
            'eng': ceil(predicted_final_sem2[i][4])
        })