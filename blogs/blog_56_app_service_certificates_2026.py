"""
Blog Post 56: Azure App Service Certificate Changes 2026
"""

BLOG_POST = {
    "title": "Azure App Service Certificate Changes in 2026: What You Need to Fix Before Traffic Breaks",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Microsoft updated guidance on **February 17, 2026** for industry-wide certificate changes affecting **Azure App Service Managed Certificates** and **App Service Certificates**.

## What Changed

The update is tied to broader CA and compliance changes, not a random Azure-only tweak.

Microsoft says customers should expect:

**New certificate chains** rolling into service.

**Shorter certificate validity periods** for some scenarios.

**No client authentication EKU support** for these App Service certificates going forward.

## Why This Matters

If you have certificate pinning anywhere in the stack, this is the kind of platform update that turns into a painful outage.

If you are using these certificates for mutual TLS or any workflow that depends on client authentication behavior, you need to review that design now instead of later.

## What To Check

1. Review every app using App Service Managed Certificates or paid App Service Certificates.
2. Remove certificate pinning where it exists.
3. Validate whether any service is relying on client authentication EKU behavior.
4. Test the new chain in lower environments before the rollout reaches production.

## The Real Takeaway

This is not a flashy Azure launch. It is an operational update with real blast radius if ignored.

The teams that handle this well will treat it like platform hygiene: inventory, validate, update, move on.

The teams that wait for a broken endpoint to remind them will have a much worse week.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "Microsoft's February 17, 2026 guidance on Azure App Service certificate changes means teams should review pinning, chain trust, and any client-auth assumptions now.",
    "publish": True,
    "tags": ["Azure", "Azure App Service", "Certificates", "Security", "Operations", "Cloud Computing"]
}
