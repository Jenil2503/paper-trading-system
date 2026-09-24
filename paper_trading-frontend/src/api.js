import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export async function signup (email, password, trackedSymbol, initialCash) {
    const res = await axios.post(`${API_BASE}/signup`,{
        email,password,
        tracked_symbol : trackedSymbol,
        initial_cash : initialCash
    });
    return res.data;
}

export async function login(email, password){
    const res = await axios.post(`${API_BASE}/login`, {email, password});
    return res.data;
}

export async function getAccount(token) {
  const res = await axios.get(`${API_BASE}/account`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function getTrades(token) {
  const res = await axios.get(`${API_BASE}/trades`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

export async function getEquityCurve(token) {
  const res = await axios.get(`${API_BASE}/equity-curve`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}