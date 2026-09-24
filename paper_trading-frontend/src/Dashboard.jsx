import { useEffect, useState } from "react";
import { getAccount, getTrades, getEquityCurve } from "./api";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

export default function Dashboard({ token, onLogout }) {
  const [account, setAccount] = useState(null);
  const [trades, setTrades] = useState([]);
  const [equityCurve, setEquityCurve] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const [accountData, tradesData, equityData] = await Promise.all([
          getAccount(token),
          getTrades(token),
          getEquityCurve(token),
        ]);
        setAccount(accountData);
        setTrades(tradesData);
        setEquityCurve(equityData);
      } catch (err) {
        setError("Failed to load dashboard data — your session may have expired.");
      }
    }
    loadData();
  }, [token]);

  if (error) {
    return (
      <div style={{ textAlign: "center", marginTop: 50, fontFamily: "sans-serif" }}>
        <p style={{ color: "red" }}>{error}</p>
        <button onClick={onLogout}>Log out</button>
      </div>
    );
  }

  if (!account) {
    return <p style={{ textAlign: "center", marginTop: 50 }}>Loading...</p>;
  }

  return (
    <div style={{ maxWidth: 800, margin: "40px auto", fontFamily: "sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Paper Trading Dashboard</h2>
        <button onClick={onLogout}>Log out</button>
      </div>

      <div style={{ background: "#f5f5f5", padding: 20, borderRadius: 8, marginBottom: 30 }}>
        <h3>Account</h3>
        <p><strong>Cash Balance:</strong> ₹{account.cash_balance.toLocaleString()}</p>
        <p><strong>Tracked Symbol:</strong> {account.tracked_symbol}</p>
      </div>

      <div style={{ marginBottom: 30 }}>
        <h3>Equity Curve</h3>
        {equityCurve.length === 0 ? (
          <p>No trades yet — equity curve will appear after the first trade.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={equityCurve}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="cash" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div>
        <h3>Trade History</h3>
        {trades.length === 0 ? (
          <p>No trades yet.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "2px solid #ccc", textAlign: "left" }}>
                <th style={{ padding: 8 }}>Time</th>
                <th style={{ padding: 8 }}>Side</th>
                <th style={{ padding: 8 }}>Qty</th>
                <th style={{ padding: 8 }}>Price</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((t) => (
                <tr key={t.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: 8 }}>{new Date(t.executed_at).toLocaleString()}</td>
                  <td style={{ padding: 8, color: t.side === "BUY" ? "green" : "red" }}>{t.side}</td>
                  <td style={{ padding: 8 }}>{t.quantity}</td>
                  <td style={{ padding: 8 }}>₹{t.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}