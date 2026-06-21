"""
Generate Azure blog posts 266-280.

Uses the Azure Updates feed, skips local and live Wix duplicates, and assigns
the same shared Wix cover image used by the previous blog posts.
"""

import sys

sys.dont_write_bytecode = True

from generate_azure_blog_batch_251_265 import (  # noqa: E402
    COMMON_COVER_IMAGE,
    news_post,
    news_title,
    parse_date,
    select_news_items,
    slugify,
    write_post,
)


START = 266
COUNT = 15


def main():
    selected, skipped, live_count = select_news_items(COUNT)
    written = []

    for offset, item in enumerate(selected):
        number = START + offset
        post = news_post(item)
        post["coverImage"] = COMMON_COVER_IMAGE

        slug = slugify(post["title"])
        written.append(write_post(number, slug, post))

    print(f"Generated {len(written)} blog files.")
    print(f"News posts: {START}-{START + COUNT - 1}")
    print(f"Live Wix titles checked: {live_count}")
    print(f"Skipped existing/local/live Azure update candidates: {len(skipped)}")
    for path, item in zip(written, selected):
        print(
            f"  {path.name}: {item.get('id')} | {parse_date(item.get('modified'))} | "
            f"{news_title(item)}"
        )


if __name__ == "__main__":
    main()
