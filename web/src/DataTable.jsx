export default function DataTable({ preview }) {
  if (!preview) return null;

  const rows = preview.split("\n").filter(r => r.trim() !== "");
  const headers = rows[0].split(",");
  

  return (
    <table border="1" cellPadding="6" style={{
  borderCollapse: "collapse",
  width: "100%",
  marginTop: "10px",
  background: "white",
  borderRadius: "10px",
  overflow: "hidden"
}}>
      <thead>
        <tr>
          {headers.map((h, idx) => <th key={idx}>{h}</th>)}
        </tr>
      </thead>

      <tbody>
        {rows.slice(1).map((row, i) => (
          <tr key={i}>
            {row.split(",").map((col, c) => (
              <td key={c}  style={{
  border: "1px solid #eee",
  padding: "8px"
}}>{col}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
