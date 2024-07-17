import os
from dotenv import load_dotenv
from input_handler import InputHandler
from data_generator import DataGenerator
from output_formatter import OutputFormatter

load_dotenv()

API_KEY = os.getenv("TOGETHER_API_KEY")

def main():
    input_handler = InputHandler()
    data_generator = DataGenerator(API_KEY)
    output_formatter = OutputFormatter()

    input_file = input("Enter the path to your input TSV file: ")
    examples = input_handler.read_tsv(input_file)
    column_names = input_handler.get_column_names(input_file)

    num_samples = int(input("Enter the number of samples to generate: "))
    generated_data = data_generator.generate(examples, num_samples)

    output_file = "generated_data.tsv"
    output_formatter.save_tsv(generated_data, output_file, column_names)

    print(f"Generated {num_samples} samples and saved to {output_file}")

if __name__ == "__main__":
    main()