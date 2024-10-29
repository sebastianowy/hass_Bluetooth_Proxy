from homeassistant.components import bluetooth

import logging
import base64

_LOGGER = logging.getLogger(__name__)

class CompanionBLEScanner(bluetooth.BaseHaRemoteScanner):

    def __init__(self, hass, entry):
        self._connector = bluetooth.HaBluetoothConnector(client=None, source=entry.entry_id, can_connect=lambda: False)
        super().__init__(entry.entry_id, entry.title, self._connector, False)
        self._sensors = []

    async def async_process_json(self, data: dict):

        service_data = {key: base64.b64decode(value) for (key, value) in data.get("service_data", {}).items()}
        m_data = {int(key, 10): base64.b64decode(value) for (key, value) in data.get("manufacturer_data", {}).items()}
        details = dict()
        name = data.get("name", None)
        
        target_key = "0000fe95-0000-1000-8000-00805f9b34fb"
        is_ptx = target_key in service_data
        if is_ptx:
            True
#             _LOGGER.warning(f"LEWDEV async_process_json DEVID PTX BUTTON async_process_json")
#             _LOGGER.warning(f"LEWDEV async_process_jsonPTX SERVICE: {service_data.get(target_key,None)}")
#             _LOGGER.warning(f"LEWDEV async_process_json DETAILS: {data} -> {service_data} -> {m_data}")


        
        self._async_on_advertisement(
            address=data["address"],
            rssi=data.get("rssi", 0),
            local_name=name,
            service_uuids=data.get("service_uuids", []),
            service_data=service_data,
            manufacturer_data=m_data,
            tx_power=data.get("tx_power", 0),
            details=details,
            advertisement_monotonic_time=data.get("timestamp"),
        )

        if is_ptx:
            True
#             _LOGGER.warning(f"LEWDEV async_process_json _async_on_advertisement successfully called for name {name}")

    async def async_update_sensors(self):
#         _LOGGER.warning(f"LEWDEV async_update_sensors sensors length {self._sensors}")
        for s in self._sensors:
            await s.async_on_scanner_update(self)

    async def async_load(self, hass):
        self._unload_callback = bluetooth.async_register_scanner(hass, self, False)

    async def async_unload(self, hass):
        self._unload_callback()
        self._sensors = []