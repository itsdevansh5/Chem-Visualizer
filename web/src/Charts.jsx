import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

export default function Charts({ summary }) {
  if (!summary) return null;

  const dist = summary.type_distribution || {};
  const labels = Object.keys(dist);
  const values = Object.values(dist);

  return (
    <div style={{ width: "600px", marginTop: "30px" }}>
      <h3>Equipment Type Distribution</h3>

      <Bar
        data={{
          labels,
          datasets: [
            {
              label: "Count",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.7)",
            },
          ],
        }}
      />
    </div>
  );
}
