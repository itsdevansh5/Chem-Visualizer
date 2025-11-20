import axios from "axios";
import { API_URL, TOKEN } from "./config";
import { useEffect, useState } from "react";

export default function HistoryList({ onSelect }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get(API_URL + "history/", {
      headers: { "Authorization": `Token ${TOKEN}` }
    }).then(res => setHistory(res.data));
  }, []);

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Last 5 Uploads:</h3>
      {history.map(item => (
        <button 
          key={item.id}
          onClick={() => onSelect(item.id)}
          style={{ display: "block", margin: "5px 0" }}
        >
          {item.name} (ID: {item.id})
        </button>
      ))}
    </div>
  );
}
