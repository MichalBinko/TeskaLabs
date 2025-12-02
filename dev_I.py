import json
import asyncio
import aiofiles

async def load_json(path):
    async with aiofiles.open(path, "r") as f:
        raw = await f.read()
    return json.loads(raw)

def find_ips (network, ips):
    if isinstance(network, dict):
        for key, value in network.items():
            if key == "address":
                count =+ 1
                ips.append(value)
            else:
                find_ips(value, ips)
    elif isinstance(network, list):
        for item in network:
            find_ips(item, ips)


def parse(raw_data):
    out_data = []

    for x in raw_data:
        ips = []
        state = x.get("state")
        if state != None:
            cpu = state.get("cpu")
            memory = state.get("memory")
            network = state.get("network")
            find_ips(network, ips)            
        else:
            cpu = {}
            memory = {}
            network = {}            
        #print("name", x.get("name"))
        #print("memory", memory.get("usage"))
        #input('tlačítko')


        out_data.append(
            {
            "name" : x.get("name"),
            "cpu_usage": cpu.get("usage"),
            "memory_usage":memory.get("usage"),
            "created_at": x.get("created_at"),
            "state": x.get("status"),
            "ip_addresses": ips,            
            }
        )
    return out_data

def write_to_file(out_data):
    with open("output.txt", "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False)



async def main():
    raw_data = await load_json("sample-data.json")
    out_data = parse(raw_data)
    write_to_file(out_data)

if __name__ == "__main__":
    asyncio.run(main())


#main()