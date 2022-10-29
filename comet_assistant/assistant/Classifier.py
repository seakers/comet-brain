import torch
import numpy as np

from transformers import AutoTokenizer

from comet_assistant.assistant.ModelLoader import ModelLoader


class Classifier:

    def __init__(self):
        self.model_loader = ModelLoader()

    def classify_role(self, command):
        # Get Models
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
        loaded_model = self.model_loader.get_model('general')

        # Evaluation
        # ==================================================
        inputs = tokenizer(command, return_tensors="pt")
        outputs = loaded_model(**inputs)
        logits = outputs.logits
        prediction = self.interpret_logits(logits, top_number=1)
        return prediction[0]

    def classify_role_intent(self, command, role):
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
        print('--> Role Intent Classification Max Confidence:', max_value)
        if max_value > 0.95:
            top_number = 1
        elif max_value > 0.90:
            top_number = 3
        else:
            self.not_answerable()
            return

        prediction = self.interpret_logits(logits, top_number=top_number)
        return prediction[0]






    def not_answerable(self):
        return 0






    def interpret_logits(self, logits, top_number=1):
        logits_list = logits.tolist()
        predicted_labels = []
        for item in logits_list:
            index_list = np.argsort(item)[-top_number:]
            index_list = index_list[::-1]
            predicted_labels.append(np.ndarray.tolist(index_list))
        return predicted_labels



