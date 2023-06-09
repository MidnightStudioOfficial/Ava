from core.chatbot.chatbot import Chatbot, ChatbotProfile
chatbot = Chatbot()
chatbot.train_bot()

import difflib

def check_accuracy2(chatbot_responses, expected_responses, keywords=None, threshold=0.8):
    if keywords is None:
        keywords = []
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for i in range(len(chatbot_responses)):
        similarity = difflib.SequenceMatcher(None, chatbot_responses[i], expected_responses[i]).ratio()
        if similarity >= threshold:
            if all(keyword in chatbot_responses[i] for keyword in keywords):
                true_positives += 1
            else:
                false_positives += 1
        else:
            false_negatives += 1
    accuracy = true_positives / len(chatbot_responses)
    precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return accuracy, precision, recall, f1_score


import matplotlib.pyplot as plt

def check_accuracy(chatbot_responses, expected_responses):
    correct = 0
    incorrect = 0
    for i in range(len(chatbot_responses)):
        if chatbot_responses[i] == expected_responses[i]:
            print(str(chatbot_responses)+" is correct")
            correct += 1
        else:
            print(str(chatbot_responses)+" is wrong")
            incorrect += 1
    accuracy = correct / len(chatbot_responses)
    
    # Plotting the results
    plt.bar(['Correct', 'Incorrect'], [correct, incorrect])
    plt.title('Accuracy Results')
    plt.show()
    
    return accuracy

c = ["play music"]
e = ["Ok I will play some music"]
print(check_accuracy(c, e))

while True:
    i = input("ENTER:")
    print(chatbot.get_response(i))