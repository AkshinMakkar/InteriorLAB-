import json
import os

class PromptMemory:
    def __init__(self, prompt_file=r"C:\Users\prana\Documents\GitHub\InteriorLab\previousPrompts.JSON", response_file=r"C:\Users\prana\Documents\GitHub\InteriorLab\previousResponses.JSON"):
        self.prompt_file = prompt_file
        self.response_file = response_file

    def read_prompts(self):
        # Read the counter value from the JSON file.
        if not os.path.exists(self.prompt_file):
            # Initialize the counter file if it doesn't exist
            with open(self.prompt_file, 'w') as f:
                json.dump({"prompts": ""}, f)

        # If file exists
        with open(self.prompt_file, 'r') as f:
            data = json.load(f)

        return data["prompts"]
    
    def update_prompts(self, new_prompt):
        # Increment the prompts in the JSON value.
        old_prompts = self.read_prompts()

        if old_prompts == "":
            current_prompts = new_prompt
        else:
            current_prompts = old_prompts + ", " + new_prompt
        
        with open(self.prompt_file, 'w') as f:
            json.dump({"prompts": current_prompts}, f)
    
    def read_responses(self):
        # Read the prompts in the JSON file.
        if not os.path.exists(self.response_file):
            # Initialize the prompt file if it doesn't exist
            with open(self.response_file, 'w') as f:
                json.dump({"responses": ""}, f)

        # If file exists
        with open(self.response_file, 'r') as f:
            data = json.load(f)

        return data["responses"]
    
    def update_responses(self, new_response):
        # Increment the prompts in the JSON value.
        old_responses = self.read_responses()
        if old_responses == "":
            current_response = new_response
        else:
            current_response = old_responses + ", " + new_response
        with open(self.response_file, 'w') as f:
            json.dump({"responses": current_response}, f)