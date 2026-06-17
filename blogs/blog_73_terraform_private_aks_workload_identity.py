"""
Blog Post 73: Terraform Private AKS Workload Identity Guide
Supporting diagram lives in portfolio_guides/terraform_azure_private_aks_workload_identity/assets.
"""

BLOG_POST = {
    "title": "Terraforming a Private AKS Platform with Workload Identity, Key Vault, and ACR",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """AKS gets a lot more interesting when you stop treating the cluster as the product and start treating the platform around it as the real work.

Anyone can stand up a cluster.

The hard part is getting networking, identity, secret access, and image supply to work together without creating a maintenance problem.

## What This Guide Builds

The target pattern is a private Azure Kubernetes Service platform built with Terraform.

It includes:

**private cluster networking**

**OIDC issuer enabled**

**Microsoft Entra Workload ID**

**Azure Key Vault provider for the Secrets Store CSI Driver**

**Azure Container Registry**

That combination is what makes the platform useful for real application teams.

## Private Cluster Means More Than One Boolean

Turning on private cluster is the easy line in Terraform.

The real platform design work is around what that decision implies.

You now care much more about:

**private DNS ownership**

**network paths**

**subscription boundaries**

**cluster identity**

That means the networking and identity model should be decided before the first production apply, not after.

## Workload Identity Is The Core Security Story

The most important design decision in this guide is to use **Microsoft Entra Workload ID** for workload access to Azure resources.

Instead of storing secrets for Azure access inside Kubernetes, the pod uses a projected service account token, the AKS OIDC issuer provides the trust anchor, and Entra exchanges that token for an Azure token.

That is a cleaner model than legacy pod identity patterns and much better than static credentials.

## Terraform Should Own The Azure Side Of The Trust

The infrastructure side needs to declare:

**the user-assigned managed identity**

**the role assignments**

**the federated identity credential**

Those pieces define which Kubernetes service account is allowed to act as which Azure identity.

That is not just an implementation detail. It is the control plane for workload-to-cloud trust.

## Secrets Store CSI Driver Makes The Pattern Practical

Workload identity becomes much more compelling when you connect it to a real secret retrieval story.

With the Azure Key Vault provider for the Secrets Store CSI Driver, applications can mount secrets from Key Vault without embedding credentials in their manifests.

That gives you:

**central secret management**

**better rotation practices**

**less credential sprawl**

**cleaner separation between platform and application responsibilities**

The key point is that the service account, the federated identity credential, the managed identity, and the `SecretProviderClass` all have to agree. If one of those pieces is wrong, the platform fails in a way that looks mysterious until you understand the chain.

## Container Registry Is Part Of The Platform, Not An Afterthought

If the cluster cannot pull images reliably, the platform is incomplete.

That is why the guide includes **Azure Container Registry** and an explicit `AcrPull` assignment for the AKS kubelet identity.

This is simple, but it belongs in the same article because a deep platform guide should connect:

**cluster deployment**

**workload authentication**

**secret access**

**image supply**

## Why This Makes A Strong Portfolio Piece

This is a strong Azure portfolio article because it shows you understand the hard parts of AKS:

**private control plane**

**federated workload trust**

**Key Vault integration**

**registry access**

**platform guardrails**

That reads like someone who can build AKS for application teams, not just someone who can follow a quickstart.

The deep version of this guide, with architecture diagram and code snippets, is included in this repository under **portfolio_guides/terraform_azure_private_aks_workload_identity**.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "A deep Terraform guide for building a private AKS platform with OIDC, Microsoft Entra Workload ID, Key Vault CSI integration, and Azure Container Registry.",
    "publish": False,
    "tags": ["Azure", "Terraform", "AKS", "Kubernetes", "Workload Identity", "Key Vault", "ACR", "Platform Engineering"]
}
