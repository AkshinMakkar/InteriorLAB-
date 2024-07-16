import json
import os

class ScadInitializer:
    def __init__(self, counter_file=r"C:\Users\prana\Documents\GitHub\InteriorLab\scadCounter.JSON"):
        self.counter_file = counter_file

    def read_counter(self):
        # Read the counter value from the JSON file.
        if not os.path.exists(self.counter_file):
            # Initialize the counter file if it doesn't exist
            with open(self.counter_file, 'w') as f:
                json.dump({"scadCounter": 0}, f)

        # If file exists
        with open(self.counter_file, 'r') as f:
            data = json.load(f)

        return data["scadCounter"]
    
    def update_counter(self):
        # Increment the counter value in the JSON value.
        counter = self.read_counter()
        counter += 1
        with open(self.counter_file, 'w') as f:
            json.dump({"scadCounter": counter}, f)

