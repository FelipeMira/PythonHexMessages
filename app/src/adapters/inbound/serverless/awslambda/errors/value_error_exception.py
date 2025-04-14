import json

from app.src.adapters.inbound.serverless.awslambda.errors.exception_handler_strategy import ExceptionHandlerStrategy
from app.src.adapters.inbound.serverless.awslambda.response.response import Response


class ValueErrorHandler(ExceptionHandlerStrategy):
    def handle(self, exception, event):
        method = event.get("requestContext", {}).get("http", {}).get("method", "UNKNOWN")
        headers = event.get("headers", {})
        headers_list = [(key, value) for key, value in headers.items()]
        body = json.dumps({"error": f"{str(exception)}"})
        return Response(
            status_code=400,
            body=body,
            headers=headers_list,
            method=method
        ).to_dict()