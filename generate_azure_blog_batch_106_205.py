"""
Generate Azure blog posts 106-205.

Creates 50 current Azure Updates posts from Microsoft's Release Communications
API, then 50 Azure how-to posts with Microsoft Learn source links.
"""

import argparse
import html
import pprint
import re
import textwrap
import unicodedata
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
BLOGS_DIR = ROOT / "blogs"
COVER_IMAGE = "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png"
AZURE_UPDATES_API = "https://www.microsoft.com/releasecommunications/api/v2/azure"
AZURE_UPDATES_URL = "https://azure.microsoft.com/updates"
NEWS_START = 106
NEWS_COUNT = 50
HOW_TO_START = 156
HOW_TO_COUNT = 50


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        if data:
            self.parts.append(data)

    def text(self):
        return " ".join(self.parts)


def ascii_clean(value):
    value = html.unescape(str(value or ""))
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2122": " TM",
        "\u00ae": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def strip_html(value):
    parser = TextExtractor()
    parser.feed(value or "")
    return ascii_clean(parser.text())


def normalize(value):
    value = ascii_clean(value).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def title_core(title):
    text = normalize(title)
    prefixes = [
        "generally available",
        "general availability",
        "public preview",
        "private preview",
        "retirement",
        "update",
        "announcing",
        "preview",
    ]
    changed = True
    while changed:
        changed = False
        for prefix in prefixes:
            if text.startswith(prefix + " "):
                text = text[len(prefix) :].strip()
                changed = True
    return text


def remove_title_prefix(title):
    title = ascii_clean(title)
    for prefix in [
        "Generally Available:",
        "General Availability:",
        "Public Preview:",
        "Private Preview:",
        "Retirement:",
        "Update:",
        "Announcing:",
        "Preview:",
    ]:
        if title.lower().startswith(prefix.lower()):
            return title[len(prefix) :].strip()
    return title


def shorten(value, limit=92):
    value = ascii_clean(value)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rsplit(" ", 1)[0] + "..."


