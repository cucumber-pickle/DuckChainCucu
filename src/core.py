import time
import json
import random
import urllib.request
import urllib.error
import urllib.parse
from colorama import *
from src.cucumber import read_config, mrh, pth, kng, htm, bru, hju, countdown_timer, log, log_line
from src.agent import generate_random_user_agent
from datetime import datetime
import http

init(autoreset=True)
config = read_config()

class DuckChainAPI:
    def __init__(self, authorization, proxy=None, timeout=10):
        self.base_url = "https://preapi.duckchain.io"
        self.authorization = f'tma {authorization}'
        self.headers = {
            "accept": "*/*",
            "authorization": self.authorization,
            "origin": "https://tgdapp.duckchain.io",
            "referer": "https://tgdapp.duckchain.io/",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Android WebView\";v=\"127\", \"Chromium\";v=\"127\"",
            "user-agent": generate_random_user_agent()
        }
        self.proxy = proxy
        self.timeout = timeout

    def _make_request(self, endpoint, params=None, retries=3):
        url = f"{self.base_url}{endpoint}"

        if params:
            url += '?' + urllib.parse.urlencode(params)
        # print(f'3 url - {url}')
        req = urllib.request.Request(url, headers=self.headers)

        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': self.proxy, 'https': self.proxy})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)

        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    return json.load(response)
            except urllib.error.HTTPError as e:
                # log(f"HTTPError: {e.code} - {e.reason}")
                return None
            except urllib.error.URLError as e:
                log(f"URLError: {e.reason}")
                log(htm + "~" * 38)
                return None
            except TimeoutError:
                log(f"TimeoutError: Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)
                continue
        log("All retry attempts failed.")
        return None

    def get_user_info(self):
        return self._make_request("/user/info")
    
    def check_in(self):
        return self._make_request("/task/sign_in?")

    def execute_tap(self):
        return self._make_request("/quack/execute")

    def get_tasks(self):
        return self._make_request("/task/task_list")
    
    def perform_sign(self):
        check_in_response = self.check_in()
        if check_in_response and check_in_response.get("code") == 200:
            log(hju + f"Daily Check-in successfully")
        elif check_in_response and check_in_response.get("code") == 500:
            log(hju + f"Daily Check-in : {kng}was complete")
        else:
            log(mrh + f"Daily Check-in failed.")

    def open_all_boxes(self, open_type=1):
        while True:
            endpoint = "/box/open"
            params = {'openType': open_type}

            response = self._make_request(endpoint, params)
            if response and response['code'] == 200 and response['message'] == "SUCCESS":
                data = response['data']
                quantity = data.get('quantity', 0)
                obtain = data.get('obtain', 0)
                boxes_left = data.get('boxesLeft', 0)
                log(hju + f"Box opened successfully!")
                log(hju + f"Quantity: {pth}{quantity} {hju}| Points : {pth}{obtain} {hju}| Boxes left: {pth}{boxes_left}")

                if boxes_left == 0:
                    log(f"{kng}All boxes opened! {pth}No more boxes left.")
                    break
            elif response and response['code'] == 500:
                log(f"{kng}You have {pth}0 {kng}boxes to open, {bru}skipping..")
                break
            else:
                log(f"{Fore.RED}Failed to open the box.")
                break

    def complete_task(self, task_id, category):
        url = f"/task/{category}"
        params = {'taskId': task_id}
        return self._make_request(url, params)


    def perform_tasks(self, tasks_response):
        if not isinstance(tasks_response, dict):
            log(f"Unexpected tasks format: {tasks_response}")
            return

        tasks = tasks_response.get('data')
        # print(f'1. tasks- {tasks}')
        # print(f'6. tasks keys- {tasks.keys()}')
        if not tasks:
            log("No tasks found in the 'data' field.")
            return

        for category, task_list in tasks.items():
            if isinstance(task_list, list):
                # print(f'4. task list - {task_list}')
                for task in task_list:
                    task_id = task.get('taskId')
                    task_type = task.get('taskType')
                    content = task.get('content')
                    integral = task.get('integral')
                    log(f"{kng}Completing {pth}{content}?")
                    try:
                        if task_type == 'twitter_interaction':
                            completion_response = self.complete_task(task_id, task_type)
                        else:
                            completion_response = self.complete_task(task_id, category)
                        if completion_response and completion_response.get("code") == 200:
                            log(hju + f"successfully! {bru}Reward {pth}{integral} {bru}Points")
                        elif completion_response and completion_response.get("code") == 500:
                            log(f"{kng}task was finished ")
                        else:
                            log(kng + f"Failed! {pth}{content} {htm}{completion_response}.")


                    except http.client.RemoteDisconnected as e:
                        log(mrh + f"RemoteDisconnected error occurred: {e}. Moving to next account.")
                        return  # Exit the current account's task processing

        else:
            log(htm + f"All tasks done")




def get_random_proxy():
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]

        if not proxies:
            log("No proxies found in proxies.txt.")
            return None

        proxy = random.choice(proxies)

        if proxy.startswith("http://"):
            return proxy
        elif proxy.startswith("https://"):
            return proxy
        elif proxy.startswith("socks5://"):
            return proxy
        else:
            return f"http://{proxy}"
    except FileNotFoundError:
        log("File 'proxies.txt' not found.")

