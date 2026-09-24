import { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  return token ? (
    <Dashboard token={token} onLogout={handleLogout} />
  ) : (
    <Login onLogin={setToken} />
  );
}

export default App;