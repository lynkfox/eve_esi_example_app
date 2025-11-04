import requests


def get_system_name(id_num):
    url = "https://esi.evetech.net/universe/names"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "",
        "Content-Type": "application/json",
        "If-None-Match": "",
        "X-Compatibility-Date": "2025-09-30",
        "X-Tenant": "",
    }
    body = [f"{id_num}"]
    response = requests.post(url=url, headers=headers, json=body, timeout=15)

    if response.status_code == 200:
        return response.json()[0].get("name", None)

    else:
        print("Could not access universe/ids, try again later")
        return None
    

def get_system_jumps():
    url = "https://esi.evetech.net/universe/system_jumps"

    headers = {
        "Accept-Language": "",
        "If-None-Match": "",
        "X-Compatibility-Date": "2025-09-30",
        "X-Tenant": "",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_body = response.json()
        count = 0
        while count < 5:
            jump_info = response_body[count]
            system_name = get_system_name(jump_info.get("system_id", 0))
            system_jumps = jump_info.get("ship_jumps", 0)

            print(f"\t💫 {system_name} has had {system_jumps} in the last hour")
            count += 1


def main():
    get_system_jumps()

if __name__ == "__main__":
    main()