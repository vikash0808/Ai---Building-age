"""CLI entry point for the AI Building Energy Simulation & Control Toolkit."""

import argparse
import json
from pathlib import Path
import sys

from idf_parser import (
    extract_cooling_setpoints,
    load_idf,
    replace_cooling_setpoint_with_count,
    save_idf,
)
from output_reader import read_csv, summarize
from run_simulation import run_energyplus

BASE_DIR = Path(__file__).resolve().parent


def run_demo(old_setpoint: str, new_setpoint: str, output_dir: Path) -> int:
    sample_idf = BASE_DIR / "examples" / "sample_building.idf"
    sample_csv_dir = BASE_DIR / "examples"

    print("=== AI Building Energy Simulation — Demo Mode ===")
    idf_text = load_idf(str(sample_idf))
    print(f"Loaded sample IDF: {sample_idf.name}")
    print(f"Cooling setpoints before update: {extract_cooling_setpoints(idf_text)}")

    updated_idf, count = replace_cooling_setpoint_with_count(idf_text, old_setpoint, new_setpoint)
    modified_path = save_idf(str(output_dir / "building_modified.idf"), updated_idf)
    print(f"Updated {count} cooling setpoint(s) ({old_setpoint} -> {new_setpoint}) -> {modified_path}")
    print(f"Cooling setpoints after update:  {extract_cooling_setpoints(updated_idf)}")

    data = read_csv(str(sample_csv_dir), filename="sample_eplusout.csv")
    summary = summarize(data)
    print("\n=== Sample EnergyPlus Output Summary ===")
    print(json.dumps(summary, indent=2))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Modify EnergyPlus cooling setpoints, run simulations, and summarize results."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run offline demo using bundled sample IDF and EnergyPlus CSV output.",
    )
    parser.add_argument("--idf", help="Path to EnergyPlus .idf model file")
    parser.add_argument("--weather", help="Path to EnergyPlus .epw weather file")
    parser.add_argument("--energyplus", default="energyplus", help="EnergyPlus executable name or full path")
    parser.add_argument("--old-setpoint", default="24.0", help="Existing cooling setpoint (default: 24.0)")
    parser.add_argument("--new-setpoint", default="23.0", help="Target cooling setpoint (default: 23.0)")
    parser.add_argument("--output-dir", default="outputs", help="Directory for modified IDF and simulation outputs")

    args = parser.parse_args(argv)
    output_dir = Path(args.output_dir)

    if args.demo:
        return run_demo(args.old_setpoint, args.new_setpoint, output_dir)

    if not args.idf or not args.weather:
        parser.error("Provide --idf and --weather, or run with --demo.")

    idf_text = load_idf(args.idf)
    updated_idf, count = replace_cooling_setpoint_with_count(
        idf_text, args.old_setpoint, args.new_setpoint
    )
    modified_idf_path = save_idf(str(output_dir / "building_modified.idf"), updated_idf)
    print(f"Updated {count} cooling setpoint(s) and wrote {modified_idf_path}")

    sim_result = run_energyplus(
        energyplus_exe=args.energyplus,
        idf_file=str(modified_idf_path),
        weather_file=args.weather,
        output_dir=str(output_dir),
    )

    if sim_result["returncode"] != 0:
        print("EnergyPlus simulation failed:", sim_result["stderr"], file=sys.stderr)
        return int(sim_result["returncode"])

    data = read_csv(str(output_dir))
    print(json.dumps(summarize(data), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
