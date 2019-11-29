# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock
import pprint

from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata

from wazo_router_confd import database
from wazo_router_confd.models.base import Base

from .common import temporary_database


def test_database_migration():
    with temporary_database() as uri:
        config = dict(database_uri=uri)

        app = mock.Mock()
        app = database.setup_database(app, config)
        try:
            database.upgrade_database(app, config, force_migration=True)
            with app.engine.begin() as conn:
                ctx = MigrationContext.configure(conn)
                diff = compare_metadata(ctx, Base.metadata)
                assert diff == [], pprint.pformat(diff, indent=2, width=20)
        finally:
            app.engine.dispose()
