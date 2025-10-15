import fastapi
from fastapi.exceptions import RequestValidationError
import uvicorn

from cs_qualif_step2.core.api.device_resource import device_router
from cs_qualif_step2.core.api.handler.conflict_exception_handler import conflict_exception_handler
from cs_qualif_step2.core.domain.exception.ConflictException import ConflictException
from cs_qualif_step2.core.domain.exception.Invalid_input_exception import InvalidInputException
from cs_qualif_step2.core.api.handler.server_exception_handler import server_exception_handler
from cs_qualif_step2.core.api.handler.validation_exception_handler import validation_exception_handler
from cs_qualif_step2.core.api.handler.invalid_input_exception_handler import invalid_input_exception_handler


def main():
    app = fastapi.FastAPI()

    app.include_router(device_router)

    app.add_exception_handler(Exception, server_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InvalidInputException, invalid_input_exception_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)


    uvicorn.run(app, host="0.0.0.0", port=8000)





    print("Done!")



if __name__ == '__main__':
    main()
