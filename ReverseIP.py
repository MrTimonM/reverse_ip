import requests
from concurrent.futures import ThreadPoolExecutor
import colorama
import ctypes
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)
ctypes.windll.kernel32.SetConsoleTitleW("Sub-Domain Tool, developed by MrTimonM")


def process_ip_address(ip_address, counter):
    url = f"https://api.reverseipdomain.com/?ip={ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data["message"] == "Invalid IP":
            print(f"{ip_address}: {Fore.RED}Invalid IP address{Style.RESET_ALL}")
            return 0

        total_number = data.get("total", 0)
        if total_number == 0:
            print(f"{ip_address}: {Fore.RED}Bad request{Style.RESET_ALL}")
        else:
            counter["subdomains"] += total_number
            print(f"{ip_address}: {Fore.GREEN}Processed ({total_number} sub-domains){Style.RESET_ALL}")

            domains = data["result"]
            if domains:
                with open("domains.txt", "a") as output_file:
                    output_file.write("\n".join(domains) + "\n")

        counter["processed"] += 1
        return total_number

    else:
        print(f"{ip_address}: {Fore.RED}Error - Failed to retrieve data from the API{Style.RESET_ALL}")
        return 0

filename = input("Enter the path to the text file: ")

with open(filename, 'r') as file:
    ip_addresses = [line.strip() for line in file]

total_ips = len(ip_addresses)
counter = {"processed": 0, "subdomains": 0, "valid_ips": 0}

num_threads = int(input("Enter the number of threads to use: "))

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = [executor.submit(process_ip_address, ip_address, counter) for ip_address in ip_addresses]

    for result in results:
        counter["subdomains"] += result.result()
        if result.result() > 0:
            counter["valid_ips"] += 1

print(f"\nTotal number of IP addresses: {total_ips}")
print(f"Number of Valid IP: {counter['valid_ips']}")
print(f"Total number of sub-domains collected: {counter['subdomains']}")

input("Press Enter to exit the program")
