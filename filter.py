import json

results = []

with open("./asin_B0051VVOB2.json", 'r') as file:
    for line in file:
        try:
            json_object = json.loads(line)

            if json_object['helpful'][0] == 0 and json_object['helpful'][1] == 0:
                continue
            else:
                results.append(json_object)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

results.sort(key=lambda x: x['helpful'][1], reverse=True)

with open("filtered.txt", 'w') as out_file:
    for item in results[:1000]:
        json_str = json.dumps(item)
        out_file.write(json_str + '\n')