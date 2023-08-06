"""Module containing classes for generic wired/wireless devices"""
from dataclasses import dataclass
from typing import Dict, Any
from abc import ABC, abstractmethod


@dataclass(slots=True)
class ReadoutErrorCounter:
    """Class used to track readout errors"""

    total_attempts: int = 0
    invalid_response: int = 0
    no_response: int = 0


class NoResponseError(Exception):
    """
    Raised when device fails to respond
    """


class Device(ABC):
    """
    Base class for all devices
    """

    address: Any
    """
    Address space is device-specific (e.g. int for modbus)
    """

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        """
        Get dict with all data from sensor;
        used for logging purposes
        """

    @property
    @abstractmethod
    def device_code(self) -> int:
        """
        Return device code (device type)
        """

    @property
    @abstractmethod
    def serial_number(self) -> int:
        """
        Return serial number, unique for each device
        """

    @classmethod
    def probe(cls, address) -> bool:
        """
        Probe given address, return True if device detected,
        False otherwise
        """
        # try instantiating; this raises NoResponseError
        # if device not detected
        try:
            _ = cls(address)
        except NoResponseError:
            return False
        return True
