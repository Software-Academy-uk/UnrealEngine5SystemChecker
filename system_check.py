import psutil
import platform
import shutil
import GPUtil

def check_gpu():
    """Check if a dedicated GPU is present."""
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No dedicated GPU found"
    return f"Dedicated GPU found: {gpus[0].name}"

def check_system_specs():
    """Retrieve system specifications: CPU, RAM, Disk Space, OS, and GPU."""
    specs = {}

    # CPU
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores
    specs['CPU'] = f"{cpu_info} ({cpu_cores} cores)"

    # RAM
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convert to GB
    specs['RAM'] = f"{ram} GB"

    # Disk space
    total, used, free = shutil.disk_usage('/')
    free_gb = round(free / (1024 ** 3), 2)  # Convert to GB
    specs['Disk Space'] = f"{free_gb} GB free"

    # OS
    os_info = platform.system() + " " + platform.release()
    specs['OS'] = os_info

    # GPU
    gpu_info = check_gpu()
    specs['GPU'] = gpu_info

    return specs
