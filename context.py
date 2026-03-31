from dataclasses import dataclass
from typing import Optional

import click

from client import DropscanClient


@dataclass
class AppContext:
    client: DropscanClient
    scanbox_id: Optional[int] = None

    def require_scanbox(self) -> int:
        if self.scanbox_id is None:
            raise click.ClickException("No scanbox selected. Run 'scanbox select <id>' first.")
        return self.scanbox_id
