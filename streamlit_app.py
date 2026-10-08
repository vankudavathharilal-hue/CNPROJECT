import streamlit as st
import pandas as pd
from datetime import datetime
from network_monitor import ping_host, dns_lookup, tcp_check

st.set_page_config(
    page_title="Network Connectivity & Latency Monitor",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Network Connectivity & Latency Monitor")
st.caption("Computer Networks Project — Ping, Latency, DNS and TCP Monitoring")

st.divider()

host = st.text_input(
    "Hostname / IP Address",
    value="google.com",
    placeholder="Example: google.com"
)

col1, col2 = st.columns([3, 1])

with col1:
    st.info("Enter a hostname or IP address and click Check Network.")

with col2:
    check = st.button("🔍 Check Network", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

if check:

    host = host.strip()

    if not host:
        st.error("Please enter a hostname or IP address.")
        st.stop()

    with st.spinner("Checking network..."):

        ping_result = ping_host(host)
        dns_result = dns_lookup(host)
        tcp_result = tcp_check(host, 443)

    latency = ping_result.get("latency")

    if ping_result["status"] == "ONLINE":
        status = "🟢 ONLINE"
    elif ping_result["status"] == "OFFLINE":
        status = "🔴 OFFLINE"
    else:
        status = "🟠 ERROR"

    current_time = datetime.now().strftime("%H:%M:%S")

    if latency is not None:
        st.session_state.history.append({
            "Time": current_time,
            "Latency (ms)": latency
        })

    st.subheader("Network Results")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Network Status",
            status
        )

    with c2:
        st.metric(
            "Latency",
            f"{latency} ms" if latency is not None else "--"
        )

    with c3:
        st.metric(
            "IP Address",
            dns_result.get("ip") or "FAILED"
        )

    with c4:
        st.metric(
            "TCP :443",
            tcp_result.get("status", "ERROR")
        )

    st.divider()

    st.subheader("Detailed Network Information")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.write("### 📡 Ping")
        st.write(f"**Host:** {host}")
        st.write(f"**Status:** {ping_result['status']}")
        st.write(
            f"**Latency:** {latency} ms"
            if latency is not None
            else "**Latency:** Failed"
        )

    with d2:
        st.write("### 🌐 DNS")
        st.write(f"**Host:** {host}")
        st.write(f"**Status:** {dns_result['status']}")
        st.write(
            f"**IP:** {dns_result['ip']}"
            if dns_result.get("ip")
            else "**IP:** Failed"
        )

    with d3:
        st.write("### 🔌 TCP")
        st.write(f"**Host:** {host}")
        st.write("**Port:** 443")
        st.write(f"**Status:** {tcp_result['status']}")

    if st.session_state.history:

        st.divider()

        st.subheader("📈 Latency History")

        chart_data = pd.DataFrame(
            st.session_state.history
        )

        chart_data = chart_data.set_index("Time")

        st.line_chart(
            chart_data,
            y="Latency (ms)"
        )

        st.subheader("📊 Statistics")

        values = chart_data["Latency (ms)"]

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric(
                "Minimum",
                f"{values.min():.2f} ms"
            )

        with s2:
            st.metric(
                "Average",
                f"{values.mean():.2f} ms"
            )

        with s3:
            st.metric(
                "Maximum",
                f"{values.max():.2f} ms"
            )

st.divider()

st.caption(
    "Network Connectivity & Latency Monitor | Computer Networks Project"
)
