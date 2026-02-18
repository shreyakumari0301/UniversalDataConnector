from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseConnector(ABC):

    @abstractmethod
    def get_data(self, params: dict) -> List[Dict[str, Any]]:
        pass
