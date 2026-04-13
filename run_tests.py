import subprocess
import shutil
import sys
from pathlib import Path

ALLURE_RESULTS = Path("reports/allure-results")
ALLURE_REPORT = Path("reports/allure-report")
HISTORY_SRC = ALLURE_REPORT / "history"
HISTORY_DST = ALLURE_RESULTS / "history"


def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    marker = sys.argv[1] if len(sys.argv) > 1 else None
    pytest_cmd = f"pytest -m {marker}" if marker else "pytest"

    # 1. Kør pytest (alluredir er konfigureret i pytest.ini)
    print(f"Kører pytest{f' -m {marker}' if marker else ''}...")
    run(pytest_cmd)

    # 2. Kopiér historik fra forrige rapport hvis den findes
    if HISTORY_SRC.exists():
        print("Kopierer Allure historik...")
        if HISTORY_DST.exists():
            shutil.rmtree(HISTORY_DST)
        shutil.copytree(HISTORY_SRC, HISTORY_DST)
    else:
        print("Ingen tidligere historik fundet, springer over.")

    # 3. Generér ny Allure-rapport med historik
    print("Genererer Allure rapport...")
    run(f"allure generate {ALLURE_RESULTS.as_posix()} -o {ALLURE_REPORT.as_posix()} --clean")

    # 4. Åbn rapporten i browseren
    print("Åbner rapport...")
    subprocess.Popen(f"allure open {ALLURE_REPORT.as_posix()}", shell=True)


if __name__ == "__main__":
    main()
