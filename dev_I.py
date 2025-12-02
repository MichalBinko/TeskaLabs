import json
import asyncio
import aiofiles

async def load_json(path):
    async with aiofiles.open(path, "r") as f:
        raw = await f.read()
    return json.loads(raw)

def parse(raw_data):
    for x in raw_data:
        print('XXX',x)   



def write_to_file(raw_data):
    with open("output.txt", "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False)



async def main():
    raw_data = await load_json("sample-data.json")
    parse(raw_data)
    write_to_file(raw_data)

if __name__ == "__main__":
    asyncio.run(main())


#main()