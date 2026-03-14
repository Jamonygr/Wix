"""
Blog Post 34: PostgreSQL Grafana Dashboards GA
"""

BLOG_POST = {
    "title": "Grafana Lands in the Portal: PostgreSQL Dashboards Are Now GA",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Monitoring PostgreSQL on Azure just got a lot less annoying. Microsoft announced on **March 11, 2026** that **Azure Database for PostgreSQL dashboards with Grafana are now generally available**.

The headline is simple: richer visibility, directly in the Azure portal, without standing up a separate Grafana deployment first.

## What Changed

Azure now offers **built-in Grafana dashboards** for Azure Database for PostgreSQL through native Azure Monitor integration.

That gives you fast access to prebuilt views for metrics like:

- CPU usage
- Storage consumption
- Active connections
- Query throughput

Microsoft also highlights the ability to correlate metrics with PostgreSQL logs and use **Grafana Explore** when you need to dig deeper.

## Why It Matters

This is a strong quality-of-life upgrade for platform and database teams.

- **No separate Grafana instance to manage**
- **Faster troubleshooting** when a query spike or performance dip shows up
- **Shared visibility** across ops, app, and database teams

The practical question shifts from "How do we wire this up?" to "What does the data say right now?"

## Where It Helps

This feature is especially useful when:

- You support multiple PostgreSQL environments
- You need quick health checks during incidents
- You want a common dashboard language across teams

Built-in dashboards do not replace every custom observability pattern, but they remove a lot of setup friction for the core cases.

## What To Do Next

1. Open the new dashboards in the Azure portal for a production-like server.
2. Validate which default charts answer your daily ops questions.
3. Save and share customized versions for your team if needed.

If you already use Azure Monitor heavily, this is an easy win to adopt.

## The Bottom Line

PostgreSQL teams want visibility without platform overhead, and this GA update moves Azure in the right direction. Native Grafana dashboards in the portal mean faster answers, fewer moving parts, and a better day-two experience.

That is a clean upgrade.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Azure Database for PostgreSQL now offers built-in Grafana dashboards in general availability, bringing portal-native performance visibility and easier troubleshooting through Azure Monitor.",

    "publish": True,

    "tags": ["Azure", "PostgreSQL", "Grafana", "Azure Monitor", "Observability", "Databases"]
}
