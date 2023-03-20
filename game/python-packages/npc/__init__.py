__version__ = "0.0.1"

# Import necessary modules
import chatgpt
import re

# Define a Non-Player Character (NPC) class for a chatbot-based application
class NPC:
    # Initialize the NPC with required information and optional controllers and proxy
    def __init__(self, character, initial_message, prompt, controllers=[], proxy=''):
        self.initial_message = initial_message
        self.prompt = prompt
        self.controllers = controllers
        self.character = character
        self.messages = [
            {"role": "system", "content": self.prompt},
            {"role": "assistant", "content": self.initial_message}
        ]
        self.proxy = proxy

    # Read and execute the initial message by the NPC
    def read_initial_message(self):
        self.character(self.initial_message)

    # Process user input and add it to the message history
    def user_says(self, pov, user_input):
        # Append the user input to the message history
        self.messages.append(
            {"role": "user", "content": user_input}
        )

        # Display the user input
        pov(user_input + "{nw}")

        # Ensure the message history does not exceed the 10000-character limit
        while len(str(self.messages)) > 10000:
            self.messages.pop(1)

        # Attempt to generate a response using the ChatGPT API
        try:
            self.messages = chatgpt.completion(self.messages, proxy=self.proxy)

            # Extract the NPC's response from the generated messages
            response = self.messages[-1]["content"]
        except:
            # Display an error message if the API call fails
            response = "(There was an error please try again)"

        # Display the NPC's response line by line with a specified time delay between messages
        self.display_line_by_line(response, 1)

    # Split a given text into sentences and display them one by one with a time delay
    def display_line_by_line(self, text, time_between_messages=1):

        split_into_sentences = []

        # Split the text into sentences using regular expressions
        split_into_sentences = re.split(r'\.\s|\n\n', text)

        # Iterate through the sentences and display them with a time delay
        for sentence in split_into_sentences:

            # Remove leading and trailing whitespace from the sentence
            sentence = sentence.strip()

            # Display the sentence with or without a time delay depending on its position in the list
            if sentence == split_into_sentences[-1]:
                self.character(sentence)
            else:
                self.character(sentence + "{w=" + str(time_between_messages) + "}{nw}")
