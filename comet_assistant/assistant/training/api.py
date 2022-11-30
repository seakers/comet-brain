import os
from multiprocessing import Process
from datasets import Dataset
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
from pathlib import Path

# Parameters
# ==================================================

# Data loading params
DEV_SAMPLE_PERCENTAGE = 0.1  # Percentage of the training data to use for validation

# Training parameters
BATCH_SIZE = 16  # Batch Size
NUM_EPOCHS = 5  # Number of training epochs





class Training:

    def __init__(self):
        # self.app_path = '/app'
        self.app_path = '/home/ubuntu/repos/comet-brain'
        self.model_path = self.app_path + '/comet_assistant/assistant/models'
        self.data_path = self.app_path + '/comet_assistant/assistant/data'
        self.roles = ["Analyst", "Engineer", "Critic", "Historian", "Teacher"]





    def load_training_data(self):
        options_list = self.roles
        options_range = range(len(options_list))
        roles_dataset = {"text": [], "labels": []}
        intents_dataset = [{"text": [], "label": []} for _ in options_range]

        num_roles_labels = len(options_list)
        # Add texts and labels
        num_intents_labels = [0 for _ in options_range]
        dict_intents_labels = [{} for _ in options_range]

        files_list = sorted(os.listdir(self.data_path))
        for filename in files_list:
            specific_label = int(filename.split('.', 1)[0])
            file_path = os.path.join(self.data_path, filename)
            with open(file_path, 'r') as file:
                file_labels = next(file)[:-1]
                file_labels = [b == "1" for b in file_labels]
                for index in range(num_roles_labels):
                    if file_labels[index]:
                        dict_intents_labels[index][specific_label] = num_intents_labels[index]
                        num_intents_labels[index] += 1

        for filename in files_list:
            specific_label = int(filename.split('.', 1)[0])
            file_path = os.path.join(self.data_path, filename)
            with open(file_path, 'r') as file:
                file_general_labels = next(file)[:-1]
                file_general_labels = [float(b == "1") for b in file_general_labels]
                for line in file:
                    # Add to general training
                    roles_dataset["text"].append(line)
                    roles_dataset["labels"].append(file_general_labels)

                    # Add to specific models training
                    for index in range(num_roles_labels):
                        if file_general_labels[index]:
                            intents_dataset[index]["text"].append(line)
                            intents_dataset[index]["label"].append(dict_intents_labels[index][specific_label])

        roles_hf_dataset = Dataset.from_dict(roles_dataset)
        intents_hf_dataset = []
        for ds in intents_dataset:
            intents_hf_dataset.append(Dataset.from_dict(ds))
        return roles_hf_dataset, intents_hf_dataset

    def train(self):
        roles_dataset, intents_dataset = self.load_training_data()

        # Train the NN for each skill questions
        self.train_transformer(roles_dataset, "General", "multi")
        for i, intent_dataset in enumerate(intents_dataset):
            self.train_transformer(intent_dataset, self.roles[i], "single")



    def train_transformer(self, dataset, role, classification_type):
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

        def preprocess_function(examples):
            return tokenizer(examples["text"], truncation=True)

        tokenized_dataset = dataset.map(preprocess_function, batched=True)
        split_dataset = tokenized_dataset.train_test_split(test_size=DEV_SAMPLE_PERCENTAGE)
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
        if classification_type == "multi":
            model = AutoModelForSequenceClassification.from_pretrained("allenai/scibert_scivocab_uncased",
                                                                       num_labels=len(
                                                                           split_dataset["train"][0]["labels"]),
                                                                       problem_type="multi_label_classification")
        elif classification_type == "single":
            num_labels = 0
            for data in dataset:
                num_labels = max(num_labels, data["label"])
            model = AutoModelForSequenceClassification.from_pretrained("allenai/scibert_scivocab_uncased",
                                                                       num_labels=num_labels + 1,
                                                                       problem_type="single_label_classification")

        output_path = self.model_path + '/' + role
        training_args = TrainingArguments(
            output_dir=output_path,
            learning_rate=2e-5,
            per_device_train_batch_size=BATCH_SIZE,
            per_device_eval_batch_size=BATCH_SIZE,
            num_train_epochs=NUM_EPOCHS,
            save_strategy="no",
            weight_decay=0.01,
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=split_dataset["train"],
            eval_dataset=split_dataset["test"],
            tokenizer=tokenizer,
            data_collator=data_collator,
        )
        trainer.train()
        model.save_pretrained(output_path)