def slugify(value):
    value = normalize(value)
    value = re.sub(r"\b(azure|microsoft|generally|available|public|preview|update)\b", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    slug = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return slug[:72].strip("_") or "azure_update"


def paragraph(value):
    return textwrap.fill(ascii_clean(value), width=92)


def sentence_summary(value, max_sentences=2):
    text = strip_html(value)
    if not text:
        return "Microsoft published this Azure update as part of the current Azure Updates feed."
    parts = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(parts[:max_sentences]).strip()
    return shorten(summary, 480)


def parse_date(value):
    if not value:
        return "June 2026"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%B %d, %Y")
    except ValueError:
        return value[:10]


def existing_local_context():
    used_ids = set()
    local_text = []
    for path in BLOGS_DIR.glob("blog_*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        used_ids.update(re.findall(r"azure\.microsoft\.com/updates\?id=([A-Za-z0-9_-]+)", text))
        local_text.append(normalize(text))
    return used_ids, " ".join(local_text)


def fetch_news_items():
    params = {
        "$count": "true",
        "includeFacets": "true",
        "top": "260",
        "skip": "0",
        "orderby": "modified desc",
    }
    response = requests.get(AZURE_UPDATES_API, params=params, timeout=45)
    response.raise_for_status()
    return response.json().get("value", [])


def select_news_items():
    used_ids, local_text = existing_local_context()
    selected = []
    skipped = []
    for item in fetch_news_items():
        item_id = str(item.get("id", "")).strip()
        official_title = ascii_clean(item.get("title", ""))
        core = title_core(official_title)
        if not item_id or item_id in used_ids:
            skipped.append((item_id, "source id", official_title))
            continue
        if not official_title or official_title.lower().startswith("test"):
            skipped.append((item_id, "empty/test", official_title))
            continue
        if core and len(core) > 8 and core in local_text:
            skipped.append((item_id, "local core phrase", official_title))
            continue
        selected.append(item)
        if len(selected) == NEWS_COUNT:
            break

    if len(selected) < NEWS_COUNT:
        raise RuntimeError(f"Only found {len(selected)} usable Azure news items.")

    return selected, skipped


def status_phrase(item):
    title = ascii_clean(item.get("title", ""))
    status = ascii_clean(item.get("status", "")) or "Published"
    if title.lower().startswith("retirement:"):
        return "a retirement notice"
    if status.lower() == "launched":
        return "a generally available update"
    if "preview" in status.lower():
        return "a preview update"
    if "development" in status.lower():
        return "an early access update"
    return "an Azure update"


def news_title(item):
    official = ascii_clean(item.get("title", ""))
    subject = shorten(remove_title_prefix(official), 82)
    lower = official.lower()
    if lower.startswith("retirement:"):
        return shorten(f"{subject} Retirement: What Azure Teams Should Check", 118)
    if lower.startswith("public preview:"):
        return shorten(f"{subject} Enters Public Preview for Azure Teams", 118)
    if lower.startswith("private preview:"):
        return shorten(f"{subject} Enters Private Preview on Azure", 118)
    if lower.startswith(("generally available:", "general availability:")):
        return shorten(f"{subject} Reaches GA for Azure Operations", 118)
    if lower.startswith("update:"):
        return shorten(f"{subject} Update: What Changed for Azure Teams", 118)
    if lower.startswith("preview:"):
        return shorten(f"{subject} Preview: What Cloud Engineers Should Know", 118)
    return shorten(official, 118)


def news_tags(item):
    tags = ["Azure", "Azure Updates"]
    for value in item.get("products", [])[:3]:
        value = ascii_clean(value)
        if value and value not in tags:
            tags.append(value)
    for value in item.get("tags", [])[:2]:
        value = ascii_clean(value)
        if value and value not in tags:
            tags.append(value)
    status = ascii_clean(item.get("status", ""))
    if status and status not in tags:
        tags.append(status)
    return tags[:8]


def news_content(item):
    official_title = ascii_clean(item.get("title", ""))
    subject = remove_title_prefix(official_title)
    modified = parse_date(item.get("modified"))
    products = ", ".join(ascii_clean(p) for p in item.get("products", [])[:4]) or "Azure"
    categories = ", ".join(ascii_clean(p) for p in item.get("productCategories", [])[:3]) or "cloud operations"
    summary = sentence_summary(item.get("description"))
    update_url = f"{AZURE_UPDATES_URL}?id={item.get('id')}"
    status = status_phrase(item)

    body = f"""
Microsoft listed **{official_title}** as {status}, last modified on **{modified}**.

The affected product area is **{products}**, with the update sitting under **{categories}** in the Azure Updates feed.

{summary}

## What Changed?

This update is about **{subject}**.

For Azure teams, the important point is not just the announcement label. The important point is whether this changes a supported design, a migration plan, a security baseline, an operations checklist, or a roadmap decision.

When Microsoft publishes an update in this feed, I treat it as a signal to check real environments instead of just reading the headline.

## Why It Matters

Cloud estates get complicated because small platform changes stack up.

A new GA feature can remove a workaround. A preview can become a good lab candidate. A retirement notice can turn into a production risk if nobody owns the migration. A billing or management change can surprise teams that assumed the old behavior would stay forever.

This is why Azure updates need an owner.

Someone should translate each relevant item into an action: test it, ignore it, adopt it, document it, or put it on a retirement backlog.

## Who Should Care

Platform engineers should care because shared Azure standards need to track supported capabilities.

Operations teams should care because changes in **{products}** can affect monitoring, incident response, automation, and runbooks.

Security and governance teams should care if the update changes access, auditability, network exposure, data handling, or compliance posture.

Application owners should care when the feature touches deployment paths, runtime behavior, availability, or cost.

## Practical Cloud Engineer Takeaway

Start by checking whether your tenant actually uses the product area named in this update.

If it does, identify the subscriptions, resource groups, and workloads that depend on it.

Then decide whether this is an immediate change, a planning item, or a watch-list item.

For previews, keep the test in a non-production environment unless Microsoft states otherwise.

For GA updates, review whether the new capability should be added to your standard architecture patterns.

For retirements, create a dated migration task and assign an owner.

## Real-World Example

Imagine a platform team that runs a monthly Azure review.

Instead of reading every update as trivia, the team filters the feed for services it actually operates, including **{products}**.

This item becomes a short decision record.

Does it affect production?

Does it change the build standard?

Does it require a proof of concept?

Does it need a customer communication?

That simple workflow turns Azure news into operational discipline.

## Possible Impact for Azure Operations

The operational impact depends on where **{subject}** sits in your environment.

If it is close to production traffic, identity, data, backup, networking, monitoring, or deployment automation, treat it seriously.

If it is not in use today, it may still be useful as a roadmap signal.

Either way, log the decision.

The worst outcome is not deciding at all and rediscovering the update during an outage, audit, migration, or renewal.

## Bottom Line

This Azure update is worth a quick review if your environment touches **{products}**.

Read the Microsoft source, map it to your estate, and turn it into a clear engineering decision.

That is how Azure news becomes useful instead of noisy.

## Sources

Microsoft Azure Updates: {update_url}

Microsoft Release Communications API: {AZURE_UPDATES_API}

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*
"""
    return textwrap.dedent(body).strip()


def news_post(item):
    title = news_title(item)
    subject = remove_title_prefix(ascii_clean(item.get("title", "")))
    return {
        "title": title,
        "coverImage": COVER_IMAGE,
        "content": news_content(item),
        "excerpt": shorten(
            f"Microsoft updated {subject}; here is what Azure teams should check, test, or document.",
            180,
        ),
        "publish": True,
        "tags": news_tags(item),
    }


HOW_TO_TOPICS = [
    {
        "slug": "virtual_network_subnets",
        "title": "How to Design an Azure Virtual Network with Subnets That Can Grow",
        "service": "Azure Virtual Network",
        "outcome": "a VNet layout with address space, dedicated subnets, and room for private endpoints, integration subnets, and future services",
        "steps": [
            "Start with an address range that does not overlap with on-premises, partner, or other cloud networks.",
            "Create separate subnets for application tiers, private endpoints, shared services, and delegated platform services.",
            "Reserve unused address space for future expansion instead of filling the VNet on day one.",
            "Attach route tables and network security groups only after you understand the traffic pattern.",
            "Document subnet ownership so teams know where new resources should and should not land.",
        ],
        "validate": "Check effective routes, confirm there is no address overlap, and test name resolution and connectivity from each subnet that will host workloads.",
        "guardrail": "Do not let every project create a one-off VNet. Standard networking patterns make later peering, inspection, DNS, and private connectivity much easier.",
        "docs": ["https://learn.microsoft.com/en-us/azure/virtual-network/quick-create-portal"],
        "tags": ["Azure", "Virtual Network", "Networking", "Subnets"],
    },
    {
        "slug": "network_security_groups",
        "title": "How to Use Network Security Groups Without Creating Rule Sprawl",
        "service": "Network Security Groups",
        "outcome": "a clean NSG pattern that allows required traffic and keeps deny-by-default thinking visible",
        "steps": [
            "Define the workload traffic matrix before writing rules.",
            "Use application security groups where they make ownership clearer.",
            "Keep inbound rules specific to source, destination, protocol, and port.",
            "Avoid broad Any-to-Any rules unless they are temporary and tracked.",
            "Review effective security rules from the NIC or subnet before blaming the application.",
        ],
        "validate": "Use effective security rules and Network Watcher connection troubleshoot to confirm that allowed flows work and blocked flows stay blocked.",
        "guardrail": "NSGs are not documentation by themselves. Keep a simple rule owner and purpose field in your change process.",
        "docs": ["https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview"],
        "tags": ["Azure", "NSG", "Networking", "Security"],
    },
    {
        "slug": "private_endpoint",
        "title": "How to Add a Private Endpoint to an Azure PaaS Service",
        "service": "Azure Private Link",
        "outcome": "a private network path to an Azure PaaS resource without exposing the service broadly to the public internet",
        "steps": [
            "Choose the target resource and confirm the supported private endpoint subresource.",
            "Create the private endpoint in a subnet reserved for private endpoints.",
            "Integrate the right private DNS zone for the service.",
            "Approve the private endpoint connection if the service requires manual approval.",
            "Test access from a VM, app, or container running inside the connected network.",
        ],
        "validate": "Resolve the service hostname from inside the VNet and confirm it returns the private endpoint IP instead of the public endpoint.",
        "guardrail": "Private endpoints solve inbound access to the service. They do not automatically fix DNS, routing, identity, or application authorization.",
        "docs": ["https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview"],
        "tags": ["Azure", "Private Link", "Private Endpoint", "Networking"],
    },
    {
        "slug": "private_dns_zones",
        "title": "How to Plan Private DNS Zones for Azure Private Link",
        "service": "Azure Private DNS",
        "outcome": "a DNS model that lets workloads resolve private endpoint names consistently across VNets",
        "steps": [
            "Identify the required privatelink zone for each Azure service.",
            "Create the private DNS zone in a shared networking subscription when possible.",
            "Link the zone to every VNet that needs to resolve the private endpoint.",
            "Avoid duplicate zones for the same service unless you have a clear split-brain design.",
            "Test resolution from each spoke VNet and from hybrid networks if forwarding is involved.",
        ],
        "validate": "Use nslookup or Resolve-DnsName from real workload networks and confirm the resolved address matches the private endpoint.",
        "guardrail": "Most Private Link outages are DNS problems wearing a networking mask. Treat DNS as core infrastructure.",
        "docs": ["https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns"],
        "tags": ["Azure", "Private DNS", "Private Link", "Networking"],
    },
    {
        "slug": "app_service_managed_identity",
        "title": "How to Enable Managed Identity for Azure App Service",
        "service": "Azure App Service",
        "outcome": "an App Service app that can authenticate to Azure resources without stored credentials",
        "steps": [
            "Enable a system-assigned managed identity on the web app.",
            "Grant that identity only the permissions it needs on the target resource.",
            "Update the application configuration to use identity-based authentication.",
            "Remove connection strings or secrets that are no longer needed.",
            "Log the identity object ID in deployment documentation for future audits.",
        ],
        "validate": "Restart the app, test the dependency call, and check the target service audit logs for the managed identity sign-in.",
        "guardrail": "Managed identity removes secrets from the app, but it does not remove the need for least privilege.",
        "docs": ["https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity"],
        "tags": ["Azure", "App Service", "Managed Identity", "Security"],
    },
    {
        "slug": "app_service_key_vault_references",
        "title": "How to Use Key Vault References in Azure App Service",
        "service": "Azure Key Vault",
        "outcome": "App Service settings that read secret values from Key Vault instead of storing secret material directly in the app configuration",
        "steps": [
            "Store the secret in Key Vault and choose whether the app should reference a specific version.",
            "Enable managed identity on the app.",
            "Grant the app identity permission to read the secret.",
            "Create the app setting with the Key Vault reference syntax.",
            "Restart or refresh the app configuration when testing secret rotation behavior.",
        ],
        "validate": "Confirm the app setting resolves at runtime and check Key Vault logs for secret get operations by the app identity.",
        "guardrail": "Key Vault references are cleaner than copied secrets, but teams still need a rotation and refresh process.",
        "docs": ["https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references"],
        "tags": ["Azure", "Key Vault", "App Service", "Secrets"],
    },
    {
        "slug": "front_door_private_link",
        "title": "How to Put Azure Front Door Premium in Front of a Private App Service Origin",
        "service": "Azure Front Door",
        "outcome": "a public edge with WAF and a private origin path to App Service",
        "steps": [
            "Create an Azure Front Door Premium profile and endpoint.",
            "Add the App Service origin and enable Private Link for the sites subresource.",
            "Approve the pending private endpoint connection on the App Service side.",
            "Route traffic through the origin group and configure health probes.",
            "Disable or restrict direct public access to the App Service origin after validation.",
        ],
        "validate": "Test the Front Door endpoint, confirm the origin is healthy, and verify the app is no longer reachable directly except through the approved path.",
        "guardrail": "Do not mix public and private origins in the same origin group. Keep the public edge and private origin model clean.",
        "docs": ["https://learn.microsoft.com/en-us/azure/frontdoor/private-link"],
        "tags": ["Azure", "Front Door", "Private Link", "App Service"],
    },
    {
        "slug": "front_door_waf",
        "title": "How to Roll Out Azure Front Door WAF Without Breaking Real Traffic",
        "service": "Azure Web Application Firewall",
        "outcome": "a WAF policy that starts in detection, gets tuned with evidence, and moves toward prevention safely",
        "steps": [
            "Create a WAF policy and attach managed rules that match the application risk profile.",
            "Start in detection mode so the team can observe rule matches.",
            "Send WAF logs to Log Analytics for review.",
            "Tune exclusions and custom rules with application owners.",
            "Move to prevention only after normal traffic has been reviewed.",
        ],
        "validate": "Review WAF logs for blocked or matched requests and test known safe requests through the application.",
        "guardrail": "WAF is not a set-and-forget checkbox. Rule tuning needs ownership and regular review.",
        "docs": ["https://learn.microsoft.com/en-us/azure/web-application-firewall/afds/afds-overview"],
        "tags": ["Azure", "WAF", "Front Door", "Security"],
    },
    {
        "slug": "aks_workload_identity",
        "title": "How to Use Workload Identity on Azure Kubernetes Service",
        "service": "Azure Kubernetes Service",
        "outcome": "AKS pods that access Azure resources through federated identity instead of static secrets",
        "steps": [
            "Enable the OIDC issuer and workload identity features on the AKS cluster.",
            "Create or choose a managed identity for the workload.",
            "Create a federated identity credential that maps the Kubernetes service account to the managed identity.",
            "Annotate the service account and deploy the workload with that service account.",
            "Grant the managed identity least-privilege access to the Azure resource.",
        ],
        "validate": "Check pod logs, token projection, and target resource audit logs to confirm the pod is using the expected identity.",
        "guardrail": "Do not grant one identity broad access for every namespace. Treat workload identity boundaries like application boundaries.",
        "docs": ["https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview"],
        "tags": ["Azure", "AKS", "Workload Identity", "Kubernetes"],
    },
    {
        "slug": "aks_node_pools",
        "title": "How to Plan AKS Node Pools for Mixed Workloads",
        "service": "Azure Kubernetes Service",
        "outcome": "an AKS cluster with node pools that separate system, user, and specialized workloads",
        "steps": [
            "Keep the system node pool dedicated to core cluster services.",
            "Create user node pools for application workloads.",
            "Use labels, taints, and tolerations to steer workloads intentionally.",
            "Add specialized pools for GPU, memory-heavy, or compliance-sensitive workloads.",
            "Review upgrade, autoscaling, and quota behavior per node pool.",
        ],
        "validate": "Inspect pod placement and simulate node pool scale or drain operations before calling the design production-ready.",
        "guardrail": "A single general-purpose node pool is easy at first and painful later. Separate noisy or sensitive workloads early.",
        "docs": ["https://learn.microsoft.com/en-us/azure/aks/create-node-pools"],
        "tags": ["Azure", "AKS", "Node Pools", "Kubernetes"],
    },
    {
        "slug": "container_apps_identity",
        "title": "How to Give Azure Container Apps a Managed Identity",
        "service": "Azure Container Apps",
        "outcome": "a container app that can call Azure services without embedding secrets in environment variables",
        "steps": [
            "Enable a system-assigned or user-assigned managed identity on the container app.",
            "Grant the identity the minimum role needed on the target Azure service.",
            "Update the app to use Azure SDK credential chaining or identity-aware configuration.",
            "Remove old secrets from the container app environment.",
            "Redeploy and verify identity access in the target service logs.",
        ],
        "validate": "Confirm the app can access the dependency and that no secret value remains in Container Apps configuration.",
        "guardrail": "Identity is part of the runtime contract. Document it beside ingress, scaling, and revision settings.",
        "docs": ["https://learn.microsoft.com/en-us/azure/container-apps/managed-identity"],
        "tags": ["Azure", "Container Apps", "Managed Identity", "Security"],
    },
    {
        "slug": "container_apps_custom_domain",
        "title": "How to Add a Custom Domain and Managed Certificate to Azure Container Apps",
        "service": "Azure Container Apps",
        "outcome": "a custom hostname on Container Apps with certificate management handled by Azure",
        "steps": [
            "Confirm the container app ingress is enabled.",
            "Create the required DNS record for the custom domain.",
            "Add the custom domain to the container app.",
            "Request or bind the managed certificate.",
            "Test HTTPS from outside the environment and monitor renewal status.",
        ],
        "validate": "Check DNS, certificate status, and browser TLS details for the custom hostname.",
        "guardrail": "Certificate automation still depends on correct DNS. Treat DNS change windows as part of the deployment.",
        "docs": ["https://learn.microsoft.com/en-us/azure/container-apps/custom-domains-managed-certificates"],
        "tags": ["Azure", "Container Apps", "TLS", "Custom Domain"],
    },
    {
        "slug": "functions_identity_connections",
        "title": "How to Use Identity-Based Connections in Azure Functions",
        "service": "Azure Functions",
        "outcome": "an Azure Functions app that connects to supported services using managed identity instead of connection secrets",
        "steps": [
            "Enable managed identity on the function app.",
            "Grant the identity the required role on the target service.",
            "Update the function app settings to use identity-based connection configuration.",
            "Deploy the function code with SDK or binding support for identity.",
            "Remove legacy connection strings after the identity path is tested.",
        ],
        "validate": "Invoke the function and check both function logs and the target service logs for the managed identity.",
        "guardrail": "Do not migrate all bindings at once. Convert one dependency, validate it, then continue.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-functions/functions-identity-based-connections-tutorial"],
        "tags": ["Azure", "Functions", "Managed Identity", "Serverless"],
    },
    {
        "slug": "blob_lifecycle_management",
        "title": "How to Configure Azure Blob Lifecycle Management",
        "service": "Azure Storage",
        "outcome": "a lifecycle policy that moves or deletes blobs based on age, tier, and business retention needs",
        "steps": [
            "Classify blob data by access pattern and retention requirement.",
            "Create lifecycle rules for hot, cool, cold, archive, or deletion actions.",
            "Scope rules by container or blob prefix when different data sets need different treatment.",
            "Test the policy on a narrow path before applying it broadly.",
            "Review storage metrics after the policy starts running.",
        ],
        "validate": "Check policy execution, blob tiers, and storage cost trends after the first full cycle.",
        "guardrail": "Lifecycle policies can save money, but a bad delete rule can remove data faster than the business expects.",
        "docs": ["https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"],
        "tags": ["Azure", "Storage", "Blob", "Lifecycle"],
    },
    {
        "slug": "azure_files_private_networking",
        "title": "How to Secure Azure Files with Private Networking",
        "service": "Azure Files",
        "outcome": "file shares that are reachable through controlled private network paths",
        "steps": [
            "Create or identify the storage account that hosts the file share.",
            "Disable broad public access when the migration plan allows it.",
            "Create a private endpoint for the file service.",
            "Configure the matching private DNS zone and VNet links.",
            "Test SMB or NFS access from the intended client network.",
        ],
        "validate": "Confirm the storage account file endpoint resolves privately and that clients can mount the share through the expected route.",
        "guardrail": "File access depends on identity, DNS, firewall rules, and client networking. Validate the full path.",
        "docs": ["https://learn.microsoft.com/en-us/azure/storage/files/storage-files-networking-overview"],
        "tags": ["Azure", "Azure Files", "Private Endpoint", "Storage"],
    },
    {
        "slug": "azure_sql_private_endpoint",
        "title": "How to Connect to Azure SQL Database Through Private Endpoint",
        "service": "Azure SQL Database",
        "outcome": "a private connection path to Azure SQL Database with DNS and firewall behavior understood",
        "steps": [
            "Create a private endpoint for the Azure SQL server.",
            "Integrate the privatelink.database.windows.net private DNS zone.",
            "Link the DNS zone to the VNets that host clients.",
            "Review public network access and firewall rules after private connectivity works.",
            "Update app connection tests to run from the real workload network.",
        ],
        "validate": "Resolve the SQL server hostname from the app network and confirm it returns the private endpoint address.",
        "guardrail": "Private endpoint changes the network path, not the database permission model. Keep authentication and authorization tight.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-sql/database/private-endpoint-overview"],
        "tags": ["Azure", "Azure SQL", "Private Endpoint", "Database"],
    },
    {
        "slug": "postgresql_high_availability",
        "title": "How to Plan High Availability for Azure Database for PostgreSQL Flexible Server",
        "service": "Azure Database for PostgreSQL",
        "outcome": "a PostgreSQL Flexible Server design with HA mode, zone choice, backups, and failover expectations documented",
        "steps": [
            "Choose whether zone-redundant or same-zone high availability fits the workload.",
            "Confirm the selected region and SKU support the required HA option.",
            "Plan maintenance windows, backup retention, and connection retry behavior.",
            "Test failover behavior with the application before production cutover.",
            "Document RTO, RPO, and operational owner expectations.",
        ],
        "validate": "Run a controlled failover test and measure how the application behaves during reconnect.",
        "guardrail": "Database HA is not complete until the application can tolerate failover and retry cleanly.",
        "docs": ["https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability"],
        "tags": ["Azure", "PostgreSQL", "High Availability", "Database"],
    },
    {
        "slug": "cosmos_db_serverless",
        "title": "How to Decide When Azure Cosmos DB Serverless Fits",
        "service": "Azure Cosmos DB",
        "outcome": "a practical decision framework for choosing serverless instead of provisioned throughput",
        "steps": [
            "Estimate request volume, storage, burst patterns, and latency expectations.",
            "Choose serverless for intermittent or unpredictable workloads that do not need reserved throughput.",
            "Use provisioned throughput when sustained high volume or predictable capacity is required.",
            "Test partition key design before focusing on pricing.",
            "Monitor request units and throttling after launch.",
        ],
        "validate": "Load test realistic access patterns and compare cost and throttling behavior against provisioned throughput.",
        "guardrail": "Serverless is a billing and capacity model, not a substitute for good partition design.",
        "docs": ["https://learn.microsoft.com/en-us/azure/cosmos-db/serverless"],
        "tags": ["Azure", "Cosmos DB", "Serverless", "Database"],
    },
    {
        "slug": "azure_monitor_alerts",
        "title": "How to Build Useful Azure Monitor Alerts",
        "service": "Azure Monitor",
        "outcome": "alerts that point to action instead of flooding the team with noise",
        "steps": [
            "Start with user-impacting symptoms, not every available metric.",
            "Create alert rules with clear severity and ownership.",
            "Route alerts to action groups that reach the right responders.",
            "Add runbook links or remediation notes to the alert description.",
            "Review fired alerts monthly and remove noisy rules.",
        ],
        "validate": "Trigger a controlled test alert and confirm routing, severity, message content, and responder ownership.",
        "guardrail": "An alert without an action is just background noise. Every production alert needs an expected response.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview"],
        "tags": ["Azure", "Azure Monitor", "Alerts", "Operations"],
    },
    {
        "slug": "log_analytics_queries",
        "title": "How to Start Writing Useful Log Analytics Queries",
        "service": "Azure Monitor Logs",
        "outcome": "KQL queries that answer operational questions from Log Analytics data",
        "steps": [
            "Start from the table that contains the signal you need.",
            "Use time filters first so the query stays fast.",
            "Project only the columns that help the investigation.",
            "Summarize by dimensions such as status code, resource, operation, or caller.",
            "Save useful queries where the team can reuse them during incidents.",
        ],
        "validate": "Run the query against known events and confirm the result matches what actually happened.",
        "guardrail": "Good queries start with a question. Do not build dashboards from random tables just because the data exists.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-query-overview"],
        "tags": ["Azure", "Log Analytics", "KQL", "Monitoring"],
    },
    {
        "slug": "application_insights",
        "title": "How to Use Application Insights for Real Application Troubleshooting",
        "service": "Application Insights",
        "outcome": "application telemetry that connects requests, dependencies, exceptions, and performance symptoms",
        "steps": [
            "Enable Application Insights for the application runtime.",
            "Confirm request, dependency, exception, and trace telemetry is flowing.",
            "Set cloud role names for multi-service applications.",
            "Create dashboards around user-facing health indicators.",
            "Use distributed tracing during incidents instead of only reading app logs.",
        ],
        "validate": "Generate a test request that calls a dependency and confirm the end-to-end trace is visible.",
        "guardrail": "Telemetry volume has a cost. Keep enough signal for incidents without collecting every debug line forever.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview"],
        "tags": ["Azure", "Application Insights", "Observability", "Monitoring"],
    },
    {
        "slug": "azure_policy_baseline",
        "title": "How to Create an Azure Policy Baseline for Governance",
        "service": "Azure Policy",
        "outcome": "a governance baseline that audits or enforces required standards across subscriptions",
        "steps": [
            "Identify the rules that should apply everywhere, such as required tags or allowed regions.",
            "Start with audit effects before enforcing deny effects broadly.",
            "Assign policies at the management group level when the rule is truly shared.",
            "Create exemptions with expiration dates and owners.",
            "Review compliance results with platform and application teams.",
        ],
        "validate": "Deploy a test resource that violates the policy and confirm the expected audit or deny behavior.",
        "guardrail": "Policy should encode standards, not surprise teams. Communicate before moving from audit to deny.",
        "docs": ["https://learn.microsoft.com/en-us/azure/governance/policy/overview"],
        "tags": ["Azure", "Azure Policy", "Governance", "Compliance"],
    },
    {
        "slug": "defender_for_cloud",
        "title": "How to Use Microsoft Defender for Cloud as an Azure Security Backlog",
        "service": "Microsoft Defender for Cloud",
        "outcome": "a security workflow that turns recommendations into owned remediation tasks",
        "steps": [
            "Enable Defender for Cloud plans that match the workloads you actually run.",
            "Review secure score and recommendations by subscription and resource type.",
            "Group recommendations by owner and risk.",
            "Create remediation tasks for the highest-value fixes.",
            "Track exceptions separately from completed work.",
        ],
        "validate": "Pick one recommendation, remediate it, and confirm Defender for Cloud reflects the changed state.",
        "guardrail": "Secure score is a guide, not a strategy. Prioritize fixes based on exposure and business impact.",
        "docs": ["https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction"],
        "tags": ["Azure", "Defender for Cloud", "Security", "Governance"],
    },
    {
        "slug": "sentinel_analytics",
        "title": "How to Start with Microsoft Sentinel Analytics Rules",
        "service": "Microsoft Sentinel",
        "outcome": "analytics rules that detect meaningful activity and create incidents responders can use",
        "steps": [
            "Connect the data sources that matter for your environment.",
            "Start with built-in rule templates before writing custom KQL.",
            "Tune rule frequency, lookback, severity, and entity mapping.",
            "Create automation only after the incident flow is understood.",
            "Review false positives with the security team.",
        ],
        "validate": "Run a controlled test event and confirm the rule creates an incident with useful entities and context.",
        "guardrail": "A SIEM rule is only useful if someone knows what to do when it fires.",
        "docs": ["https://learn.microsoft.com/en-us/azure/sentinel/overview"],
        "tags": ["Azure", "Microsoft Sentinel", "Security", "SIEM"],
    },
    {
        "slug": "azure_firewall_hub",
        "title": "How to Place Azure Firewall in a Hub-and-Spoke Network",
        "service": "Azure Firewall",
        "outcome": "centralized network inspection for spoke traffic using a shared hub firewall",
        "steps": [
            "Deploy Azure Firewall into a dedicated AzureFirewallSubnet in the hub VNet.",
            "Peer spoke VNets to the hub with the correct gateway and forwarding settings.",
            "Create route tables that send required traffic through the firewall.",
            "Build application and network rules around real traffic needs.",
            "Send firewall logs to Log Analytics for review.",
        ],
        "validate": "Test traffic from a spoke workload and confirm the firewall sees and allows or denies the flow as expected.",
        "guardrail": "Central inspection is powerful, but bad routes can break everything. Roll out route changes carefully.",
        "docs": ["https://learn.microsoft.com/en-us/azure/firewall/overview"],
        "tags": ["Azure", "Azure Firewall", "Networking", "Security"],
    },
    {
        "slug": "private_dns_resolver",
        "title": "How to Use Azure DNS Private Resolver for Hybrid Name Resolution",
        "service": "Azure DNS Private Resolver",
        "outcome": "DNS forwarding between Azure private zones and on-premises networks without custom DNS VMs",
        "steps": [
            "Create inbound and outbound resolver endpoints in dedicated subnets.",
            "Configure forwarding rulesets for the domains that need conditional forwarding.",
            "Link the ruleset to the VNets that need outbound resolution.",
            "Update on-premises DNS forwarders to use the inbound endpoint where required.",
            "Test resolution in both directions.",
        ],
        "validate": "Resolve Azure private names from on-premises and resolve on-premises names from Azure workloads.",
        "guardrail": "DNS forwarding is a dependency for private apps. Monitor it like infrastructure, not like a side setting.",
        "docs": ["https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview"],
        "tags": ["Azure", "DNS", "Hybrid", "Networking"],
    },
    {
        "slug": "expressroute_planning",
        "title": "How to Plan Azure ExpressRoute for Production Connectivity",
        "service": "Azure ExpressRoute",
        "outcome": "a private connectivity plan with circuit, peering, routing, and resiliency expectations defined",
        "steps": [
            "Choose a connectivity provider and circuit bandwidth based on measured demand.",
            "Plan private peering and route advertisements carefully.",
            "Decide how traffic inspection and forced tunneling should work.",
            "Design redundant circuits or backup VPN where availability requires it.",
            "Document operational contacts and escalation paths with the provider.",
        ],
        "validate": "Test route propagation, failover expectations, and application connectivity before migration waves begin.",
        "guardrail": "ExpressRoute is not automatically simpler than VPN. Routing ownership needs to be explicit.",
        "docs": ["https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction"],
        "tags": ["Azure", "ExpressRoute", "Hybrid", "Networking"],
    },
    {
        "slug": "vpn_gateway",
        "title": "How to Build a Site-to-Site VPN Gateway in Azure",
        "service": "Azure VPN Gateway",
        "outcome": "encrypted connectivity between an Azure VNet and another network",
        "steps": [
            "Create the gateway subnet with enough address space.",
            "Deploy the VPN gateway SKU that matches throughput and availability needs.",
            "Create the local network gateway with the on-premises public IP and address prefixes.",
            "Create the connection with matching IPsec settings and shared key.",
            "Confirm route propagation and firewall rules on both sides.",
        ],
        "validate": "Test traffic across the tunnel and confirm both Azure and on-premises devices show the connection as established.",
        "guardrail": "Most VPN issues are mismatched routing, selectors, or security policies. Capture both sides of the configuration.",
        "docs": ["https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways"],
        "tags": ["Azure", "VPN Gateway", "Hybrid", "Networking"],
    },
    {
        "slug": "bicep_modules",
        "title": "How to Structure Azure Bicep Modules for Reuse",
        "service": "Azure Bicep",
        "outcome": "Bicep modules that teams can reuse without copying entire deployment files",
        "steps": [
            "Start with a clear module boundary around one deployable resource group pattern.",
            "Expose only the parameters that consumers should control.",
            "Use outputs for values other modules need.",
            "Keep naming and tagging conventions consistent.",
            "Version modules and test them with example deployments.",
        ],
        "validate": "Deploy the module into a test resource group with minimal and full parameter sets.",
        "guardrail": "A module should reduce duplication. If it hides important design choices, it becomes a different problem.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview"],
        "tags": ["Azure", "Bicep", "Infrastructure as Code", "DevOps"],
    },
    {
        "slug": "terraform_remote_state",
        "title": "How to Store Terraform State in Azure Storage",
        "service": "Terraform on Azure",
        "outcome": "remote Terraform state stored in an Azure Storage account instead of on a local machine",
        "steps": [
            "Create a resource group, storage account, and blob container for state.",
            "Secure the storage account with appropriate access controls.",
            "Configure the azurerm backend in Terraform.",
            "Initialize Terraform so the state backend is created and used.",
            "Restrict who can read or write the state file.",
        ],
        "validate": "Run terraform init and terraform plan from a clean machine or pipeline to confirm the remote backend is working.",
        "guardrail": "State can contain sensitive values. Treat the storage account as a security boundary.",
        "docs": ["https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage"],
        "tags": ["Azure", "Terraform", "State", "Infrastructure as Code"],
    },
    {
        "slug": "azure_devops_app_service",
        "title": "How to Deploy Azure App Service from Azure DevOps",
        "service": "Azure DevOps",
        "outcome": "a pipeline that builds and deploys an application to Azure App Service",
        "steps": [
            "Create or choose the App Service target environment.",
            "Create a service connection with the right Azure scope.",
            "Build the app artifact in the pipeline.",
            "Deploy the artifact to the App Service deployment slot or production app.",
            "Add smoke tests after deployment.",
        ],
        "validate": "Run the pipeline and confirm the deployed version, app health endpoint, and deployment logs.",
        "guardrail": "Use deployment slots for production apps so validation can happen before traffic moves.",
        "docs": ["https://learn.microsoft.com/en-us/azure/app-service/deploy-azure-pipelines"],
        "tags": ["Azure", "Azure DevOps", "App Service", "CI/CD"],
    },
    {
        "slug": "github_actions_oidc",
        "title": "How to Connect GitHub Actions to Azure with OpenID Connect",
        "service": "GitHub Actions",
        "outcome": "a GitHub Actions workflow that authenticates to Azure without a long-lived client secret",
        "steps": [
            "Create an app registration or managed identity for the deployment workflow.",
            "Create a federated credential that matches the GitHub repository, branch, or environment.",
            "Grant the identity only the Azure role scope it needs.",
            "Update the workflow to use OIDC login.",
            "Remove old stored Azure client secrets from GitHub.",
        ],
        "validate": "Run the workflow and check Azure sign-in logs for the federated identity.",
        "guardrail": "Keep federated credential subject filters tight. A broad repository pattern can become an unnecessary risk.",
        "docs": ["https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect"],
        "tags": ["Azure", "GitHub Actions", "OIDC", "DevOps"],
    },
    {
        "slug": "acr_private_link",
        "title": "How to Secure Azure Container Registry with Private Link",
        "service": "Azure Container Registry",
        "outcome": "container image pulls and pushes through private network connectivity",
        "steps": [
            "Create a private endpoint for the registry.",
            "Configure the private DNS zone for Azure Container Registry.",
            "Link the zone to build and runtime VNets.",
            "Review public network access and firewall settings.",
            "Test image pull from AKS, Container Apps, or a VM inside the private network.",
        ],
        "validate": "Run docker pull or a platform deployment from the target network and confirm name resolution uses the private endpoint.",
        "guardrail": "Private registry access requires the build system and runtime environment to both have a valid network path.",
        "docs": ["https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-link"],
        "tags": ["Azure", "Container Registry", "Private Link", "Containers"],
    },
    {
        "slug": "application_gateway_ingress",
        "title": "How to Use Application Gateway Ingress Controller with AKS",
        "service": "Azure Application Gateway",
        "outcome": "AKS ingress managed through Application Gateway integration",
        "steps": [
            "Confirm the AKS cluster and Application Gateway network layout.",
            "Enable or install Application Gateway Ingress Controller.",
            "Grant required permissions for the controller identity.",
            "Create Kubernetes ingress resources with the right annotations.",
            "Test routing, TLS, and health probe behavior.",
        ],
        "validate": "Deploy a sample service and confirm Application Gateway routes to the correct AKS backend.",
        "guardrail": "Ingress is both Kubernetes and Azure networking. Troubleshoot from both sides before changing rules blindly.",
        "docs": ["https://learn.microsoft.com/en-us/azure/application-gateway/tutorial-ingress-controller-add-on-existing"],
        "tags": ["Azure", "AKS", "Application Gateway", "Ingress"],
    },
    {
        "slug": "azure_backup",
        "title": "How to Build a Basic Azure Backup Plan",
        "service": "Azure Backup",
        "outcome": "a backup policy and recovery process that fits the workload's retention and restore needs",
        "steps": [
            "Identify the workloads that need backup and the required retention period.",
            "Create or choose a Recovery Services vault.",
            "Configure backup policies around business recovery requirements.",
            "Enable backup for the target workloads.",
            "Run a test restore and document the process.",
        ],
        "validate": "Do not stop at successful backup jobs. Prove that restore works and that the restored data is usable.",
        "guardrail": "A backup that has never been restored is only a hope. Schedule restore tests.",
        "docs": ["https://learn.microsoft.com/en-us/azure/backup/backup-overview"],
        "tags": ["Azure", "Backup", "Recovery", "Operations"],
    },
    {
        "slug": "site_recovery",
        "title": "How to Start Planning Disaster Recovery with Azure Site Recovery",
        "service": "Azure Site Recovery",
        "outcome": "a disaster recovery plan that defines replication, failover, testing, and ownership",
        "steps": [
            "Identify the applications that require disaster recovery.",
            "Document RTO, RPO, dependencies, and failover order.",
            "Prepare the vault, replication settings, and target environment.",
            "Create recovery plans for grouped failover.",
            "Run test failovers without affecting production.",
        ],
        "validate": "Measure test failover time and confirm application owners can validate the recovered workload.",
        "guardrail": "DR is an application exercise, not only an infrastructure feature. Dependencies decide whether recovery is real.",
        "docs": ["https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview"],
        "tags": ["Azure", "Site Recovery", "Disaster Recovery", "Resiliency"],
    },
    {
        "slug": "azure_migrate",
        "title": "How to Use Azure Migrate for a First Migration Assessment",
        "service": "Azure Migrate",
        "outcome": "a discovery and assessment workflow that turns server inventory into migration planning data",
        "steps": [
            "Create an Azure Migrate project.",
            "Deploy the appliance or choose the discovery method for the environment.",
            "Collect server inventory, performance, and dependency data.",
            "Create assessments for sizing and readiness.",
            "Review blockers before planning migration waves.",
        ],
        "validate": "Compare discovered inventory with known CMDB or virtualization records to catch missing workloads.",
        "guardrail": "Assessment data gets stale. Refresh discovery before making final migration commitments.",
        "docs": ["https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview"],
        "tags": ["Azure", "Azure Migrate", "Migration", "Assessment"],
    },
    {
        "slug": "cost_management_budgets",
        "title": "How to Create Azure Cost Management Budgets",
        "service": "Azure Cost Management",
        "outcome": "budgets and alerts that help teams notice spend changes before the invoice arrives",
        "steps": [
            "Choose the management group, subscription, or resource group scope.",
            "Create a budget that matches the team's expected monthly spend.",
            "Configure alert thresholds before and after the target amount.",
            "Send alerts to owners who can actually take action.",
            "Review budget accuracy after the first billing cycle.",
        ],
        "validate": "Confirm budget emails or action group notifications reach the right people.",
        "guardrail": "Budgets do not control spend by themselves. Pair alerts with owner accountability and cleanup routines.",
        "docs": ["https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets"],
        "tags": ["Azure", "Cost Management", "FinOps", "Budgets"],
    },
    {
        "slug": "azure_advisor",
        "title": "How to Turn Azure Advisor Recommendations into Engineering Work",
        "service": "Azure Advisor",
        "outcome": "a review process that converts Advisor recommendations into prioritized backlog items",
        "steps": [
            "Open Advisor recommendations by subscription and category.",
            "Group items by cost, security, reliability, operational excellence, and performance.",
            "Assign owners for recommendations that affect live workloads.",
            "Suppress recommendations only with a documented reason.",
            "Track completed recommendations in the platform backlog.",
        ],
        "validate": "Fix one recommendation and confirm Advisor updates after the next refresh.",
        "guardrail": "Advisor is most useful when reviewed regularly. Do not let recommendations become permanent wallpaper.",
        "docs": ["https://learn.microsoft.com/en-us/azure/advisor/advisor-overview"],
        "tags": ["Azure", "Advisor", "Operations", "FinOps"],
    },
    {
        "slug": "managed_disk_snapshots",
        "title": "How to Create a Snapshot of an Azure Managed Disk",
        "service": "Azure Managed Disks",
        "outcome": "a point-in-time disk snapshot that can support recovery, testing, or image workflows",
        "steps": [
            "Identify the managed disk and confirm the application consistency requirement.",
            "Stop or quiesce the workload if crash consistency is not enough.",
            "Create the snapshot in the target resource group and region.",
            "Tag the snapshot with owner, source, purpose, and expiration.",
            "Delete snapshots that are no longer needed.",
        ],
        "validate": "Create a disk from the snapshot in a test environment and confirm it contains the expected data.",
        "guardrail": "Snapshots are not a full backup strategy. Manage retention and access carefully.",
        "docs": ["https://learn.microsoft.com/en-us/azure/virtual-machines/snapshot-copy-managed-disk"],
        "tags": ["Azure", "Managed Disks", "Snapshots", "Virtual Machines"],
    },
    {
        "slug": "vm_scale_sets",
        "title": "How to Use Azure Virtual Machine Scale Sets for Repeatable VM Capacity",
        "service": "Virtual Machine Scale Sets",
        "outcome": "a scale set design that creates consistent VM instances and supports scaling operations",
        "steps": [
            "Choose an orchestration mode that fits the workload.",
            "Define the VM image, size, networking, and identity settings.",
            "Configure autoscale rules around real demand signals.",
            "Plan upgrades, health probes, and application deployment.",
            "Monitor instance health and scaling behavior.",
        ],
        "validate": "Scale out and scale in under controlled conditions and confirm the application remains healthy.",
        "guardrail": "Scale sets solve capacity consistency, but the app still needs stateless design or careful state handling.",
        "docs": ["https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/overview"],
        "tags": ["Azure", "Virtual Machines", "Scale Sets", "Compute"],
    },
    {
        "slug": "azure_bastion",
        "title": "How to Use Azure Bastion for Safer VM Access",
        "service": "Azure Bastion",
        "outcome": "browser-based VM access without exposing RDP or SSH directly to the internet",
        "steps": [
            "Create the AzureBastionSubnet with the required size.",
            "Deploy Azure Bastion in the VNet that contains or peers to target VMs.",
            "Remove public IP exposure from VMs where possible.",
            "Grant VM login permissions through RBAC and operating system access controls.",
            "Monitor Bastion usage and failed access attempts.",
        ],
        "validate": "Connect to a VM through Bastion and confirm direct public RDP or SSH is closed.",
        "guardrail": "Bastion improves access posture, but identity and VM permissions still need least privilege.",
        "docs": ["https://learn.microsoft.com/en-us/azure/bastion/bastion-overview"],
        "tags": ["Azure", "Bastion", "Virtual Machines", "Security"],
    },
    {
        "slug": "entra_app_registration",
        "title": "How to Register an Application in Microsoft Entra ID",
        "service": "Microsoft Entra ID",
        "outcome": "an app registration that can represent an application for authentication and authorization flows",
        "steps": [
            "Create the app registration with a clear name and supported account type.",
            "Configure redirect URIs for the application platform.",
            "Add API permissions only when the app actually needs them.",
            "Create credentials or certificates only when a managed identity or federation is not possible.",
            "Record the application ID and tenant ID for deployment configuration.",
        ],
        "validate": "Run the authentication flow in a test environment and check sign-in logs for the application.",
        "guardrail": "App registrations are security assets. Review credentials, owners, and permissions regularly.",
        "docs": ["https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app"],
        "tags": ["Azure", "Entra ID", "App Registration", "Identity"],
    },
    {
        "slug": "azure_rbac",
        "title": "How to Assign Azure RBAC Roles with Least Privilege",
        "service": "Azure RBAC",
        "outcome": "role assignments that grant the access needed without handing out broad subscription ownership",
        "steps": [
            "Identify the exact task the user, group, or identity needs to perform.",
            "Choose the narrowest built-in role that supports that task.",
            "Assign the role at the smallest practical scope.",
            "Use groups for people and managed identities for workloads.",
            "Review role assignments regularly.",
        ],
        "validate": "Test that the principal can perform the intended task and cannot perform unrelated privileged actions.",
        "guardrail": "Owner and Contributor are convenient, but they are rarely the right default.",
        "docs": ["https://learn.microsoft.com/en-us/azure/role-based-access-control/overview"],
        "tags": ["Azure", "RBAC", "Identity", "Security"],
    },
    {
        "slug": "managed_identity_vm",
        "title": "How to Use Managed Identity from an Azure Virtual Machine",
        "service": "Managed Identities",
        "outcome": "a VM that authenticates to Azure services through managed identity instead of stored credentials",
        "steps": [
            "Enable system-assigned or user-assigned managed identity on the VM.",
            "Grant the identity the required role on the target resource.",
            "Update scripts or applications to request tokens from the Azure identity endpoint.",
            "Remove stored credentials from the VM.",
            "Monitor target resource logs for identity-based access.",
        ],
        "validate": "Run a test command from the VM that accesses the target resource using the managed identity.",
        "guardrail": "A compromised VM can use its managed identity. Keep VM hardening and role scope tight.",
        "docs": ["https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview"],
        "tags": ["Azure", "Managed Identity", "Virtual Machines", "Security"],
    },
    {
        "slug": "load_balancer_health_probes",
        "title": "How to Configure Azure Load Balancer Health Probes",
        "service": "Azure Load Balancer",
        "outcome": "health probes that remove unhealthy backend instances from rotation",
        "steps": [
            "Choose TCP, HTTP, or HTTPS probes based on what the workload can answer reliably.",
            "Create a lightweight health endpoint when using HTTP probes.",
            "Configure probe interval and unhealthy threshold deliberately.",
            "Attach the probe to the load balancing rule.",
            "Test how the backend behaves when the health endpoint fails.",
        ],
        "validate": "Stop the service on one backend instance and confirm Load Balancer stops sending traffic to it.",
        "guardrail": "A health probe should measure readiness, not run expensive business logic.",
        "docs": ["https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-custom-probe-overview"],
        "tags": ["Azure", "Load Balancer", "Networking", "Availability"],
    },
    {
        "slug": "traffic_manager_failover",
        "title": "How to Use Azure Traffic Manager for DNS-Based Failover",
        "service": "Azure Traffic Manager",
        "outcome": "a DNS routing profile that can direct clients to healthy endpoints",
        "steps": [
            "Create a Traffic Manager profile with the routing method that matches the scenario.",
            "Add endpoints for each regional application deployment.",
            "Configure endpoint monitoring path, protocol, and expected status.",
            "Set DNS TTL with failover expectations in mind.",
            "Test endpoint disablement and recovery.",
        ],
        "validate": "Simulate a regional endpoint failure and confirm DNS responses shift to the healthy endpoint.",
        "guardrail": "Traffic Manager is DNS-based, so client and resolver caching affect failover timing.",
        "docs": ["https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview"],
        "tags": ["Azure", "Traffic Manager", "DNS", "Resiliency"],
    },
    {
        "slug": "event_grid",
        "title": "How to Use Azure Event Grid for Event-Driven Automation",
        "service": "Azure Event Grid",
        "outcome": "an event subscription that routes Azure or application events to an automation target",
        "steps": [
            "Choose the event source and event types that matter.",
            "Create the destination, such as a Function, Logic App, webhook, or queue.",
            "Create the Event Grid subscription with filters where useful.",
            "Validate delivery, retry, and dead-letter behavior.",
            "Monitor failed deliveries.",
        ],
        "validate": "Trigger a real test event and confirm the destination receives the expected event payload.",
        "guardrail": "Event-driven systems need idempotent handlers because retries and duplicate handling are part of real operations.",
        "docs": ["https://learn.microsoft.com/en-us/azure/event-grid/overview"],
        "tags": ["Azure", "Event Grid", "Automation", "Integration"],
    },
    {
        "slug": "service_bus_queue",
        "title": "How to Start with Azure Service Bus Queues",
        "service": "Azure Service Bus",
        "outcome": "a queue that decouples producers and consumers with reliable message handling",
        "steps": [
            "Create a Service Bus namespace and queue.",
            "Choose lock duration, duplicate detection, and dead-letter settings deliberately.",
            "Give producers and consumers separate least-privilege access.",
            "Write consumers to complete, abandon, defer, or dead-letter messages correctly.",
            "Monitor queue depth, dead-letter count, and processing latency.",
        ],
        "validate": "Send test messages, process them, and confirm failed messages land in the dead-letter queue when expected.",
        "guardrail": "Queues hide spikes, but they do not remove the need to monitor backlog and failed processing.",
        "docs": ["https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview"],
        "tags": ["Azure", "Service Bus", "Messaging", "Integration"],
    },
    {
        "slug": "event_hubs_capture",
        "title": "How to Use Azure Event Hubs Capture for Streaming Data Retention",
        "service": "Azure Event Hubs",
        "outcome": "streaming events captured to storage for replay, analytics, or archive scenarios",
        "steps": [
            "Create an Event Hubs namespace and event hub.",
            "Choose a storage account or Data Lake destination for capture.",
            "Configure capture window size and time interval.",
            "Send test events through the hub.",
            "Check captured files and downstream processing permissions.",
        ],
        "validate": "Confirm event files arrive in the destination path and can be read by the intended analytics process.",
        "guardrail": "Capture helps retention, but consumers still need partition-aware processing and replay design.",
        "docs": ["https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about"],
        "tags": ["Azure", "Event Hubs", "Streaming", "Analytics"],
    },
    {
        "slug": "logic_apps_workflow",
        "title": "How to Build a Basic Azure Logic Apps Workflow",
        "service": "Azure Logic Apps",
        "outcome": "a workflow that connects a trigger, actions, conditions, and monitoring in a supportable way",
        "steps": [
            "Choose the trigger that starts the workflow.",
            "Add connector actions with clear inputs and outputs.",
            "Use conditions or scopes for branching and error handling.",
            "Secure connections and secrets through managed identity where possible.",
            "Review run history after test executions.",
        ],
        "validate": "Trigger the workflow with test data and inspect each action's input, output, and retry behavior.",
        "guardrail": "Logic Apps workflows are production integrations. Name actions clearly and monitor failures.",
        "docs": ["https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview"],
        "tags": ["Azure", "Logic Apps", "Workflow", "Integration"],
    },
    {
        "slug": "api_management_policy",
        "title": "How to Add a Policy in Azure API Management",
        "service": "Azure API Management",
        "outcome": "an API gateway policy that changes request, response, security, or routing behavior intentionally",
        "steps": [
            "Choose the API, operation, or product scope for the policy.",
            "Add the policy in the inbound, backend, outbound, or on-error section.",
            "Use named values for reusable configuration.",
            "Test policy behavior with the API test console or a client.",
            "Version policy changes with the API source where possible.",
        ],
        "validate": "Send a request that should exercise the policy and confirm headers, status, transformation, or routing changed as intended.",
        "guardrail": "Gateway policies can become hidden application logic. Keep them reviewed and documented.",
        "docs": ["https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-policies"],
        "tags": ["Azure", "API Management", "Policies", "Integration"],
    },
    {
        "slug": "redis_private_endpoint",
        "title": "How to Connect Azure Cache for Redis Through Private Endpoint",
        "service": "Azure Cache for Redis",
        "outcome": "Redis connectivity over a private network path with DNS configured correctly",
        "steps": [
            "Create a private endpoint for the cache.",
            "Configure the private DNS zone and link it to client VNets.",
            "Review public network access settings.",
            "Update applications to connect using the standard cache hostname.",
            "Test latency and connection behavior from the workload network.",
        ],
        "validate": "Resolve the cache hostname from the app network and confirm the connection succeeds over the private address.",
        "guardrail": "Private endpoint protects the network path, but Redis authentication and client timeout settings still matter.",
        "docs": ["https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-private-link"],
        "tags": ["Azure", "Redis", "Private Endpoint", "Cache"],
    },
]


