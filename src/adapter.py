# src/adapter.py
class BaseSourceAdapter:
    """Base adapter for authorized data ingestion."""
    def __init__(self, source_name):
        self.source_name = source_name
        self.authorized = False

    def fetch_data(self):
        if not self.authorized:
            raise PermissionError(f"Automated ingestion for {self.source_name} is not authorized.")
        pass

class ApprovedAPIAdapter(BaseSourceAdapter):
    """Adapter for future approved commercial APIs."""
    def __init__(self):
        super().__init__(source_name="Authorized_Commercial_API")