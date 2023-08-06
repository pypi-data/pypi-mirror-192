from typing import Final, Dict, Any, TypeVar, Type, Iterable
from .generic import Device
from .sensor_wired import SensorWiredIAQ, SensorWiredRHT

# links device identifiers to its class
DEVICE_IDENTIFIERS: Final[Dict[int, Device]] = {
    SensorWiredIAQ.DEVICE_CODE: SensorWiredIAQ,
    SensorWiredRHT.DEVICE_CODE: SensorWiredRHT,
}

T = TypeVar("T", bound=Device)


def find_devices(device_cls: Type[T], address_space: Iterable[Any]) -> list[T]:
    """
    Look for devices in given address space
    """
    return list(filter(device_cls.probe, address_space))

    # TODO add device args
