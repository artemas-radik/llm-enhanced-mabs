# Example: reuse your existing OpenAI setup
from openai import OpenAI
import json
from tqdm import tqdm

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

def get_response(name, description, review):
    iters = 0
    while iters < 10:
        iters +=1
        messages = [
            {"role": "system", "content": "Below is an instruction that describes a task. Write a response that appropriately completes the request. Be extremely concise."},

            {"role": "user", "content": "Below is a name and description of an eCommerce product, as well as a review of the product left by a customer. Output an integer between 0 and 100 describing how helpful this review would be to other customers, with 0 being the least helpful and 100 being the most helpful. Make sure you pay special attention to the fact that reviews with negative sentiment are not necessarily less helpful."},

            {"role": "user", "content": f"Name: \"{name}\". Description: \"{description}\". Review: \"{review}\""},
        ]

        completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=messages,
        temperature=0.7,
        )

        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        messages.append({"role": "user", "content": "Output just the single integer from your previous response and nothing else."})

        completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=messages,
        temperature=0.7,
        )

        messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        rating = completion.choices[0].message.content

        if rating.isdigit():
            num = int(rating)
            if 0 <= num <= 100:
                return messages, rating
            
    return [], 50

file_name = "./filtered.txt"
results = []

total_lines = sum(1 for _ in open(file_name, 'r'))

with open(file_name, 'r') as file:
    for line in tqdm(file, total=total_lines):
        try:
            json_object = json.loads(line)
            messages, rating = get_response("Kindle Fire", "The Kindle Fire tablet is a lightweight, sleek device where you can navigate the internet, store photos, make video calls and more.", json_object["reviewText"])
            json_object["llm_messages"] = messages
            json_object["llm_rating"] = rating
            results.append(json_object)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

with open("results.txt", 'w') as out_file:
    for item in results:
        json_str = json.dumps(item)
        out_file.write(json_str + '\n')