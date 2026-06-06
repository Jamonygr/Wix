"""
Blog Post 81: Azure Kubernetes Fleet Manager Cross-Cluster Networking
"""

BLOG_POST = {
    "title": "Azure Kubernetes Fleet Manager Adds Cross-Cluster Networking Preview",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Microsoft announced on **May 22, 2026** the public preview of **cross-cluster networking for Azure Kubernetes Fleet Manager**.

This is a big deal for teams running more than one AKS cluster.

## What It Does

The preview uses Cilium-based networking and Advanced Container Networking Services to connect workloads across clusters.

The goal is to make services and workloads communicate across cluster boundaries as if they were local, while still preserving cluster isolation and governance.

Microsoft calls out several key capabilities:

**seamless east-west connectivity**

**global service discovery**

**multi-cluster observability**

**unified security and governance**

**zero-touch lifecycle management**

## Why This Matters

Multi-cluster Kubernetes is common for resilience, regional placement, compliance, and blast-radius control.

But networking across clusters has historically been painful.

Teams end up with VPNs, gateways, manual service discovery, and a pile of operational complexity.

If Azure can make cross-cluster networking feel native, that removes a real platform tax.

## My Take

This is exactly the kind of Kubernetes feature that matters more in production than it does in a slide deck.

Single clusters are easy to talk about.

Fleets are where platform engineering gets serious.

Networking, observability, identity, and policy all have to follow the workload.

## Bottom Line

Cross-cluster networking for Azure Kubernetes Fleet Manager is still preview, so test carefully.

But the direction is strong.

Azure is making AKS fleet operations feel less like a custom networking project and more like a managed platform capability.

That is where enterprise Kubernetes needs to go.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "Azure Kubernetes Fleet Manager added public preview support for Cilium-based cross-cluster networking, improving service discovery, observability, governance, and resilience across AKS fleets.",
    "publish": True,
    "tags": ["Azure", "AKS", "Azure Kubernetes Fleet Manager", "Kubernetes", "Networking", "Cilium", "Preview"]
}
