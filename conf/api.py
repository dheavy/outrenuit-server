from rest_framework import routers
from apps.users.views import UserViewSet
from apps.artefacts.views import FreudianSlipViewSet, ObservationViewSet
from apps.interpretations.views import InterpretationViewSet
from apps.dreams.views import DreamViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'slips', FreudianSlipViewSet)
router.register(r'observations', ObservationViewSet)
router.register(r'interpretations', InterpretationViewSet)
router.register(r'dreams', DreamViewSet)
