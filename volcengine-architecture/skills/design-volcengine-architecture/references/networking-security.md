# Networking and Security

## Capability decomposition

- Separate address space and routing, north-south ingress/egress, east-west connectivity, hybrid connectivity and name resolution.
- Apply identity, network and application controls as complementary boundaries.
- Treat encryption, key custody, audit evidence and incident response as lifecycle concerns.
- Design exposure paths explicitly from DNS through edge protection and load balancing to private workloads.

## Architecture-changing questions

- Which trust zones, accounts and environments must be isolated, and which flows must cross them?
- Is traffic public, private, hybrid or cross-account, and who owns routing and DNS?
- Does ingress require transport-level distribution, application-level routing or both?
- Which identities are human, workload or federated, and where are credentials issued and rotated?
- Which data needs customer-managed keys or application-level envelope encryption?
- Which threats and compliance controls require WAF, boundary firewalling, audit or evidence retention?

## Product-family mappings

```yaml
products:
  - product_name: 私有网络
    official_url: https://www.volcengine.com/docs/6401
    stable_capabilities: [isolated virtual networking, subnets and routes, security groups, network access control]
    use_when: [cloud resources require private network boundaries, routing and address ownership must be explicit]
    avoid_or_verify_when: [address planning is incomplete, required hybrid or cross-network connectivity is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 负载均衡
    official_url: https://www.volcengine.com/docs/6406
    stable_capabilities: [traffic distribution, transport and application load-balancer families, health checking, listener routing]
    use_when: [multiple backends serve one entry point, failover or layer-aware routing is required]
    avoid_or_verify_when: [protocol and client-source requirements are unclear, load-balancer family selection is unresolved]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 专线连接
    official_url: https://www.volcengine.com/docs/6407
    stable_capabilities: [dedicated hybrid connectivity, data-center to virtual-network connectivity, routed private paths]
    use_when: [on-premises and cloud networks require a dedicated private connection]
    avoid_or_verify_when: [redundancy, routing ownership or provider lead time is not planned]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 访问控制 IAM
    official_url: https://www.volcengine.com/docs/6257/64959?lang=zh
    stable_capabilities: [identity management, policy-based authorization, role and temporary credential access, federation]
    use_when: [human or workload access to cloud resources must be centrally authorized]
    avoid_or_verify_when: [long-lived credentials are embedded in workloads, least-privilege policies are not defined]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 密钥管理系统
    official_url: https://www.volcengine.com/product/kms
    stable_capabilities: [managed key custody, cryptographic operations, envelope encryption, cloud-service encryption integration]
    use_when: [sensitive data requires managed encryption keys, key use and rotation need governance]
    avoid_or_verify_when: [key ownership or recovery responsibility is unclear, required service integration is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: Web应用防火墙
    official_url: https://www.volcengine.com/docs/6511
    stable_capabilities: [web and API traffic inspection, application attack protection, access-control policies, security logging]
    use_when: [public web or API traffic needs application-layer protection]
    avoid_or_verify_when: [the protected protocol is not web traffic, origin and load-balancer integration is unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 云防火墙
    official_url: https://www.volcengine.com/docs/6516
    stable_capabilities: [internet and virtual-network boundary control, traffic visibility, intrusion prevention, network security audit]
    use_when: [central network boundary policy and inspection are required across cloud network paths]
    avoid_or_verify_when: [traffic steering is not modeled, asset and network support boundaries are unverified]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- Build trust zones with separate VPCs or subnets, then define only the routes and security policies required by documented flows.
- Terminate public traffic through the chosen edge or load-balancer path; place WAF on web/API ingress and keep origins private where supported.
- Use cloud firewall controls for inspected network boundaries; retain security groups and network ACLs as workload and subnet guardrails.
- Give workloads IAM roles or temporary credentials and use KMS-backed encryption where the selected service integration supports it.
- Use redundant hybrid paths and independent routing failure tests when on-premises connectivity is critical.

## Review points

- Draw every ingress, egress, east-west, management and replication path.
- Validate route symmetry, address overlap, DNS behavior and failure-domain isolation.
- Check least privilege for identities, network rules, service roles and key administrators.
- Confirm certificate, secret and key rotation owners plus break-glass access.
- Verify protection order, original client identity propagation, logging and alert ownership.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck supported protocols, address families, connectivity combinations, protection coverage, certificate and cipher support, log retention, service integrations and compliance evidence.

## Official discovery links

- [Virtual Private Cloud documentation](https://www.volcengine.com/docs/6401)
- [Load Balancing documentation](https://www.volcengine.com/docs/6406)
- [Direct Connect documentation](https://www.volcengine.com/docs/6407)
- [IAM documentation](https://www.volcengine.com/docs/6257/64959?lang=zh)
- [Key Management Service product page](https://www.volcengine.com/product/kms)
- [Web Application Firewall documentation](https://www.volcengine.com/docs/6511)
- [Cloud Firewall documentation](https://www.volcengine.com/docs/6516)
- [Volcano Engine Trust Center](https://www.volcengine.com/trust/security)

