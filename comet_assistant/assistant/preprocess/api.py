import os
from string import Template
import random
import glob
from comet_assistant.assistant.preprocess.Substitutions import Substitutions
from django.conf import settings


class Preprocessing:

    def __init__(self):
        self.app_path = settings.COMET_PATH
        self.templates_path = self.app_path + '/comet_assistant/assistant/questions'
        self.data_path = self.app_path + '/comet_assistant/assistant/data'
        self.templates = self.load_templates()
        self.substitutions = Substitutions()

        # --> Create data path if dne
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def load_templates(self):
        template_objects = []
        for filename in os.listdir(self.templates_path):
            filepath = os.path.join(self.templates_path, filename)

            # --> Load template object
            template_objects.append(self.load_template(filepath, filename, self.data_path))

        return template_objects

    def load_template(self, filepath, filename, datapath):

        # --> Parameters to extract from template
        question_class = int(filename.split('.', 1)[0])
        num_questions = 0
        parameter_map = {}
        labels = ""
        template_lines = []

        # --> Extract parameters
        with open(filepath, 'r') as file:
            state = 1
            for line in file:
                if line == '--\n':
                    state += 1
                else:
                    if state == 1:
                        num_questions = int(line[:-1])
                    elif state == 2:
                        line_info = line.split()
                        parameter_map[line_info[0]] = line_info[1]
                    elif state == 3:
                        labels = line[:-1]
                    elif state == 4:
                        template_lines.append(Template(line[:-1]))

        return {
            'num_questions': num_questions,
            'parameter_map': parameter_map,
            'labels': labels,
            'template_lines': template_lines,

            'file': filename,
            'path': filepath,
            'question_class': question_class,
            'outfile': os.path.join(datapath, filename)
        }


    def clean_data_dir(self):
        files = glob.glob(self.data_path + '/*')
        for f in files:
            os.remove(f)


    def process(self):
        self.clean_data_dir()
        for qtemplate in self.templates:
            with open(qtemplate['outfile'], 'w') as file:
                file.write(qtemplate['labels'] + "\n")

                # --> Generate the random questions with substitutions
                for i in range(1, qtemplate['num_questions'] + 1):

                    # --> 1. Get a random substitution for each template parameter
                    params = {}
                    for param, param_type in qtemplate['parameter_map'].items():
                        params[param] = self.substitutions.get_substitution(param_type)

                    # --> 2. Get random template line for substitution
                    template_str = random.choice(qtemplate['template_lines'])

                    # --> 3. Substitute values into template line
                    question = template_str.substitute(params)
                    file.write(question + '\n')





