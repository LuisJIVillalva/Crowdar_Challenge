import pytest

from core.functions import run_service, format_json_pretty
from core.logging_local import log
from jsonschema import validate

from schemas.backend.departments_schema import DEPARTMENTS_SCHEMA
from utils.endpoint_list import GET_DEPARTMENTS


@pytest.mark.parametrize("case_name",

                         ("department_ok", "department_null", "department_empty"),

                         ids=["1:case_ok",
                              "2:department_null",
                              "3:department_empty"
                              ])
def test_get_departament(case_name):
    """
    El objetivo de este test es validar que la respuesta del servicio contenga departamentos
    """
    log.test("El objetivo de este test es validar que la respuesta del servicio contenga departamentos")
    try:
        log.info("Ejecutando GET")
        header = {
            "User-Agent": "Chrome"
        }

        response = run_service(GET_DEPARTMENTS, "GET", 200, header=header).json()

        #Se fuerza el fallo para validar los casos de null y empty
        if case_name == "department_null":
            response.pop("departments")
        if case_name == "department_empty":
            response['departments'] = []

        log.info("Respuesta obtenida:")
        log.info(format_json_pretty(response))

        log.info("Validando que estén todos los campos esperados y que sean del tipo esperado")
        validate(instance=response, schema=DEPARTMENTS_SCHEMA)

    except BaseException as err:
        raise Exception("Hubo un error --> {}".format(str(err).replace('\n', ' ')))
