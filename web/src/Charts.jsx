import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale } from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

export default function Charts({ summary }) {
  if (!summary) return null;

  const labels = Object.keys(summary.type_distribution);
  const values = Object.values(summary.type_distribution);

  return (
    <div style={{ width: 500, marginTop: 30 }}>
      <Bar
        data={{
          labels,
          datasets: [
            {
              label: "Equipment Count",
              data: values,
              backgroundColor: "rgba(75, 192, 192, 0.6)",
            },
          ],
        }}
      />
    </div>
  );
}
