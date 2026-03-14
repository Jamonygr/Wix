"""
Blog Post 31: Log Analytics Retry Bin GA
"""

BLOG_POST = {
    "title": "Log Analytics Gets a Save Button: Retry Bin Is Now GA",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Ops teams, this one fixes a real pain point. Microsoft announced on **March 12, 2026** that **manual Retry bin support for Log Analytics summary rules is now generally available**.

If you run summary rules to batch-aggregate data and re-ingest it into custom tables, a failed bin can leave holes in your dataset. Before this update, cleanup could get messy fast. Now there is a cleaner move.

## What Changed

Summary rules in Log Analytics workspace now support **manual Retry bin**.

That means you can re-run a **specific failed time bin** instead of redefining the rule, rebuilding tables, or replaying a larger chunk of data than you actually need.

The retry uses a `retryBinStartTime` value while keeping the existing rule settings intact, including:

- Query
- Bin size
- Destination table
- Rule configuration

## Why It Matters

This is one of those quiet platform upgrades that saves serious operational time.

- **Fewer data gaps** when a single batch window fails.
- **Less rework** because you do not need to rebuild the whole summary flow.
- **Cleaner operations** for teams using Log Analytics as an input for reporting, alerting, or downstream analytics.

If your dashboards or detections depend on summarized tables, this turns a painful recovery into a targeted fix.

## Where It Helps Most

Retry bin is especially useful when:

- You run scheduled summary rules on large datasets.
- You depend on summarized tables for cost or security analytics.
- You need a precise remediation path for auditability.

Instead of treating every failed bin like a mini disaster, you can now handle it like a normal maintenance task.

## What To Do Next

1. Review existing summary rules in your Log Analytics workspaces.
2. Update your runbooks to include bin-level retry steps.
3. Test the recovery flow in a non-production workspace before you need it for real.

## The Bottom Line

Retry bin is not flashy, but it is exactly the kind of feature mature Azure teams want. Better recovery, less rebuild work, and tighter control over summarized data pipelines.

That is a solid GA.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Azure Monitor Log Analytics summary rules now support manual Retry bin in general availability, letting teams re-run failed time bins without rebuilding rules or tables.",

    "publish": True,

    "tags": ["Azure", "Azure Monitor", "Log Analytics", "Observability", "Operations", "Cloud"]
}
