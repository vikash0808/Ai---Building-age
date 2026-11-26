from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import idf_parser
import main as cli_main
import output_reader
import run_simulation


class BuildingSimulationTests(unittest.TestCase):
    def setUp(self):
        self.examples_dir = Path(__file__).resolve().parent.parent / "examples"
        self.sample_idf = self.examples_dir / "sample_building.idf"

    def test_replace_cooling_setpoint_preserves_geometry_coordinates(self):
        original = idf_parser.load_idf(str(self.sample_idf))
        updated, count = idf_parser.replace_cooling_setpoint_with_count(
            original, "24.0", "23.0"
        )
        # Only the cooling schedule value should change, NOT the 24.0 wall coordinates
        self.assertEqual(count, 1)
        self.assertIn("Until: 18:00, 23.0,", updated)
        self.assertIn("24.0, 0.0, 0.0,", updated)
        self.assertIn("24.0, 0.0, 3.0;", updated)

    def test_extract_cooling_setpoints(self):
        text = idf_parser.load_idf(str(self.sample_idf))
        values = idf_parser.extract_cooling_setpoints(text)
        self.assertEqual(values, ["28.0", "24.0", "28.0"])

    def test_output_reader_reads_and_summarizes_csv(self):
        data = output_reader.read_csv(str(self.examples_dir), filename="sample_eplusout.csv")
        summary = output_reader.summarize(data)
        self.assertEqual(summary["rows"], 6)
        self.assertIn("MAIN_ZONE:Zone Mean Air Temperature [C](Hourly)", summary["columns"])
        temp_stats = summary["numeric_summary"]["MAIN_ZONE:Zone Mean Air Temperature [C](Hourly)"]
        self.assertEqual(temp_stats["count"], 6)
        self.assertEqual(temp_stats["min"], 23.0)
        self.assertEqual(temp_stats["max"], 24.2)

    def test_run_energyplus_validates_missing_files(self):
        with self.assertRaises(FileNotFoundError):
            run_simulation.run_energyplus("energyplus", "missing.idf", "missing.epw", "out")

    def test_run_energyplus_executes_with_mocked_subprocess(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            idf = tmp_path / "model.idf"
            epw = tmp_path / "weather.epw"
            exe = tmp_path / "energyplus"
            idf.write_text("Version, 23.1;", encoding="utf-8")
            epw.write_text("LOCATION,Demo", encoding="utf-8")
            exe.write_text("stub", encoding="utf-8")

            mock_res = MagicMock(returncode=0, stdout="OK", stderr="")
            with patch("run_simulation.subprocess.run", return_value=mock_res) as mocked_run:
                res = run_simulation.run_energyplus(
                    str(exe), str(idf), str(epw), str(tmp_path / "out")
                )
            self.assertEqual(res["returncode"], 0)
            mocked_run.assert_called_once()

    def test_cli_demo_mode_runs_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            exit_code = cli_main.main(["--demo", "--output-dir", tmp])
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "building_modified.idf").exists())


if __name__ == "__main__":
    unittest.main()
