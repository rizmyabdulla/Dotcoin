import requests
import time
from colorama import init, Fore, Style
import sys
import os
from headers import get_headers
from dotenv import load_dotenv

init(autoreset=True)

load_dotenv()


ENDPOINT = "https://api.dotcoin.bot/rest/v1"
BASE = "https://api.dotcoin.bot"
def print_welcome_message():
    print(Fore.MAGENTA + Style.BRIGHT + "\n######           #                ##           \n ##  ##         ##                            \n ##  ##  ####  ####  ###   ####  ###  #####   \n ##  ## ## ###  ##  ## ## ## ###  ##   ## ##  \n ##  ## ##  ##  ##  ##    ##  ##  ##   ## ##  \n ##  ## ### ##  ##  ###   ### ##  ##   ## ##  \n######   ####    ##  ####  ####  #### ### ### \n          ")
    print(Fore.GREEN + Style.BRIGHT + "Dotcoin BOT")
    print(Fore.GREEN + Style.BRIGHT + "Youtube: https://youtube.com/@Yk-Daemon")
    print(Fore.GREEN + Style.BRIGHT + "Github: https://github.com/rizmyabdulla/dotcoin")
    print(Fore.GREEN + Style.BRIGHT + "Join our tg channel for updates: https://t.me/ykdaemon")
    print(Fore.GREEN + Style.BRIGHT + "Tg group: https://t.me/yk_daemon\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_credentials():
    try:
        with open('tokens.txt', 'r') as file:
            credentials_list = file.readlines()
        if not credentials_list:
            print(f"\n{Fore.RED+Style.BRIGHT}The file 'tokens.txt' is empty. Please add your Authorization tokens for your accounts.")
            exit()
        return [cred.strip() for cred in credentials_list]
    except FileNotFoundError:
        print(f"{Fore.RED+Style.BRIGHT}The file 'tokens.txt' was not found.")
        return []


def fetch_task_ids(apikey, authorization):
    url = f'{ENDPOINT}/rpc/get_filtered_tasks'
    headers = get_headers(apikey, authorization)
    
    data = {'platform': 'ios', 'locale': 'en', 'is_premium': False}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return [task['id'] for task in response.json()]
    except requests.RequestException as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to fetch tasks: {e}")
        return []

def upgrade_dtc_miner(apikey, authorization, uId):
    headers = get_headers(apikey, authorization, uId)
    urls = [
        f'{BASE}/functions/v1/upgradeDTCMiner',
        f'{BASE}/functions/v1/upgradeDTCMinerWeb3'
    ]
    
    for i, url in enumerate(urls, start=1):
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get('success', False):
                print(f"{Fore.GREEN}{Style.BRIGHT}Attempt {'Web2' if i == 1 else 'Web3'}: Successfully upgraded DTC Miner.")
                return True
            
            print(f"{Fore.YELLOW}{Style.BRIGHT}Attempt on {'Web2' if i == 1 else 'Web3'} unsuccessful. Code: {response_data.get('code')}")
        
        except requests.RequestException as e:
            print(f"{Fore.RED}{Style.BRIGHT}Attempt on {'Web2' if i == 1 else 'Web3'} failed, error: {str(e)}")
            continue
    
    print(f"{Fore.RED}{Style.BRIGHT}Failed to upgrade DTC Miner after all attempts. Verification may be required.")
    return False

def add_attempts(lvl, apikey, authorization,current_level):
    url = f'{ENDPOINT}/rpc/add_attempts'
    headers = get_headers(apikey, authorization)

    while True:
        print(f"\r{Fore.CYAN+Style.BRIGHT}[ Upgrade ] : Try upgrading 'Add attempts' to level {lvl}", end="" , flush=True)
        sys.stdout.flush()
        try:
            data = {'lvl': lvl}
            # print(data)
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if lvl > current_level:
                return False
            if response_data.get('success', False):
                    # print(f"\r{Fore.GREEN+Style.BRIGHT}[ Upgrade ] : Success!\n")
                return True
            else:
                # print(f"\r{Fore.RED+Style.BRIGHT}[ Upgrade ] : Failed\n")
                lvl += 1
        except Exception as e:
            sys.stdout.write(f"Error while adding attempts: {e}\n")


def add_multitap(lvl, apikey, authorization,current_level):
    url = f'{ENDPOINT}/rpc/add_multitap'
    headers = get_headers(apikey, authorization)

    while True:
        print(f"\r{Fore.CYAN+Style.BRIGHT}[ Upgrade ] : Try upgrading 'multitap' to level {lvl}", end="" , flush=True)
        sys.stdout.flush()
        try:
            data = {'lvl': lvl}
            # print(data)
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if lvl > current_level:
                return False
            if response_data.get('success', False):
                    # print(f"\r{Fore.GREEN+Style.BRIGHT}[ Upgrade ] : Success!\n")
                return True
            else:
                # print(f"\r{Fore.RED+Style.BRIGHT}[ Upgrade ] : Failed\n")
                lvl += 1
        except Exception as e:
            sys.stdout.write(f"Error while adding attempts: {e}\n")


def auto_complete_task(apikey, authorization):
    task_ids = fetch_task_ids(apikey, authorization)
    base_url = f'{ENDPOINT}/rpc/complete_task'
    headers = get_headers(apikey, authorization)
    for task_id in task_ids:
        data = {'oid': str(task_id)}
        response = requests.post(base_url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Task {task_id} ] : Success")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Task {task_id} ] {task_id}. Status code: {response.status_code} : Failed")

def save_coins(coins, apikey, authorization):
    url = f'{ENDPOINT}/rpc/save_coins'
    headers = get_headers(apikey, authorization)
    data = {'coins': coins}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error when saving coins: {e}")
        return False

