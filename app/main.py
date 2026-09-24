from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db import supabase
from pydantic import BaseModel
from app.auth import hash_password, verify_password, create_access_token, get_current_user_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SignupRequest(BaseModel):
    email: str
    password: str
    tracked_symbol: str
    initial_cash: float


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/account")
def get_account(user_id: Annotated[int, Depends(get_current_user_id)]):
    result = supabase.table("accounts").select("*").eq("user_id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Account Not Found")
    return result.data[0]


@app.get("/trades")
def get_trades(user_id: Annotated[int, Depends(get_current_user_id)]):
    result = supabase.table("trades") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("executed_at", desc=True) \
        .execute()
    return result.data


@app.get("/equity-curve")
def get_equity_curve(user_id: Annotated[int, Depends(get_current_user_id)]):
    account = supabase.table("accounts").select("*").eq("user_id", user_id).execute()
    if not account.data:
        raise HTTPException(status_code=404, detail="Account Not Found")

    account = account.data[0]
    current_cash = account["cash_balance"]

    trades = supabase.table("trades") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("executed_at") \
        .execute()

    cash = current_cash
    reversed_points = []

    for trade in reversed(trades.data):
        value = trade["price"] * trade["quantity"]
        reversed_points.append({"timestamp": trade["executed_at"], "cash": cash})
        if trade["side"] == "BUY":
            cash += value
        else:
            cash -= value

    return list(reversed(reversed_points))


@app.post("/signup")
def signup(payload: SignupRequest):
    existing = supabase.table("users").select("*").eq("email", payload.email).execute()

    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    if payload.initial_cash <= 0 or payload.initial_cash > 100000:
        raise HTTPException(status_code=400, detail="Initial cash must be between 0 and 100000")

    hashed = hash_password(payload.password)

    user_result = supabase.table("users").insert({
        "email": payload.email,
        "hashed_password": hashed
    }).execute()

    user_id = user_result.data[0]["id"]
    supabase.table("accounts").insert({
        "user_id": user_id,
        "cash_balance": payload.initial_cash,
        "tracked_symbol": payload.tracked_symbol
    }).execute()

    token = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/login")
def login(payload: LoginRequest):
    result = supabase.table("users").select("*").eq("email", payload.email).execute()

    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    user = result.data[0]
    if not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or Password")

    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}