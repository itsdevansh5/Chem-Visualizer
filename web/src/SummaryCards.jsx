const cardStyle = {
  flex: 1,
  padding: "20px",
  borderRadius: "12px",
  background: "#ffffff",
  border: "1px solid #e8e8e8",
  boxShadow: "0 1px 8px rgba(0,0,0,0.06)",
  textAlign: "center",
  transition: "0.2s",
};

const containerStyle = {
  display: "flex",
  gap: "20px",
  marginTop: "10px",
  marginBottom: "25px",
};

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  const avg = summary.averages;

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h3 style={{ marginBottom: "10px" }}>Total Count</h3>
        <h1 style={{ color: "#007bff" }}>{summary.total_count}</h1>
      </div>

      <div style={cardStyle}>
        <h3 style={{ marginBottom: "10px" }}>Avg Flowrate</h3>
        <h1 style={{ color: "#28a745" }}>{avg.Flowrate.toFixed(2)}</h1>
      </div>

      <div style={cardStyle}>
        <h3 style={{ marginBottom: "10px" }}>Avg Pressure</h3>
        <h1 style={{ color: "#ff9900" }}>{avg.Pressure.toFixed(2)}</h1>
      </div>

      <div style={cardStyle}>
        <h3 style={{ marginBottom: "10px" }}>Avg Temperature</h3>
        <h1 style={{ color: "#dc3545" }}>{avg.Temperature.toFixed(2)}</h1>
      </div>
    </div>
  );
}
