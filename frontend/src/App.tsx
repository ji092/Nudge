import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");

  // get_windows 임시 테스트용 — 사이드바 구현 시 교체될 자리.
  async function getWindows() {
    try {
      setGreetMsg(await invoke("get_windows"));
    } catch (err) {
      setGreetMsg(String(err));
    }
  }

  return (
    <main className="container">
      <h1>Welcome to Tauri + React</h1>

      <div className="row">
        <a href="https://vite.dev" target="_blank">
          <img src="/vite.svg" className="logo vite" alt="Vite logo" />
        </a>
        <a href="https://tauri.app" target="_blank">
          <img src="/tauri.svg" className="logo tauri" alt="Tauri logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <p>Click on the Tauri, Vite, and React logos to learn more.</p>

      <div className="row">
        <button onClick={getWindows}>Greet</button>
      </div>
      <p style={{ whiteSpace: "pre-wrap", textAlign: "left" }}>{greetMsg}</p>
    </main>
  );
}

export default App;
