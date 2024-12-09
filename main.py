import random, sys
import asyncio
import aiofiles
from loguru import logger
from gradient import Gradient
from stats import Stats
from config import shuffle, delay_min, delay_max, TELEGRAM
from telegram import send_message_with_photo
logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: <7}</level> | '
                              '<level>{message}</level>')

logger.add("./logs/app.txt", format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {level} | {message}")
logger.add("./logs/status_node.txt", level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {message}", filter=lambda record: "| Farming | Status node:" in record["message"])
logger.add("./logs/registered_accounts.txt", level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {message}", filter=lambda record: "| Registration in Gradient.network | Successfully registration" in record["message"])
logger.add("./logs/registered_accounts.txt", level="SUCCESS", format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {message}", filter=lambda record: "| Already registered accounts" in record["message"])

with open('proxy.txt') as f:
    proxy = []
    proxy = f.readlines()

with open('ref_codes.txt') as f:
    ref_codes = []
    ref_codes = f.readlines()
    random.shuffle(ref_codes)

with open('emails.txt') as f:
    lines = []
    lines = f.readlines()

emails = []
passwords = []
gradients = []
gradients_stats = []

for line in lines:
    line = line.strip()
    if ':' in line:
        email, password = line.split(':', 1)
        emails.append(email)
        passwords.append(password)


if len(emails) != len(proxy):
    print("The number of emails is not equal to the number of proxies")
    print("Fill in the files correctly!!")
    sys.exit()

numbers = list(range(len(emails)))
for number in numbers:
    gradients.append(Gradient(emails[number], passwords[number], proxy=proxy[number], number_of_list=number))

if shuffle:
    random.shuffle(numbers)


async def perform_registration():
    tasks = []
    count_all = len(emails)
    current_count = 0
    for number in numbers:
        index = gradients[number].number_of_list
        tasks.append(asyncio.create_task(gradients[number].registration_process(ref_codes[number])))
        delay = random.randint(delay_min, delay_max)
        current_count +=1
        if current_count != count_all:
            logger.info(
                f'{index} | {gradients[number].mail} |⏳ Delay between accounts {delay}s')
            await asyncio.sleep(delay)
    await asyncio.gather(*tasks)


async def perform_start_farming():
    tasks = []
    for number in numbers:
        index = gradients[number].number_of_list
        tasks.append(asyncio.create_task(gradients[number].perform_farming_actions(ref_codes[number])))
        delay = random.randint(delay_min, delay_max)

        logger.info(
            f'{index} | {gradients[number].mail} |⏳ Delay between accounts {delay}s')
        await asyncio.sleep(delay)
    await asyncio.gather(*tasks)


async def perform_start_get_stats():
    tasks = []
    for number in numbers:
        tasks.append(asyncio.create_task(gradients[number].profile()))
    await asyncio.gather(*tasks)


async def check_proxy():
    tasks = []
    for number in numbers:
        tasks.append(asyncio.create_task(gradients[number].get_ip()))
    await asyncio.gather(*tasks)


async def initialize_file():
    async with aiofiles.open("./logs/STATS.txt", mode="w", encoding="utf-8") as file:
        pass


async def main(mode):
    if mode == "proxy":
        await check_proxy()

    elif mode == 'farming':
        if TELEGRAM:
            send_message_with_photo()
        await perform_start_farming()

    elif mode == 'update_stats':
        await initialize_file()
        await perform_start_get_stats()

    elif mode == 'all_points':
        await Stats.get_all_points()

    elif mode == 'active_node':
        await Stats.get_work_active()

    elif mode == 'registration':
        await perform_registration()

    else:
        print(f'No found this mode <{mode}>. Try another mode')


async def start():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        await main(mode)
    else:
        print("Please add the mode: (python main <mode>)")


if __name__ == '__main__':
    asyncio.run(start())

