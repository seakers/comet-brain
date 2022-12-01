import torch
import numpy as np

from transformers import AutoTokenizer

from comet_assistant.assistant.ModelLoader import ModelLoader


class Classifier:

    def __init__(self):
        self.roles = ["Analyst", "Engineer", "Critic", "Historian", "Teacher"]
        self.model_loader = ModelLoader()

    def get_role(self, role):
        if isinstance(role, int):
            role = self.roles[role]
            return role
        elif isinstance(role, list):
            role = role[0]
            return self.get_role(role)
        else:
            return role

    def get_intent(self, role, intent):
        role = self.get_role(role)
        role_index = self.roles.index(role) + 1
        if isinstance(intent, list):
            intent = intent[0]
        intent_num = str(role_index)
        if intent >= 10:
            intent_num += '0'
        else:
            intent_num += '00'
        intent_num += str(intent)
        return int(intent_num)






    def classify_role(self, command):
        # Get Models
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        loaded_model = self.model_loader.get_model('General')

        # Evaluation
        # ==================================================
        inputs = tokenizer(command, return_tensors="pt")
        outputs = loaded_model(**inputs)
        logits = outputs.logits
        prediction = self.interpret_logits(logits, top_number=1)
        return prediction[0]

    def classify_role_intent(self, command, role):
        role = self.get_role(role)

        # Get Models
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        loaded_model = self.model_loader.get_model(role)

        # Evaluation
        # ==================================================
        inputs = tokenizer(command, return_tensors="pt")
        outputs = loaded_model(**inputs)
        logits = outputs.logits
        softmax = torch.nn.Softmax(dim=1)
        probs = softmax(logits)
        logits = probs.detach().numpy()

        # --> Prediction Confidence
        max_value = np.amax(logits)
        # print('--> Role Intent Classification Max Confidence:', max_value)
        if max_value > 0.95:
            top_number = 1
        elif max_value > 0.90:
            top_number = 3
        else:
            self.not_answerable(max_value)
            return

        prediction = self.interpret_logits(logits, top_number=top_number)
        return prediction[0]


    def not_answerable(self, max_value):
        raise Exception("Question prediction confidence too low: " + str(max_value))






    def interpret_logits(self, logits, top_number=1):
        logits_list = logits.tolist()
        predicted_labels = []
        for item in logits_list:
            index_list = np.argsort(item)[-top_number:]
            index_list = index_list[::-1]
            predicted_labels.append(np.ndarray.tolist(index_list))
        return predicted_labels



