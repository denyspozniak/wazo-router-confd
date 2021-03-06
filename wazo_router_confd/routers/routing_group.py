# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal, get_principal
from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import routing_group as schema
from wazo_router_confd.services import routing_group as service


router = APIRouter()


@router.post("/routing-groups", response_model=schema.RoutingGroup)
def create_routing_group(
    routing_group: schema.RoutingGroupCreate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    return service.create_routing_group(db, principal, routing_group=routing_group)


@router.get("/routing-groups", response_model=schema.RoutingGroupList)
def read_routing_groups(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    routing_groups = service.get_routing_groups(
        db, principal, offset=offset, limit=limit
    )
    return routing_groups


@router.get("/routing-groups/{routing_group_id}", response_model=schema.RoutingGroup)
def read_routing_group(
    routing_group_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_routing_group = service.get_routing_group(
        db, principal, routing_group_id=routing_group_id
    )
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group


@router.put("/routing-groups/{routing_group_id}", response_model=schema.RoutingGroup)
def update_routing_group(
    routing_group_id: int,
    routing_group: schema.RoutingGroupUpdate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_routing_group = service.update_routing_group(
        db, principal, routing_group=routing_group, routing_group_id=routing_group_id
    )
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group


@router.delete("/routing-groups/{routing_group_id}", response_model=schema.RoutingGroup)
def delete_routing_group(
    routing_group_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_routing_group = service.delete_routing_group(
        db, principal, routing_group_id=routing_group_id
    )
    if db_routing_group is None:
        raise HTTPException(status_code=404, detail="RoutingGroup not found")
    return db_routing_group