def get_user_info(apikey, authorization):
    url = f'{ENDPOINT}/rpc/get_user_info'
    headers = get_headers(apikey, authorization)

    data = {}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def auto_upgrade_boosters():
    user_input = input("Auto upgrade boosters? (y/n): ")
    if user_input.lower() == 'y':
        try:
            upgrade_amount = int(input("How many times do you want to upgrade? "))
            return upgrade_amount
        except ValueError:
            print("Invalid input, must be a number.")
            return 0
    return 0 


def auto_gacha(apikey, authorization, coins):
    url = f'{ENDPOINT}/rpc/try_your_luck'
    headers = get_headers(apikey, authorization)

    data = {'coins': coins}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get('success', False):
            print(f"{Fore.GREEN+Style.BRIGHT}[ Gacha ] : Win")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Gacha ] : Failed")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Gacha ] : Failed with status code {response.status_code}")

def restore_attempts(apikey, authorization):
    url = "https://api.dotcoin.bot/rest/v1/rpc/restore_attempt"
    headers = get_headers(apikey, authorization)

    data = {}
    false_count = 0
    while false_count < 1:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        # print(false_count, response_data)
        # print(response_data)
        check_response = response_data.get('success', False)
        if check_response == True:
            # false_count += 1
            print(f"{Fore.GREEN+Style.BRIGHT}[ Restore Attempt ] : Successfully restored free energy")
        else:
            false_count += 1
            print(f"{Fore.RED+Style.BRIGHT}[ Restore Attempt ] : Failed to restore energy, it's at its limit!")
        time.sleep(1)

def main():
    print_welcome_message()
    complete_task = input("Auto complete Task? (default n) (y/n): ").strip().lower()
    if complete_task in ['y', 'n', '']:
        complete_task = complete_task or 'n'
    else:
        complete_task = 'n'
    credentials = load_credentials()
    upgrade_amount = auto_upgrade_boosters()
    upgrade_success = {}

    apikey = os.getenv('API_KEY')

    auto_upgrade_dtc = input("Auto upgrade DTC Miner? (y/n): ").strip().lower()
    if auto_upgrade_dtc not in ['y', 'n']:
        auto_upgrade_dtc = 'n'
    while True:
        for index, authorization in enumerate(credentials):
            info = get_user_info(apikey, authorization)
            print(f"\n{Fore.CYAN + Style.BRIGHT}============== [ Account {index} | {info['first_name']} ] ==============\n")

            if not upgrade_success.get(authorization, False):
                if upgrade_amount > 0:
                    for _ in range(upgrade_amount):
                        current_attempts_level = info['daily_attempts']
                        current_multitap_level = info['multiple_clicks']

                        attempt_success = add_attempts(0, apikey, authorization, current_attempts_level)
                        if attempt_success:
                            upgrade_success[authorization] = True
                            print(f"\r{Fore.GREEN + Style.BRIGHT}[ Upgrade ] : Daily attempts upgraded{' ' * 20}", flush=True)
                            break
                        else:
                            print(f"\r{Fore.RED + Style.BRIGHT}[ Upgrade ] : Failed to upgrade daily attempts{' ' * 20}", flush=True)

                        multitap_success = add_multitap(1, apikey, authorization, current_multitap_level)
                        if multitap_success:
                            upgrade_success[authorization] = True
                            print(f"\r{Fore.GREEN + Style.BRIGHT}[ Upgrade ] : Multitap upgraded{' ' * 20}", flush=True)
                            break
                        else:
                            print(f"\r{Fore.RED + Style.BRIGHT}[ Upgrade ] : Failed to upgrade multitap{' ' * 20}", flush=True)

            time.sleep(2)

            
            if info:
                if complete_task == 'y':
                    auto_complete_task(apikey, authorization)
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Level ] : {info['level']}")
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ] : {info['balance']}")
                print(f"{Fore.BLUE+Style.BRIGHT}[ Energy ] : {info['daily_attempts']}")
                print(f"{Fore.BLUE+Style.BRIGHT}[ Limit Energy ] : {info['limit_attempts']}")
                print(f"{Fore.BLUE+Style.BRIGHT}[ Multiple Click Level ] : {info['multiple_clicks']}")
                auto_gacha(apikey, authorization, 150000)
                energy = info['daily_attempts']
                while energy > 0:
                    for _ in range(energy):
                        print(f"{Fore.BLUE+Style.BRIGHT}\r[ Tap ] : Tapping..", end="" , flush=True)
                        time.sleep(3)
                        save_coins(20000, apikey, authorization)
                        print(f"{Fore.GREEN+Style.BRIGHT}\r[ Tap ] : Success             ", flush=True)
                    info = get_user_info(apikey, authorization)
                    energy = info['daily_attempts']
                    if energy == 0:
                        restore_attempts(apikey, authorization)
                        info = get_user_info(apikey, authorization)
                        energy = info['daily_attempts']
                else:
                    print(f"{Fore.RED+Style.BRIGHT}[ Energy ] Your energy is running out. Waiting for energy refill...")
                    if energy == 0:
                        restore_attempts(apikey, authorization)
                        info = get_user_info(apikey, authorization)
                        energy = info['daily_attempts']

                if auto_upgrade_dtc == 'y':
                    upgrade_dtc_miner(apikey, authorization, info['id'])

     

            else:
                print("\r{Fore.RED+Style.BRIGHT}Invalid access token, continue to next account.")
        time.sleep(2)
        print(f"\n{Fore.CYAN+Style.BRIGHT}==============All accounts have been processed=================")
        for i in range(300, 0, -1):
            sys.stdout.write(f"\rReprocess all accounts in {i} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        print()

        clear_console()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW+Style.BRIGHT}Exiting... See ya 👋")
        sys.exit(0)