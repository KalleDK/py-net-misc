from __future__ import annotations

import builtins
from typing import Any, cast

import pytest

from net_misc.macaddress import MacFormat, get_pydantic_core_schema


def test_get_pydantic_core_schema_requires_pydantic_core(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def reject_pydantic_core(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name == "pydantic_core":
            raise ImportError("pydantic_core unavailable")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", reject_pydantic_core)

    with pytest.raises(RuntimeError, match="pydantic_core is required"):
        get_pydantic_core_schema(MacFormat.COLON, bytes, cast(Any, None))
