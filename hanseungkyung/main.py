import subprocess
import sys

if __name__ == "__main__":
    # tests 폴더 전체 실행
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q"]))
