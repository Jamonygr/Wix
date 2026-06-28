"""
Blog Post 35: PostgreSQL CMK Premium SSD v2 Preview
"""

BLOG_POST = {
    "title": "PostgreSQL Locks It Down: Customer-Managed Keys on Premium SSD v2 Enter Preview",

    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",

    "content": """Security-conscious database teams have a new option on the board. On **March 11, 2026**, Microsoft announced a **public preview** for **customer-managed encryption keys on Premium SSD v2 disks for Azure Database for PostgreSQL**.

This one is about stronger control over data-at-rest encryption without giving up the performance profile of Premium SSD v2.

## What Changed

Azure Database for PostgreSQL can now use **customer-managed keys (CMKs)** with **Premium SSD v2** storage in public preview.

Your keys live in **Azure Key Vault**, giving you more direct control over encryption policy while Azure continues handling the managed database service itself.

## Why It Matters

For regulated industries and stricter internal governance models, encryption control is never just a checkbox.

- **Customer-controlled keys** improve separation of duties.
- **Key rotation and access policy control** can align with internal standards.
- **Premium SSD v2 performance** remains available for demanding workloads.

That combination matters because security teams do not want to trade away performance, and engineering teams do not want compliance to slow everything down.

## Who Should Care

This preview is especially relevant for:

- Financial services and healthcare workloads
- Teams with strict audit or compliance requirements
- PostgreSQL deployments already using Key Vault-backed security patterns

If your organization requires proof that encryption keys are under customer control, this preview closes an important gap.

## What To Do Next

1. Check whether your PostgreSQL workloads already rely on Premium SSD v2.
2. Review your Azure Key Vault standards for key lifecycle and access.
3. Pilot the preview in a non-production environment with compliance stakeholders involved early.

Preview features still need validation, but the direction here is strong.

## The Bottom Line

Customer-managed keys on Premium SSD v2 make Azure Database for PostgreSQL more credible for tightly governed workloads. It is a focused update, but one with real enterprise weight.

Security teams should pay attention.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",

    "excerpt": "Azure Database for PostgreSQL now supports customer-managed encryption keys on Premium SSD v2 disks in public preview, improving control over data-at-rest encryption for regulated workloads.",

    "publish": True,

    "tags": ["Azure", "PostgreSQL", "Security", "Encryption", "Key Vault", "Premium SSD v2"]
}
