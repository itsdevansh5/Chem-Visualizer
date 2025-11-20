export default function DataTable({ preview }) {
  if (!preview) return null;

  const rows = preview.split("\n").filter(r => r.trim() !== "");
  const headers = rows[0].split(",");

  return (
    <table border="1" cellPadding="6" style={{ marginTop: 20 }}>
      <thead>
        <tr>
          {headers.map((h, idx) => <th key={idx}>{h}</th>)}
        </tr>
      </thead>

      <tbody>
        {rows.slice(1).map((row, i) => (
          <tr key={i}>
            {row.split(",").map((col, c) => (
              <td key={c}>{col}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
