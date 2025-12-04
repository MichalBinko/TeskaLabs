import os
import json
import asyncio
import aiofiles
from datetime import datetime, timezone
import logging

from . import db

logger = logging.getLogger(__name__)

JSON_PATH = os.getenv("APP_JSON_PATH", "/data/sample-data.json")


async def load_json(path):
    async with aiofiles.open(path, "r") as f:
        raw = await f.read()
    return json.loads(raw)


def to_utc(created_at):
    if not created_at:
        return None
    dt = datetime.fromisoformat(created_at)
    return int(dt.astimezone(timezone.utc).timestamp())


def find_ips(network, ips):
    if isinstance(network, dict):
        for key, value in network.items():
            if key == "address":
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
            "created_at": to_utc(x.get("created_at")),
            "status": x.get("status"),
            "ip_addresses": ips,            
            }
        )
    return out_data
"""
def write_to_file(out_data):
    with open("output.txt", "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False)
"""


async def main():
    conn = None
    try:
        logger.info("Spouštím LXC import, JSON_PATH=%s", JSON_PATH)
        try:
            raw_data = await load_json(JSON_PATH)
        except FileNotFoundError:
            logger.error("V kontejneru se nepodařilo najít soubor: %s", JSON_PATH)
            return
        #raw_data = await load_json(JSON_PATH)
        logger.info("Načteno %d záznamů ze vstupního JSONu", len(raw_data))
        out_data = parse(raw_data)
        logger.info("Naparsováno %d kontejnerů", len(out_data))        
        #write_to_file(out_data)
        logger.info("Připojuji se k databázi...")        
        conn = await db.get_connection()
        logger.info("Připojení k databázi OK")        
        await db.init_db(conn)
        await db.insert_containers(conn, out_data)
    except Exception as e:
        logger.exception("Chyba běhu: %r", e)    
    
    finally:
        if conn is not None:
            await conn.close()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",)
    asyncio.run(main())


#main()