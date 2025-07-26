import platform
import psutil

def get_sysinfo() -> str:
    sys = platform.uname()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return (
        f"<b>🧠 System</b>: {sys.system} {sys.release} ({sys.machine})\n"
        f"<b>🕹️ Uptime</b>: {round(psutil.boot_time() / 3600, 1)} hrs\n"
        f"<b>💾 Memory</b>: {mem.used // (1024 ** 2)}MB / {mem.total // (1024 ** 2)}MB\n"
        f"<b>📀 Disk</b>: {disk.used // (1024 ** 3)}GB / {disk.total // (1024 ** 3)}GB\n"
        f"<b>⚙️ CPU</b>: {psutil.cpu_percent()}% used"
    )


def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.utcnow()
    return str(now - boot_time).split('.')[0]


