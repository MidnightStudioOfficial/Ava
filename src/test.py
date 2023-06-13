from core.skill.skill import Skills



s = Skills("Data")

# load skill sample data
training_sentences = []
training_labels = []
labels = []
responses = []
    
for intent, skill in s.skills.items():
    for sample in skill.samples:
        training_sentences.append(sample)
        training_labels.append(intent)
    if intent not in labels:
        labels.append(intent)
        
print(training_sentences)
print(training_labels)
print(labels)
print(responses)