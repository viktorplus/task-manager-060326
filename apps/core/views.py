from uuid import UUID

from django.db.models.functions import uuid
from django.http import HttpResponse
from rest_framework.request import Request
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import Project, Task, Tag


def hello(request, name):
    return HttpResponse(f'Hello, {name}!')




