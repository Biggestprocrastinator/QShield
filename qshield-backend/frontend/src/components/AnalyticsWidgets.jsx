import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";
import { Bar, Doughnut } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const barOptions = {
  indexAxis: "y",
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      grid: { display: false },
      ticks: {
        color: "#f8fafc",
        font: { size: 11 }
      }
    },
    y: {
      grid: { display: false },
      ticks: {
        color: "#f8fafc",
        font: { size: 11 },
        padding: 2
      }
    }
  },
  plugins: {
    legend: { display: false }
  }
};

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "bottom",
      labels: {
        color: "#f8fafc",
        font: { size: 11 }
      }
    }
  }
};

const WidgetCard = ({ title, children, subtitle }) => (
  <div className="bg-gray-900 rounded-2xl border border-white/10 shadow-xl p-3 h-[260px] flex flex-col overflow-hidden">
    <div className="flex items-center justify-between mb-2">
      <h3 className="text-sm font-medium text-white truncate tracking-wide leading-tight">{title}</h3>
      {subtitle && <span className="text-[10px] uppercase tracking-[0.3em] text-secondary">{subtitle}</span>}
    </div>
    <div className="flex-1 min-h-0">{children}</div>
  </div>
);

export function CertificateExpiryCard({ data }) {
  if (!data) return null;
  const cbom = data.cbom || [];
  const expiryBuckets = { critical: 0, warning: 0, safe: 0, good: 0 };
  cbom.forEach((item) => {
    const days = item?.certificate?.expiry_days;
    if (typeof days !== "number" || Number.isNaN(days)) return;
    if (days <= 30) expiryBuckets.critical += 1;
    else if (days <= 60) expiryBuckets.warning += 1;
    else if (days <= 90) expiryBuckets.safe += 1;
    else expiryBuckets.good += 1;
  });
  const expiryValues = [
    expiryBuckets.critical,
    expiryBuckets.warning,
    expiryBuckets.safe,
    expiryBuckets.good
  ];
  const allZero = expiryValues.every((value) => value === 0);
  return (
    <WidgetCard title="Certificate Expiry Timeline">
      {allZero ? (
        <p className="text-sm text-on-surface-variant">No certificate expiry data available.</p>
      ) : (
        <Bar
          data={{
            labels: ["0–30 Days", "30–60 Days", "60–90 Days", ">90 Days"],
            datasets: [
              {
                data: expiryValues,
                backgroundColor: ["#ef4444", "#f97316", "#facc15", "#22c55e"],
                borderWidth: 0
              }
            ]
          }}
          options={barOptions}
        />
      )}
    </WidgetCard>
  );
}

export function IpVersionCard({ data }) {
  if (!data) return null;
  const ipAddresses = data.inventory?.ip_addresses || [];
  const ipv4Count = ipAddresses.filter((ip) => ip?.includes(".")).length;
  const ipv6Count = ipAddresses.filter((ip) => ip?.includes(":")).length;
  const totalIPs = ipv4Count + ipv6Count;
  const donutData = {
    labels: ["IPv4", "IPv6"],
    datasets: [
      {
        data: totalIPs ? [ipv4Count, ipv6Count] : [0, 0],
        backgroundColor: ["#38bdf8", "#a5b4fc"],
        borderWidth: 0
      }
    ]
  };
  const ipv4Percent = totalIPs ? Math.round((ipv4Count / totalIPs) * 100) : 0;
  return (
    <WidgetCard title="IP Version Breakdown" subtitle="Split">
      {totalIPs ? (
        <>
          <div className="relative h-[200px]">
            <Doughnut data={donutData} options={donutOptions} />
          </div>
          <p className="text-center text-xs text-white mt-2">
            IPv4 {ipv4Percent}% · IPv6 {100 - ipv4Percent}%
          </p>
        </>
      ) : (
        <p className="text-sm text-on-surface-variant">No IP data available.</p>
      )}
    </WidgetCard>
  );
}
