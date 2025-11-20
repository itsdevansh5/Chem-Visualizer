import React, { useState } from "react";
import UploadForm from "./UploadForm";
import DataTable from "./DataTable";
import Charts from "./Charts";
import HistoryList from "./HistoryList";
import axios from "axios";
import { API_URL, TOKEN } from "./config";

export default function App() {
  const [data, setData] = useState(null);

  const fetchSummary = async (id) => {
    const res = await axios.get(API_URL + `summary/${id}/`, {
      headers: { "Authorization": `Token ${TOKEN}` }
    });
    setData(res.data);
  };

  const downloadPDF = async () => {
    const id = data.id;
    const res = await axios.get(API_URL + `report/${id}/`, {
      headers: { "Authorization": `Token ${TOKEN}` },
      responseType: "blob"
    });

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement("a");
    link.href = url;
    link.download = `report_${id}.pdf`;
    link.click();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Chemical Equipment Visualizer — Web</h1>

      <UploadForm onUpload={setData} />
      <HistoryList onSelect={fetchSummary} />

      {data && (
        <>
          <h2 style={{ marginTop: 20 }}>Data Preview</h2>
          <DataTable preview={data.preview_csv} />

          <h2 style={{ marginTop: 20 }}>Charts</h2>
          <Charts summary={data.summary} />

          <button onClick={downloadPDF} style={{ marginTop: 20 }}>
            Download PDF
          </button>
        </>
      )}
    </div>
  );
}
