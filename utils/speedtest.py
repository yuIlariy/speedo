import speedtest

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping
    isp = st.config['client']['isp']
    return f"📡 ISP: {isp}\n⬇️ Download: {download:.2f} Mbps\n⬆️ Upload: {upload:.2f} Mbps\n🕒 Ping: {ping:.2f} ms"
