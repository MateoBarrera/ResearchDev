from ninja import Router, Form
from api.models import Analysis
from api.schemas import AnalysisSchema, AnalysisSchemaIn
from django.forms.models import model_to_dict
from typing import List


analysis_router = Router()


@analysis_router.get("/", response=List[AnalysisSchema])
def read_analysis(request):
    analysis = Analysis.objects.all()
    return analysis


@analysis_router.get("/{analysis_id}", response=AnalysisSchema)
def read_analysis(request, analysis_id: int):
    analysis = Analysis.objects.get(analysis_id=analysis_id)
    print("2" * 50)
    print(analysis)

    return analysis


@analysis_router.post("/")
def create_analysis(request, analysis: AnalysisSchemaIn):
    print("1" * 50)
    print(analysis)
    analysis_instance = Analysis.objects.create(**analysis.dict())
    return {"success": True, "analysis": model_to_dict(analysis_instance)}


@analysis_router.put("/{analysis_id}")
def update_analysis(request, analysis_id: int, analysis: AnalysisSchema):
    analysis_instance = Analysis.objects.get(analysis_id=analysis_id)
    for attr, value in analysis.dict().items():
        setattr(analysis_instance, attr, value)
    analysis_instance.save()
    return {"success": True, "analysis": model_to_dict(analysis_instance)}


@analysis_router.delete("/{analysis_id}")
def delete_analysis(request, analysis_id: int):
    analysis = Analysis.objects.get(analysis_id=analysis_id)
    analysis.delete()
    return {"success": True, "message": "Analysis deleted successfully"}
