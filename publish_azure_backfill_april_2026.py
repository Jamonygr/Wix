"""
Publish the April 2026 Azure backfill posts in blogs_v3.

This reuses the dependency-free Wix publisher and its duplicate-title checks.
"""

import publish_azure_news_june_2026 as publisher


publisher.BLOG_FILES = [
    "blog_41_aks_network_insights_agent.py",
    "blog_42_elastic_san_windows_extension.py",
    "blog_43_virtual_network_manager_ipam.py",
    "blog_44_front_door_http_ddos.py",
    "blog_45_elastic_san_backup.py",
    "blog_46_aks_wireguard_encryption.py",
    "blog_47_elastic_san_crc_protection.py",
    "blog_48_postgresql_cascading_replicas.py",
    "blog_49_elastic_san_capacity_autoscaling.py",
    "blog_50_arc_kubernetes_monitor.py",
    "blog_51_arc_sql_vm_migration.py",
    "blog_52_cosmos_db_dynamic_masking.py",
    "blog_53_postgresql_fabric_mirroring.py",
    "blog_54_postgresql_premium_ssd_v2.py",
    "blog_55_azure_monitor_pipeline.py",
]


if __name__ == "__main__":
    publisher.main()

