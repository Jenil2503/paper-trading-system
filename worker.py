from worker.price_fetch import fetch_ohlc
from worker.signals import generate_signals
from db import supabase

def get_test_account():
    result = supabase.table("accounts").select("*").execute()
    if not result.data:
        raise ValueError("No accounts found - signup as user first")
    
    return result

def get_position(user_id : int, symbol : str):
    result = supabase.table("positions") \
        .select("*") \
        .eq("user_id", user_id) \
        .eq("symbol" , symbol) \
        .execute()
        
    return result.data[0] if result.data else None


def get_account(user_id : int):
    result = supabase.table("accounts").select("*").eq("user_id", user_id).execute()
    
    return result.data[0]

def execute_buy(user_id : int, symbol : str, price : float, quantity : int):
    account = get_account(user_id)
    cost = price*quantity
    
    if(cost > account["cash_balance"]):
        print(f"Not enough to buy {quantity} {symbol} at {price}")
        return
    

    
    supabase.table("trades").insert({
        "user_id" : user_id, "symbol" : symbol, "side" : "BUY",
        "quantity" : int(float(quantity)), "price" : price
    }).execute()
    
    existing = get_position(user_id, symbol)
    if existing:
        new_qty = existing["quantity"] + quantity
        supabase.table("positions").update({"quantity" : new_qty}).eq("id", existing["id"]).execute()
    else:
        supabase.table("positions").insert({
            "user_id" : user_id, "symbol" : symbol,
            "quantity" : int(float(quantity)), "avg_entry_price" : price
        }).execute()
    
    supabase.table("accounts").update({
        "cash_balance" : account["cash_balance"] - cost
    }).eq("user_id", user_id).execute()
    
    print(f"BUY EXECUTED : {quantity} {symbol} @ {price}")
    
    
def execute_sell(user_id : int, symbol : str, price : float):
    
    position = get_position(user_id,symbol)
    
    if not position or position["quantity"] <= 0:
        print(f"No position to sell for {symbol}")
        return
    
    quantity = position["quantity"]
    proceeds = price * quantity
    supabase.table("trades").insert({
        "user_id" : user_id, 
        "symbol" : symbol, "side" : "SELL",
        "quantity" : int(float(quantity)), "price" : price
    }).execute()
    
    supabase.table("positions").update({"quantity" : 0}).eq("id",position["id"]).execute()
    
    account = get_account(user_id)
    supabase.table("accounts").update({
        "cash_balance" : account["cash_balance"] + proceeds
    }).eq("user_id",user_id).execute()
    
    print(f"SELL EXECUTED : {quantity} {symbol} @ {price}")
    
        
def run(): 
    accounts = get_test_account()
    accounts = accounts.data
    # accounts = accounts[1
    for account in accounts:
        
        user_id = account["user_id"]
        symbol = account["tracked_symbol"]
        
        df = fetch_ohlc(symbol)
        df = generate_signals(df)
        latest = df.iloc[-1]
        
        price = float(latest["Close"])
        unit_size = float(latest["unit_size"])
        # unit_size = unit_size//10
        entry = int(latest["entry_signal"])
        exit_ = int(latest["exit_signal"])
        
        print(f"[user {user_id}] {symbol}@ {price} | entry = {entry} exit = {exit_}")
        
        existing_position = get_position(user_id, symbol)
        
        if entry == 1 and not existing_position:
            # dollar_risk = 0.01*account["cash_balance"]
            quantity = unit_size*account["cash_balance"]*.1
           
            execute_buy(user_id,symbol, price, quantity)
        elif entry == 1 and existing_position:
            print("Entry signal fired, but already holding a postion - skipping.")
        elif exit_ == 1 and existing_position:
            execute_sell(user_id, symbol, price)
        elif entry == 1 and not existing_position:
            print("Exit signal fired, but no holding a postion - skipping.")
        else:
            print("No Signal - Holding")
        
if __name__ == "__main__":
    run()