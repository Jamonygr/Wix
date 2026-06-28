"""
Blog Post 37: MSSQL VS Code Query Profiler Preview
"""

BLOG_POST = {
    "title": "VS Code Gets Query Vision: MSSQL Query Profiler Enters Public Preview",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Database performance tuning just moved closer to where developers already work. On **March 11, 2026**, Microsoft announced a **public preview** of **Query Profiler in the MSSQL extension for Visual Studio Code**.

If you build against Azure SQL Database or SQL Server and hate bouncing between editor and monitoring tools, this update is aimed right at you.

## What Changed

The MSSQL extension now includes **Query Profiler**, which brings real-time visibility into database activity directly inside VS Code.

Microsoft says the feature can help you:

- Capture live query and database activity
- Identify slow operations
- Spot performance bottlenecks during development
- Review active sessions and execution details

It is powered by **Extended Events**, which matters because it keeps the monitoring path relatively low overhead.

## Why It Matters

Most database performance issues get found in one tool and fixed in another. That split slows everything down.

With Query Profiler inside VS Code, developers can stay closer to the code, query, and connection flow they already use.

- **Faster feedback loops**
- **Better visibility while testing changes**
- **Less context switching**

That is the kind of improvement developers actually feel every day.

## What It Supports

Microsoft calls out support for:

- **Azure SQL Database**
- **SQL Server** on-premises
- **SQL Server** in private or public cloud environments

That broad support makes the preview more practical for mixed estates.

## What To Do Next

1. Update the MSSQL extension in a development environment.
2. Use Query Profiler on a known query-heavy workflow.
3. Compare the experience with your current profiling path.

If the preview helps your team catch bad query behavior earlier, it is already doing useful work.

## The Bottom Line

Query Profiler in VS Code is a smart move from Microsoft. It shortens the gap between writing SQL-connected code and understanding what the database is actually doing.

That is a developer-grade update.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "The MSSQL extension for Visual Studio Code now includes Query Profiler in public preview, giving developers real-time database insight for Azure SQL Database and SQL Server without leaving the editor.",

    "publish": True,

    "tags": ["Azure", "Azure SQL", "Visual Studio Code", "MSSQL", "Developer Tools", "Performance"]
}
