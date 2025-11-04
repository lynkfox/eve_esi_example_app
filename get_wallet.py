from oauth_flow.validate_token import is_token_valid
import requests
from oauth_flow.oauth_pkce_flow import get_valid_access_token

def get_character_id(name):
    url = "https://esi.evetech.net/universe/ids"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "",
        "Content-Type": "application/json",
        "If-None-Match": "",
        "X-Compatibility-Date": "2025-09-30",
        "X-Tenant": "",
    }
    body = [f"{name}"]
    response = requests.post(url=url, headers=headers, json=body, timeout=15)

    if response.status_code == 200:
        characters = response.json().get("characters")
        if characters:
            for char in characters:
                if char.get("name") == name:
                    return char.get("id", 0)
        return None
    else:
        print("Could not access universe/ids, try again later")
        return None


def get_my_isk(token):
    
    headers = {"Authorization": f"Bearer {token}"}
    valid, claims = is_token_valid(token)

    if valid:

        name = claims['name']
        char_id = get_character_id(name)


        balance_url = f"https://esi.evetech.net/latest/characters/{char_id}/wallet/"
        r2 = requests.get(balance_url, headers=headers, timeout=15)

        if r2.status_code == 200:
            print(f"\n💰 Wallet balance for {name}: {r2.json():,.2f} ISK")
        else:
            print("Failed to get wallet balance:", r2.status_code, r2.text)
    
    else:
        print("Token is invalid - please login again")



def main():

    access_token = get_valid_access_token()
    get_my_isk(access_token)


if __name__ == "__main__":
    main()