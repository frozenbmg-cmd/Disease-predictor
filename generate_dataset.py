import pandas as pd
import random

symptoms = [
    "fever","cough","headache","fatigue","body_pain","diarrhea","vomiting",
    "sore_throat","chills","nausea","runny_nose","congestion","sneezing",
    "dizziness","abdominal_pain","chest_pain","breathlessness","rash",
    "itching","weight_loss","loss_of_appetite"
]

disease_map = {
    "Common Cold": ["cough","runny_nose","sneezing","sore_throat"],
    "Flu": ["fever","cough","fatigue","body_pain","chills"],
    "Dengue": ["fever","headache","body_pain","rash"],
    "Malaria": ["fever","chills","headache"],
    "Typhoid": ["fever","abdominal_pain","weakness"],
    "Food Poisoning": ["diarrhea","vomiting","nausea","abdominal_pain"],
    "Migraine": ["headache","nausea","dizziness"],
    "Asthma": ["breathlessness","cough"],
    "Allergy": ["rash","itching","sneezing"],
    "Healthy": []
}

rows = []

for _ in range(400):
    disease = random.choice(list(disease_map.keys()))
    row = [0]*len(symptoms)

    if disease != "Healthy":
        for s in disease_map[disease]:
            if s in symptoms:
                row[symptoms.index(s)] = 1

        # noise
        for _ in range(random.randint(0,2)):
            row[random.randint(0,len(symptoms)-1)] = 1

    rows.append(row + [disease])

df = pd.DataFrame(rows, columns=symptoms + ["disease"])
df.to_csv("dataset.csv", index=False)

print("dataset generated")