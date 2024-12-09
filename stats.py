import aiofiles
import json
import os

class Stats:
    @staticmethod
    async def get_all_points(file_path: str = "accounts.json"):
        try:

            if not os.path.exists(file_path):
                print(f"Файл {file_path} не найден.")
                return


            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
                content = await file.read()
                if not content.strip():
                    print("Файл пуст.")
                    return

                accounts = json.loads(content)

            total_accounts = 0
            total_points = 0
            sorted_accounts = sorted(accounts.items(), key=lambda x: int(x[0]))

            for account_number, account_data in sorted_accounts:
                email = account_data.get("email", "Неизвестный email")
                points = account_data.get("point", {}).get("total", 0)

                print(f"| {account_number} | email: {email}, Points: {points / 100000}")

                total_accounts += 1
                total_points += points

            print("\nОбщая статистика:")
            print(f"Всего аккаунтов: {total_accounts}")
            print(f"Общее количество Points: {total_points / 100000}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @staticmethod
    async def get_work_active(file_path: str = "accounts.json"):

        try:
            if not os.path.exists(file_path):
                print(f"Файл {file_path} не найден.")
                return

            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
                content = await file.read()
                if not content.strip():
                    print("Файл пуст.")
                    return

                accounts = json.loads(content)

            total_accounts = 0
            total_work_active = 0
            sorted_accounts = sorted(accounts.items(), key=lambda x: int(x[0]))
            for account_number, account_data in sorted_accounts:
                email = account_data.get("email", "Неизвестный email")
                work_active = account_data.get("node", {}).get("workActive", 0)

                print(f"| {account_number} | email: {email}, WorkActive: {work_active}")

                total_accounts += 1
                total_work_active += work_active

            print("\nОбщая статистика:")
            print(f"Всего аккаунтов: {total_accounts}")
            print(f"Общее количество WorkActive: {total_work_active}")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

