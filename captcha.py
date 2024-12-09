import asyncio
from loguru import logger
from config import API_KEY_CAPSOLVER
import capsolver

API_KEY = API_KEY_CAPSOLVER
site_key = "6Lfe5TAqAAAAAI3mJZFYU17Rzjh9DB5KDRReuqYV"
url = "https://app.gradient.network/signup"
CAPSOLVER_URL = "https://api.capsolver.com/createTask"


async def solve_captcha_2captcha(number_of_list, mail, retry = 0):
    idx = "Solving Captcha"
    capsolver.api_key = API_KEY
    capsolver.api_base
    try:
        solution = capsolver.solve({
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteKey": site_key,
            "websiteURL": url,
        })
        logger.info(f"{number_of_list} | {mail} | {idx} | Successfully solving captcha")
        return solution["gRecaptchaResponse"]

    except:
        logger.warning(f"{number_of_list} | {mail} | {idx} | Unsuccessfully solving captcha")
        retry += 1
        if retry > 5:
            logger.error(f"{number_of_list} | {mail} | {idx} | WRONG CAPTCHA")
            return False
        logger.info(f"{number_of_list} | {mail} | {idx} | Try one more time after 10 seconds")
        await asyncio.sleep(10)
        await solve_captcha_2captcha(number_of_list, mail, retry=retry)
