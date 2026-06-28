"""
Blog Post 27: AKS Azure Linux 2.0 Retirement Timeline
"""

BLOG_POST = {
    "title": "AKS Alert: Azure Linux 2.0 Retirement Clock Hits March 31, 2026",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """AKS operators, this is your hard deadline. Azure Linux 2.0 is officially on the retirement path, and the clock runs out on **March 31, 2026**.

Here is the timeline you cannot ignore.

## The Timeline

- **November 30, 2025**: Support ended and security updates stopped.
- The node image is frozen at **202512.06.0**.
- **March 31, 2026**: Azure Linux 2.0 node images will be removed and you will no longer be able to scale node pools.

## What It Means

If Azure Linux 2.0 is still in your cluster, you are riding on a frozen image with a firm removal date. Past March 31, scaling is blocked and risk goes up fast.

## The Escape Plan

Microsoft recommends migrating by:

- Upgrading node pools to a supported Kubernetes version, or
- Moving to **osSku AzureLinux3**

Do this before the deadline so you are not forced into a high-stress emergency migration.

## Quick Checklist

1. Inventory clusters using Azure Linux 2.0.
2. Validate app compatibility with AzureLinux3.
3. Run test upgrades in dev or staging.
4. Schedule production upgrades well before March 31, 2026.

## The Bottom Line

This is a real deadline with real impact. If you operate AKS, now is the time to migrate. The neon grid does not wait for anyone.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "AKS will remove Azure Linux 2.0 node images starting March 31, 2026, after support ended November 30, 2025. Migrate node pools to AzureLinux3 or a supported Kubernetes version now.",

    "publish": True,

    "tags": ["Azure", "AKS", "Kubernetes", "Azure Linux", "Infrastructure", "Operations"]
}
