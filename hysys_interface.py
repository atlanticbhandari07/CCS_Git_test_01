"""
ASPEN HYSYS COM Interface Module
Provides Python interface to ASPEN HYSYS v14 using COM automation.
"""

import win32com.client
import pythoncom
import os
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HYSYSConnectionError(Exception):
    """Custom exception for HYSYS connection errors"""
    pass


class HYSYSConnection:
    """Manages connection to ASPEN HYSYS application via COM interface."""

    def __init__(self):
        self.hysys_app = None
        self.active_case = None
        self.flowsheet = None
        self._connected = False

    def connect(self, visible: bool = True) -> bool:
        """Connect to ASPEN HYSYS application."""
        try:
            logger.info("Attempting to connect to ASPEN HYSYS v14...")
            pythoncom.CoInitialize()
            try:
                self.hysys_app = win32com.client.GetActiveObject("HYSYS.Application")
                logger.info("Connected to existing HYSYS instance")
            except:
                self.hysys_app = win32com.client.Dispatch("HYSYS.Application")
                logger.info("Created new HYSYS instance")
            self.hysys_app.Visible = visible
            self._connected = True
            logger.info("Successfully connected to HYSYS")
            return True
        except Exception as e:
            error_msg = f"Failed to connect to HYSYS: {str(e)}"
            logger.error(error_msg)
            raise HYSYSConnectionError(error_msg)

    def open_case(self, case_path: str) -> bool:
        """Open a HYSYS case file."""
        if not self._connected:
            raise HYSYSConnectionError("Not connected to HYSYS. Call connect() first.")
        if not os.path.exists(case_path):
            raise FileNotFoundError(f"HYSYS case file not found: {case_path}")
        try:
            logger.info(f"Opening HYSYS case: {case_path}")
            abs_case_path = os.path.abspath(case_path)
            sim_cases = self.hysys_app.SimulationCases
            self.active_case = sim_cases.Open(abs_case_path)
            self.flowsheet = self.active_case.Flowsheet
            logger.info("Case opened successfully")
            return True
        except Exception as e:
            error_msg = f"Failed to open HYSYS case: {str(e)}"
            logger.error(error_msg)
            raise HYSYSConnectionError(error_msg)

    def get_unit_operation(self, unit_name: str):
        """Get a unit operation object by name."""
        if self.flowsheet is None:
            raise HYSYSConnectionError("No active flowsheet. Open a case first.")
        try:
            unit_op = self.flowsheet.Operations.Item(unit_name)
            return unit_op
        except Exception as e:
            raise ValueError(f"Unit operation '{unit_name}' not found: {str(e)}")

    def get_stream(self, stream_name: str):
        """Get a material stream object by name."""
        if self.flowsheet is None:
            raise HYSYSConnectionError("No active flowsheet. Open a case first.")
        try:
            return self.flowsheet.MaterialStreams.Item(stream_name)
        except Exception as e:
            raise ValueError(f"Material stream '{stream_name}' not found: {str(e)}")

    def get_energy_stream(self, stream_name: str):
        """Get an energy stream object by name."""
        if self.flowsheet is None:
            raise HYSYSConnectionError("No active flowsheet. Open a case first.")
        try:
            return self.flowsheet.EnergyStreams.Item(stream_name)
        except Exception as e:
            raise ValueError(f"Energy stream '{stream_name}' not found: {str(e)}")

    def solve_flowsheet(self, timeout: int = 30) -> bool:
        """Trigger HYSYS solver and wait for convergence."""
        if self.flowsheet is None:
            raise HYSYSConnectionError("No active flowsheet. Open a case first.")
        try:
            import time
            solver = None
            for obj in [self.active_case, self.flowsheet]:
                if obj is not None:
                    try:
                        solver = obj.Solver
                        break
                    except AttributeError:
                        continue
            if solver is None:
                time.sleep(2)
                return True
            try:
                solver.CanSolve = True
            except:
                pass
            start_time = time.time()
            while True:
                try:
                    if solver.IsSolved:
                        break
                except:
                    break
                if time.time() - start_time > timeout:
                    return False
                time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"Solver failed: {e}")
            return False

    def close(self, save: bool = False) -> None:
        """Close HYSYS connection and cleanup."""
        try:
            if save and self.active_case:
                self.active_case.Save()
            if self.active_case:
                self.active_case.Close()
            self._connected = False
            pythoncom.CoUninitialize()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
