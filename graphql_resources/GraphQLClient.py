from typing import Any, Dict, Optional
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = HTTPEndpoint(endpoint)

    def execute_query(self, query: Operation):
        try:
            result = self.endpoint(query)

            if "errors" in result:
                return {"success": False, "errors": result["errors"]}

            return {"success": True, "data": result.get("data", {})}

        except Exception as e:
            return {"success": False, "error": str(e)}
