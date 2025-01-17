from .lamol_datasets import LAMOLDataset
import os
import pandas as pd

DATA_DIR = 'datasets/German/German_1_'

BIN_PROMPTS = {
    'german-sexism' : 'Does the comment include sexism?',
    'german-racism' : 'Does the comment include racism?',
    'german-threat' : 'Is the comment threatening?',
    'german-insult' : 'Is the comment insulting',
    'german-profanity' : 'Does the comment include profanity?'
}

BIN_LABEL_MAPPINGS = {
    'german-sexism' : ["no","yes"],
    'german-racism' : ["no","yes"],
    'german-threat' : ["no","yes"],
    'german-insult' : ["no","yes"],
    'german-profanity' : ["no","yes"]
}


class GermanDataset(LAMOLDataset):
    def __init__(self, args, task_name, split, tokenizer, gen_token, full_init=True, use_vocab_space=True, **kwargs):
        super().__init__(args, task_name, split, tokenizer, gen_token, full_init=False, use_vocab_space=use_vocab_space, **kwargs)
        if self.split == 'dev':
            self.split = 'val'
        if full_init:
            self.init_data()

    def init_data(self):
        data = []
        prompt = BIN_PROMPTS[self.task_name]
        sep_token = self.tokenizer.sep_token
        column_guide = {
            'german-sexism' : 'Sexism Count Crowd',
            'german-racism' : 'Racism Count Crowd',
            'german-threat' : 'Threat Count Crowd',
            'german-insult' : 'Insult Count Crowd',
            'german-profanity' : 'Profanity Count Crowd'
        }
        file_name = DATA_DIR + self.split + '.csv'
        df = pd.read_csv(file_name)
        # TODO: change to following code to apply function to each row
        for _, item in df.iterrows():
            context = item['text']
            answer = item[column_guide[self.task_name]]
            if answer > 0:
                answer = 'yes'
            else:
                answer = 'no'
            label_id = BIN_LABEL_MAPPINGS[self.task_name].index(answer)
            
            entry = {
                'context': context,
                'qas':[{'question': prompt, 'answers': [{'text': answer, 'label': label_id}]}]
            }
            data.append(entry)
        self.data = data
        self.data_tokenization(self.data)
