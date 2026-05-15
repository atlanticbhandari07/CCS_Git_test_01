# CCS_Git_test_01

Carbon Capture and Storage (CCS) simulation and optimization scripts for ASPEN HYSYS.

## Overview

This repository contains Python scripts for:
- Heat exchanger optimization (Delta Tmin, CAPEX, OPEX, NPV)
- Absorber stage optimization
- Gas velocity optimization
- Eigenvalue and power dispatch analysis
- CO2 capture cost calculations

## Prerequisites

- **ASPEN HYSYS v14** installed on your system
- Python 3.9+
- See `requirements.txt` for Python dependencies

## Quick Start

```bash
pip install -r requirements.txt
python hysys_hx_optimizer.py
```

See `USAGE.txt` for full instructions.

## Project Structure

| File | Description |
|------|-------------|
| `hysys_hx_optimizer.py` | Main heat exchanger optimizer |
| `hysys_interface.py` | HYSYS COM connection interface |
| `heat_exchanger_extractor.py` | Data extraction from HYSYS |
| `deltaTmin_optimizer.py` | Delta Tmin optimization logic |
| `capex_calculator.py` | CAPEX calculations |
| `opex_calculator.py` | OPEX calculations |
| `utils.py` | Shared helper functions |
| `config.yaml` | Configuration file |
| `Area and Cost overall.py` | Area/cost/NPV plotting |
| `stages code with fan from 18.py` | Absorber stage optimization |
| `gas velocity opt new.py` | Gas velocity optimization |
| `plot_eigenvalues.py` | Eigenvalue visualization |
