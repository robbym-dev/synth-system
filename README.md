# Synthetic Data Generator for Financial Topics

This project provides a robust synthetic data generation pipeline for creating financial topic datasets. It uses few-shot learning and the Llama 2 language model to generate high-quality, diverse synthetic data.

## Features

- Generate synthetic financial topic data based on few-shot examples
- Configurable number of samples
- Balanced distribution of ratings (Good, Bad, Unsure)
- Uses Llama 2 via Together AI for high-quality text generation

## Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone this repository:
```
git clone https://github.com/robbym-dev/synth-system.git
cd synth-system
```

2. Install required packages:

```
pip install -r requirements.txt
```

3. Set up your Together AI API key:
```
EXPORT TOGETHER_API_KEY=<together_api_key_here>
```

### Usage

1. Prepare your few-shot examples file:
- Create a TSV (Tab-Separated Values) file with your examples
- Format: `input_data`, `prompt_template`, `generated_content`, `rating`
- Save it as `input_examples.tsv` in the project root

2. Run the generator:
```
python main.py
```

3. When prompted:
- Enter the path to your input TSV file (e.g., `input_examples.tsv`)
- Enter the number of synthetic samples you want to generate

4. The generated data will be saved in `generated_data.tsv`

## Project Structure

- `main.py`: Main script to run the generator
- `data_generator.py`: Core logic for synthetic data generation
- `input_handler.py`: Handles reading input examples
- `output_formatter.py`: Formats and saves generated data

## Future Developments

- Implement more diverse primitive generators for various data types
- Add support for different domains beyond financial topics
- Enhance coverage maximization strategies
- Implement more robust quality control and validation mechanisms
- Add support for different output formats (JSON, CSV, etc.)
- Integrate with other language models and APIs for comparison and flexibility

## License
This project is licensed under the MIT License - see the LICENSE file for details.