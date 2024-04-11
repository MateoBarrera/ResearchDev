from ninja import Router
from api.models import Site
from api.schemas import SiteSchema, SiteCreateSchema, ErrorSchema
from django.shortcuts import get_object_or_404
from typing import List

site_router = Router()


@site_router.get("/", response=List[SiteSchema])
def read_sites(request):
    return Site.objects.all()


@site_router.get("/{id}", response=SiteSchema)
def read_site(request, id: int):
    site = get_object_or_404(Site, id=id)
    return site


@site_router.post("/", response={200: SiteSchema, 404: ErrorSchema})
def create_site(request, site: SiteCreateSchema):
    site_data = site.model_dump()
    site_instance = Site.objects.create(**site_data)
    return site_instance


@site_router.put("/{id}", response=SiteSchema)
def update_site(request, id: int, site: SiteCreateSchema):
    site_instance = get_object_or_404(Site, id=id)
    for attr, value in site.dict().items():
        setattr(site_instance, attr, value)
    site_instance.save()
    return site_instance


@site_router.delete("/{id}")
def delete_site(request, id: int):
    site = get_object_or_404(Site, id=id)
    site.delete()
    return {"success": True, "message": "Site deleted successfully"}
