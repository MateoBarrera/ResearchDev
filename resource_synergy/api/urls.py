from ninja import NinjaAPI
from .endpoints.analysis import analysis_router
from .endpoints.site import site_router

api = NinjaAPI(version="1.0")

api.add_router("/analysis", analysis_router)
api.add_router("/site", site_router)
