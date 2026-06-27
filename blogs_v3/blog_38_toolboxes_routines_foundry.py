"""
Blog Post 38: Toolboxes and Routines in Microsoft Foundry - Narrative Style with Image
"""

BLOG_POST = {
    "title": "Toolboxes and Routines Give Agents a Playbook: Foundry Connects Discovery to Execution",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "sourceUrl": "https://devblogs.microsoft.com/foundry/toolbox-build-26/",
    "sourceDate": "2026-06-03",

    "content": """Agents become useful when they can do more than talk. They need tools, procedures, permissions, and reliable ways to turn intent into action. Microsoft's Foundry updates around toolboxes and routines focus on exactly that execution layer, where agentic AI leaves the chat window and enters business workflow.

Toolboxes give agents access to capabilities in a more organized way. Instead of every agent being wired manually to every API, tools can be packaged, discovered, and reused. That improves consistency and makes it easier to govern what agents are allowed to do.

Routines add another important layer: repeatable process. Many business tasks are not single API calls. They are sequences of steps with checks, decisions, and handoffs. A routine can encode that structure so an agent follows an approved path rather than improvising every time.

This is where enterprise agent design starts to look like platform engineering. Teams define reusable capabilities, safe execution paths, and policies. Agents then operate inside those boundaries. The result is more scalable than a collection of one-off assistants with custom integrations.

The discovery-to-execution idea is especially powerful. An agent should be able to understand what tools exist, choose the right one, and execute a routine that matches the task. That requires metadata, governance, and orchestration, not just clever prompting.

For Azure AI teams, the message is clear: build the agent toolbox before expecting agents to transform work. The better the tools and routines, the more dependable the agent. Foundry is giving that execution layer more shape.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Microsoft Foundry toolboxes and routines help agents discover approved capabilities and execute repeatable business workflows with stronger governance.",

    "publish": True,

    "tags": ["Microsoft Foundry", "Toolboxes", "Routines", "Agentic AI", "Workflow Automation"]
}

