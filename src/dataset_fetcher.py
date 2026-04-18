import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


def _build_page_url(base_url: str, limit: int, offset: int) -> str:
    query = urlencode({"$limit": limit, "$offset": offset})
    separator = "&" if urlparse(base_url).query else "?"
    return f"{base_url}{separator}{query}"


def _request_page(page_url: str, retries: int = 4, timeout: int = 60) -> bytes:
    headers = {"User-Agent": "doc-patterns-lab4/1.0"}
    request = Request(page_url, headers=headers)

    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=timeout) as response:  # nosec B310
                return response.read()
        except HTTPError as error:
            should_retry = error.code >= 500 and attempt < retries
            if should_retry:
                time.sleep(2 ** attempt)
                continue
            raise
        except URLError:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise

    raise RuntimeError("Failed to fetch Socrata page after retries.")


def download_socrata_csv(url: str, output_path: Path, page_size: int = 50000) -> None:
    """Download a Socrata dataset as CSV with pagination and save to a local file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(f"{output_path.suffix}.tmp")

    first_page = True
    offset = 0

    with temp_path.open("wb") as target:
        while True:
            page_url = _build_page_url(url, page_size, offset)
            payload = _request_page(page_url)

            if not payload.strip():
                break

            lines = payload.splitlines(keepends=True)
            if not lines:
                break

            if first_page:
                target.writelines(lines)
                first_page = False
            else:
                target.writelines(lines[1:])

            if len(lines) <= 1:
                break

            row_count = len(lines) - 1
            if row_count < page_size:
                break

            offset += page_size

    temp_path.replace(output_path)
