# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class CarrierTrunk(BaseModel):
    id: int
    carrier_id: int
    name: constr(max_length=256)
    sip_proxy: constr(max_length=128)
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None
    auth_password: Optional[constr(max_length=192)] = None
    realm: Optional[constr(max_length=64)] = None
    registrar_proxy: Optional[constr(max_length=128)] = None
    from_domain: Optional[constr(max_length=64)] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkRead(BaseModel):
    id: int
    carrier_id: int
    name: constr(max_length=256)
    sip_proxy: constr(max_length=128)
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None
    realm: Optional[constr(max_length=64)] = None
    registrar_proxy: Optional[constr(max_length=128)] = None
    from_domain: Optional[constr(max_length=64)] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkCreate(BaseModel):
    carrier_id: int
    name: str
    sip_proxy: str
    sip_proxy_port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30


class CarrierTrunkUpdate(BaseModel):
    name: constr(max_length=256)
    sip_proxy: constr(max_length=128)
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None
    auth_password: Optional[constr(max_length=192)] = None
    realm: Optional[constr(max_length=64)] = None
    registrar_proxy: Optional[constr(max_length=128)] = None
    from_domain: Optional[constr(max_length=64)] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30
