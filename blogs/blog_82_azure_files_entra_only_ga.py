"""
Blog Post 82: Azure Files Entra-Only Identities GA
"""

BLOG_POST = {
    "title": "Azure Files Entra-Only Identities Hit GA and Cut the Domain Controller Dependency",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Microsoft announced on **May 19, 2026** that **Entra-Only identities for Azure Files SMB** are generally available.

That is a meaningful storage and identity update.

## What It Does

Azure Files SMB can now use native Microsoft Entra ID authentication for cloud-only identities.

That means organizations can grant secure, identity-based access to file shares without depending on:

**Active Directory**

**hybrid sync**

**managed domain controllers**

**VPN-heavy access patterns**

Microsoft also highlighted portal-based NTFS permissions management and expanded authorization support for Entra-only users and groups.

## Why This Matters

File shares are often where cloud-native identity dreams go to get complicated.

SMB compatibility is useful, but old identity assumptions can drag on-premises dependencies into otherwise modern Azure designs.

This update gives teams a cleaner path for Azure Files, especially for Azure Virtual Desktop and FSLogix profile scenarios.

## My Take

This is not flashy, but it is important.

Identity simplification is infrastructure modernization.

Every domain controller, sync path, and legacy dependency you can remove is less operational drag and less security surface.

## Bottom Line

Azure Files Entra-Only identities going GA is a practical Zero Trust improvement.

If you are using Azure Files for VDI, app data, or Windows workloads, this is worth reviewing.

The best cloud updates are sometimes the ones that quietly remove entire categories of old architecture pain.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "Azure Files Entra-Only identities are generally available for SMB, enabling cloud-native identity-based access without Active Directory, hybrid sync, or managed domain controllers.",
    "publish": True,
    "tags": ["Azure", "Azure Files", "Microsoft Entra ID", "Storage", "Zero Trust", "SMB", "Azure Virtual Desktop"]
}
