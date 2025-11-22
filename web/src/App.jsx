import React, { useState } from "react";
import UploadForm from "./UploadForm";
import DataTable from "./DataTable";
import Charts from "./Charts";
import HistoryList from "./HistoryList";
import SummaryCards from "./SummaryCards";
import axios from "axios";
import { API_URL, TOKEN } from "./config";

export default function App() {
  const [data, setData] = useState(null);

  // Fetch summary for history click
  const fetchSummary = async (id) => {
    try {
      const res = await axios.get(`${API_URL}summary/${id}/`, {
        headers: { Authorization: `Token ${TOKEN}` },
      });
      console.log("SUMMARY RESPONSE =", res.data);
      setData(res.data);
    } catch (err) {
      console.error("Error fetching summary:", err);
    }
  };

  // Download PDF report
  const downloadPDF = async () => {
    try {
      const id = data.id;
      const res = await axios.get(`${API_URL}report/${id}/`, {
        headers: { Authorization: `Token ${TOKEN}` },
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.download = `report_${id}.pdf`;
      link.click();
    } catch (err) {
      console.error("Error downloading PDF:", err);
    }
  };

  return (
    <div
      style={{
        padding: "30px",
        maxWidth: "1100px",
        margin: "0 auto",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
        Chemical Equipment Visualizer — Web
      </h1>

      {/* Upload form */}
      <UploadForm onUpload={setData} />

      {/* History list */}
      <HistoryList onSelect={fetchSummary} />

      {/* Display data only when available */}
      {data && (
        <>
          {/* Summary Cards */}
          <h2 style={{ marginTop: "30px" }}>Summary</h2>
<SummaryCards summary={data.summary} />


          {/* Preview Table */}
          <h2 style={{ marginTop: "20px" }}>Data Preview</h2>
          <DataTable preview={data.preview_csv} />

          {/* Charts */}
          <h2 style={{ marginTop: "30px" }}>Charts</h2>
          <Charts summary={data.summary} />

          {/* Download PDF */}
          <button
            onClick={downloadPDF}
            style={{
              marginTop: "20px",
              padding: "10px 20px",
              border: "none",
              borderRadius: "5px",
              background: "#007bff",
              color: "white",
              cursor: "pointer",
            }}
          >
            Download PDF
          </button>
        </>
      )}
    </div>
  );
}
