import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from "chart.js";
import { Pie, Bar } from "react-chartjs-2";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: "#f8fafc"
      }
    }
  }
};

export default function Charts({ data }) {
  if (!data || !data.inventory || !data.cbom) return null;

  console.log("DATA:", data);
  console.log("DOMAINS:", data.inventory?.domains);
  console.log("CBOM:", data.cbom);

  const domains = data.inventory.domains || [];
  const cbom = data.cbom || [];
  const uniqueIPs = new Set(data.inventory.ip_addresses || []).size;

  const web = domains.length;
  const api = domains.filter((domain) => domain.toLowerCase().includes("api")).length;
  const server = uniqueIPs;

  const pieData = {
    labels: ["Web", "API", "Server"],
    datasets: [
      {
        data: [web || 0, api || 0, server || 0],
        backgroundColor: ["#3b82f6", "#10b981", "#f59e0b"]
      }
    ]
  };

  const riskCount = { low: 0, medium: 0, high: 0 };
  cbom.forEach((item) => {
    const r = (item.risk_level || "").toLowerCase();
    if (riskCount[r] !== undefined) {
      riskCount[r]++;
    }
  });

  const barData = {
    labels: ["Low", "Medium", "High"],
    datasets: [
      {
        label: "Risk Distribution",
        data: [riskCount.low, riskCount.medium, riskCount.high],
        backgroundColor: ["#22c55e", "#eab308", "#ef4444"]
      }
    ]
  };

  return (
    <div className="col-span-12 w-full grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
      <div className="bg-gray-900 relative p-4 rounded-xl shadow-xl border border-white/5 h-72 w-full">
        <h2 className="text-white mb-3 font-semibold">Asset Distribution</h2>
        <div className="h-[220px] w-full">
          <Pie data={pieData} options={chartOptions} />
        </div>
      </div>
      <div className="bg-gray-900 relative p-4 rounded-xl shadow-xl border border-white/5 h-72 w-full">
        <h2 className="text-white mb-3 font-semibold">Risk Distribution</h2>
        <div className="h-[220px] w-full">
          <Bar data={barData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}
