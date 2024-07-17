import csv

class InputHandler:
    def read_tsv(self, file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            return list(reader)

    def get_column_names(self, file_path):
        with open(file_path, 'r', newline='', encoding='utf-8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            return next(reader)  # Return the header row