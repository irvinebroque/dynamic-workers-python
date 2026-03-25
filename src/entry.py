from js import Object
from pyodide.ffi import to_js as _to_js
from workers import Response, WorkerEntrypoint, python_from_rpc

DYNAMIC_WORKER_FILE = "dynamic_hello.py"
DYNAMIC_WORKER_COMPATIBILITY_DATE = "2026-03-24"
DYNAMIC_WORKER_COMPATIBILITY_FLAGS = [
    "python_workers"
]
DYNAMIC_WORKER_SOURCE = """
from workers import Response, WorkerEntrypoint

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello from a dynamic Worker")
""".strip()


def to_js_object(value):
    return _to_js(value, dict_converter=Object.fromEntries)


def build_dynamic_worker_code():
    return to_js_object(
        {
            "compatibilityDate": DYNAMIC_WORKER_COMPATIBILITY_DATE,
            "compatibilityFlags": DYNAMIC_WORKER_COMPATIBILITY_FLAGS,
            "mainModule": DYNAMIC_WORKER_FILE,
            "modules": {DYNAMIC_WORKER_FILE: DYNAMIC_WORKER_SOURCE},
            "globalOutbound": None,
        }
    )


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        worker = self.env.LOADER.load(build_dynamic_worker_code())
        entrypoint = worker.getEntrypoint()
        response = python_from_rpc(await entrypoint.fetch(request.js_object))
        return Response(await response.text(), status=response.status)
