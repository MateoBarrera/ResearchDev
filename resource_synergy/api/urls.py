from ninja import NinjaAPI
from .endpoints.analysis import analysis_router

api = NinjaAPI(version="1.0")

api.add_router("/analysis", analysis_router)
