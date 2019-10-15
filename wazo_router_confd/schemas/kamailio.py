# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from wazo_router_confd.schemas import ipbx as ipbx_schema


class RoutingRequest(BaseModel):
    event: Optional[str] = None
    source_ip: Optional[str] = None
    source_port: Optional[int] = None
    call_id: Optional[str] = None
    from_name: Optional[str] = None
    from_uri: str
    from_tag: Optional[str] = None
    to_uri: str
    to_name: Optional[str] = None
    to_tag: Optional[str] = None


class CDRRequest(BaseModel):
    event: Optional[str] = None
    source_ip: Optional[str] = None
    source_port: Optional[int] = None
    call_id: Optional[str] = None
    from_uri: str
    to_uri: str
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class AuthRequest(BaseModel):
    source_ip: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class AuthResponse(BaseModel):
    success: bool
    ipbx: Optional[ipbx_schema.IPBXRead]
