from ninja import Router
from api.models import ResourceEvaluation
from ninja.orm import create_schema

from ninja import NinjaAPI

api = NinjaAPI()


@api.post("/upload_resource_evaluation/")
def upload_resource_evaluation(request, evaluation: ResourceEvaluation):
    evaluation_instance = ResourceEvaluation(**evaluation.dict())
    evaluation_instance.save()
    return {"success": True, "message": "Evaluación de recurso cargada exitosamente"}


@api.get("/get_resource_evaluation/")
def get_resource_evaluation(request):
    evaluations = {"hola": "mundo"}
    return evaluations


# ResourceEvaluationCreate = create_schema(ResourceEvaluation)
