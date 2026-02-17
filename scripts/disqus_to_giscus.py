#!/usr/bin/env python3
"""
Import Disqus XML export comments into GitHub Discussions for giscus.

Default behavior:
- Parses Disqus export (.xml or .xml.gz; local file only)
- Maps each Disqus thread URL to a pathname title for giscus mapping=pathname
- Creates one Discussion per pathname (if missing)
- Imports comments/replies into that Discussion
- Adds marker comments so repeated runs don't duplicate imported comments
- Skips paths not found in current Hugo content unless --include-unmatched is set

Usage (dry-run first):
  python3 scripts/disqus_to_giscus.py \
    --export /path/to/disqus.xml.gz \
    --repo shrektan/shrektan_blog \
    --repository-id MDEwOlJlcG9zaXRvcnkxMTkyNDkyNTU= \
    --category-id DIC_kwDOBxuZZ84C2pup \
    --content-dir /Users/shrektan/dev/shrektan_blog/content \
    --dry-run
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


NS = {"d": "http://disqus.com", "dsq": "http://disqus.com/disqus-internals"}
MARKER_RE = re.compile(r"<!--\s*disqus-post-id:(\d+)\s*-->")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", required=True, help="Local Disqus export (.xml or .xml.gz)")
    ap.add_argument("--repo", required=True, help="owner/name")
    ap.add_argument("--repository-id", required=True, help="GraphQL repository node ID (repoID from giscus)")
    ap.add_argument("--category-id", required=True, help="GraphQL discussion category node ID (categoryID from giscus)")
    ap.add_argument("--content-dir", default="", help="Local Hugo content dir (e.g. .../content)")
    ap.add_argument("--include-unmatched", action="store_true", help="Import paths not found in current content map")
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args()


def load_export_root(path: str) -> ET.Element:
    raw = Path(path).read_bytes()
    if path.endswith(".gz"):
        raw = gzip.decompress(raw)
    return ET.fromstring(raw)


def parse_disqus(root: ET.Element):
    threads: dict[str, dict[str, str]] = {}
    for t in root.findall("d:thread", NS):
        tid = t.attrib.get("{http://disqus.com/disqus-internals}id")
        if not tid:
            continue
        threads[tid] = {
            "link": (t.findtext("d:link", default="", namespaces=NS) or "").strip(),
            "title": (t.findtext("d:title", default="", namespaces=NS) or "").strip(),
        }

    posts_by_thread: dict[str, list[dict[str, str]]] = defaultdict(list)
    for p in root.findall("d:post", NS):
        if (p.findtext("d:isDeleted", default="false", namespaces=NS) or "").lower() == "true":
            continue
        if (p.findtext("d:isSpam", default="false", namespaces=NS) or "").lower() == "true":
            continue

        post_id = p.attrib.get("{http://disqus.com/disqus-internals}id")
        if not post_id:
            continue

        thread_ref = p.find("d:thread", NS)
        if thread_ref is None:
            continue
        thread_id = thread_ref.attrib.get("{http://disqus.com/disqus-internals}id")
        if not thread_id:
            continue

        parent = p.find("d:parent", NS)
        parent_id = None if parent is None else parent.attrib.get("{http://disqus.com/disqus-internals}id")

        author = p.find("d:author", NS)
        author_name = "Unknown"
        author_username = ""
        if author is not None:
            author_name = (author.findtext("d:name", default="Unknown", namespaces=NS) or "Unknown").strip()
            author_username = (author.findtext("d:username", default="", namespaces=NS) or "").strip()

        message_el = p.find("d:message", NS)
        parts: list[str] = []
        if message_el is not None:
            if message_el.text and message_el.text.strip():
                parts.append(message_el.text)
            for ch in list(message_el):
                parts.append(ET.tostring(ch, encoding="unicode"))
        message = "".join(parts).strip()

        created_at = (p.findtext("d:createdAt", default="", namespaces=NS) or "").strip()
        posts_by_thread[thread_id].append(
            {
                "post_id": post_id,
                "parent_id": parent_id or "",
                "author_name": author_name,
                "author_username": author_username,
                "created_at": created_at,
                "message": message,
            }
        )

    for tid in posts_by_thread:
        posts_by_thread[tid].sort(key=lambda x: x["created_at"])
    return threads, posts_by_thread


def build_live_path_index(content_dir: str):
    live_paths: set[str] = set()
    by_date: dict[str, list[str]] = defaultdict(list)
    if not content_dir:
        return live_paths, by_date

    root = Path(content_dir)
    for p in root.glob("post/*/index.md"):
        txt = p.read_text(encoding="utf-8", errors="replace")
        mdate = re.search(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?\s*$", txt, flags=re.M)
        mslug = re.search(r"^slug:\s*['\"]?([^\n'\"]+)['\"]?\s*$", txt, flags=re.M)
        if not (mdate and mslug):
            continue
        date = mdate.group(1)
        y, mo, d = date.split("-")
        slug = mslug.group(1).strip()
        path = f"/post/{y}/{mo}/{d}/{slug}/"
        live_paths.add(path)
        by_date[date].append(path)

    # Common single pages
    live_paths.add("/about/")
    live_paths.add("/")
    return live_paths, by_date


def normalize_path(link: str, live_paths: set[str], by_date: dict[str, list[str]], include_unmatched: bool) -> str | None:
    path = urllib.parse.urlparse(link).path or "/"
    if not path.startswith("/"):
        path = "/" + path
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    if not path.endswith("/"):
        path += "/"

    # Already in target style
    if re.match(r"^/post/\d{4}/\d{2}/\d{2}/[^/]+/$", path):
        if (not live_paths) or (path in live_paths) or include_unmatched:
            return path
        return None

    # Legacy style /YYYY-MM-DD-slug/
    seg = path.strip("/").split("/")[-1]
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})-(.+)$", seg)
    if m:
        y, mo, d, slug = m.groups()
        date = f"{y}-{mo}-{d}"
        cand = f"/post/{y}/{mo}/{d}/{slug}/"
        if not live_paths or cand in live_paths:
            return cand
        # If only one post on that date, use canonical path even if slug changed in history.
        if len(by_date.get(date, [])) == 1:
            return by_date[date][0]
        return cand if include_unmatched else None

    if (not live_paths) or (path in live_paths) or include_unmatched:
        return path
    return None


def gql(token: str, query: str, variables: dict):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        payload = json.loads(r.read().decode("utf-8"))
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def list_discussions(token: str, owner: str, name: str, category_id: str):
    q = """
    query($owner:String!, $name:String!, $categoryId:ID!, $after:String) {
      repository(owner:$owner, name:$name) {
        discussions(first:100, after:$after, categoryId:$categoryId, orderBy:{field:CREATED_AT, direction:ASC}) {
          nodes { id title url }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
    """
    out = {}
    after = None
    while True:
        data = gql(token, q, {"owner": owner, "name": name, "categoryId": category_id, "after": after})
        conn = data["repository"]["discussions"]
        for n in conn["nodes"]:
            out[n["title"]] = n
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
    return out


def list_existing_markers(token: str, discussion_id: str):
    q = """
    query($id:ID!, $after:String) {
      node(id:$id) {
        ... on Discussion {
          comments(first:100, after:$after) {
            nodes {
              id
              body
              replies(first:100) { nodes { id body } }
            }
            pageInfo { hasNextPage endCursor }
          }
        }
      }
    }
    """
    out = {}
    after = None
    while True:
        data = gql(token, q, {"id": discussion_id, "after": after})
        conn = data["node"]["comments"]
        for n in conn["nodes"]:
            m = MARKER_RE.search(n["body"] or "")
            if m:
                out[m.group(1)] = n["id"]
            for r in n.get("replies", {}).get("nodes", []):
                m2 = MARKER_RE.search(r["body"] or "")
                if m2:
                    out[m2.group(1)] = r["id"]
        if not conn["pageInfo"]["hasNextPage"]:
            break
        after = conn["pageInfo"]["endCursor"]
    return out


def create_discussion(token: str, repository_id: str, category_id: str, title: str, body: str):
    m = """
    mutation($repositoryId:ID!, $categoryId:ID!, $title:String!, $body:String!) {
      createDiscussion(input:{repositoryId:$repositoryId, categoryId:$categoryId, title:$title, body:$body}) {
        discussion { id title url }
      }
    }
    """
    data = gql(token, m, {"repositoryId": repository_id, "categoryId": category_id, "title": title, "body": body})
    return data["createDiscussion"]["discussion"]


def add_comment(token: str, discussion_id: str, body: str, reply_to_id: str | None):
    m = """
    mutation($discussionId:ID!, $body:String!, $replyToId:ID) {
      addDiscussionComment(input:{discussionId:$discussionId, body:$body, replyToId:$replyToId}) {
        comment { id url }
      }
    }
    """
    data = gql(token, m, {"discussionId": discussion_id, "body": body, "replyToId": reply_to_id})
    return data["addDiscussionComment"]["comment"]


def comment_body(post: dict[str, str]) -> str:
    who = post["author_name"]
    if post["author_username"]:
        who += f" (@{post['author_username']})"
    message = post["message"] or "(empty)"
    return (
        f"<!-- disqus-post-id:{post['post_id']} -->\n"
        f"**Imported from Disqus**\n\n"
        f"- Author: {who}\n"
        f"- Original time: `{post['created_at']}`\n\n"
        f"---\n\n"
        f"{message}"
    )


def main():
    args = parse_args()
    owner, name = args.repo.split("/", 1)

    root = load_export_root(args.export)
    threads, posts_by_thread = parse_disqus(root)
    live_paths, by_date = build_live_path_index(args.content_dir)

    posts_by_path: dict[str, list[dict[str, str]]] = defaultdict(list)
    thread_meta_by_path: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    skipped: dict[str, int] = defaultdict(int)

    for tid, posts in posts_by_thread.items():
        meta = threads.get(tid, {})
        path = normalize_path(meta.get("link", ""), live_paths, by_date, args.include_unmatched)
        if not path:
            skipped[meta.get("link", "")] += len(posts)
            continue
        posts_by_path[path].extend(posts)
        thread_meta_by_path[path].append((tid, meta.get("link", ""), meta.get("title", "")))

    for p in posts_by_path.values():
        p.sort(key=lambda x: x["created_at"])

    total_comments = sum(len(v) for v in posts_by_path.values())
    print(f"Paths with comments: {len(posts_by_path)}")
    print(f"Comments to import: {total_comments}")
    if skipped:
        print(f"Skipped comments (unmatched paths): {sum(skipped.values())}")
        for link, cnt in list(sorted(skipped.items(), key=lambda kv: -kv[1]))[:20]:
            print(f"  - {cnt} : {link}")

    if args.dry_run:
        for path, arr in sorted(posts_by_path.items(), key=lambda kv: kv[0]):
            print(f"DRY-RUN {path}: {len(arr)} comments")
        return

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required for migration run.")

    discussions = list_discussions(token, owner, name, args.category_id)

    created = 0
    imported = 0
    for path, comments in sorted(posts_by_path.items(), key=lambda kv: kv[0]):
        disc = discussions.get(path)
        if not disc:
            thread_lines = "\n".join(
                f"- thread `{tid}`: {link} ({title})" for tid, link, title in thread_meta_by_path[path]
            )
            body = (
                "Imported from Disqus for giscus pathname mapping.\n\n"
                f"Pathname: `{path}`\n\n"
                f"Source threads:\n{thread_lines}\n"
            )
            disc = create_discussion(token, args.repository_id, args.category_id, path, body)
            discussions[path] = disc
            created += 1
            print(f"Created discussion: {path}")
        else:
            print(f"Using existing discussion: {path}")

        marker_map = list_existing_markers(token, disc["id"])
        disqus_to_gh = dict(marker_map)

        for post in comments:
            pid = post["post_id"]
            if pid in disqus_to_gh:
                continue
            parent_id = post["parent_id"] or ""
            reply_to = disqus_to_gh.get(parent_id) if parent_id else None
            c = add_comment(token, disc["id"], comment_body(post), reply_to)
            disqus_to_gh[pid] = c["id"]
            imported += 1

    print(f"Done. Created discussions: {created}, imported new comments: {imported}")


if __name__ == "__main__":
    main()
