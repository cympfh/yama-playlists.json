#!/usr/bin/env python3
import json
import urllib.request
from urllib.parse import parse_qs, urlparse

import click


def extract_video_id(url: str) -> str | None:
    if not url:
        return None
    try:
        p = urlparse(url)
        if "youtube.com" in p.netloc or "youtu.be" in p.netloc:
            qs = parse_qs(p.query)
            if "v" in qs and qs["v"]:
                return qs["v"][0]
            if p.netloc.endswith("youtu.be") and p.path:
                return p.path.lstrip("/")
        return None
    except Exception:
        return None


def normalize_url(url: str) -> str:
    vid = extract_video_id(url)
    if vid:
        return f"https://www.youtube.com/watch?v={vid}"
    return url


def fetch_title(vid: str) -> str:
    oembed = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(oembed, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("title", "") or ""
    except Exception:
        return ""


@click.command()
@click.option(
    "--input",
    "-i",
    default="playlists.json",
    type=click.Path(exists=True, dir_okay=False),
    help="input json",
)
@click.option(
    "--output",
    "-o",
    default="playlists.norm.json",
    type=click.Path(dir_okay=False),
    help="output json",
)
def main(input: str, output: str) -> None:
    with open(input, encoding="utf-8") as f:
        data = json.load(f)

    filled = 0
    for playlist in data.get("playlists", []):
        for track in playlist.get("Tracks", []):
            url = track.get("Url", "")
            new_url = normalize_url(url)
            track["Url"] = new_url

            title = (track.get("Title") or "").strip()
            if not title:
                vid = extract_video_id(new_url)
                if vid:
                    new_title = fetch_title(vid)
                    if new_title:
                        track["Title"] = new_title
                        filled += 1
                        click.echo(f"filled: {new_title}")
                    # else leave empty

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    click.echo(f"done: {filled} titles filled -> {output}")


if __name__ == "__main__":
    main()
