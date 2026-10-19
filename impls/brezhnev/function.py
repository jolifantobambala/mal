from dataclasses import dataclass, field

from env import Env

import typing as t

@dataclass
class Function:
    ast: any
    params: list
    env: Env
    fn: t.Callable
