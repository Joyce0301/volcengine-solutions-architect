# Compute and Cloud Native

## Capability decomposition

- Separate workload runtime, accelerator need, orchestration, autoscaling, artifact delivery and persistent state.
- Decide whether operations should manage hosts, Kubernetes clusters or functions.
- Model control plane, worker capacity, networking, identity and observability as separate failure and security boundaries.
- Keep state outside replaceable compute unless a workload-specific persistence design says otherwise.

## Architecture-changing questions

- Is the workload long-running, scheduled, event-driven, bursty, stateful or accelerator-dependent?
- Does the team need operating-system control, Kubernetes APIs or a function-level abstraction?
- What are the startup, scaling, placement, interruption and maintenance constraints?
- Which workloads require GPU acceleration, and has software and device compatibility been validated?
- Which zones, networks and failure domains must the service span?
- How are images, dependencies, secrets, configuration and rollout state governed?

## Product-family mappings

```yaml
products:
  - product_name: 云服务器 ECS
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [virtual machine compute, operating-system control, network and block-storage attachment]
    use_when: [the workload requires host-level control, legacy or specialized software needs a virtual machine]
    avoid_or_verify_when: [a managed container or function runtime would meet the need, image and maintenance ownership is unclear]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: GPU云服务器
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [accelerated virtual machine compute, GPU-backed workloads, machine-learning and graphics execution]
    use_when: [training, inference, rendering or scientific workloads require GPU acceleration]
    avoid_or_verify_when: [accelerator software compatibility or utilization is untested, managed model service would satisfy the workload]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 容器服务
    official_url: https://www.volcengine.com/docs/6460
    stable_capabilities: [managed Kubernetes clusters, node and workload orchestration, cluster networking, Kubernetes ecosystem integration]
    use_when: [teams need Kubernetes APIs and portable container orchestration, multiple services share a platform]
    avoid_or_verify_when: [the team cannot operate Kubernetes workloads, a simpler runtime meets the requirement]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 函数服务
    official_url: https://www.volcengine.com/sem
    stable_capabilities: [managed function execution, event-driven invocation, serverless scaling, function deployment]
    use_when: [short-lived or event-driven logic benefits from managed execution and demand-based scaling]
    avoid_or_verify_when: [runtime or execution constraints are unverified, the workload requires persistent local state or host control]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
  - product_name: 弹性伸缩
    official_url: https://www.volcengine.com/docs/6406
    stable_capabilities: [compute capacity adjustment, policy-driven scaling, integration with load-balanced backends]
    use_when: [virtual machine capacity must track workload demand or replace unhealthy capacity]
    avoid_or_verify_when: [scaling signals and safe drain behavior are undefined, state prevents replaceable instances]
    dynamic_fields_to_recheck: [region, price, specification, quota, SLA, version]
```

## Integration patterns

- Use load balancers and private networks as explicit ingress and isolation layers for ECS or container workloads.
- Keep container images immutable, scan and promote them through environments, and separate deployment identity from runtime identity.
- Pair autoscaling with application readiness, graceful termination, queue or load signals and downstream protection.
- Use functions for bounded event handlers; place durable state, retries and dead-letter handling in external services.
- For GPU workloads, separate data staging, job scheduling, checkpointing and model artifact publication.

## Review points

- Validate failure-domain placement and recovery when a node, zone or control dependency fails.
- Confirm requests, limits, health probes, disruption controls and safe rollout/rollback.
- Test cold start, image pull, scale-out time and dependency saturation against workload objectives.
- Check host, cluster and workload identity boundaries plus secret delivery and rotation.
- Assign ownership for patching, runtime upgrades, cluster upgrades and base images.

## Dynamic facts to recheck

For every shortlisted product, recheck `region`, `price`, `specification`, `quota`, `SLA` and `version` in the official documentation for the target account and record the query date. Also recheck instance and accelerator families, operating systems, Kubernetes and runtime support, scaling limits, networking modes, storage attachment, maintenance behavior and lifecycle notices.

## Official discovery links

- [Volcano Engine AI cloud and infrastructure overview](https://www.volcengine.com/sem)
- [Container Service documentation](https://www.volcengine.com/docs/6460)
- [Virtual Private Cloud documentation](https://www.volcengine.com/docs/6401)
- [Load Balancing documentation](https://www.volcengine.com/docs/6406)

