import os
from pathlib import Path
from transformers import AutoModelForSequenceClassification



class ModelLoader:

    def __init__(self):
        self.model_folder_path = Path('/app/comet_assistant/assistant/models')
        self.nn_models = {}

        for file in os.scandir(self.model_folder_path):
            if file.is_dir():
                role_name = file.name
                role_model_path = self.model_folder_path / role_name
                loaded_model = AutoModelForSequenceClassification.from_pretrained(role_model_path)
                self.nn_models[role_name] = loaded_model


    def get_model(self, key):
        return self.nn_models[key]


