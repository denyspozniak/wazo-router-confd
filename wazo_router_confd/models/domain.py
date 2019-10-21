# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .tenant import Tenant  # noqa


class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'id'),
        UniqueConstraint('tenant_id', 'domain'),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    domain = Column(String(64))
