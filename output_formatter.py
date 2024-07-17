import csv

class OutputFormatter:
    def save_tsv(self, data, file_path, column_names):
        with open(file_path, 'w', newline='', encoding='utf-8') as tsvfile:
            writer = csv.DictWriter(tsvfile, fieldnames=column_names, delimiter='\t')
            writer.writeheader()
            for item in data:
                writer.writerow(item)