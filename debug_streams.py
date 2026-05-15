"""
Debug script to list all streams and unit operations in HYSYS case
"""

import os
import logging
from hysys_interface import HYSYSConnection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_hysys_case(case_path: str):
    """Open HYSYS case and list all streams and unit operations."""
    try:
        hysys = HYSYSConnection()
        hysys.connect(visible=True)
        if os.path.exists(case_path):
            hysys.open_case(os.path.abspath(case_path))
        else:
            logger.error(f"Case file not found: {case_path}")
            return
        print("\n" + "="*70)
        print("AVAILABLE MATERIAL STREAMS")
        print("="*70)
        hysys.list_all_streams()
        print("\n" + "="*70)
        print("AVAILABLE UNIT OPERATIONS")
        print("="*70)
        hysys.list_all_unit_operations()
        hysys.close()
        logger.info("Debug complete. Use the stream names above in your config.yaml")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    case_file = r"D:\Motey\simulation with adjust and set block.hsc"
    debug_hysys_case(case_file)
