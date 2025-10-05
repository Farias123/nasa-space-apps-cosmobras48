from src.core.fastapi.responses import create_data_model
from src.modules.cbtracking.infrastructure.services.horizons.models import HorizonDataResponse

HorizonDataDetail = create_data_model(
    HorizonDataResponse, custom_single_name="object"
)

HorizonDataDetails = create_data_model(
    HorizonDataResponse, plural=True, custom_plural_name="objects"
)
