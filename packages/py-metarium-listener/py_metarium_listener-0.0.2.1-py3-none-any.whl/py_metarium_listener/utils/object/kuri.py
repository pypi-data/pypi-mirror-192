from collections import namedtuple

METARIUM_FUNCTION_CALL_SRC_CREATE = "new_arikuri"
METARIUM_FUNCTION_CALL_SRC_ACCEPT = "accept_arikuri_transfer"
METARIUM_FUNCTION_CALL_SRC_TRANSFER = "transfer_arikuri"
METARIUM_FUNCTION_CALL_SRC_DELETE = "delete_arikuri"

KuriObject = namedtuple(
    "KuriObject",
    "kuri call_function caller call_index",
    defaults=[None, None, None, None]
)

KuriOperation = namedtuple(
    "KuriOperation",
    "create accept transfer delete",
    defaults=[
        METARIUM_FUNCTION_CALL_SRC_CREATE,
        METARIUM_FUNCTION_CALL_SRC_ACCEPT,
        METARIUM_FUNCTION_CALL_SRC_TRANSFER,
        METARIUM_FUNCTION_CALL_SRC_DELETE
    ]
)