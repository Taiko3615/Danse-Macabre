__version__ = "0.0.1"

# Import necessary modules
import chatgpt
import re
import json

# Define a Non-Player Character (NPC) class for a chatbot-based application
class NPC:
    # Initialize the NPC with required information and optional controllers and proxy
    def __init__(self, character, prompt, controllers=[], proxy=''):
        self.prompt = prompt
        self.controllers = controllers
        self.character = character
        self.messages = [
            {"role": "system", "content": self.prompt},
        ]
        self.proxy = proxy

        #A list of labels that the NPC requests the main thread to callback
        #For some reasons it doens't work if the NPC calls them directly
        self.callbacks=[]

    #To be able to save we need to make this object picklable
    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove any unpicklable attributes from the state dictionary here
        state['chatgpt'] = None
        state['re'] = None
        state['json'] = None
        return state

    def __setstate__(self, state):
        # Restore the instance state from the state dictionary
        self.__dict__.update(state)
        import chatgpt
        import re
        import json
        self.chatgpt = chatgpt
        self.re = re
        self.json = json


    #Makes the NPC say something
    def npc_says(self, message, display_message=True):
        self.messages.append(
            {"role": "assistant", "content": message}
        )
        if display_message : self.display_line_by_line(message)

    # Process user input and add it to the message history
    def user_says(self, user_input):

        # Append the user input to the message history
        self.messages.append(
            {"role": "user", "content": user_input}
        )

        #Remove any weird characters
        user_input = re.sub(r'[^\w\s\'!\(\)\?\.\,\:\;\-]', '', user_input)

        # Ensure the message history does not exceed the 10000-character limit
        while len(str(self.messages)) > 10000:
            self.messages.pop(1)

        # Attempt to generate a response using the ChatGPT API
        try:
            self.messages = chatgpt.completion(self.messages, proxy=self.proxy)

            # Extract the NPC's response from the generated messages
            response = self.messages[-1]["content"]
        except Exception as e:
            # Display an error message if the API call fails
            response = "(There was an error please try again)"

        # Display the NPC's response line by line with a specified time delay between messages
        self.display_line_by_line(response)

        #Finally call the controllers
        for controller in self.controllers:
            result = controller.control(self.messages, self.proxy)
            if result is not None:
                self.callbacks.append(result)

    # Split a given text into sentences and display them one by one with a time delay
    def display_line_by_line(self, text):

        #if the text is short enough, we display it in one time.
        if len(text) < 150 :
            self.character(text)
            return

        split_into_sentences = []

        # Split the text into sentences using regular expressions
        split_into_sentences = re.split(r'\.\s|\n\n', text)

        # Iterate through the sentences and display them with a time delay
        for sentence in split_into_sentences:

            # Remove leading and trailing whitespace from the sentence
            sentence = sentence.strip()

            self.character(sentence)

# This class is designed to analyze a conversation and check if specific keywords
# have been mentioned, triggering a callback function if the conditions are met
class Controller:
    def __init__(self, control_phrase, callback, activated = True, permanent = False):
        # Construct the control prompt by including the control_phrase
        self.prompt = (
            """I want you to act as a sentence analyser that responds to questions based on a conversation between a user and an assistant.
        if ("""
            + control_phrase
            + """) then respond this exact word '<TRUE>'
        else respond this exact word '<FALSE>'"""
        )

        # Store the callback function
        self.callback = callback

        #By default the callback is active, but it can be deactivated
        self.activated = activated

        #By default a callback with be deactivated once triggered, but some controllers are permanent
        self.permanent = permanent

    def control(self, messages, proxy):

        #If the callback is deactivated, we skip this
        if not self.activated : return None

        #We will only keep max 5000 characters worth of conversation
        few_last_messages = messages.copy()

        #By default we remove the first message because it's the prompt
        few_last_messages.pop(0)

        # Ensure the message history does not exceed the 5000-character limit
        while len(str(few_last_messages)) > 5000:
            few_last_messages.pop(0)

        # Construct the control messages by including the conversation history
        control_messages = [
            {"role": "system", "content": self.prompt},
            {
                "role": "user",
                "content": (
                    "Here is the conversation between the user and the assistant \n\n <"
                    + json.dumps(few_last_messages)
                    + "> \n\n"
                    + self.prompt
                ),
            },
        ]

        try:
            # Make a ChatGPT API call to get the response
            response = chatgpt.completion(control_messages, proxy=proxy)[-1]["content"]
        except:
            # Display an error message if the API call fails
            response = "<FALSE> ERROR"

        # Sometimes he "hesitates" ans says "I"m not sure if it is True or False"
        # So we only move forward if there's True and not False in his response
        if "<TRUE>" in response and not "<FALSE>" in response and self.callback is not None:

            #If not permanent, then the callback should only be called once
            if not self.permanent : self.activated = False

            return self.callback

        return None
