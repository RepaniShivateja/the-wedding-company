from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import get_master_db
from app.schemas import (
    AdminLoginRequest,
    AdminLoginResponse,
    GenericMessage,
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.security import create_access_token, decode_access_token
from app.services.organization_service import OrganizationService

app = FastAPI(title="Multi-tenant Org Service", version="1.0.0")
auth_scheme = HTTPBearer()


async def get_org_service():
    db = await get_master_db()
    return OrganizationService(db)


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    db = await get_master_db()
    payload = decode_access_token(credentials.credentials)
    admin_id = payload.get("admin_id")
    org_name = payload.get("org_name")

    if not admin_id or not org_name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    admin = await db["users"].find_one({"_id": ObjectId(admin_id), "role": "admin"})
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")

    return {"admin_id": admin_id, "org_name": org_name}


@app.post("/org/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_org(payload: OrganizationCreate, service: OrganizationService = Depends(get_org_service)):
    return await service.create_organization(payload)


@app.get("/org/get", response_model=OrganizationResponse)
async def get_org(
    organization_name: str = Query(..., description="Organization name"),
    service: OrganizationService = Depends(get_org_service),
):
    return await service.get_organization(organization_name)


@app.put("/org/update", response_model=OrganizationResponse)
async def update_org(payload: OrganizationUpdate, service: OrganizationService = Depends(get_org_service)):
    return await service.update_organization(payload)


@app.delete("/org/delete", response_model=GenericMessage)
async def delete_org(
    organization_name: str = Query(..., description="Organization name"),
    admin=Depends(get_current_admin),
    service: OrganizationService = Depends(get_org_service),
):
    return await service.delete_organization(organization_name, requester_org=admin["org_name"])


@app.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(payload: AdminLoginRequest, service: OrganizationService = Depends(get_org_service)):
    auth_info = await service.authenticate_admin(payload.email, payload.password)
    token = create_access_token(auth_info)
    return AdminLoginResponse(access_token=token)

