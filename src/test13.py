import nltk
import sklearn.metrics
import matplotlib.pyplot as plt

def check_accuracy(chatbot_responses, expected_responses):
    # convert the responses to lowercase and tokenize them
    chatbot_responses = [nltk.word_tokenize(response.lower()) for response in chatbot_responses]
    expected_responses = [nltk.word_tokenize(response.lower()) for response in expected_responses]

    # calculate the semantic similarity using wordnet
    similarity_scores = []
    for i in range(len(chatbot_responses)):
        similarity = nltk.jaccard_distance(set(chatbot_responses[i]), set(expected_responses[i]))
        similarity_scores.append(1 - similarity) # convert distance to similarity

    # define a threshold for classifying the responses as correct or incorrect
    threshold = 0.8
    predicted_labels = [1 if score >= threshold else 0 for score in similarity_scores]
    true_labels = [1] * len(chatbot_responses)

    # calculate the accuracy and other metrics
    accuracy = sklearn.metrics.accuracy_score(true_labels, predicted_labels)
    precision = sklearn.metrics.precision_score(true_labels, predicted_labels)
    recall = sklearn.metrics.recall_score(true_labels, predicted_labels)
    f1_score = sklearn.metrics.f1_score(true_labels, predicted_labels)

    # print the results
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1_score}")

    # plot the confusion matrix
    cm = sklearn.metrics.confusion_matrix(true_labels, predicted_labels)
    plt.figure()
    plt.imshow(cm, cmap="Blues")
    plt.title("Confusion matrix")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.colorbar()
    plt.show()

    # plot the ROC curve
    fpr, tpr, thresholds = sklearn.metrics.roc_curve(true_labels, similarity_scores)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.title("ROC curve")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.show()
