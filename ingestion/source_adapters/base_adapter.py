"""
Base PMS Adapter Interface
Defines the standard contract for importing hospitality data from Property Management Systems.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BasePMSAdapter(ABC):
    """Abstract Base Class for PMS Integration Adapters."""

    @abstractmethod
    def fetch_properties(self) -> List[Dict[str, Any]]:
        """Retrieve property profiles."""
        pass

    @abstractmethod
    def fetch_rooms_and_types(self) -> Dict[str, List[Dict[str, Any]]]:
        """Retrieve room types and individual physical rooms."""
        pass

    @abstractmethod
    def fetch_reservations(self, property_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve guest reservations with guest contact details."""
        pass

    @abstractmethod
    def fetch_folios(self, property_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve guest, booking, and house folios."""
        pass

    @abstractmethod
    def fetch_invoices(self, property_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve issued tax invoices with itemized charge lines."""
        pass

    @abstractmethod
    def fetch_payments(self, property_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve recorded payment transactions."""
        pass
