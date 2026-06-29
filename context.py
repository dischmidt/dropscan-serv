from dataclasses import dataclass
from typing import Optional

import click

from client import DropscanClient


@dataclass
class AppContext:
    client: DropscanClient
    scanbox_id: Optional[int] = None

    def resolve_scanbox(self, scanbox_id: int | None = None) -> int:
        if scanbox_id is not None:
            return scanbox_id
        return self.require_scanbox()

    def require_scanbox(self) -> int:
        if self.scanbox_id is None:
            raise click.ClickException(
                "No scanbox selected. Set DROPSCAN_SCANBOX, use --scanbox <id>, or run "
                "'scanbox select <id>' first."
            )
        return self.scanbox_id
