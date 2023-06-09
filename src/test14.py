from core.chatbot.chatbot import Chatbot, ChatbotProfile
import matplotlib.pyplot as plt
chatbot = Chatbot()
chatbot.train_bot()

# Define a list of test inputs and their expected outputs
test_inputs = ['Hi', 'How are you?', 'What is your name?', 'What do you like to do?']
expected_outputs = ['Hello', 'I am fine, thank you. How about you?', 'My name is MyBot.', 'I like to chat with people.']

# Initialize variables for keeping track of accuracy and number of new responses learned
num_correct = 0
total = len(test_inputs)
num_new_responses = 0

# Test the bot's responses and train it on new responses if it gets a response wrong
for i in range(total):
    input_text = test_inputs[i]
    expected_output = expected_outputs[i]

    # Get the bot's response to the input
    bot_response = chatbot.get_response(input_text)

    # Check if the bot's response matches the expected output
    if str(bot_response) == expected_output:
        num_correct += 1
    else:
        # If the bot's response is wrong, ask the user for the correct response
        print('Input:', input_text)
        print('Expected output:', expected_output)
        print("Bot: I'm sorry, my response was incorrect. Can you please tell me the correct response?")
        #correct_response = input('You: ')

        # Train the bot on the correct response
        #new_trainer = ListTrainer(bot)
        #new_trainer.train([correct_response])

        num_new_responses += 1

    # Print the input, expected output, and bot's response
    print('Input:', input_text)
    print('Expected output:', expected_output)
    print('Bot response:', bot_response)
    print()

# Calculate and print the accuracy and number of new responses learned
accuracy = num_correct / total
print('Accuracy:', accuracy)
print('Number of new responses learned:', num_new_responses)

plt.plot(test_inputs, expected_outputs)
plt.xlabel('Test Inputs')
plt.ylabel('Expected Outputs')
plt.title('Test Results')
plt.show()
