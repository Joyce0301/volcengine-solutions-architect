# Task 7 Report: Forward Skill Scenarios

## Outcome

Completed forward testing for all six frozen scenarios with fresh child-agent responses using the worktree-local `design-volcengine-architecture` Skill. The first run exposed two systemic failures:

- responses did not make the requirements gap block the first observable content;
- dynamic-fact handling was not validator-compatible, and the validator also falsely matched `TPS` inside `https://`.

Applied the smallest repairs to the Skill and validator, reran affected scenarios, and persisted the best fresh post-repair raw outputs.

Fix round 1 status on 2026-08-09: local validator and Skill contracts were tightened after review, but fresh scenario regeneration was stopped before any new affected output completed. The existing forward files are therefore not all valid under the stricter validator. This report preserves that provenance and does not mark the affected scenarios as PASS.

## Artifacts

- `tests/forward/ai-agent.md`
- `tests/forward/cloud-native.md`
- `tests/forward/realtime-data.md`
- `tests/forward/media.md`
- `tests/forward/intelligent-service.md`
- `tests/forward/regulated-finance.md`
- `tests/forward/collection-provenance.md`
- `volcengine-architecture/skills/design-volcengine-architecture/SKILL.md`
- `volcengine-architecture/skills/design-volcengine-architecture/scripts/validate-deliverable.py`
- `tests/test_validate_deliverable.py`

## Child provenance

The final persisted runs are recorded in `tests/forward/collection-provenance.md` with child agent name, timestamp, session log line, literal prompt, and SHA-256 of the raw response before observations.

Final child outputs used:

- `ai-agent`: `/root/task7_forward/rerun_ai_agent_final`
- `cloud-native`: `/root/task7_forward/rerun_cloud_native`
- `realtime-data`: `/root/task7_forward/rerun_realtime_data`
- `media`: `/root/task7_forward/rerun_media`
- `intelligent-service`: `/root/task7_forward/rerun_intelligent_service`
- `regulated-finance`: `/root/task7_forward/rerun_regulated_finance`

Discarded or unused child runs:

- Initial pre-repair runs were preserved only as measurement context, then replaced by fresh post-repair outputs.
- `/root/forward_intelligent_service_final` was persisted as the sixth pre-repair artifact before the repair cycle, then superseded by `/root/task7_forward/rerun_intelligent_service`.
- `/root/task7_forward/rerun_cloud_native_final` hung after the final validator wording repair and was interrupted; its output was not used.

## Repairs

Skill repair:

- Required `## Requirements gap check` as the first visible content before questions, summary, routing, products, topology, or recommendations.
- Kept the existing twelve-section final proposal after that preface so the structural validator contract remains intact.
- Clarified dynamic/current fact handling: assert dynamic values only with official `volcengine.com` evidence and `Retrieved: YYYY-MM-DD` in the same paragraph/table cell; otherwise use unknown/runtime-verification wording without trigger terms.
- Required every product mapping evidence cell to include official URL plus retrieval date.

Validator repair:

- Changed dynamic detection from substring matching to word-boundary matching for English trigger terms.
- Added regression coverage so ordinary `https://www.volcengine.com/...` URLs do not trigger `TPS` detection.
- Added product mapping validation requiring every evidence cell to include an official Volcengine URL and retrieval date.
- Added routing validation requiring a fenced `routing:` record before `## Architecture decisions`.
- Added regression coverage for plural dynamic terms: `prices`, `regions`, `SLAs`, and `quotas`.

Reference repair:

- Added official discovery entries for realtime event intake/buffering/query-serving products in `data-analytics.md`.
- Added ASR/TTS product candidates in `ai-and-agent.md`.
- Added content moderation product candidates in `media-edge.md`.

Fresh rerun status:

- `/root/finish_task7_fix/rerun_cloud_native_fix`: interrupted after user instruction to stop long-running generation; no output persisted.
- `/root/finish_task7_fix/rerun_realtime_data_fix`: interrupted after user instruction to stop long-running generation; no output persisted.
- `/root/finish_task7_fix/rerun_regulated_finance_fix`: interrupted after user instruction to stop long-running generation; no output persisted.
- `media` and `intelligent-service`: no new rerun started before the stop instruction.

## Forward observations

Historical Task 7 observation blocks remain in the persisted forward files. Under the stricter fix-round validator, those observation PASS lines are no longer sufficient completion evidence for the affected files:

- Requirements gap list before solution
- Only architecture-changing questions
- Facts separated from assumptions
- Product alternatives and switch conditions
- Security, reliability, observability, and cost covered
- Official evidence and retrieval dates
- Production-readiness claim appropriately bounded

The six scenarios all identify critical open gaps and mark readiness as `NOT READY`. High-risk cases include independent security/reliability review content. Material scale/cost cases include FinOps findings. However, cloud-native, media, realtime-data, and regulated-finance require fresh regenerated outputs or provenance-preserving replacements before they can be counted as validated under fix round 1.

## Verification

```text
python3 -m unittest tests/test_validate_deliverable.py
............
----------------------------------------------------------------------
Ran 12 tests in 0.003s

OK
```

```text
tests/forward/ai-agent.md
VALID
tests/forward/cloud-native.md
missing routing record before architecture decisions
product mapping evidence lacks official URL and retrieval date
tests/forward/intelligent-service.md
VALID
tests/forward/media.md
missing routing record before architecture decisions
tests/forward/realtime-data.md
missing routing record before architecture decisions
tests/forward/regulated-finance.md
product mapping evidence lacks official URL and retrieval date
```

Current stop condition: blocked by the explicit instruction to stop fresh scenario generation. The local validator/Skill/reference fixes are verified by unit tests; the forward scenario artifacts require fresh reruns or provenance-preserving replacement before the stricter six-file validator suite can pass.

```text
tests/forward/ai-agent.md first=## Requirements gap check
tests/forward/cloud-native.md first=## Requirements gap check
tests/forward/realtime-data.md first=## Requirements gap check
tests/forward/media.md first=## Requirements gap check
tests/forward/intelligent-service.md first=## Requirements gap check
tests/forward/regulated-finance.md first=## Requirements gap check
```

```text
tests/forward/ai-agent.md observations=1 pass_lines=7
tests/forward/cloud-native.md observations=1 pass_lines=7
tests/forward/realtime-data.md observations=1 pass_lines=7
tests/forward/media.md observations=1 pass_lines=7
tests/forward/intelligent-service.md observations=1 pass_lines=7
tests/forward/regulated-finance.md observations=1 pass_lines=7
```
