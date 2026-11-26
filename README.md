# 🏢 AI Building Energy Simulation & Control Toolkit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![EnergyPlus](https://img.shields.io/badge/EnergyPlus-0078D4?style=for-the-badge)

A Python automation toolkit built for **building energy modeling, automated HVAC setpoint experimentation, and EnergyPlus simulation analytics** (developed as a hackathon project). It provides modular scripts to parse and modify EnergyPlus `.idf` files, run headless EnergyPlus simulations via subprocess, and summarize simulation output metrics using Pandas.

---

## ✨ Key Capabilities

- **IDF Model Parsing & Modification (`idf_parser.py`):** Load, edit, and save EnergyPlus Input Data Files (`.idf`) programmatically, including automated cooling setpoint adjustments.
- **Automated EnergyPlus Runner (`run_simulation.py`):** Invoke the EnergyPlus CLI programmatically with a target `.idf` model, `.epw` weather file, and output directory, capturing exit codes and stdout/stderr logs.
- **Simulation Output Analytics (`output_reader.py`):** Parse generated `eplusout.csv` files into Pandas DataFrames and compute structured numeric summaries (row counts, column metadata, descriptive statistics).
- **Setpoint Controller Prototype (`sample_controller.py`):** Demonstrates programmatic cooling setpoint updates (e.g., adjusting `24.0` → `23.0`) to produce modified building models for closed-loop or AI-driven optimization experiments.

---

## 🏗️ Workflow Architecture

```text
  Building Model (.idf)
           │
           ▼
   idf_parser.py / sample_controller.py
   (Programmatic Setpoint Modification)
           │
           ▼
    run_simulation.py  ◄── Weather File (.epw)
    (EnergyPlus CLI Execution)
           │
           ▼
      eplusout.csv
           │
           ▼
    output_reader.py
    (Pandas Parsing & Statistical Summary)
```

---

## 📁 Project Structure

```text
Ai---Building-age/
├── idf_parser.py               # Read, modify cooling setpoints, and save .idf files
├── sample_controller.py        # Example automated cooling setpoint update script
├── run_simulation.py           # Subprocess wrapper to execute EnergyPlus simulations
├── output_reader.py            # Pandas reader & summary generator for eplusout.csv
├── Hackathon_Presentation.pptx # Project pitch & hackathon overview deck
└── README.md
```

---

## 💻 Getting Started

### Prerequisites
- Python 3.9+
- [EnergyPlus](https://energyplus.net/) installed locally (for executing simulations)
- `pandas`

### Installation
```bash
git clone https://github.com/vikash0808/Ai---Building-age.git
cd Ai---Building-age
pip install pandas
```

### Example Usage

**1. Modify a building's cooling setpoint:**
```python
from idf_parser import load_idf, save_idf, replace_cooling_setpoint

idf_text = load_idf("building.idf")
updated_idf = replace_cooling_setpoint(idf_text, "24.0", "23.0")
save_idf("building_modified.idf", updated_idf)
```

**2. Run an EnergyPlus simulation and analyze results:**
```python
from run_simulation import run_energyplus
from output_reader import read_csv, summarize

res = run_energyplus(
    energyplus_exe="/path/to/energyplus",
    idf_file="building_modified.idf",
    weather_file="weather.epw",
    output_dir="sim_output",
)

if res["returncode"] == 0:
    df = read_csv("sim_output")
    print(summarize(df))
```

---

## 👨‍💻 Author

**Vikash Dhillan** — B.Tech Computer Science  
GitHub: [@vikash0808](https://github.com/vikash0808)
