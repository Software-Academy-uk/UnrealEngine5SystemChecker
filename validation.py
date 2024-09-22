# Function to validate system specs for Unreal Engine 5
def validate_specs(specs):
    validation_results = []

    # CPU: 4 cores minimum
    cpu_cores = int(specs['CPU'].split('(')[-1].split(' ')[0])
    if cpu_cores < 4:
        validation_results.append("CPU does not meet the requirement (at least 4 cores).")

    # RAM: 16 GB minimum
    ram = float(specs['RAM'].split(' ')[0])
    if ram < 16:
        validation_results.append("Not enough RAM (at least 16 GB required).")

    # Disk Space: 50 GB minimum free space
    free_disk = float(specs['Disk Space'].split(' ')[0])
    if free_disk < 50:
        validation_results.append("Not enough disk space (at least 50 GB required).")

    # GPU: Must have a dedicated GPU
    if "No dedicated GPU" in specs['GPU']:
        validation_results.append("No dedicated GPU found (required for Unreal Engine 5).")

    return validation_results
