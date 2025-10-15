from http.client import HTTPResponse
import hashlib

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import re

from cs_qualif_step2.core.api.handler.conflict_exception_handler import conflict_exception_handler
from cs_qualif_step2.core.api.handler.invalid_input_exception_handler import invalid_input_exception_handler
from cs_qualif_step2.core.application.dto.device_config import DeviceConfig
from cs_qualif_step2.config.get_device_service import get_device_service
from cs_qualif_step2.core.api.dto.request.register_device_request import DeviceRegistrationRequest
from cs_qualif_step2.core.application.device_service import DeviceService
from cs_qualif_step2.core.domain.device.exception.device_with_same_mac_address_exception import \
    DeviceWithSameMacAddressException
from cs_qualif_step2.core.domain.device.exception.invalid_mac_adress import InvalidMacAddress
from cs_qualif_step2.core.infra.in_memory_device_repository import InMemoryDeviceRepository

device_router = APIRouter(
    prefix="/api/v1/devices",
    tags=["devices"]
)


@device_router.post("/api/v1/devices/register")
def register_device(
    device_registration_request: DeviceRegistrationRequest,
    device_service: DeviceService = Depends(get_device_service),
):
    device_config = DeviceConfig(
        macAddress=device_registration_request.macAddress,
        model=device_registration_request.model,
        firmwareVersion=device_registration_request.firmwareVersion,
        serialNumber=device_registration_request.serialNumber,
        displayName=device_registration_request.displayName,
        location=device_registration_request.location,
        timezone=device_registration_request.timezone,
    )



    try:

        if InMemoryDeviceRepository.find_by_mac_address(device_config.macAddress):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=""
            )

        if not device_config.macAddress or device_config.model or device_config.location or device_config.macAddress:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=""
            )




        # etc ...


        device_id = device_service.register_device(device_config)


    except InvalidMacAddress:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"device_id": device_id}
        )
