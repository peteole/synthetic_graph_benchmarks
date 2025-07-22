import os
import requests

def download_file(url: str, folder: str) -> str:
    """
    Download a file from the given URL and save it to the specified folder.
    
    Args:
        url (str): The URL of the file to download.
        folder (str): The folder where the file will be saved.
    
    Returns:
        str: The path to the downloaded file.
    """
    os.makedirs(folder, exist_ok=True)
    filename = url.split("/")[-1]
    filepath = f"{folder}/{filename}"
    if os.path.exists(filepath):
        print(f"File {filename} already exists in {folder}. Skipping download.")
        return filepath
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    
    with open(filepath, "wb") as file:
        file.write(response.content)
    
    return filepath


def available_cpu_count():
    # 1. Slurm-aware (allocated CPUs)
    slurm_cpus = os.environ.get("SLURM_CPUS_ON_NODE") or os.environ.get(
        "SLURM_CPUS_PER_TASK"
    )
    if slurm_cpus:
        return int(slurm_cpus)

    # 2. Respect CPU affinity if psutil is available
    try:
        process = psutil.Process()
        if hasattr(process, "cpu_affinity"):
            # psutil.cpu_count() returns the number of logical CPUs
            # cpu_affinity() returns the CPUs that the process is allowed to run on
            # We return the length of the CPU affinity list
            affinity = process.cpu_affinity()
            if affinity:
                return len(affinity)
    except Exception:
        pass

    # 3. Try Python 3.9+'s os.sched_getaffinity (Linux only)
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))

    # 4. Fall back to all visible CPUs (may overcount on clusters)
    return os.cpu_count() or 1  # fallback to 1 if os.cpu_count() returns None