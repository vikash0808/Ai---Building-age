# 🏢 AI Building Energy Simulation & Control Toolkit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![EnergyPlus](https://img.shields.io/badge/EnergyPlus-0078D4?style=for-the-badge)

A Python automation toolkit built for **building energy modeling, safe HVAC setpoint control, and EnergyPlus simulation analytics** (developed as a hackathon project). It parses and modifies EnergyPlus `.idf` cooling schedules safely without touching building geometry, runs EnergyPlus simulations via CLI, and summarizes `eplusout.csv` metrics.

---

## ✨ Key Capabilities

- **Targeted IDF Setpoint Control (`idf_parser.py`):** Modifies cooling setpoints strictly inside `Schedule:Compact` cooling blocks so unrelated numbers (such as wall coordinates) are never corrupted.
- **Validated Simulation Runner (`run_simulation.py`):** Validates `.idf`, `.epw`, and EnergyPlus executable paths before launching subprocess simulations with timeouts and captured logs.
- **Resilient Output Analytics (`output_reader.py`):** Summarizes EnergyPlus `eplusout.csv` metrics (row counts, min, max, mean) using Pandas with an automatic Python stdlib `csv` fallback.
- **Working CLI & Offline Demo (`main.py`):** Run an end-to-end demo immediately using bundled sample data (`examples/`), even without EnergyPlus installed.

---

## 📁 Project Structure

```text
Ai---Building-age/
├── main.py                     # CLI entry point (--demo and full EnergyPlus mode)
├── idf_parser.py               # Safe cooling-schedule IDF parser & modifier
├── run_simulation.py           # Validated EnergyPlus CLI subprocess runner
├── output_reader.py            # EnergyPlus CSV reader & statistical summarizer
├── sample_controller.py        # Standalone setpoint modification script
├── examples/
│   ├── sample_building.idf     # Sample EnergyPlus building model
│   └── sample_eplusout.csv     # Sample EnergyPlus hourly output CSV
├── tests/
│   └── test_pipeline.py        # Automated unit & end-to-end CLI tests
├── Hackathon_Presentation.pptx # Hackathon overview deck
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 💻 Getting Started

### 1. Clone & (Optionally) Install Pandas
```bash
git clone https://github.com/vikash0808/Ai---Building-age.git
cd Ai---Building-age
pip install -r requirements.txt
```

### 2. Run the Offline Demo (No EnergyPlus Required)
```bash
python main.py --demo
```

### 3. Run with a Real EnergyPlus Installation
```bash
python main.py \
  --idf path/to/building.idf \
  --weather path/to/weather.epw \
  --energyplus /path/to/energyplus \
  --old-setpoint 24.0 \
  --new-setpoint 23.0 \
  --output-dir outputs
```

### 4. Run Unit Tests
```bash
python -m unittest discover -s tests -v
```

---

## 👨‍💻 Author

**Vikash Dhillan** — B.Tech Computer Science  
GitHub: [@vikash0808](https://github.com/vikash0808)
