---
name: select-volcengine-products
description: Select canonical Volcengine products and official evidence entry points for an architecture capability. Use for product-family routing, canonical product naming, alternatives, and runtime verification requirements.
---

# Volcengine Product-Family Catalog

## Standalone invocation

When invoked directly, map each requested capability to a canonical product from `product-registry.json` and the relevant domain skill. Return product, responsibility, requirement-linked rationale, alternative, switch condition, and an official `volcengine.com` discovery URL. Write a retrieval date only after actually opening the official page during the current task; otherwise label the evidence `runtime verification required`. Do not use an alias without its canonical name or assert current availability, commercial terms, limits, or service commitments without runtime verification.

Use this catalog to route architecture work, not to assert current commercial availability. Product records in the linked references contain stable capability labels and official discovery entry points only. Before recommending a concrete deployment, recheck every listed dynamic field against the official page for the target account and deployment context.

Canonical product labels and common aliases are indexed in [product-registry.json](product-registry.json). The registry is the machine-readable source for report validation; domain references remain the source for capability, selection, and evidence guidance.

## Family routing

| Need | Reference | Official indexes |
| --- | --- | --- |
| Foundation models, model lifecycle, agents, knowledge retrieval | `$design-volcengine-ai-agent` | [Volcano Engine AI cloud](https://www.volcengine.com/sem), [Ark documentation](https://www.volcengine.com/docs/82379/66619f8df281250274ef4f88?lang=zh) |
| Virtual machines, accelerators, containers, functions, image delivery | `$design-volcengine-cloud-native` | [Volcano Engine documentation center](https://www.volcengine.com/docs/86403/1829870?lang=zh), [Container Service documentation](https://www.volcengine.com/docs/6460) |
| Data ingestion, streaming, lakehouse, warehouses, development and governance | `$design-volcengine-data-analytics` | [Volcano Engine documentation center](https://www.volcengine.com/docs/86403/1829870?lang=zh), [DataLeap documentation](https://www.volcengine.com/docs/6260) |
| Relational, document and cache databases; object and shared-file storage | `$design-volcengine-database-storage` | [MySQL documentation](https://www.volcengine.com/docs/6313), [Object Storage documentation](https://www.volcengine.com/docs/6349) |
| Network boundaries, traffic entry, identity, encryption and application protection | `$design-volcengine-network-security` | [Virtual Private Cloud documentation](https://www.volcengine.com/docs/6401), [Volcano Engine Trust Center](https://www.volcengine.com/trust/security) |
| Content delivery, video, images, real-time media and edge workloads | `$design-volcengine-media-edge` | [CDN documentation](https://www.volcengine.com/docs/6454), [Video on Demand documentation](https://www.volcengine.com/docs/4) |

## Selection rules

- Route by required capability and operating model before choosing a named product.
- Use the exact `product_name` from the selected domain reference as the canonical report label. Add a common abbreviation only after the canonical name; never replace the canonical name with a generic category or abbreviation alone.
- Treat adjacent families as composable: for example, an AI service may still require compute, storage, networking, security and observability decisions.
- A product name here proves only that an official discovery entry existed when this reference was built. It does not prove availability or suitability for a region, account, workload or compliance regime.
- Recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` at design time, record the query date, and cite the exact official page used.
- If official pages conflict, prefer the more specific and more recently updated source. Preserve unresolved conflicts as open questions.

## Evidence entry points

- [Volcano Engine documentation center](https://www.volcengine.com/docs/86403/1829870?lang=zh)
- [Volcano Engine product overview](https://www.volcengine.com/sem)
- [Volcano Engine Trust Center](https://www.volcengine.com/trust/security)
