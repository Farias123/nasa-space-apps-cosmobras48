from typing import Any, TypeVar

from pydantic import BaseModel, create_model


D = TypeVar("M", bound=BaseModel)


def create_data_model(
    model: type[BaseModel],
    plural: bool = False,
    custom_single_name: str | None = None,
    custom_plural_name: str | None = None,
    **kwargs: Any,
) -> type[BaseModel]:
    """Create dymanically a model structure for API responses, where the incoming data is a list or not."""

    data_field_name = model.__name__.lower()

    if plural:
        model_name = f"Multiple{model.__name__}"

        if custom_plural_name:
            data_field_name = custom_plural_name
        else:
            data_field_name += "s"

        kwargs[data_field_name] = (list[model], ...)  # type: ignore[valid-type]
    else:
        model_name = f"Single{model.__name__}"
        data_field_name = custom_single_name if custom_single_name else model_name
        kwargs[data_field_name] = (model, ...)

    return create_model(model_name, **kwargs)


class GenericResponse[D: BaseModel](BaseModel):
    status: int
    data: D
