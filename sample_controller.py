"""Standalone example controller demonstrating cooling setpoint modification."""

import argparse
from pathlib import Path

from idf_parser import load_idf, replace_cooling_setpoint_with_count, save_idf

DEFAULT_INPUT = Path(__file__).resolve().parent / "examples" / "sample_building.idf"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs" / "building_modified.idf"


def main():
    parser = argparse.ArgumentParser(description="Update cooling setpoint in an EnergyPlus IDF file.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to source .idf file")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Path to write modified .idf file")
    parser.add_argument("--old", default="24.0", help="Existing cooling setpoint value")
    parser.add_argument("--new", default="23.0", help="New cooling setpoint value")
    args = parser.parse_args()

    idf_text = load_idf(args.input)
    updated_idf, count = replace_cooling_setpoint_with_count(idf_text, args.old, args.new)
    saved_path = save_idf(args.output, updated_idf)
    print(f"Updated {count} cooling setpoint entry(s) ({args.old} -> {args.new}) and saved to {saved_path}.")


if __name__ == "__main__":
    main()
