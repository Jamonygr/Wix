"""
Blog Post 74: Terraform Hub-Spoke Firewall DNS Guide
Supporting diagram lives in portfolio_guides/terraform_azure_hub_spoke_firewall_dns/assets.
"""

BLOG_POST = {
    "title": "Terraforming a Hub-Spoke Azure Landing Zone with Firewall, Bastion, and DNS Private Resolver",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Hub-spoke is one of those Azure patterns that sounds simple until the first shared networking project starts colliding with DNS, routing, and ownership boundaries.

This guide is about doing that work properly with Terraform.

## What The Pattern Actually Needs

A real hub-spoke landing zone is not just:

**one hub**

**a few spokes**

**some peerings**

The deeper platform story includes:

**Azure Firewall for centralized egress control**

**Azure Bastion for controlled administration**

**Private DNS Resolver for centralized name resolution**

**route tables that make the intended traffic flow enforceable**

**a spoke onboarding model that can scale**

That is what turns hub-spoke from a diagram into an operating model.

## Address Planning Comes Before Terraform Elegance

Teams often want to jump straight into modules and `for_each`.

That is the wrong place to start.

The first real design step is deciding whether the IP plan leaves room for:

**Firewall subnets**

**Bastion**

**DNS resolver endpoints**

**future spokes**

If the address plan is bad, beautifully written Terraform only automates the bad decision.

## Centralized Egress Only Works If Routing Is Explicit

Azure Firewall in the hub is useful because it gives you a controlled point for egress policy.

But the firewall does not become the egress path just because it exists.

That only happens when route tables actually send traffic there.

This is one of the most important points in the whole guide:

**topology is not traffic policy**

**route tables are traffic policy**

## DNS Is Usually The Hardest Shared Service

Hub-spoke environments often look clean in diagrams and fail in practice because DNS got split across too many teams or too many ad hoc decisions.

That is where **Azure Private DNS Resolver** changes the story.

It gives the hub a stronger role in centralized name resolution for private Azure services and hybrid lookups.

Once that exists, spoke onboarding gets cleaner because the naming model is no longer reinvented by each workload team.

## Terraform Should Reflect Ownership Boundaries

A strong implementation usually separates:

**hub network**

**firewall policy**

**dns resolver**

**spoke virtual networks**

**peering**

That matters because shared connectivity stacks usually have a much longer lifecycle than application stacks. They need clearer change control and lower blast radius.

## Why This Is Good Portfolio Material

This kind of guide shows more than service familiarity.

It shows you understand:

**shared platform design**

**route intent**

**centralized control points**

**DNS as infrastructure**

**repeatable onboarding patterns**

That is exactly the kind of content that makes an Azure portfolio look more credible.

The deep version of this guide, with architecture diagram and Terraform snippets, is included in this repository under **portfolio_guides/terraform_azure_hub_spoke_firewall_dns**.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "A deep Terraform guide for designing a hub-spoke Azure landing zone with centralized egress, Azure Firewall, Bastion, Private DNS Resolver, and scalable spoke onboarding.",
    "publish": False,
    "tags": ["Azure", "Terraform", "Networking", "Hub and Spoke", "Azure Firewall", "DNS", "Landing Zone", "Architecture"]
}
