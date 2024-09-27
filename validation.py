# Function to validate system specs for Unreal Engine
def validate_specs(specs, requirements):
    validation_results = []

    # CPU
    cpu_cores = int(specs['CPU'].split('(')[-1].split(' ')[0])
    if cpu_cores < requirements['CPU']:
        validation_results.append(f"CPU does not meet the requirement ({requirements['CPU']} cores).")

    # RAM
    ram = float(specs['RAM'].split(' ')[0])
    if ram < requirements['RAM']:
        validation_results.append(f"Not enough RAM (at least {requirements['RAM']} GB required).")

    # Disk Space
    free_disk = float(specs['Disk Space'].split(' ')[0])
    if free_disk < requirements['Disk Space']:
        validation_results.append(f"Not enough disk space (at least {requirements['Disk Space']} GB required).")

    # GPU
    if "No dedicated GPU" in specs['GPU'] and requirements['GPU']:
        validation_results.append("No dedicated GPU found (required for Unreal Engine).")

    return validation_results
