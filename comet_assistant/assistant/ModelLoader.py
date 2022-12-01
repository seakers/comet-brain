from django.conf import settings


class ModelLoader:

    def __init__(self):
        self.nn_models = settings.NN_MODELS

    def get_model(self, key):
        return self.nn_models[key]


