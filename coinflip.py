# made by sa#0006 | github.com/entity9/growcasino-coinflip
import json, websockets, asyncio
async def coinflip():
    session_id = input("Session-id: "); auth_session = json.dumps({"id":"authSession","sessionID":session_id})

    bet = 1;bet_side = "heads";bet_data = json.dumps({"id":"onCoinflip","sessionID":session_id,"bet":bet,"side":bet_side})
    username = None;history = [];current_balance = 0.0

    async for ws in websockets.connect("wss://ws.growcasino.net/"):
        await ws.send(auth_session)
        username = (json.loads(str(await ws.recv())))["username"]
        print("Logged in as", username)
        await ws.send(bet_data)
        while True:
            message = await ws.recv()
            response = json.loads(str(message))
            if response["id"] == "onBalanceUpdated":
                current_balance = (float(response["balance"])*100)
                if current_balance >= 1000.0: # gapped to reach 10dls then stop
                    print(f"[+] Reached 10DLS")
                    break
                else:
                    if current_balance > 0:
                        await asyncio.sleep(0.5)
                        bet_data = json.dumps({"id":"onCoinflip","sessionID":session_id,"bet":bet,"side":bet_side})
                        await ws.send(bet_data)
                        print("[=] Wallet: ", str(current_balance)+"WL")
                    else:
                        print("[-] Lost all")
            if response["id"] == "onCoinflipResult" and response["username"] == username:
                history.append(response["outcome"])
                cside = history[len(history)-1]

                # make your autobet scripts here :) enjoy

                if len(history) >= 2 and history[len(history)-1] == history[len(history)-2]:
                    if history[len(history)-1] == history[len(history)-2] == history[len(history)-3]:
                        bet = bet * 1.25
                    else:
                        bet = bet * 2
                    if cside == "tails":
                        bet_side = "heads"
                    else:
                        bet_side = "tails"
                else:
                    bet_side = cside
                    bet = 1
                if bet > current_balance and current_balance > 1:
                    bet = current_balance/2

if __name__ == "__main__": asyncio.run(coinflip())
