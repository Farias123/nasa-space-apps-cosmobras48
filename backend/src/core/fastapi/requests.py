from pydantic import (
    BaseModel,
)

from fastapi import (
    Request,
)


aliases: dict[str, str] = {"id": "fixed_id"}


class QueryParameters(BaseModel):
    """Model for query parameter."""

    dynamic_fields: dict

    @classmethod
    def parser(
        cls,
        request: Request,
    ) -> dict:
        """Parse query string parameters."""
        dynamic_fields = {}
        reserved_keys = cls.model_fields
        query_keys = request.query_params

        for key in query_keys:
            key = aliases.get(key, key)

            if key in reserved_keys:
                continue

            dynamic_fields[key] = request.query_params[key]

        return {
            **({"dynamic_fields": dynamic_fields} if dynamic_fields is not None else {}),
        }
