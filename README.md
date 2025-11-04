# Example ESI app

Two example apps, one with a public endpoint and one using an endpoint behind oauth


# get_system_jumps

## Run with `python get_system_jumps.py`

It will call the [Get System Jumps](https://developers.eveonline.com/api-explorer#/operations/GetUniverseSystemJumps) end point, then run through the first 5 values in the response. It will take the system_id value and call the [Get names and categories for a set of ids](https://developers.eveonline.com/api-explorer#/operations/PostUniverseNames) for each one (ineffecient but its for an example) and print out the system name and number of jumps in the last hour

# get_wallet

Uses the Oauth 2 PKCE flow - so it generates `token.json` file with your token information. (Suitable for stand alone apps that cannot save token information securely in a db)

### NOTE!!!!
the `token.json file should NEVER be shared or committed to a git history. It is already in the gitignore, do not change that, do not save it, do not share it.

## Run with `python get_wallet.py`

If being run for the first time it will open a browser window (or provide a link) that will start the Oauth process. Logging in with your eve toon will grant this app - assuming you have set up an Eve App properly - the wallet scope. When complete or if token.json already exists, it will validate then call the [Get Characters wallet balance](https://developers.eveonline.com/api-explorer#/operations/GetCharactersCharacterIdWallet) end point for your character (retrieving your name from the validation token, and then your ID from the [Bulk names to id](https://developers.eveonline.com/api-explorer#/operations/PostUniverseIds) endpoint) and display your wallet balance.


# 