def validate_specs(specs, requirements):
    """Validate system specs against given requirements."""
    errors = []

    # CPU validation
    try:
        if '(' in specs['CPU']:
            # Handle cases like "Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz (4 cores)"
            cpu_cores = int(specs['CPU'].split('(')[-1].split(' ')[0])
        else:
            cpu_cores = int(specs['CPU'].split(' ')[0])  # Handle simpler case
        if cpu_cores < requirements['CPU']:
            errors.append(f"CPU does not meet the requirement ({requirements['CPU']} cores).")
    except (ValueError, IndexError):
        errors.append("Unable to parse CPU cores from system specs.")

    # RAM validation
    try:
        ram = float(specs['RAM'].split(' ')[0])
        if ram < requirements['RAM']:
            errors.append(f"Not enough RAM (at least {requirements['RAM']} GB required).")
    except ValueError:
        errors.append("Unable to parse RAM from system specs.")

    # Disk Space validation
    try:
        disk_space = float(specs['Disk Space'].split(' ')[0])
        if disk_space < requirements['Disk Space']:
            errors.append(f"Not enough disk space (at least {requirements['Disk Space']} GB required).")
    except ValueError:
        errors.append("Unable to parse Disk Space from system specs.")

    # GPU validation
    if requirements['GPU'] and 'No dedicated GPU' in specs['GPU']:
        errors.append("Dedicated GPU required but not found.")

    return errors
