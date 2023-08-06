from time import sleep
from typing import Dict, Final
from minimalmodbus import IllegalRequestError
from .modbus import ModbusRTUDevice


class SensorWiredIAQ(ModbusRTUDevice):
    """
    Wired sensor measuring temperature, relative humidity,
    carbon dioxide and VOC, optionally particulate matter
    """

    DEVICE_CLASS: Final[str] = "IAQ_Wired"
    DEVICE_CODE: Final[int] = 0x0010

    input_registers: Dict[str, int] = {
        "T": 30003,  # deg C
        "T_F": 30004,  # deg F
        "RH": 30005,  # %, from SHT4x
        "CO2": 30006,  # ppm
        "VOC_INDEX": 30007,  # VOC index as calculated by Sensirion library (1 to 500, average 100)
        "VOC_TICKS": 30008,  # raw VOC ticks
        "PMC_MASS_1_0": 30009,  # ug / m^3
        "PMC_MASS_2_5": 30010,  # ug / m^3
        "PMC_MASS_4_0": 30011,  # ug / m^3
        "PMC_MASS_10_0": 30012,  # ug / m^3
        "PMC_NUMBER_0_5": 30013,  # 1 / m^3
        "PMC_NUMBER_1_0": 30014,  # 1 / m^3
        "PMC_NUMBER_2_5": 30015,  # 1 / m^3
        "PMC_NUMBER_4_0": 30016,  # 1 / m^3
        "PMC_NUMBER_10_0": 30017,  # 1 / m^3
        "PMC_TYPICAL_PARTICLE_SIZE": 30018,  # nm
        "READ_ERR_T": 30019,  # temperature sensor error code (0 if no error)
        "READ_ERR_RH": 30020,  # humidity sensor error code (0 if no error)
        "READ_ERR_CO2": 30021,  # CO2 sensor error code (0 if no error)
        "READ_ERR_VOC": 30022,  # VOC sensor error code (0 if no error)
        "READ_ERR_PMC": 30023,  # PMC sensor error code (0 if no error)
    } | ModbusRTUDevice.input_registers
    holding_registers: Dict[str, int] = {
        "MODBUS_ADDR": 40001,
        "BAUDRATE": 40002,
        "LED_ON": 40003,
        "LED_BRIGHTNESS": 40004,
        "LED_SMOOTH": 40005,
        "CO2_ALERT_LIMIT1": 40006,
        "CO2_ALERT_LIMIT2": 40007,
        "SCD4x_T_OFFSET": 40008,
    } | ModbusRTUDevice.holding_registers

    @property
    def CO2(self) -> int:
        return int(self.read_register(self.input_registers["CO2"]))

    @property
    def T(self) -> float:
        return self.read_register(self.input_registers["T"], signed=True) / 10

    @property
    def RH(self) -> float:
        return self.read_register(self.input_registers["RH"])

    @property
    def VOC(self):
        return self.read_register(self.input_registers["VOC_INDEX"])

    @property
    def LED(self) -> int:
        return int(self.read_register(self.holding_registers["LED_BRIGHTNESS"]))

    @LED.setter
    def LED(self, value: int):
        if value == 0:
            self.write_register(self.holding_registers["LED_ON"], 0)
        else:
            self.write_register(self.holding_registers["LED_BRIGHTNESS"], value)
            sleep(0.1)
            self.write_register(self.holding_registers["LED_ON"], 1)

    def __remove_sensor_from_input_registers(self, sensor: str):
        """
        Remove all items containing "sensor" str from input_registers
        """
        deleted_registers = list(filter(lambda x: sensor in x, self.input_registers))
        _ = list((self.input_registers.pop(x) for x in deleted_registers))

    def __init__(self, modbus_address, baudrate=19200, dev="/dev/rs485"):
        super().__init__(modbus_address, baudrate, dev)
        # detect sensor configuration and modify input_registers accordingly
        # Check if VOC sensor present
        try:
            self.read_register(self.input_registers["VOC_INDEX"])
        except IllegalRequestError:
            self.__remove_sensor_from_input_registers("VOC")
        # Check if PMC sensor present
        try:
            self.read_register(self.input_registers["PMC_MASS_1_0"])
        except IllegalRequestError:
            self.__remove_sensor_from_input_registers("PMC")


class SensorWiredRHT(ModbusRTUDevice):
    """
    Wired sensor measuring temperature, relative humidity
    and light intensity.
    """

    DEVICE_CLASS: Final[str] = "RHT_Wired"
    DEVICE_CODE: Final[int] = 0x0020

    input_registers: Dict[str, int] = {
        "SER_NUM_1": 30001,
        "SER_NUM_2": 30002,
        "T": 30003,  # from SHT4x
        "T_F": 30004,
        "RH": 30005,  # from SHT4x
        "LIGHT_INTENSITY_1": 30006,
        "LIGHT_INTENSITY_2": 30007,
        "ERROR_T_RH": 30008,
        "ERROR_LIGHT": 30009,
    } | ModbusRTUDevice.input_registers
    holding_registers: Dict[str, int] = {
        "MODBUS_ADDR": 40001,
        "BAUDRATE": 40002,
        "LTR329_GAIN": 40003,
        "LTR329_MEAS_RATE": 40004,
        "LTR329_INTEGRATION_TIME": 40005,
        "LTR329_MODE": 40006,
    } | ModbusRTUDevice.holding_registers

    @property
    def CO2(self):
        return int(self.read_register(self.input_registers["CO2"]))

    @property
    def T(self):
        return self.read_register(self.input_registers["T"], signed=True) / 10

    @property
    def RH(self):
        return self.read_register(self.input_registers["RH"])
