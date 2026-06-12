"""
Blog Post 92: ASR Linux NVMe Preview
"""

BLOG_POST = {
    "title": "Azure Site Recovery Adds Preview Support for Linux NVMe Azure VMs",
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    "content": """Microsoft listed **Azure Site Recovery support for Linux Azure VMs with NVMe disk controllers** as a **public preview** in **June 2026**.

This is a useful resiliency update for teams running newer high-performance Azure VM families.

## What Changed?

Azure Site Recovery now supports replication and disaster recovery for Linux Azure VMs using NVMe-enabled Generation 2 VM families in Azure-to-Azure scenarios.

Microsoft Learn calls out examples such as **Da/Ea/Fa v6-series** and **Ebsv5/Ebdsv5**.

The documented Linux distro support is limited to **RHEL 9**, **SLES 15**, and **Ubuntu 24**.

Because this is preview, teams should treat it as a validation opportunity rather than a blanket production standard.

## Why It Matters

High-performance VM families are increasingly used for data-heavy, I/O-heavy, and latency-sensitive workloads.

That creates a resiliency problem when disaster recovery support lags behind compute innovation.

If the VM shape supports the workload but the DR service does not support the disk controller or operating system combination, the architecture has a hidden gap.

This preview starts closing that gap for Linux workloads on NVMe-enabled Azure VMs.

## Who Should Care

IaaS admins should care if they manage v6-series or NVMe-enabled VM deployments.

Linux platform teams should care if their workloads are built on RHEL, SUSE, or Ubuntu.

Disaster recovery owners should care because Azure Site Recovery support matrices directly affect recovery design.

Application owners should care if high-performance Linux VMs are part of a critical service tier.

## Practical Cloud Engineer Takeaway

Do not assume every Linux VM with NVMe is covered.

Check VM family, generation, region, distro, kernel, and Azure Site Recovery churn limits.

Then run an actual test failover.

A checkbox in the portal is not a DR validation.

You need to prove replication health, failover behavior, network mapping, application startup, and data consistency under realistic conditions.

Also update runbooks. Operators need to know when a workload uses NVMe-enabled VMs because recovery behavior and support requirements may differ from older VM families.

## Real-World Example

A Linux database workload running on an NVMe-enabled VM family may have excellent performance in its primary region.

But if the DR plan does not support that VM and disk-controller combination, the architecture has a serious gap.

With this preview, the team can start testing Azure Site Recovery for that class of workload instead of designing a custom recovery pattern from scratch.

The test should include replication health, test failover, application startup, DNS or private endpoint behavior, and performance after failover.

It should also document what is still preview and which Linux distributions are supported.

That is the difference between "we enabled ASR" and "we can actually recover this service."

## Possible Impact for Azure Operations

This preview can improve DR planning for newer Linux workloads.

It may let teams protect workloads that previously required awkward architecture exceptions.

The operational impact is mostly positive, but only if the preview is tested carefully.

For production-critical systems, keep the official support matrix close and avoid assuming GA-level coverage until Microsoft says so.

DR is not about optimism.

It is about tested recovery.

## Bottom Line

Azure Site Recovery support for Linux NVMe VMs is a good preview for modern IaaS resiliency.

It gives teams a path to test DR for newer high-performance VM families.

Just keep the preview status clear and prove recovery with real failover exercises.

## Sources

Microsoft Azure Updates: https://azure.microsoft.com/updates?id=565103

Microsoft Learn Azure Site Recovery feature updates: https://learn.microsoft.com/en-us/azure/site-recovery/feature-updates-whats-new

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    "excerpt": "Azure Site Recovery added public preview support for Linux Azure VMs with NVMe disk controllers, helping teams test DR for newer high-performance VM families.",
    "publish": True,
    "tags": ["Azure", "Azure Site Recovery", "Linux", "NVMe", "Virtual Machines", "Disaster Recovery", "Public Preview"]
}
