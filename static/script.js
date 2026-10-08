const latencyValues = [];
const timeLabels = [];

const chart = new Chart(
    document.getElementById("latencyChart"),
    {
        type: "line",
        data: {
            labels: timeLabels,
            datasets: [{
                label: "Latency (ms)",
                data: latencyValues,
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

async function checkNetwork() {
    const host = document.getElementById("host").value.trim();
    const button = document.getElementById("checkBtn");

    if (!host) {
        alert("Please enter a hostname or IP address.");
        return;
    }

    button.disabled = true;
    button.textContent = "Checking...";

    try {
        const [pingRes, dnsRes, tcpRes] = await Promise.all([
            fetch(`/api/ping?host=${encodeURIComponent(host)}`),
            fetch(`/api/dns?host=${encodeURIComponent(host)}`),
            fetch(`/api/tcp?host=${encodeURIComponent(host)}&port=443`)
        ]);

        const ping = await pingRes.json();
        const dns = await dnsRes.json();
        const tcp = await tcpRes.json();

        document.getElementById("status").textContent = ping.status;
        document.getElementById("latency").textContent =
            ping.latency !== null ? `${ping.latency} ms` : "-- ms";
        document.getElementById("ip").textContent = dns.ip || "FAILED";
        document.getElementById("tcp").textContent = tcp.status;

        if (ping.latency !== null) {
            latencyValues.push(ping.latency);
            timeLabels.push(new Date().toLocaleTimeString());
            chart.update();
        }
    } catch (error) {
        document.getElementById("status").textContent = "ERROR";
        console.error(error);
    } finally {
        button.disabled = false;
        button.textContent = "Check Network";
    }
}

function clearChart() {
    latencyValues.length = 0;
    timeLabels.length = 0;
    chart.update();
}

document.getElementById("host").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        checkNetwork();
    }
});
