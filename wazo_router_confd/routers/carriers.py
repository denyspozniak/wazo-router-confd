# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal, get_principal
from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import carrier as schema
from wazo_router_confd.services import carrier as service


router = APIRouter()


@router.post("/carriers", response_model=schema.Carrier)
def create_carrier(
    carrier: schema.CarrierCreate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier = service.get_carrier_by_name(db, principal, name=carrier.name)
    if db_carrier:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated name",
                "resource": "carrier",
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
    return service.create_carrier(db, principal, carrier=carrier)


@router.get("/carriers", response_model=schema.CarrierList)
def read_carriers(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    carriers = service.get_carriers(db, principal, offset=offset, limit=limit)
    return carriers


@router.get("/carriers/{carrier_id}", response_model=schema.Carrier)
def read_carrier(
    carrier_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier = service.get_carrier(db, principal, carrier_id=carrier_id)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier


@router.put("/carriers/{carrier_id}", response_model=schema.Carrier)
def update_carrier(
    carrier_id: int,
    carrier: schema.CarrierUpdate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier = service.update_carrier(
        db, principal, carrier=carrier, carrier_id=carrier_id
    )
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier


@router.delete("/carriers/{carrier_id}", response_model=schema.Carrier)
def delete_carrier(
    carrier_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_carrier = service.delete_carrier(db, principal, carrier_id=carrier_id)
    if db_carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")
    return db_carrier
