"""Subprocess wrapper for running EnergyPlus building energy simulations."""

from pathlib import Path
import shutil
import subprocess
from typing import Any, Dict


def run_energyplus(
    energyplus_exe: str,
    idf_file: str,
    weather_file: str,
    output_dir: str,
    timeout: int = 600,
) -> Dict[str, Any]:
    """Validate inputs and execute EnergyPlus CLI cleanly."""
    idf_path = Path(idf_file)
    weather_path = Path(weather_file)
    out_path = Path(output_dir)

    if not idf_path.exists():
        raise FileNotFoundError(f"IDF model file not found: {idf_path}")
    if not weather_path.exists():
        raise FileNotFoundError(f"Weather (.epw) file not found: {weather_path}")

    resolved_exe = shutil.which(energyplus_exe) or (
        energyplus_exe if Path(energyplus_exe).exists() else None
    )
    if not resolved_exe:
        raise FileNotFoundError(
            f"EnergyPlus executable not found: '{energyplus_exe}'. "
            "Install EnergyPlus or pass the full path to energyplus."
        )

    out_path.mkdir(parents=True, exist_ok=True)
    cmd = [
        resolved_exe,
        "-w",
        str(weather_path),
        "-d",
        str(out_path),
        str(idf_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "output_dir": str(out_path),
        "command": cmd,
    }


if __name__ == "__main__":
    print("Run 'python main.py --demo' for a quick demo, or 'python main.py --help' for CLI options.")
