"""Module containing generic Modbus classes/devices"""
from typing import Dict, Final
import minimalmodbus
import serial
from .generic import Device, ReadoutErrorCounter, NoResponseError


class Modbus:
    """Class holding Modbus related constants"""

    HOLDING_REGISTER_START = 40001
    HOLDING_REGISTER_END = 49999
    INPUT_REGISTER_START = 30001
    INPUT_REGISTER_END = 39999
    # ranges for testing if address is in address range
    input_register_range = range(INPUT_REGISTER_START, INPUT_REGISTER_END + 1)
    holding_register_range = range(HOLDING_REGISTER_START, HOLDING_REGISTER_END + 1)


class ModbusRTUDevice(Device):
    """
    Base class for wired device controlled over MODBUS RTU (via RS-485)

    RS-485 to USB converter is needed for devices based off this class
    """

    # Reflects array fw/Core/Src/config.c:config_baudrates[]
    BAUDRATES = [4800, 9600, 14400, 19200, 28800, 38400, 57600, 76800, 115200]
    # magic constant for resetting: common to all Modbus RTU devices
    MAGIC_RESET_CONSTANT: Final[int] = 0xABCD
    # registers common to all Modbus RTU devices
    input_registers: Dict[str, int] = {
        "SERIAL_NUMBER_1": 30001,
        "SERIAL_NUMBER_2": 30002,
    }
    holding_registers: Dict[str, int] = {"RESET_DEVICE": 49999}

    def __comm_device_init(self) -> minimalmodbus.Instrument:
        comm_device = minimalmodbus.Instrument(
            self.dev, self.address, close_port_after_each_call=True
        )
        # RS-485 serial paramater init
        comm_device.serial.baudrate = self.baudrate
        comm_device.serial.bytesize = 8
        comm_device.serial.parity = serial.PARITY_EVEN
        comm_device.serial.stopbits = 1
        comm_device.serial.timeout = 0.05  # seconds
        comm_device.mode = minimalmodbus.MODE_RTU  # rtu or ascii mode
        comm_device.clear_buffers_before_each_transaction = True
        return comm_device

    def __init__(self, modbus_address, baudrate=19200, dev="/dev/rs485"):
        self.address: int = modbus_address
        self.baudrate: int = baudrate
        self.dev: str = dev
        self.comm_device: minimalmodbus.Instrument = self.__comm_device_init()
        self.readout_errors: ReadoutErrorCounter = ReadoutErrorCounter()
        # check if device actually exists on the bus (by reading serial number);
        # if not, raise NoResponseException
        try:
            self.read_register(self.input_registers["SERIAL_NUMBER_1"])
        except minimalmodbus.NoResponseError as exc:
            raise NoResponseError from exc

    def read_register(
        self, register_number: int, signed: bool = False, retries: int = 10
    ) -> int:
        """Read Modbus input/holding register via serial device"""
        if register_number in Modbus.input_register_range:
            function_code = 4
            register_offset = register_number - Modbus.INPUT_REGISTER_START
        elif register_number in Modbus.holding_register_range:
            function_code = 3
            register_offset = register_number - Modbus.HOLDING_REGISTER_START
        else:
            # wrong register number
            raise ValueError
        for _ in range(retries):
            try:
                self.readout_errors.total_attempts += 1
                # minimalmodbus divides received register value by 10
                return (
                    self.comm_device.read_register(
                        register_offset, 1, functioncode=function_code, signed=signed
                    )
                    * 10
                )
            except minimalmodbus.NoResponseError as exception:
                last_exception = exception
                self.readout_errors.no_response += 1
                continue
            except minimalmodbus.InvalidResponseError as exception:
                last_exception = exception
                self.readout_errors.invalid_response += 1
                continue
        # retries failed, raise last exception to inform user
        raise last_exception

    def write_register(
        self, register_number: int, register_value: int, retries: int = 10
    ) -> None:
        """
        Write to slave holding register
        """
        # only holding registers can be written
        if register_number not in Modbus.holding_register_range:
            raise ValueError
        register_offset = register_number - Modbus.HOLDING_REGISTER_START
        for _ in range(retries):
            try:
                return self.comm_device.write_register(
                    register_offset, register_value, functioncode=6
                )
            except (
                minimalmodbus.NoResponseError,
                minimalmodbus.InvalidResponseError,
            ) as exception:
                last_exception = exception
                continue
        raise last_exception

    def __getitem__(self, key: int) -> int:
        return self.read_register(key)

    def __setitem__(self, key: int, value: int) -> None:
        return self.write_register(key, value)

    def reset(self) -> bool:
        """
        Soft-reset the device
        """
        try:
            self.write_register(
                ModbusRTUDevice.holding_registers["RESET_DEVICE"],
                ModbusRTUDevice.MAGIC_RESET_CONSTANT,
            )
            return False  # got answer => failed to reset
        except minimalmodbus.NoResponseError:
            return True  # no answer => reset successful

    @property
    def device_code(self) -> int:
        """
        Return device code. This can be matched to DEVICE_CODE
        in child classes.
        """
        return int(self.read_register(self.input_registers["SERIAL_NUMBER_1"]))

    @property
    def serial_number(self) -> int:
        """
        Return serial number
        """
        serial_number_1 = self.device_code
        serial_number_2 = int(
            self.read_register(self.input_registers["SERIAL_NUMBER_2"])
        )
        return (serial_number_1 << 16) + serial_number_2

    def get_data(self) -> Dict[str, int]:
        """
        Get all data from sensor
        """
        return {
            name: self.read_register(number)
            for name, number in self.input_registers.items()
        }