def how_to_content(topic):
    steps = "\n\n".join(f"{index}. {ascii_clean(step)}" for index, step in enumerate(topic["steps"], 1))
    sources = "\n\n".join(f"Microsoft Learn: {url}" for url in topic["docs"])
    body = f"""
A useful Azure how-to should end with something you can operate, not just something that deployed once.

This guide walks through **{topic['outcome']}** using **{topic['service']}**.

## When To Use This Pattern

Use this pattern when you need a repeatable way to configure **{topic['service']}** and explain the decision to another engineer later.

The goal is not to click through the portal as fast as possible.

The goal is to understand the resource, the security boundary, the validation step, and the operational owner.

## Before You Start

Confirm the subscription, resource group, region, naming standard, tags, and identity model before creating anything.

Also confirm whether this change affects production traffic, data access, cost, or compliance.

If it does, create the change record first and make rollback expectations explicit.

## Steps

{steps}

## Validate The Work

{topic['validate']}

Validation is where many cloud guides get weak.

Do not stop at a green deployment screen. Test from the same network, identity, pipeline, or application path that will use the service in real life.

## Production Notes

{topic['guardrail']}

Add tags, diagnostic settings, alert ownership, and documentation before calling the work finished.

If the resource is important enough to deploy, it is important enough to monitor.

## Common Mistakes

The first mistake is deploying without knowing the owner.

The second mistake is skipping least privilege because a broad role is faster.

The third mistake is forgetting DNS, routing, logging, or cost review until after the first incident.

Keep the implementation small, but make the operating model clear.

## Bottom Line

**{topic['service']}** is easier to support when the design is intentional.

Build it with a clear purpose, validate the real path, and leave behind enough documentation that the next engineer can understand the decision.

## Sources

{sources}

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*
"""
    return textwrap.dedent(body).strip()


