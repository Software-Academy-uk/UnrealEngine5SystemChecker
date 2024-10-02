import psutil
import platform
import shutil
import GPUtil

def check_gpu():
    """Check if a dedicated GPU is present and provide driver status."""
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No dedicated GPU found"
        
        # Check the GPU driver
        gpu_name = gpus[0].name
        driver_version = gpus[0].driver
        return f"Dedicated GPU found: {gpu_name} (Driver version: {driver_version})"
    except Exception:
        return "Error retrieving GPU information. Ensure the drivers are installed."


def driver_guidance():
    """Provide links to driver download pages for NVIDIA, AMD, and Intel GPUs."""
    gpu_manufacturer = ""
    
    # Check GPU manufacturer
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPU detected. Please visit the relevant page to download drivers."
        
        gpu_name = gpus[0].name.lower()
        
        if "nvidia" in gpu_name:
            gpu_manufacturer = "NVIDIA"
            driver_link = "https://www.nvidia.com/Download/index.aspx"
        elif "amd" in gpu_name or "radeon" in gpu_name:
            gpu_manufacturer = "AMD"
            driver_link = "https://www.amd.com/en/support"
        elif "intel" in gpu_name:
            gpu_manufacturer = "Intel"
            driver_link = "https://www.intel.com/content/www/us/en/download-center/home.html"
        else:
            return "GPU detected, but manufacturer unknown. Please check your system for drivers."

        return f"Detected {gpu_manufacturer} GPU. Please update your drivers here: {driver_link}"
    
    except Exception:
        return "Error detecting GPU drivers. Please visit the appropriate manufacturer website for help."


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
