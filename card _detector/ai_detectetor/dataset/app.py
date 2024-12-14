import subprocess
import time

def launch_scripts():
    try:
        # Lancer le premier script
        capture_process = subprocess.Popen(["python", "data_set_capture.py"])

        # Lancer le second script (GPU)
        gpu_capture_process = subprocess.Popen(["python", "data_set_capture(GPU).py"])

        # Garder les processus actifs
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Interruption détectée. Arrêt des scripts...")
        capture_process.terminate()
        gpu_capture_process.terminate()

if __name__ == "__main__":
    launch_scripts()
