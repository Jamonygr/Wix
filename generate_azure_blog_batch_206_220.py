"""
Generate Azure blog posts 206-220.

Uses the same Azure Updates style as the earlier generated batch and assigns
the shared Wix cover image used by the previous blog posts.
"""

import sys

sys.dont_write_bytecode = True

from generate_azure_blog_batch_106_205 import (  # noqa: E402
    ascii_clean,
    existing_local_context,
    fetch_news_items,
    news_post,
    news_title,
    parse_date,
    slugify,
    title_core,
    write_post,
)


START = 206
COUNT = 15
COMMON_COVER_IMAGE = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"


def select_news_items(count):
    used_ids, local_text = existing_local_context()
    selected = []
    skipped = []

    for item in fetch_news_items():
        item_id = str(item.get("id", "")).strip()
        official_title = ascii_clean(item.get("title", ""))
        core = title_core(official_title)

        if not item_id or item_id in used_ids:
            skipped.append((item_id, "source id", official_title))
            continue

        if not official_title or official_title.lower().startswith("test"):
            skipped.append((item_id, "empty/test", official_title))
            continue

        if core and len(core) > 8 and core in local_text:
            skipped.append((item_id, "local core phrase", official_title))
            continue

        selected.append(item)
        if len(selected) == count:
            break

    if len(selected) < count:
        raise RuntimeError(f"Only found {len(selected)} usable Azure news items.")

    return selected, skipped


def main():
    selected, skipped = select_news_items(COUNT)
    written = []

    for offset, item in enumerate(selected):
        number = START + offset
        post = news_post(item)
        post["coverImage"] = COMMON_COVER_IMAGE

        slug = slugify(post["title"])
        written.append(write_post(number, slug, post))

    print(f"Generated {len(written)} blog files.")
    print(f"News posts: {START}-{START + COUNT - 1}")
    print(f"Skipped existing/local Azure update candidates: {len(skipped)}")
    for path, item in zip(written, selected):
        print(
            f"  {path.name}: {item.get('id')} | {parse_date(item.get('modified'))} | "
            f"{news_title(item)}"
        )


if __name__ == "__main__":
    main()