def how_to_post(topic):
    return {
        "title": ascii_clean(topic["title"]),
        "coverImage": COVER_IMAGE,
        "content": how_to_content(topic),
        "excerpt": shorten(f"A practical Azure how-to for {topic['service']}: {topic['outcome']}.", 180),
        "publish": True,
        "tags": topic["tags"][:8],
    }


def write_post(number, slug, post, force=False):
    file_path = BLOGS_DIR / f"blog_{number:03d}_{slug}.py"
    if file_path.exists() and not force:
        raise FileExistsError(f"{file_path} already exists. Re-run with --force to overwrite.")

    header = f'"""\nBlog Post {number}: {post["title"]}\n"""\n\n'
    content = header + "BLOG_POST = " + pprint.pformat(post, width=100, sort_dicts=False) + "\n"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite generated blog files if they exist.")
    args = parser.parse_args()

    if len(HOW_TO_TOPICS) < HOW_TO_COUNT:
        raise RuntimeError(f"Expected at least {HOW_TO_COUNT} how-to topics, found {len(HOW_TO_TOPICS)}.")

    selected_news, skipped = select_news_items()
    written = []

    for offset, item in enumerate(selected_news):
        number = NEWS_START + offset
        post = news_post(item)
        slug = slugify(post["title"])
        written.append(write_post(number, slug, post, force=args.force))

    for offset, topic in enumerate(HOW_TO_TOPICS[:HOW_TO_COUNT]):
        number = HOW_TO_START + offset
        post = how_to_post(topic)
        written.append(write_post(number, topic["slug"], post, force=args.force))

    print(f"Generated {len(written)} blog files.")
    print(f"News posts: {NEWS_START}-{NEWS_START + NEWS_COUNT - 1}")
    print(f"How-to posts: {HOW_TO_START}-{HOW_TO_START + HOW_TO_COUNT - 1}")
    print(f"Skipped existing/local Azure update candidates: {len(skipped)}")
    for path in written[:3]:
        print(f"  {path.relative_to(ROOT)}")
    if len(written) > 3:
        print("  ...")
        print(f"  {written[-1].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
