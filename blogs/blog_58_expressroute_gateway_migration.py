"""
Blog Post 58: ExpressRoute Gateway Migration
"""

BLOG_POST = {
    "title": "ExpressRoute Gateway Migration Is Underway: Check Your Azure Network Before Microsoft Does It For You",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Microsoft shared guidance in **March 2026** for a **Microsoft-initiated migration** of certain **ExpressRoute gateways** away from **Basic SKU public IP** dependencies.

## What Is Happening

Azure is upgrading impacted ExpressRoute gateways in the backend to use **Microsoft-managed Standard SKU public IP** behavior.

The migration window Microsoft documented runs between **March 7, 2026 and April 30, 2026** for affected gateways.

## Why You Should Care

Any networking change handled by the platform is still your problem if your environment assumptions are wrong.

This matters if you have:

**Legacy firewall expectations**

**Strict route or dependency assumptions**

**Poor documentation around gateway configuration**

## What To Verify

1. Check whether your gateway is flagged for migration in the Azure portal.
2. Review any monitoring, automation, or access rules tied to the current public IP behavior.
3. Validate failover and connectivity paths before the migration window closes.
4. Make sure the network team actually knows this change is happening.

## Why This Update Is Good

The old Basic SKU pattern has been overdue for cleanup. Standardized, Microsoft-managed behavior is a healthier long-term state.

Still, every platform cleanup creates risk for customers who built brittle assumptions around the old setup.

## Bottom Line

If your hybrid connectivity is important, do not treat this like background noise. Read the migration notice, verify your gateway status, and remove surprises before Azure removes them for you.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "Microsoft is migrating affected ExpressRoute gateways between March 7 and April 30, 2026. Azure network teams should verify portal notices and gateway assumptions now.",
    "publish": True,
    "tags": ["Azure", "ExpressRoute", "Networking", "Hybrid Cloud", "Operations", "Migration"]
}
