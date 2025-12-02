import json

def load_json(path):
    with open(path, "r") as f:
        raw = f.read()
    return json.loads(raw)

def parse(raw_data):
    for x in raw_data:
        print(x)   



def write_to_file(raw_data):
    with open("output.txt", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False)



def main():
    raw_data = load_json("sample-data.json")
    parse(raw_data)
    write_to_file(raw_data)


main()