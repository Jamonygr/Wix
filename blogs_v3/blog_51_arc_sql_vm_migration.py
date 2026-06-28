"""
Blog Post 51: Azure Arc SQL Server VM Migration Target - Narrative Style with Image
"""

BLOG_POST = {
    "title": "Azure Arc Adds SQL Server on Azure VMs as a Migration Target: More Paths for Database Modernization",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "sourceUrl": "https://azure.microsoft.com/updates?id=560805",
    "sourceDate": "2026-04-22",

    "content": """Database migration is rarely one-size-fits-all. Some workloads are ready for platform services, some need specific instance-level control, and some require a staged move before deeper modernization can happen.

Azure Arc migration now supports SQL Server on Azure Virtual Machines as a public preview migration target. That expands the path for Arc-enabled SQL Server instances beyond Azure SQL Managed Instance and into SQL Server running on Azure infrastructure.

This is useful because SQL Server estates are often full of nuance. Legacy applications, third-party dependencies, custom server settings, and operational requirements can make a VM-based landing zone the right first step.

The key benefit is workflow consistency. Teams can use a unified Azure Arc migration experience while choosing the target that fits the workload. That helps avoid splitting migration planning across too many unrelated tools.

It also supports a more realistic modernization journey. Moving to SQL Server on Azure VMs can reduce datacenter dependency now, while leaving room to modernize further later when application constraints are better understood.

For Azure migration teams, this preview is a reminder that modernization is not only about the most cloud-native target. It is about giving every workload a safe next step.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Azure Arc migration now previews SQL Server on Azure VMs as a migration target, giving SQL Server estates another practical modernization path.",

    "publish": True,

    "tags": ["Azure", "Azure Arc", "SQL Server", "Migration", "Databases"]
}

