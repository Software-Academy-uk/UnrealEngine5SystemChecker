import psutil
import platform
import shutil
import GPUtil
import webbrowser

# Define the minimum required driver versions for Unreal Engine
MINIMUM_DRIVER_VERSION_NVIDIA = "456.38"
MINIMUM_DRIVER_VERSION_AMD = "20.10.1"
MINIMUM_DRIVER_VERSION_INTEL = "27.20.100.8587"

# Define driver download links
DRIVER_DOWNLOAD_LINKS = {
    "NVIDIA": "https://www.nvidia.com/Download/index.aspx",
    "AMD": "https://www.amd.com/en/support",
    "Intel": "https://www.intel.com/content/www/us/en/download-center/home.html",
}


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


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if gpus:
        return {"name": gpus[0].name, "driver_version": gpus[0].driver}
    return None


def is_driver_up_to_date(gpu_name, driver_version):
    if "NVIDIA" in gpu_name:
        return driver_version >= MINIMUM_DRIVER_VERSION_NVIDIA, DRIVER_DOWNLOAD_LINKS[
            "NVIDIA"
        ]
    elif "AMD" in gpu_name:
        return driver_version >= MINIMUM_DRIVER_VERSION_AMD, DRIVER_DOWNLOAD_LINKS[
            "AMD"
        ]
    elif "Intel" in gpu_name:
        return driver_version >= MINIMUM_DRIVER_VERSION_INTEL, DRIVER_DOWNLOAD_LINKS[
            "Intel"
        ]
    return False, None


def check_driver_and_link_user():
    driver_details = "\n--- Driver information ---\n"
    gpu_info = get_gpu_info()
    if gpu_info:
        is_up_to_date, download_link = is_driver_up_to_date(
            gpu_info["name"], gpu_info["driver_version"]
        )
        driver_details += f"Current driver verison: {gpu_info['driver_version']}\n"
        if is_up_to_date:
            return (
                f"Your {gpu_info['name']} driver is up to date for Unreal Engine.",
                driver_details,
            )
        else:
            webbrowser.open(download_link)
            return (
                f"Your {gpu_info['name']} driver is outdated. Please update it.",
                driver_details,
            )
    else:
        print("No GPU detected.")


def check_system_specs():
    """Retrieve system specifications: CPU, RAM, Disk Space, OS, and GPU."""
    specs = {}

    # CPU
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores
    specs["CPU"] = f"{cpu_info} ({cpu_cores} cores)"

    # RAM
    ram = round(psutil.virtual_memory().total / (1024**3), 2)  # Convert to GB
    specs["RAM"] = f"{ram} GB"

    # Disk space
    total, used, free = shutil.disk_usage("/")
    free_gb = round(free / (1024**3), 2)  # Convert to GB
    specs["Disk Space"] = f"{free_gb} GB free"

    # OS
    os_info = platform.system() + " " + platform.release()
    specs["OS"] = os_info

    # GPU
    gpu_info = check_gpu()
    specs["GPU"] = gpu_info

    return specs
