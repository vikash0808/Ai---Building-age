"""Safe parsing and setpoint modification utilities for EnergyPlus .idf files."""

from pathlib import Path
import re
from typing import List, Tuple

_COOLING_BLOCK_RE = re.compile(
    r"(Schedule:Compact\s*,[^;]*?(?:Cool|Clg)[^;]*?;)",
    flags=re.IGNORECASE | re.DOTALL,
)


def load_idf(path: str) -> str:
    """Load an EnergyPlus .idf file as UTF-8 text."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"IDF file not found: {file_path}")
    return file_path.read_text(encoding="utf-8", errors="ignore")


def save_idf(path: str, content: str) -> Path:
    """Write modified IDF content to disk, creating parent directories if needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def extract_cooling_setpoints(idf_text: str) -> List[str]:
    """Extract numeric cooling setpoint values found inside cooling Schedule:Compact blocks."""
    values: List[str] = []
    for block in _COOLING_BLOCK_RE.findall(idf_text):
        for match in re.finditer(r"Until:\s*\d{1,2}:\d{2}\s*,\s*(\d+(?:\.\d+)?)\s*[,;]", block, flags=re.IGNORECASE):
            values.append(match.group(1))
    return values


def replace_cooling_setpoint_with_count(
    idf_text: str,
    old_value: str,
    new_value: str,
) -> Tuple[str, int]:
    """Replace a cooling setpoint value only inside cooling Schedule:Compact blocks.

    Returns a tuple of (updated_idf_text, replacement_count) so unrelated values
    such as building geometry coordinates, dates, or timestamps are never corrupted.
    """
    old_str = str(old_value).strip()
    new_str = str(new_value).strip()
    if not old_str or not new_str:
        raise ValueError("Both old_value and new_value must be non-empty.")

    token_re = re.compile(
        rf"(?<![A-Za-z0-9_.:/-]){re.escape(old_str)}(?=\s*[,;])"
    )
    total_replacements = 0

    def _replace_in_block(match: re.Match) -> str:
        nonlocal total_replacements
        block = match.group(1)
        updated_block, count = token_re.subn(new_str, block)
        total_replacements += count
        return updated_block

    updated_text = _COOLING_BLOCK_RE.sub(_replace_in_block, idf_text)
    return updated_text, total_replacements


def replace_cooling_setpoint(idf_text: str, old_value: str, new_value: str) -> str:
    """Backward-compatible helper returning only the updated IDF text."""
    updated_text, _ = replace_cooling_setpoint_with_count(idf_text, old_value, new_value)
    return updated_text
