import { useState } from "react";
import { login, signup } from "./api";

export default function Login({ onLogin }) {
  const [mode, setMode] = useState("login"); // "login" or "signup"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [trackedSymbol, setTrackedSymbol] = useState("");
  const [initialCash, setInitialCash] = useState(100000);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    try {
      let data;
      if (mode === "login") {
        data = await login(email, password);
      } else {
        data = await signup(email, password, trackedSymbol, Number(initialCash));
      }
      localStorage.setItem("token", data.access_token);
      onLogin(data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h2>{mode === "login" ? "Log In" : "Sign Up"}</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
        />

        {mode === "signup" && (
          <>
            <input
              type="text"
              placeholder="Tracked symbol (e.g. RELIANCE.NS)"
              value={trackedSymbol}
              onChange={(e) => setTrackedSymbol(e.target.value)}
              required
              style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
            />
            <input
              type="number"
              placeholder="Initial cash (max 100000)"
              value={initialCash}
              onChange={(e) => setInitialCash(e.target.value)}
              max={70000000}
              min={1}
              required
              style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
            />
          </>
        )}

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button type="submit" style={{ width: "100%", padding: 10 }}>
          {mode === "login" ? "Log In" : "Sign Up"}
        </button>
      </form>

      <p style={{ marginTop: 15, cursor: "pointer", color: "blue" }}
         onClick={() => setMode(mode === "login" ? "signup" : "login")}>
        {mode === "login" ? "Need an account? Sign up" : "Already have an account? Log in"}
      </p>
    </div>
  );
}