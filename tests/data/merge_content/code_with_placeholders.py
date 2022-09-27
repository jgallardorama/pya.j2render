

from crud import activityLogs as crud_activity
from crud import deployruns as crud_deployruns
from crud import user as crud_users
from fastapi import APIRouter, Depends, HTTPException
from helpers.get_data import (check_providers, check_squad_deployrun,
                              check_squad_user)
from helpers.push_task import sync_git
from schemas import schemas
from security import deps
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=schemas.Stack)
def create_new_deployrun(
    deployrun: schemas.StackCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # # ## j2t_begin_block create_new_deployrun

    # # ## j2t_end_block create_new_deployrun
    pass


@router.patch("/{deployrun_id}", response_model=schemas.Stack)
def update_deployrun(
    deployrun_id: int,
    deployrun: schemas.StackCreate,
    current_user: schemas.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # # ## j2t_begin_block update_deployrun

    # # ## j2t_end_block update_deployrun
    pass


@router.get("/")
async def get_all_deployruns(
    current_user: schemas.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
):
    # # ## j2t_begin_block get_all_deployrun
    # mi codigo 123
    # # ## j2t_end_block get_all_deployrun
    pass


@router.get("/{deployrun_id}")
async def get_deployrun_by_id_or_name(
    deployrun_id,
    current_user: schemas.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # # ## j2t_begin_block get_deployrun
    # mi codigo 456

    # # ## j2t_end_block get_deployrun
    pass


@router.delete("/{deployrun_id}")
async def delete_deployrun_by_id_or_name(
    deployrun_id,
    current_user: schemas.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
):
    # # ## j2t_begin_block delete_deployrun

    # # ## j2t_end_block delete_deployrun
    pass
