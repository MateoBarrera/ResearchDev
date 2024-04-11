from ninja import Router, Form
from api.models import Analysis, Site
from api.schemas import (
    AnalysisSchema,
    AnalysisCreateSchema,
    ErrorSchema,
    AnalysisSitePatch,
)
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from typing import List


analysis_router = Router()


@analysis_router.get("/", response=List[AnalysisSchema])
def read_analysis(request):
    return Analysis.objects.all()


@analysis_router.get("/{id}", response=AnalysisSchema)
def read_analysis(request, id: int):
    analysis = get_object_or_404(Analysis, id=id)
    return analysis


@analysis_router.post("/", response={200: AnalysisSchema, 404: ErrorSchema})
def create_analysis(request, analysis: AnalysisCreateSchema):
    if analysis.site_id:
        site_exists = Site.objects.filter(id=analysis.site_id).exists()
        if not site_exists:
            return 404, {"detail": "Site does not exist", "code": "site_not_found"}

    analysis_data = analysis.model_dump()
    analysis_instance = Analysis.objects.create(**analysis_data)
    return analysis_instance


@analysis_router.post("/{slug}/set-site/", response=AnalysisSchema)
def update_analysis_site(request, slug, site: AnalysisSitePatch):
    analysis = get_object_or_404(Analysis, slug=slug)
    if site.site_id:
        site = get_object_or_404(Site, id=site.site_id)
        analysis.site = site
    else:
        analysis.site = None
    analysis.save()
    return analysis


@analysis_router.put("/{id}", response=AnalysisSchema)
def update_analysis(request, id: int, analysis: AnalysisCreateSchema):
    analysis_instance = Analysis.objects.get(id=id)
    for attr, value in analysis.dict().items():
        setattr(analysis_instance, attr, value)
    analysis_instance.save()
    return {"success": True, "analysis": model_to_dict(analysis_instance)}


@analysis_router.delete("/{id}")
def delete_analysis(request, id: int):
    analysis = Analysis.objects.get(id=id)
    analysis.delete()
    return {"success": True, "message": "Analysis deleted successfully"}
