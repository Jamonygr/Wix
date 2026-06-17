"""
Blog Post 72: Terraform Zero-Trust App Service Guide
Supporting diagram lives in portfolio_guides/terraform_azure_app_service_zero_trust/assets.
"""

BLOG_POST = {
    "title": "Terraforming a Zero-Trust Azure App Service Platform with Front Door, Private Link, and Key Vault",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Most App Service examples are good enough to get a demo online and bad enough to create work for your future self.

The app is public by default. Secrets end up in settings. DNS gets handled last. Private dependencies arrive later and force a redesign.

This guide takes the opposite approach and builds the platform as if production actually matters.

## What This Pattern Solves

The target design is simple to explain and strong in practice.

**Azure Front Door Premium** is the public edge.

**Azure App Service** is the application platform.

**Private Link** protects the origin path.

**VNet integration** handles outbound access to private dependencies.

**Managed identity** removes credential sprawl.

**Key Vault references** keep secrets out of raw app settings.

**Azure Monitor and Application Insights** give operators proof that the platform is healthy.

## The First Rule: Inbound And Outbound Are Different Problems

Private endpoint protects inbound traffic to the app.

VNet integration controls outbound traffic from the app.

They are not interchangeable, and Microsoft documents that they must not share the same subnet.

That means your Terraform should reflect that separation directly.

## Terraform Layout Matters More Than People Admit

A serious implementation should separate reusable platform concerns into modules:

**network**

**app_service**

**key_vault**

**frontdoor**

**monitoring**

That structure is not just aesthetic. It reduces the blast radius of changes and makes environment promotion far less messy.

## The App Service Resource Is Not The Whole Story

Creating a Linux web app in Terraform is the easy part.

The important part is how you configure it.

You want:

**system-assigned managed identity enabled at creation time**

**TLS tightened**

**VNet integration declared**

**Application Insights connected**

**Key Vault references used for secrets**

That combination turns App Service from a generic hosting target into a governed application platform.

## DNS Is What Makes Private Endpoint Real

A lot of cloud diagrams make private endpoint look like a checkbox.

It is not a checkbox. It is a DNS dependency.

If your platform does not correctly handle:

**privatelink.azurewebsites.net**

**privatelink.vaultcore.azure.net**

then the architecture is only correct on a whiteboard.

That is why Terraform should manage the private DNS zones, virtual network links, and private endpoint zone groups together.

## Front Door Premium Is The Public Edge You Actually Want

If the application is public, it should be public through one controlled edge.

That is the role of **Azure Front Door Premium** in this pattern.

It gives you:

**global entry**

**TLS termination**

**WAF policy**

**routing**

**Private Link support to App Service**

The rollout sequence matters:

1. Build Front Door.
2. Validate the private origin path.
3. Only then tighten or disable direct public app access.

Do not reverse that order unless you want to create your own incident.

## Monitoring Has To Be In Terraform Too

A platform is not complete because it deployed.

A platform is complete when operators can see:

**request failures**

**latency**

**dependency issues**

**WAF events**

**secret access failures**

That is why Application Insights, Log Analytics, and diagnostic settings belong in the same Terraform story as the network and the app.

## Why This Is A Strong Portfolio Piece

This guide works well in a portfolio because it proves you can do more than deploy resources.

It shows that you understand:

**network boundaries**

**identity-first design**

**secret hygiene**

**public edge hardening**

**operational visibility**

That is the difference between infrastructure that exists and infrastructure that can survive contact with reality.

The deep version of this guide, with architecture asset and code snippets, is included in this repository under **portfolio_guides/terraform_azure_app_service_zero_trust**.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "A deep Terraform guide for building a zero-trust Azure App Service platform with Front Door Premium, Private Link, VNet integration, managed identity, Key Vault references, and observability.",
    "publish": False,
    "tags": ["Azure", "Terraform", "Azure App Service", "Azure Front Door", "Private Link", "Key Vault", "Managed Identity", "Architecture"]
}
