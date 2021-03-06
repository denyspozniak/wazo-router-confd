# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from typing import Optional

from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.did import DID
from wazo_router_confd.schemas import did as schema
from wazo_router_confd.services import tenant as tenant_service


re_did_prefix_from_regex = re.compile('[^0-9]')


def get_did(db: Session, principal: Principal, did_id: int) -> DID:
    db_did = db.query(DID).filter(DID.id == did_id)
    if principal is not None and principal.tenant_uuids:
        db_did = db_did.filter(DID.tenant_uuid.in_(principal.tenant_uuids))
    return db_did.first()


def get_did_by_regex(db: Session, principal: Principal, regex: Optional[str]) -> DID:
    db_did = db.query(DID).filter(DID.did_regex == regex)
    if principal is not None and principal.tenant_uuids:
        db_did = db_did.filter(DID.tenant_uuid.in_(principal.tenant_uuids))
    return db_did.first()


def get_dids(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.DIDList:
    items = db.query(DID)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(DID.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.DIDList(items=items)


def get_did_prefix_from_regex(did_regex: Optional[str] = None) -> str:
    did_prefix = (
        re_did_prefix_from_regex.split(did_regex.lstrip('^'))[0]
        if did_regex is not None
        else ''
    )
    return did_prefix


def create_did(db: Session, principal: Principal, did: schema.DIDCreate) -> DID:
    did.tenant_uuid = tenant_service.get_uuid(principal, db, did.tenant_uuid)
    db_did = DID(
        did_regex=did.did_regex,
        did_prefix=get_did_prefix_from_regex(did.did_regex),
        carrier_trunk_id=did.carrier_trunk_id,
        tenant_uuid=did.tenant_uuid,
        ipbx_id=did.ipbx_id,
    )
    db.add(db_did)
    db.commit()
    db.refresh(db_did)
    return db_did


def update_did(
    db: Session, principal: Principal, did_id: int, did: schema.DIDUpdate
) -> DID:
    db_did = get_did(db, principal, did_id)
    if db_did is not None:
        db_did.did_regex = (
            did.did_regex if did.did_regex is not None else db_did.did_regex
        )
        db_did.did_prefix = get_did_prefix_from_regex(db_did.did_regex)
        db_did.ipbx_id = did.ipbx_id if did.ipbx_id is not None else db_did.ipbx_id
        db_did.carrier_trunk_id = (
            did.carrier_trunk_id
            if did.carrier_trunk_id is not None
            else db_did.carrier_trunk_id
        )
        db_did.tenant_uuid = (
            did.tenant_uuid if did.tenant_uuid is not None else db_did.tenant_uuid
        )
        db.commit()
        db.refresh(db_did)
    return db_did


def delete_did(db: Session, principal: Principal, did_id: int) -> DID:
    db_did = get_did(db, principal, did_id)
    if db_did is not None:
        db.delete(db_did)
        db.commit()
    return db_did
