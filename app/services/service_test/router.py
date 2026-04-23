"""Router du module service_test."""
from fastapi import APIRouter

router = APIRouter(prefix="/service_test", tags=["service_test"])


@router.get('/test')
async def test_path ():
    return 'ok'