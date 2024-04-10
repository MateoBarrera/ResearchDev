from ninja import Router
from api.models import ResourceEvaluation
from ninja.orm import create_schema

router = Router()


@router.post("/upload_resource_evaluation/")
def upload_resource_evaluation(request, evaluation: ResourceEvaluationCreate):
    evaluation_instance = ResourceEvaluation(**evaluation.dict())
    evaluation_instance.save()
    return {"success": True, "message": "Evaluación de recurso cargada exitosamente"}


ResourceEvaluationCreate = create_schema(ResourceEvaluation)
