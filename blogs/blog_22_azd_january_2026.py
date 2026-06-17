"""
Blog Post 22: Azure Developer CLI January 2026
"""

BLOG_POST = {
    "title": "Azure Developer CLI January 2026: Config Control, Faster Loops, and Clean Breaks",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Azd fans, cue the neon glow. The January 2026 Azure Developer CLI release is all about tighter configuration control, smoother auth, and faster daily loops. If you build apps on Azure, these updates make your workflow feel more like a game cheat code than a chore.

Here is the quick tour of what changed in the 1.23.x release train.

## Config Gets a Command Center

The CLI adds new config management commands so you can view and update global settings cleanly. There is also new support for environment configuration, plus the ability to remove environments without manual cleanup.

The result: fewer mystery configs and a clearer mental model of how azd is shaping your projects.

## Cross-Tenant Auth for Remote State

If you manage remote state across tenants, azd now supports cross-tenant authentication. That is a big deal for enterprise teams juggling subscriptions and identity boundaries.

## Extension Updates and Podman Fallback

Two quality-of-life wins:

- **Extension update notifications** keep your toolchain current.
- **Podman fallback** kicks in when Docker is missing, so devs can keep moving.

## Performance and Cleanup

The release brings file-based caching and other performance improvements. It also removes deprecated commands and drops Azure Spring Apps support, which is a clean break to keep the tool lean.

## How to Use It

- **Upgrade azd** and review new config commands right away.
- **Validate cross-tenant flows** if your state lives outside your primary tenant.
- **Update internal docs** to reflect removed commands and Spring Apps changes.

## The Bottom Line

Azd keeps evolving into the smoothest way to ship Azure apps. January 2026 puts configuration and speed front and center, with a few smart breaking changes that simplify the long-term path.

Faster loops, clearer configs, and fewer surprises. That is the kind of release we like.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Azure Developer CLI 1.23.x adds new config management, environment config support, cross-tenant auth for remote state, and performance upgrades, while removing deprecated commands for a cleaner workflow.",

    "publish": True,

    "tags": ["Azure", "Azure Developer CLI", "azd", "DevOps", "Developer Tools", "Cloud"]
}
