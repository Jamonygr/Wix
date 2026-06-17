"""
Blog Post 21: Azure SDK January 2026 Release
"""

BLOG_POST = {
    "title": "Azure SDK January 2026: Foundry Agents, Search Facets, and Neon-Grade Dev Power",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Slide in on a synthwave baseline, developers. The January 2026 Azure SDK release just dropped, and it is one of those updates that quietly changes what you can build. If you are working with agents, search, or modern AI workflows, this release is all signal.

Below is the fast breakdown of what matters most and how to put it to work.

## AI Foundry 1.2.0-beta.1 for .NET

The .NET SDK for AI Foundry lights up with agent-first capabilities. The January drop adds support for the Foundry Agents Service plus deeper project wiring with `Azure.AI.Projects.OpenAI`.

Key upgrades include:

- **Agents Service support** to build real multi-step agent workflows.
- **Integration with Azure.AI.Projects.OpenAI** for simpler setup and project wiring.
- **Evaluation and insights** so you can measure agent behavior, not just output.
- **Red teaming and schedules** to automate testing and recurring runs.

If you are moving from prototype to production, this is the SDK shape you have been waiting for.

## Azure AI Search 11.8.0-beta.1 for .NET

Search gets stronger and more analytic. The SDK now targets the `2025-11-01-preview` service version and adds capability you will notice immediately.

Highlights:

- **Facet aggregation types** like `avg`, `min`, `max`, and `cardinality` for better metrics.
- **New knowledge source types**: `web`, `remoteSharePoint`, `indexedSharePoint`, and `indexedOneLake`.
- **Support for new Azure OpenAI models** including `gpt-5`, `gpt-5-mini`, and `gpt-5-nano`.
- **Renamed Knowledge Agent to Knowledge Base**, a breaking change to watch for.

If your RAG pipeline depends on richer sources or better analytics, this update is the lift you want.

## Other Dev Goodies

The release also includes a stable Functions extension for Azure Web PubSub for SocketIO (1.0.0) and ongoing management library improvements. These are the kind of small upgrades that keep production environments smooth and stable.

## How to Use This Drop

- **Pin beta packages** to a feature branch and test agent workflows end to end.
- **Audit breaking changes** before rolling into CI, especially Knowledge Agent to Knowledge Base.
- **Start with one pilot**: a search + agent workflow is the best way to feel the impact quickly.

## The Bottom Line

January 2026 is a serious SDK release for Azure. The Foundry and Search updates bring agentic development closer to real-world production, and the tooling upgrades reduce friction across the board.

Plug in, update, and ship something radical.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "The January 2026 Azure SDK release adds AI Foundry Agents support, richer Azure AI Search capabilities, and a stable Web PubSub SocketIO extension, unlocking faster agent-first development on Azure.",

    "publish": True,

    "tags": ["Azure", "Azure SDK", "AI Foundry", "Azure AI Search", ".NET", "Developer Tools"]
}
