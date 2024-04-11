from ninja import Router
from api.models import Source
from api.schemas import SourceSchema, ErrorSchema
from django.shortcuts import get_object_or_404
from typing import List

source_router = Router()


@source_router.get("/", response=List[SourceSchema])
def read_resource(request):
    return Source.objects.all()
