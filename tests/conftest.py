import sys
from pathlib import Path

import pytest
import yaml

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BUNDLE_ROOT / "src" / "store_ops" / "lib"))
sys.path.insert(0, str(BUNDLE_ROOT / "src" / "store_ops" / "pipelines" / "sales_medallion"))


@pytest.fixture(scope="session")
def bundle_root() -> Path:
    return BUNDLE_ROOT


@pytest.fixture(scope="session")
def root_config(bundle_root) -> dict:
    return yaml.safe_load((bundle_root / "databricks.yml").read_text())


@pytest.fixture(scope="session")
def resource_files(bundle_root) -> dict[Path, dict]:
    files = {}
    for path in sorted((bundle_root / "resources").rglob("*.yml")):
        files[path.relative_to(bundle_root)] = yaml.safe_load(path.read_text()) or {}
    return files


@pytest.fixture(scope="session")
def jobs(resource_files) -> dict[str, tuple[Path, dict]]:
    found = {}
    for path, cfg in resource_files.items():
        for key, job in (cfg.get("resources", {}).get("jobs") or {}).items():
            found[key] = (path, job)
    return found
