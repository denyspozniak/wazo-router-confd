# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class IPBX(BaseModel):
    id: int
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    username: Optional[constr(max_length=50)] = None
    password: Optional[constr(max_length=192)] = None
    password_ha1: Optional[constr(max_length=64)] = None

    class Config:
        orm_mode = True


class IPBXRead(BaseModel):
    id: int
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    username: Optional[constr(max_length=50)] = None

    class Config:
        orm_mode = True


class IPBXCreate(BaseModel):
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    username: Optional[constr(max_length=50)] = None
    password: Optional[constr(max_length=192)] = None
    password_ha1: Optional[constr(max_length=64)] = None


class IPBXUpdate(BaseModel):
    tenant_id: int
    domain_id: int
    customer: Optional[int] = None
    ip_fqdn: str
    port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    username: Optional[str] = None
    password: Optional[str] = None
    password_ha1: Optional[str] = None
