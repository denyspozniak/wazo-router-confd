# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal, get_principal
from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import carrier_trunk as schema
from wazo_router_confd.services import carrier_trunk as service


router = APIRouter()


@router.post("/carrier_trunks", response_model=schema.CarrierTrunkRead)
def create_carrier_trunk(
    carrier_trunk: schema.CarrierTrunkCreate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier_trunk = service.get_carrier_trunk_by_name(
        db, principal, name=carrier_trunk.name
    )
    if db_carrier_trunk:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated name",
                "resource": "carrier_trunk",
                "timestamp": time(),
                "details": {
                    "config": {
                        "name": {
                            "constraing_id": "name",
                            "constraint": {"unique": True},
                            "message": "Duplicated name",
                        }
                    }
                },
            },
        )
    return service.create_carrier_trunk(db, principal, carrier_trunk=carrier_trunk)


@router.get("/carrier_trunks", response_model=schema.CarrierTrunkList)
def read_carrier_trunks(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    carrier_trunks = service.get_carrier_trunks(
        db, principal, offset=offset, limit=limit
    )
    return carrier_trunks


@router.get(
    "/carrier_trunks/{carrier_trunk_id}", response_model=schema.CarrierTrunkRead
)
def read_carrier_trunk(
    carrier_trunk_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier_trunk = service.get_carrier_trunk(
        db, principal, carrier_trunk_id=carrier_trunk_id
    )
    if db_carrier_trunk is None:
        raise HTTPException(status_code=404, detail="Carrier Trunk not found")
    return db_carrier_trunk


@router.put(
    "/carrier_trunks/{carrier_trunk_id}", response_model=schema.CarrierTrunkRead
)
def update_carrier_trunk(
    carrier_trunk_id: int,
    carrier_trunk: schema.CarrierTrunkUpdate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier_trunk = service.update_carrier_trunk(
        db, principal, carrier_trunk=carrier_trunk, carrier_trunk_id=carrier_trunk_id
    )
    if db_carrier_trunk is None:
        raise HTTPException(status_code=404, detail="Carrier Trunk not found")
    return db_carrier_trunk


@router.delete(
    "/carrier_trunks/{carrier_trunk_id}", response_model=schema.CarrierTrunkRead
)
def delete_carrier_trunk(
    carrier_trunk_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier_trunk = service.delete_carrier_trunk(
        db, principal, carrier_trunk_id=carrier_trunk_id
    )
    if db_carrier_trunk is None:
        raise HTTPException(status_code=404, detail="Carrier Trunk not found")
    return db_carrier_trunk
