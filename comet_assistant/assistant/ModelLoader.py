import os
from pathlib import Path
from transformers import AutoModelForSequenceClassification



class ModelLoader:

    def __init__(self):
        self.model_folder_path = Path('/app/comet_assistant/assistant/models')
        self.nn_models = {}

        for file in os.scandir(self.model_folder_path):
            if file.is_file():
                role_file_path = Path(self.model_folder_path, file.name)
                role_name = role_file_path.stem
                self.nn_models[role_name] = AutoModelForSequenceClassification.from_pretrained(role_file_path)


    def get_model(self, key):
        return self.nn_models[key]


