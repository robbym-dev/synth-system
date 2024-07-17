import requests
import json
from tqdm import tqdm
import logging
from collections import Counter
import random

logging.basicConfig(level=logging.INFO)

class DataGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.together.xyz/inference"
        self.target_categories = ["Good", "Bad", "Unsure"]

    def generate(self, examples, num_samples):
        generated_data = []
        target_counts = self._calculate_target_counts(num_samples)
        current_counts = Counter()
        
        pbar = tqdm(total=num_samples, desc="Generating samples", unit="sample")

        while sum(current_counts.values()) < num_samples:
            target_category = self._choose_target_category(current_counts, target_counts)
            prompt = self._create_prompt(examples, target_category)
            try:
                response = self._call_api(prompt)
                parsed_response = self._parse_response(response)
                if parsed_response and parsed_response['rating'].lower() == target_category.lower():
                    generated_data.append(parsed_response)
                    current_counts[target_category] += 1
                    pbar.update(1)
            except Exception as e:
                logging.error(f"Error during API call or parsing: {str(e)}")

        pbar.close()
        return generated_data

    def _create_prompt(self, examples, target_category):
        prompt = f"Generate a new, unique entry about a financial topic with the following structure. The rating MUST be '{target_category}':\n\n"
        prompt += "input_data: [A brief financial topic or concept]\n"
        prompt += "prompt_template: [A template with {{topic}} as a placeholder]\n"
        prompt += "generated_content: [2-3 sentences that answer the prompt]\n"
        prompt += f"rating: {target_category}\n\n"
        prompt += "Here are some examples:\n\n"
        
        # Use examples of the target category
        target_examples = [ex for ex in examples if ex['rating'].lower() == target_category.lower()]
        for example in random.sample(target_examples, min(3, len(target_examples))):
            for key, value in example.items():
                prompt += f"{key}: {value}\n"
            prompt += "\n"
        
        prompt += f"Now, generate a new, unique example following the same structure. Remember, the rating MUST be '{target_category}' and the topic should be related to finance or economics:\n"
        return prompt

    def _call_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "togethercomputer/llama-2-70b-chat",
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.7
        }
        response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
        return response.json()['output']['choices'][0]['text'].strip()

    def _parse_response(self, response):
        lines = response.split('\n')
        result = {}
        current_key = None
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                if key in ['input_data', 'prompt_template', 'generated_content', 'rating']:
                    current_key = key
                    result[current_key] = value.strip()
            elif current_key:
                result[current_key] += ' ' + line.strip()
        
        if len(result) == 4 and all(k in result for k in ['input_data', 'prompt_template', 'generated_content', 'rating']):
            return result
        return None

    def _calculate_target_counts(self, num_samples):
        base_count = num_samples // len(self.target_categories)
        remainder = num_samples % len(self.target_categories)
        
        target_counts = {category: base_count for category in self.target_categories}
        for i in range(remainder):
            target_counts[self.target_categories[i]] += 1
        
        return target_counts

    def _choose_target_category(self, current_counts, target_counts):
        remaining = {cat: target_counts[cat] - current_counts[cat] for cat in self.target_categories}
        return max(remaining, key=remaining.get)