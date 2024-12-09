import time
import requests
from playwright.async_api import async_playwright, expect
import random, aiohttp
import aiofiles
import asyncio
import json
from fake_useragent import UserAgent
from loguru import logger
from config import HEADLESS, DELAY_BETWEEN_GETTING_STATS, DINAMIC_PROXY, TELEGRAM_STATS_DELAY
import os, imaplib
from bs4 import BeautifulSoup
import email
from config import TELEGRAM
from telegram import send_message_error, send_message, send_message_success, send_message_warning
from email.policy import default
from captcha import solve_captcha_2captcha

EXTENTION_PATH = os.path.join(os.getcwd(), '1.0.16_0')
#caacbgbklghmpodbdafajbgdnegacfmo

class Gradient:
    all_stats = []
    def __init__(self, mail: str, email_password: str, proxy: str, number_of_list: int, ):
        self.mail = mail.strip()
        self.proxy = proxy.strip()
        self.number_of_list = number_of_list
        self.email_password = email_password.strip()
        self.ref_code = None
        self.token_id = None
        self.token_refresh = None

    @staticmethod
    def format_proxy(proxy_string: str) -> str:
        try:
            parts = proxy_string.split(':')
            if len(parts) != 4:
                raise ValueError("The proxy format is incorrect. The format was expected 'username:password:host:port'.")

            username, password, host, port = parts
            formatted_proxy = f"socks5://{username}:{password}@{host}:{port}"
            return formatted_proxy
        except Exception as e:
            return f"Error: {e}"

    async def get_ip(self):
        Gradient.count = 0
        url = "https://api.ipify.org?format=json"
        proxy_url = self.format_proxy(self.proxy)
        idx = "PROXY"
        try:
                async with aiohttp.ClientSession() as session:
                        async with session.get(url, proxy=proxy_url, timeout=10) as response:
                            if response.status == 200:
                                data = await response.json()
                                print(f"{self.number_of_list} | {self.mail} | {idx} | Connected Proxy: {data['ip']}")
                            else:
                                print(f"{self.number_of_list} | {self.mail} | {idx} | ERROR Proxy: {response.status}")

        except Exception as e:
            print(f"{self.number_of_list} | {self.mail} | {idx} | Failed to connect to the proxy")

    @staticmethod
    def extract_verification_code_from_html(html_body):
        soup = BeautifulSoup(html_body, "html.parser")
        code_divs = soup.find_all("div", class_="pDiv")
        verification_code = ''.join(div.get_text(strip=True) for div in code_divs if not "empty" in div.get("class", []))
        return verification_code if verification_code else None

    async def connect_to_email(self, imap_server='imap.firstmail.ltd', imap_port=993, retry=0):
        idx = "Connect the email"
        sender_email = "noreply@gradient.network"
        try:
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(self.mail, self.email_password)
            mail.select("INBOX")

            status, messages = mail.search(None, f'FROM "{sender_email}"')
            if status != 'OK' or not messages[0]:
                if retry > 5:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY GETTING EMAIL CODE!")
                    return None
                await asyncio.sleep(5)
                await self.connect_to_email(imap_server, imap_port, retry=retry)

            mail_ids = messages[0].split()
            latest_email_id = mail_ids[-1]
            status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
            if status != 'OK':
                logger.error(
                    f"{self.number_of_list} | {self.mail} | {idx} | Error fetching the latest email from {sender_email}.")
                return None

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1], policy=default)
                    subject = msg['subject']
                    from_ = msg['from']
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                code = self.extract_verification_code_from_html(body)
                                logger.info(
                                    f"{self.number_of_list} | {self.mail} | {idx} | Subject: {subject} | From: {from_} | Code: {code}")
                                return code
                    else:
                        body = msg.get_payload(decode=True).decode()
                        code = self.extract_verification_code_from_html(body)
                        logger.info(
                            f"{self.number_of_list} | {self.mail} | {idx} | Subject: {subject} | From: {from_} | Code: {code}")
                        return code

        except Exception as error:
            retry += 1
            if retry > 5:
                logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY GETTING CODE!")
                return None

            logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Error: {error}")
            logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Delay 20 seconds")
            await asyncio.sleep(20)
            logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Starting {retry}/5 time")
            await self.connect_to_email(imap_server, imap_port, retry=retry)


    async def sign_up(self, ref_code, retry = 0):
        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxies = {
            'http': f'http://{username}:{password}@{host}:{port}',
            'https': f'http://{username}:{password}@{host}:{port}'}

        params = {
            'key': 'AIzaSyCWz-svq_InWzV9WaE3ez4XqxCE0C34ddI',
        }

        json_data = {
            'returnSecureToken': True,
            'email': self.mail,
            'password': self.email_password,
            'clientType': 'CLIENT_TYPE_WEB',
        }

        headers = {
            'authority': 'identitytoolkit.googleapis.com',
            'accept': '*/*',
            'accept-language': 'en-EN,de;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        try:
            response = requests.post(
                'https://identitytoolkit.googleapis.com/v1/accounts:signUp',
                params=params,
                headers=headers,
                json=json_data,
                proxies=proxies,
            )

            if response.status_code == 200:
                tokens = response.json()
                logger.info(f"{self.number_of_list} | {self.mail} | Sign-up successful for email")
                return tokens

            else:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message")
                if error_message == "EMAIL_EXISTS":
                    logger.warning(f"{self.number_of_list} | {self.mail} | This email already exist")
                    tokens = await self.sign_in_with_password()
                    if tokens is None:
                        raise Exception
                    self.token = tokens
                    response = await self.look_up(tokens)
                    if response is False:
                        raise Exception
                    if response['users'][0]['emailVerified'] == True:
                        tokens = await self.get_access_token(token_refresh=tokens["refreshToken"])
                        response = await self.bind_invite_code(tokens["access_token"], ref_code=ref_code)
                        if response:
                            logger.success(f"{self.number_of_list} | {self.mail} | Already registered accounts")
                    else:
                        email_code = await self.send_to_email(tokens)
                        if not email_code:
                            return False
                        email_code = await self.connect_to_email()
                        checher = await self.verify_email(email_code)
                        if checher == True:
                            tokens = await self.get_access_token(token_refresh=tokens["refreshToken"])
                            response = await self.bind_invite_code(tokens["access_token"], ref_code=ref_code)
                            if response == True:
                                logger.success(f"{self.number_of_list} | {self.mail} | Already registered accounts")
                else:
                    logger.error(f"{self.number_of_list} | {self.mail} | Sign-up failed with status: {error_message}")
                return None

        except Exception as e:
            logger.error(f"{self.number_of_list} | {self.mail} | Sign-up failed: {e}")
            retry += 1
            if retry > 4:
                return
            await asyncio.sleep(10)
            return await self.sign_up(ref_code=ref_code, retry=retry)

    async def save_account_data_async(self, account_data: dict, output_file: str = "accounts.json"):
        data = account_data.get('data', {})

        extracted_data = {
            "id": data.get("id"),
            "email": data.get("email"),
            "code": data.get("code"),
            "referredBy": data.get("referredBy"),
            "point": {
                "total": data.get("point", {}).get("total", 0)
            },
            "node": {
                "workActive": data.get("node", {}).get("workActive", 0)
            }
        }

        database = {}
        if os.path.exists(output_file):
            async with aiofiles.open(output_file, mode="r", encoding="utf-8") as file:
                content = await file.read()
                if content.strip():
                    database = json.loads(content)

        database[self.number_of_list] = extracted_data

        async with aiofiles.open(output_file, mode="w", encoding="utf-8") as file:
            await file.write(json.dumps(database, indent=4, ensure_ascii=False))

        formatted_line = (
            f"№: {self.number_of_list}, "
            f"Email: {extracted_data['email']}, "
            f"Points: {extracted_data['point']['total'] / 100000}, "
            f"Code: {extracted_data['code']}, "
            f"Referred By: {extracted_data['referredBy']}, "
            f"Work Active: {extracted_data['node']['workActive']}\n"
        )

        async with aiofiles.open("./logs/STATS.txt", mode="a", encoding="utf-8") as file:
            await file.write(formatted_line)

    async def sign_in_with_password(self):
        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        params = {
            'key': 'AIzaSyCWz-svq_InWzV9WaE3ez4XqxCE0C34ddI',
        }

        json_data = {
            'returnSecureToken': True,
            'email': self.mail,
            'password': self.email_password,
            'clientType': 'CLIENT_TYPE_WEB',
        }

        headers = {
            'authority': 'identitytoolkit.googleapis.com',
            'accept': '*/*',
            'accept-language': 'en-EN,de;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
                        params=params,
                        headers=headers,
                        json=json_data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:

                    if response.status == 200:
                        tokens = await response.json()
                        logger.info(f"{self.number_of_list} | {self.mail} | successful sign_in_with_password")
                        return tokens
                    else:
                        error_data = await response.json()
                        error_message = error_data.get("error", {}).get("message")
                        if error_message == "INVALID_LOGIN_CREDENTIALS":
                            return None
                        else:
                            logger.error(
                                f"{self.number_of_list} | {self.mail} | Sign-in failed with status: {error_message}")
                            return None

        except aiohttp.ClientError as e:
            logger.error(f"{self.number_of_list} | {self.mail} | Sign-in failed: {e}")
            return None

    async def look_up(self, tokens, retry=0):
        idx = 'look_up'
        if tokens is None or 'idToken' not in tokens:
            logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Token отсутствует или некорректен")
            return False

        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        POST_URL = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"
        headers = {
            'authority': 'identitytoolkit.googleapis.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }

        params = {
            'key': 'AIzaSyCWz-svq_InWzV9WaE3ez4XqxCE0C34ddI',
        }

        json_data = {
            'idToken': tokens['idToken'],
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL,
                        params=params,
                        headers=headers,
                        json=json_data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:
                    if response.status == 200:
                        logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Успех: {response.status}")
                        return await response.json()
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False
        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            if retry < 3:
                await asyncio.sleep(10)
                return await self.look_up(tokens, retry=retry + 1)
            return False

    async def send_to_email(self, tokens, retry=0):
        idx = "request for email code"
        if tokens is None:
            logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Token is None")
            return False

        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        captcha_solution = await solve_captcha_2captcha(self.number_of_list, self.mail)
        if captcha_solution is None:
            logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Something wrong with captcha")
            return await solve_captcha_2captcha(self.number_of_list, self.mail)

        POST_URL = 'https://api.gradient.network/api/user/send/verify/email'
        headers = {
            'authority': 'api.gradient.network',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'de-DE,de;q=0.9',
            'authorization': f"Bearer {tokens['idToken']}",
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'referer': 'https://app.gradient.network/',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        json_data = {
            'code': captcha_solution,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL,
                        headers=headers,
                        json=json_data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:
                    if response.status == 200:
                        logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Успех: {response.status}")
                        return True
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False
        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            if retry < 3:
                retry+=1
                await asyncio.sleep(10)
                return await self.send_to_email(tokens, retry=retry)
            return False

    async def verify_email(self, email_code, retry=0):
        idx = "Verification email"
        if self.token is None:
            return None

        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        POST_URL = "https://api.gradient.network/api/user/verify/email"

        headers = {
            'authority': 'api.gradient.network',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f"Bearer {self.token['idToken']}",
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'referer': 'https://app.gradient.network/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        json_data = {
            'code': email_code,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL,
                        headers=headers,
                        json=json_data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:
                    if response.status == 200:
                        logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Успех: {await response.json()}")
                        return True
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False
        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            if retry < 3:
                await asyncio.sleep(10)
                return await self.verify_email(email_code, retry=retry + 1)
            return False


    async def get_access_token(self, token_refresh, retry=0):
        idx = "get_access_token"
        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        POST_URL = "https://securetoken.googleapis.com/v1/token"
        headers = {
            'authority': 'securetoken.googleapis.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://app.gradient.network',
            'referer': 'https://app.gradient.network/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        params = {
            'key': 'AIzaSyCWz-svq_InWzV9WaE3ez4XqxCE0C34ddI',
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': token_refresh,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL,
                        params=params,
                        headers=headers,
                        data=data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:
                    if response.status == 200:
                        logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Успех: {response.status}")
                        tokens = await response.json()
                        return tokens
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False

        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            if retry < 3:
                await asyncio.sleep(10)
                return await self.get_access_token(token_refresh, retry=retry + 1)
            return False


    async def bind_invite_code(self, access_token, ref_code, retry=0):
        idx = "bind_invite_code"
        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"

        POST_URL = "https://api.gradient.network/api/user/register"

        headers = {
            'authority': 'api.gradient.network',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {access_token}',
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'referer': 'https://app.gradient.network/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        json_data = {
            'code': ref_code.strip(),
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL,
                        headers=headers,
                        json=json_data,
                        proxy=proxy_url,
                        proxy_auth=proxy_auth
                ) as response:
                    if response.status == 200:
                        checker = await response.json()
                        try:
                            if checker["data"]["code"] is not None:
                                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Успех: {response.status}")
                                return True
                        except Exception as e:
                            logger.error(
                                f"{self.number_of_list} | {self.mail} | {idx} | Ошибка в bind_invite_code: {checker}")
                            return False
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False

        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            if retry < 3:
                await asyncio.sleep(10)
                return await self.bind_invite_code(access_token, ref_code, retry=retry + 1)
            return False


    async def profile(self, retry = 0):
        idx = 'profile'
        try:
            tokens = await self.sign_in_with_password()
            if tokens is None:
                if retry > 4:
                    return False
                return await self.profile(retry=retry)

        except Exception as e:
            logger.error(f"{self.number_of_list} | {self.mail} | {idx} | {e}")
            if retry > 4:
                return False
            return await self.profile(retry=retry)
        idx = "profile"
        proxy = self.proxy.split(':')
        username, password, host, port = proxy
        proxy_auth = aiohttp.BasicAuth(username, password)
        proxy_url = f"http://{host}:{port}"
        POST_URL = "https://api.gradient.network/api/user/profile"
        headers = {
            'authority': 'api.gradient.network',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f"Bearer {tokens['idToken']}",
            'content-type': 'application/json',
            'origin': 'https://app.gradient.network',
            'referer': 'https://app.gradient.network/',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }

        json_data = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        POST_URL, headers=headers, json=json_data,
                        proxy=proxy_url, proxy_auth=proxy_auth) as response:

                    if response.status == 200:
                        checker = await response.json()
                        try:
                            if checker.get("msg") == 'Please verify email first':
                                logger.warning(
                                    f"{self.number_of_list} | {self.mail} | {idx} | This account is not registered")
                                return
                        except Exception:
                            pass
                        logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Updated Stats")
                        await self.save_account_data_async(account_data=checker)
                    else:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Ошибка {response.status}")
                        return False

        except aiohttp.ClientError as e:
            logger.warning(
                f"{self.number_of_list} | {self.mail} | {idx} | Произошла ошибка при выполнении запроса: {str(e)}")
            retry += 1
            if retry < 3:
                await asyncio.sleep(10)
                return await self.profile(retry=retry)


    async def registration_process(self, ref_code):
        logger.info(f"{self.number_of_list} | {self.mail} | Registration...")
        self.token = await self.sign_up(ref_code)
        if self.token is None or self.token is False:
            return False
        email_to_code = await self.send_to_email(self.token)
        if not email_to_code:
            logger.error(f"{self.number_of_list} | {self.mail} | Unsuccessfully send_to_email()")
            return False

        await asyncio.sleep(5)
        email_code = await self.connect_to_email()
        if not email_code:
            return False
        verify_email_checker = await self.verify_email(email_code)
        if verify_email_checker is False:
            return False
        token2 = await self.get_access_token(self.token['refreshToken'])
        await asyncio.sleep(2)
        if token2 is False:
            return False
        checker = await self.bind_invite_code(token2["access_token"], ref_code)
        if checker:
            logger.success(f"{self.number_of_list} | {self.mail} | Already registered accounts")
            return True
        logger.error(f"{self.number_of_list} | {self.mail} | Unsuccesfully registration")

    async def perform_farming_actions(self, ref_code: str, count_change_proxy = 0, retry = 0):
        self.ref_code = ref_code
        idx = "Logging to Gradient.network"
        async with async_playwright() as p:
            proxy = self.proxy.split(':')
            username, password, host, port = proxy
            try:
                context = await p.chromium.launch_persistent_context(
                    '',
                    headless=HEADLESS,
                    proxy={'server': f'http://{host}:{port.strip()}',
                           'username': username,
                           'password': password},
                    user_agent=UserAgent().chrome,
                    args=[
                             '--disable-extensions-except=' + EXTENTION_PATH,
                             '--load-extension=' + EXTENTION_PATH,
                             ] + (['--headless=new'] if HEADLESS else []),
                )

            except Exception as error:
                retry += 1
                if retry > 5:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY STARTING BROWSER!")
                    return
                logger.error(
                    f"{self.number_of_list} | {self.mail} | {idx} | Unsuccessfully starting browser! Error: {error}")
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Delay 20 seconds")
                await asyncio.sleep(20)
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Starting {retry}/5 time")
                await context.close()
                await self.perform_farming_actions(ref_code, retry=retry, count_change_proxy=count_change_proxy)

            idx = "Logining in Gradient.network"
            try:
                await asyncio.sleep(2)
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Go to the website..")
                page = await context.new_page()
                await page.goto('https://app.gradient.network/')
                await page.bring_to_front()
                await page.wait_for_load_state()
                await asyncio.sleep(random.randint(2, 6))
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Successfully connect to website")

            except Exception as error:
                retry += 1
                if retry > 5:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY CONNECT TO WEBSITE!")
                    return
                logger.error(
                    f"{self.number_of_list} | {self.mail} | {idx} | Unsuccessfully connect to website! Error: {error}")
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Delay 20 seconds")
                await asyncio.sleep(20)
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Starting {retry}/5 time")
                await context.close()
                await self.perform_farming_actions(ref_code, retry=retry, count_change_proxy=count_change_proxy)

            try:
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Logining...")
                await page.bring_to_front()
                inputs = page.get_by_placeholder("Enter Email")
                await expect(inputs).to_be_visible()
                await inputs.type(self.mail)
                inputs2 = page.get_by_placeholder("Enter Password")
                await expect(inputs2).to_be_visible()
                await inputs2.type(self.email_password)
                await asyncio.sleep(random.randint(2, 6))
                button = page.locator('//html/body/div[1]/div[2]/div/div/div/div[4]/button[1]')
                await expect(button).to_be_visible()
                await button.click()
                await asyncio.sleep(5)
                try:
                    await page.locator('//html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/span').wait_for(
                        timeout=3000)
                    text = await page.locator(
                        '//html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div/span').text_content()
                    if text == "Wrong email or password":
                        logger.error(
                            f"{self.number_of_list} | {self.mail} | {idx} | Wrong email or password")
                        return

                except:
                    pass

                try:
                    await page.locator('//html/body/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]/div[2]').wait_for(
                        timeout=3000)
                    text = await page.locator(
                        '//html/body/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]/div[2]').text_content()
                    if text == "3,000 EXP and a 2% reward boost.":
                        logger.error(
                            f"{self.number_of_list} | {self.mail} | {idx} | Account is not registered")
                        return

                except:
                    pass

                await asyncio.sleep(6)
                await page.keyboard.press('Escape')
                await asyncio.sleep(3)
                try:
                    await page.locator('//html/body/div[1]/div[1]/div[2]/header/div/div[2]/div[2]/div[2]').wait_for(
                        timeout=3000)
                    text = await page.locator(
                        '//html/body/div[1]/div[1]/div[2]/header/div/div[2]/div[2]/div[2]').text_content()
                    logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Successfully logining: {text}")
                except:
                    pass

            except Exception as error:
                if retry > 5:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSuccessfully logining!")
                    return
                logger.error(
                    f"{self.number_of_list} | {self.mail} | {idx} | UnSuccessfully logining! Error: {error}")
                await context.close()
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Delay 20 seconds")
                await asyncio.sleep(20)
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Starting {retry}/5 time")
                await self.perform_farming_actions(ref_code, retry=retry, count_change_proxy=count_change_proxy)
            idx = "Checking the first status"

            try:
                await asyncio.sleep(2)
                page2 = await context.new_page()
                await page2.goto("chrome-extension://caacbgbklghmpodbdafajbgdnegacfmo/popup.html")
                await asyncio.sleep(5)
                try:
                    button_got_it = page2.locator('//html/body/div[2]/div/div[2]/div/div[2]/div/div/div/button')
                    await expect(button_got_it).to_be_visible()
                    await button_got_it.click()
                except:
                    pass

                await asyncio.sleep(1)
                await page2.keyboard.press('Escape')
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Waiting 2 minutes for the updating extension...")
                await asyncio.sleep(120)
                await page2.reload()
                try:
                    k = 0
                    while await page2.locator('//*[@id="root-gradient-extension-popup-20240807"]/div/div[2]/div/div[2]/div[1]').inner_text() == "We are customizing":
                        logger.info(
                            f"{self.number_of_list} | {self.mail} | {idx} | Waiting for the getting correct status...")
                        logger.info(
                            f"{self.number_of_list} | {self.mail} | {idx} | Waiting 2 minutes for the updating extension...")
                        k+=1
                        if k > 15:
                            logger.warning(
                                f"{self.number_of_list} | {self.mail} | {idx} | Time out for the updating extension")
                            break
                        else:
                            await asyncio.sleep(120)
                            await page2.reload()

                except:
                    pass

                await asyncio.sleep(2)
                status = await self.get_status_extension(page2)
                if status == "Good" or status == "Disconnected":
                    logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Status: {status} --> Starting infinity work")
                else:
                    if not DINAMIC_PROXY:
                        count_change_proxy += 1
                        if count_change_proxy > 3:
                            logger.error(
                                f"{self.number_of_list} | {self.mail} | {idx} | Status: {status}. BAD PROXY. CLOSE THE ACCOUNT")
                            await context.close()
                            return
                        else:
                            logger.warning(
                                f"{self.number_of_list} | {self.mail} | {idx} | Status: {status}. Update proxy")
                            await self.perform_farming_actions(ref_code, retry=retry,
                                                               count_change_proxy=count_change_proxy)

                    await context.close()
                    logger.warning(
                        f"{self.number_of_list} | {self.mail} | {idx} | Status: {status}. Update proxy")
                    await self.perform_farming_actions(ref_code, retry=retry, count_change_proxy=count_change_proxy)

                await page.bring_to_front()
                await page.goto('https://app.gradient.network/')
            except:
                pass
            try:
                await self.infinity_work(context)
            except:
                pass


    async def get_stats_alone(self, retry = 0):
        idx = "STATS"
        async with async_playwright() as p:
            proxy = self.proxy.split(':')
            username, password, host, port = proxy
            try:
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Waiting for getting the stats...")
                context = await p.chromium.launch_persistent_context(
                    '',
                    headless=HEADLESS,
                    proxy={'server': f'http://{host}:{port.strip()}',
                           'username': username,
                           'password': password},
                    user_agent=UserAgent().chrome,
                    args=["--disable-blink-features=AutomationControlled"] + (['--headless=new']) if HEADLESS else [],
                )

            except Exception as error:
                retry += 1
                if retry > 4:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY GETTING THE STATS: {error}")
                    return
                await asyncio.sleep(20)
                await context.close()
                await self.get_stats_alone(retry=retry)

            try:
                await asyncio.sleep(2)
                page = await context.new_page()
                await page.goto('https://app.gradient.network/')
                await page.bring_to_front()
                await page.wait_for_load_state()
                await asyncio.sleep(random.randint(2, 6))

            except Exception as error:
                retry+=1
                if retry > 5:
                    logger.error(f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY CONNECT TO WEBSITE! Error: {error}")
                    await context.close()
                    return
                await context.close()
                await self.get_stats_alone(retry=retry)

            try:
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Logining...")
                await page.bring_to_front()
                inputs = page.get_by_placeholder("Enter Email")
                await expect(inputs).to_be_visible()
                await inputs.type(self.mail)
                inputs2 = page.get_by_placeholder("Enter Password")
                await expect(inputs2).to_be_visible()
                await inputs2.type(self.email_password)
                await asyncio.sleep(random.randint(2, 6))
                button = page.locator('//html/body/div[1]/div[2]/div/div/div/div[4]/button[1]')
                await expect(button).to_be_visible()
                await button.click()
                await asyncio.sleep(3)
                await page.keyboard.press('Escape')
                await asyncio.sleep(1)
                await page.goto('https://app.gradient.network/dashboard/node')
                await asyncio.sleep(random.randint(2, 6))
            except:
                pass

            try:
                status, points = await self.dashboard_node_alone(page)
                if points == "Page is closed" or points == "Unknown":
                    logger.warning(
                        f"{self.number_of_list} | {self.mail} | {idx} | Something wrong! Try again after 20 seconds..")
                    await context.close()
                    retry+=1
                    if retry > 5:
                        logger.error(
                            f"{self.number_of_list} | {self.mail} | {idx} | UNSUCCESSFULLY CONNECT TO WEBSITE! Error: {error}")
                        await context.close()
                        await self.get_stats_alone(retry=retry)
                        return

                logger.info(
                    f"{self.number_of_list} | {self.mail} | {idx} | Status node: {status}; Points: {points}")
            except Exception as error:
                logger.error(
                    f"{self.number_of_list} | {self.mail} | {idx} | Something wrong! Try again after 20 seconds..")
                await context.close()
                await asyncio.sleep(20)
                await self.get_stats_alone()


    async def dashboard_node_alone(self, page):
        points = None
        status = None
        if page.is_closed():
            points = "Page is closed"
            status = "Page is closed"
            return status, points
        try:
            points = page.locator('//html/body/div[1]/div[1]/div[2]/header/div/div[2]/div[2]/div[2]')
            await expect(points).to_be_visible()
        except:
            pass
        try:
            status = page.locator('//html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]/div/span')
            await expect(status).to_be_visible(timeout=5000)
        except:
            try:
                status = page.locator(
                    '//html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div/div[2]/table/tbody/tr/td[2]/div/span')
                await expect(status).to_be_visible(timeout=5000)
            except:
                try:
                    status = page.locator(
                        '//html/body/div[1]/div[1]/div[2]/main/div/div/div/div/div/div[2]/div/span')
                    await expect(status).to_be_visible(timeout=5000)
                    logger.warning(f"{self.number_of_list} | {self.mail} | While extension doesnt add to the list..")
                except:
                    pass
                points = await asyncio.wait_for(points.inner_text(), timeout=10)
                status = "While adding"
                return status, points
        try:
            points = await asyncio.wait_for(points.inner_text(), timeout=10)
            status = await asyncio.wait_for(status.inner_text(), timeout=10)

        except asyncio.TimeoutError:
            status = "Unknown"
            points = "Unknown"
        await page.close()
        return status, points


    @staticmethod
    async def get_status_extension(page2):
        try:
            await page2.reload()
            await page2.wait_for_load_state()
            status = page2.locator('//*[@id="root-gradient-extension-popup-20240807"]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]')
            return await status.inner_text()

        except:
            return None


    @staticmethod
    async def get_points(page):
        try:
            await page.reload()
            await page.wait_for_load_state()
            status = page.locator(
                '//html/body/div[1]/div[1]/div[2]/header/div/div[2]/div[2]/div[2]')
            return await status.inner_text()

        except:
            return None


    async def infinity_work(self, context, retry = 0):
        idx = 'Farming'
        current_time = 0
        while True:
            try:
                pages = context.pages
                page = pages[2]
                page2 = pages[3]
            except:
                pages = None

            if not pages:
                logger.warning(f"{self.number_of_list} | {self.mail} | {idx} | Context closed. Restart required.")
                logger.info(
                    f"{self.number_of_list} | {self.mail} | {idx} | Time sleep 20 seconds")
                await context.close()
                await asyncio.sleep(20)
                if TELEGRAM:
                    send_message(f"⚠️ {self.number_of_list} | {self.mail} | Context closed. Restart required.")
                await self.perform_farming_actions(self.ref_code)
                return

            try:
                await page.reload()
                await page2.reload()
                logger.info(f"{self.number_of_list} | {self.mail} | {idx} | Start farming..")
                await page2.bring_to_front()
                status = await self.get_status_extension(page2)
                await page.bring_to_front()
                points = await self.get_points(page)

                if TELEGRAM and (current_time > TELEGRAM_STATS_DELAY):
                    current_time = 0
                    if status == "Unsupported":
                        send_message_error(self.number_of_list, self.mail, status, points)
                    elif status == "Disconnected":
                        send_message_warning(self.number_of_list, self.mail, status, points)
                    else:
                        send_message_success(self.number_of_list, self.mail, status, points)

                if status == "Unsupported":
                    retry+=1
                    if retry > 0 and not DINAMIC_PROXY:
                        logger.error(f"{self.number_of_list} | {self.mail} | {idx} | Status: {status}. Static proxy. Close the account")
                        send_message(f"❌❌❌ {self.number_of_list} | {self.mail} | Status: {status}. Static proxy. Close the account")
                        return

                    logger.warning(
                        f"{self.number_of_list} | {self.mail} | {idx} | Status: {status}. Update proxy")
                    await context.close()
                    await self.perform_farming_actions(self.ref_code)
                    return

                else:
                    logger.info(
                        f"{self.number_of_list} | {self.mail} | {idx} | Status node: {status}; Points: {points}")
                    delay = random.randint(DELAY_BETWEEN_GETTING_STATS - 100, DELAY_BETWEEN_GETTING_STATS + 100)
                    logger.info(
                        f"{self.number_of_list} | {self.mail} | {idx} | Waiting {delay}s for the updating stats...")
                    await asyncio.sleep(delay)
                    current_time += delay

            except:
                logger.info(
                    f"{self.number_of_list} | {self.mail} | {idx} | Something is wrong. Try the next time")
                await page.close()
                page2 = await context.new_page()
                await page2.goto("https://app.gradient.network/dashboard")
                await asyncio.sleep(20)
                current_time += 20