def log_user_info(user_info):
    if user_info['code'] == 200 and user_info['message'] == "SUCCESS":
        data = user_info['data']
        duck_name = data['duckName']
        log(hju + f"Duck name: {pth}{duck_name}")
        log(hju + f"Decibels: {pth}{data['decibels']}{hju}| Box Amount: {pth}{data['boxAmount']} ")
    else:
        log(mrh + f"Failed to retrieve user info. Code: {user_info['code']}, Message: {user_info['message']}")

def log_quack_result(quack_result, quack_number):
    if quack_result['code'] == 200 and quack_result['message'] == "SUCCESS":
        data = quack_result['data']
        quack_records = data.get('quackRecords', [])
        A = quack_records[8] if len(quack_records) > 8 else None
        B = quack_records[0] if len(quack_records) > 0 else None

        result = A if A else B if B else "No record available"
        
        log(f"{bru}Quack {pth}{quack_number}: {pth}{data['result']} {hju}| Result: {pth}{result}")
        log(f"{hju}Decibel Change: {pth}{data['decibel']} {hju}| Quack Times: {pth}{data['quackTimes']}")
    else:
        log(mrh + f"Failed to execute quack. Code: {quack_result['code']}, Message: {quack_result['message']}")

def main():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        log("File 'config.json' not found.")
        return

    use_proxy = config.get("use_proxy", False)
    quack_delay = config.get("quack_delay", 0)
    quack_amount = config.get("quack_amount", 10)
    complete_task = config.get("complete_task", False)
    account_delay = config.get("account_delay", 5)
    countdown_loop = config.get("countdown_loop", 3800)
    try:
        with open('data.txt', 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        log("File 'tokens.txt' not found.")
        return

    if not tokens:
        log("No tokens found in tokens.txt")
        return

    total_accounts = len(tokens)
    for index, token in enumerate(tokens, start=1): 
        proxy = get_random_proxy() if use_proxy else None
        duck = DuckChainAPI(authorization=token, proxy=proxy)
        log(bru + f"Processing account {pth}{index} / {total_accounts}") 
        log(htm + "~" * 38)

        user_info = duck.get_user_info()
        if user_info and user_info.get('code') == 200:
            duck_name = user_info['data']['duckName']
            if not duck_name:
                log(f'{Fore.RED} no Duck name!')
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                open("http.log", "a", encoding="utf-8").write(
                    f"{now} / {index}  / {token} / no Duck name\n")
                continue
        if user_info and user_info.get('code') != 500:
            log_user_info(user_info)

            duck.perform_sign()
            duck.open_all_boxes()

            for i in range(quack_amount):
                quack_result = duck.execute_tap()
                if quack_result:
                    log_quack_result(quack_result, i + 1)
                else:
                    log(f"{Fore.RED}Failed to execute quack #{i+1}.")
                time.sleep(quack_delay)

            if complete_task:
                tasks = duck.get_tasks()
                if tasks:
                    duck.perform_tasks(tasks)
                else:
                    log(htm + f"No tasks found on the response")
            else:
                log(kng + f"Auto complete task is disable!")

            log_line()
            countdown_timer(account_delay)
        else:
            log(f"{Fore.RED} Data broken!")
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            open("http.log", "a", encoding="utf-8").write(
                f"{now} / {index}  / {token} / Data broken\n")
    countdown_timer(countdown_loop)