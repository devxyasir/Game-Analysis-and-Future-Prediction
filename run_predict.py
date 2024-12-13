import subprocess

# List of Python files to run sequentially
python_files = [
    'fetch.py',   # This file extracts player information from JSON
    'utils/cs2/extract_player_info.py',   # This file extracts player information from JSON
    'utils/cs2/predict_performance.py',    # This file predicts player performance based on historical data
    'utils/lol/extract_player_info.py',       # Replace with your actual script names
    'utils/lol/predict_performance.py'        # Replace with your actual script names
]

def run_scripts(scripts):
    for script in scripts:
        print(f"Running {script}...")
        try:
            subprocess.run(['python', script], check=True)  # Use 'python3' if on Unix-like systems
            print(f"Finished running {script}.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running {script}: {e}")

if __name__ == "__main__":
    run_scripts(python_files)
