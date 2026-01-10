import sys
import subprocess

with open("error_log.txt", "w") as err_file:
    try:
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        err_file.write(result.stderr)
        if result.returncode != 0:
            print(f"Process failed with return code {result.returncode}")
    except Exception as e:
        print(f"Wrapper failed: {e}")
