from ninja import Router
from api.models import Site, ResourceVariable
from api.schemas import (
    SiteSchema,
    SiteCreateSchema,
    SitePatchSchema,
    ResourceVariableSchema,
    ErrorSchema,
)
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
    resources = None
    if site.resources:
        resources = ResourceVariable.objects.filter(id__in=site.resources)
        if not resources.exist():
            return 404, {
                "detail": "Resource does not exist",
                "code": "resource_not_found",
            }
        else:
            resources = None
    site_data = site.model_dump()
    site_data.pop("resources", None)
    site_instance = Site.objects.create(**site_data)

    if resources:
        site_instance.resources.add(resources)

    return site_instance


@site_router.post("/{id}/set-resources/", response={200: SiteSchema, 404: ErrorSchema})
def update_site_resources(request, id: int, resources: List[SitePatchSchema]):
    site = get_object_or_404(Site, id=id)
    for resource in resources:
        if resource.resource_id:
            resource = get_object_or_404(ResourceVariable, id=resource.resource_id)
            site.resources.add(resource)
    site.save()
    return site


@site_router.put("/{id}", response=SiteSchema)
def update_site(request, id: int, site: SiteCreateSchema):
    site_instance = get_object_or_404(Site, id=id)
    if site.resources:
        site_instance.resources.clear()
        resources = ResourceVariable.objects.filter(id__in=site.resources)
        if resources.exists():
            site_instance.resources.add(*resources)

    site_data = site.model_dump()
    site_data.pop("resources", None)
    for attr, value in site_data.items():
        setattr(site_instance, attr, value)
    site_instance.save()
    return site_instance


@site_router.delete("/{id}")
def delete_site(request, id: int):
    site = get_object_or_404(Site, id=id)
    site.delete()
    return {"success": True, "message": "Site deleted successfully"}


@site_router.get("/{id}/resource", response=List[ResourceVariableSchema])
def get_resource_data(request, id: int):
    site = get_object_or_404(Site, id=id)
    resources = site.resources.all()
    return resources


@site_router.get("/{id}/resource/{resource_id}", response=ResourceVariableSchema)
def get_resource_data(request, id: int, resource_id: int):
    site = get_object_or_404(Site, id=id)
    resource = get_object_or_404(ResourceVariable, id=resource_id)
    return resource


""" @site_router.post(
    "/{id}/resource/{resource_id}/set-data",
    response={200: ResourceVariableSchema, 404: ErrorSchema},
)
def set_resource_data(request, id: int, resource_id: int, data: ):
    if not Site.objects.filter(id=id).exists():
        return 404, {"detail": "Site does not exist", "code": "site_not_found"}
    resource = get_object_or_404(ResourceVariable, id=resource_id)
    resource.data = data.data
    resource.save()
    return resource """
