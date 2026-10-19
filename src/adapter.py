import pandas as pd
from pathlib import Path

class BaseSourceAdapter:
    def __init__(self, source_name):
        self.source_name = source_name
        self.authorized = False

    def fetch_data(self):
        if not self.authorized:
            raise PermissionError(f"Automated ingestion for {self.source_name} is not authorized.")
        pass

class SimulatedOptInAdapter(BaseSourceAdapter):
    """Adapter for Day 6 DPDP-compliant simulated opt-in form fixtures."""
    def __init__(self, file_path):
        super().__init__(source_name="Simulated_Opt_In_Form")
        self.authorized = True
        self.file_path = Path(file_path)

    def fetch_data(self):
        super().fetch_data()
        if not self.file_path.exists():
            raise FileNotFoundError(f"Fixture not found: {self.file_path}")
        return pd.read_csv(
            self.file_path,
            dtype={"Mobile_Number": str, "Requirement": str, "Target_Zone": str}
        )