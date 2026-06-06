# Harness ERP Spring/Maven Dogfood Benchmark

## Target

- Repository: [baskduf/harness-erp](https://github.com/baskduf/harness-erp)
- Evidence commit:
  [`ef34c12517158da62032a33bb93e318c0418b6f7`](https://github.com/baskduf/harness-erp/commit/ef34c12517158da62032a33bb93e318c0418b6f7)
- Stack and framework: Java 21, Spring Boot 4.0.6, Maven wrapper, H2
- Evaluation window: 2026-06-06 dogfood benchmark
- Agent or model: Codex in Codex desktop
- Evaluation mode: harnessed-only initial benchmark
- Harness source:
  [`f06600e2baaadcc0930573409c850c11a3168ace`](https://github.com/baskduf/harness-starter-kit/commit/f06600e2baaadcc0930573409c850c11a3168ace)

This report records a Spring/Maven backend dogfood run. It is operational
evidence for harness adoption, source tracking, task outcome records, failure
memory, and gate placement. It does not prove that harness adoption improved
agent effectiveness because no pre-harness baseline exists.

## Scope

This report counts only ERP-001 through ERP-005 as comparable product-task
outcomes.

Excluded non-comparable setup run:

- `setup-2026-06-06`

Reason for exclusion: setup created the initial Spring Boot ERP MVP, adopted the
harness, corrected one generated dependency coordinate, and established source
tracking. It is useful setup evidence, but it is not a comparable product-task
run.

## Task Set

| Task ID | Scenario | Expected boundary | Common failure |
| --- | --- | --- | --- |
| `ERP-001` | Add employee search by name. | Employee controller, service, repository, DTOs, tests, task outcome, effectiveness report. | Query logic added without a service test. |
| `ERP-002` | Add purchase request amount validation. | Purchase request DTO/service/controller paths, tests, task outcome, effectiveness report. | Validation exists only at the controller boundary. |
| `ERP-003` | Add approval comment. | Approval DTOs, approval service behavior, approval entity, approval response DTO, approval tests, task outcome, effectiveness report. | Comment is returned but not persisted. |
| `ERP-004` | Add department field to employees. | Employee entity, DTOs, service, controller, employee tests, optional glossary, task outcome, effectiveness report. | Field missing from list/search response. |
| `ERP-005` | Add role-based access policy as documented behavior. | Decision record, role type, access-policy class, policy tests, optional glossary/AGENTS, task outcome, effectiveness report. | Security behavior claimed without tests or explicit deferral. |

## Results

| Metric | Baseline | Harnessed | Delta |
| --- | --- | --- | --- |
| Product-task outcomes counted | Not available | 5 | Initial benchmark only |
| Wrong-file edits | Not available | 1 in 5 tasks | Inconclusive; no baseline |
| Repeated known mistakes | Not available | 0 observed | Inconclusive; no baseline |
| First-pass verification success | Not available | 5 / 5 | Initial benchmark only |
| Drift violations detected | Not available | 0 observed | Inconclusive; no baseline |
| Human rework minutes | Not available | Unknown | Not measured |
| Reverted files | Not available | 0 observed | Inconclusive; no baseline |

## Non-Comparable Setup Runs

| Run | Reason excluded | Use in metrics |
| --- | --- | --- |
| `setup-2026-06-06` | Initial ERP MVP, harness adoption, source tracking, and Spring Boot coordinate correction. | Excluded from comparable product-task count |

## Run Log

| Condition | Task ID | Run | Verification result | Notes |
| --- | --- | ---: | --- | --- |
| harnessed-only | `setup` | 1 | pass after non-comparable setup fix | Spring Boot parent coordinate was corrected from generated `4.0.6.RELEASE` to resolvable `4.0.6`; failure memory now records the check. |
| harnessed-only | `ERP-001` | 1 | first pass and final pass | Added case-insensitive employee search through the service/repository boundary. |
| harnessed-only | `ERP-002` | 1 | first pass and final pass | Added service-layer positive amount validation. |
| harnessed-only | `ERP-003` | 1 | first pass and final pass | Added persisted approval/rejection comments with blank-to-null normalization. |
| harnessed-only | `ERP-004` | 1 | first pass and final pass | Added required employee department field; fixture-only edits in approval and purchase request tests were counted as a boundary miss. |
| harnessed-only | `ERP-005` | 1 | first pass and final pass | Added documented and tested role access policy while intentionally deferring runtime HTTP security. |

## Changed-Files Consistency

| Task ID | Expected boundary | Actual changed files | Wrong-file edit result |
| --- | --- | --- | --- |
| `ERP-001` | Employee controller, service, repository, tests, task outcome, effectiveness report | Employee controller, repository, service, service test, effectiveness report, task outcome | false |
| `ERP-002` | Purchase request DTO/service/controller/entity paths as needed, tests, task outcome, effectiveness report | Create purchase request DTO, purchase request service, service test, effectiveness report, task outcome | false |
| `ERP-003` | Approval controller/domain/DTO/service/test paths, task outcome, effectiveness report | Approval controller, approval entity, approval request/response DTOs, approval service, service test, effectiveness report, task outcome | false |
| `ERP-004` | Employee entity/DTO/service/controller/repository as needed, employee tests, optional glossary, task outcome, effectiveness report | Employee files, employee service test, glossary, effectiveness report, task outcome, plus fixture-only edits in approval and purchase request service tests | true |
| `ERP-005` | Decision record, policy code/tests, optional glossary/AGENTS, task outcome, effectiveness report | AGENTS.md, role policy decision, glossary, `AccessPolicy`, `Role`, `AccessPolicyTest`, effectiveness report, task outcome | false |

## Source Records

- Adoption and setup evidence:
  - [adoption report](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/harness/adoption-report.md)
  - [Harness Doctor setup baseline](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/harness/harness-doctor-setup.md)
  - [source tracking](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/.harness/source.json)
- Task outcome records reviewed:
  - [ERP-001 employee search](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/effectiveness/task-outcomes/ERP-001-employee-search.yaml)
  - [ERP-002 purchase request amount validation](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/effectiveness/task-outcomes/ERP-002-purchase-request-amount-validation.yaml)
  - [ERP-003 approval comment](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/effectiveness/task-outcomes/ERP-003-approval-comment.yaml)
  - [ERP-004 employee department field](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/effectiveness/task-outcomes/ERP-004-employee-department-field.yaml)
  - [ERP-005 role-based access policy](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/effectiveness/task-outcomes/ERP-005-role-based-access-policy.yaml)
- Failure memory reviewed:
  - [Spring Boot coordinate resolution](https://github.com/baskduf/harness-erp/blob/ef34c12517158da62032a33bb93e318c0418b6f7/docs/failures/0001-spring-boot-coordinate-resolution.md)
- Repository refs compared:
  - setup commit `a1521406f443d3a5a9d2c86bb987658068afafd8`
  - final evidence commit `ef34c12517158da62032a33bb93e318c0418b6f7`
- Prompt refs compared: local prompt files from 2026-06-06 with recorded
  SHA-256 hashes in each task outcome record.
- Verification commands compared:
  - `python scripts/check_harness.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_effectiveness_plan.py`
  - `python /Users/wb/Desktop/harness-starter-kit/scripts/check_failure_memory.py`

## Interpretation

### Observed benchmark

The Harness ERP dogfood run produced five harnessed-only product-task
observations. All five product tasks passed first verification and final
verification. One task, ERP-004, recorded fixture-only edits outside the strict
expected boundary and counted them as a wrong-file edit instead of hiding the
boundary miss.

### What improved

No improvement claim is made. This report has no comparable pre-harness
baseline or later comparison window.

### What did not improve

Human rework minutes were not measured. The run therefore cannot assess whether
review effort decreased. The benchmark also uses one small Spring Boot target,
so the result does not generalize to larger backend systems by itself.

### Confounders or limitations

- This is a harnessed-only initial benchmark, not a controlled experiment.
- The setup run is excluded from product-task metrics.
- The sample size is small.
- Prompt files were local artifacts; task outcome records preserve prompt
  hashes, but the prompt text is not stored in this kit.
- Harness Doctor scored the target at 67/100 after cleanup. That is a target
  readiness signal, not effectiveness evidence.

### Narrow claim

This report establishes an initial Spring/Maven backend dogfood benchmark for
source tracking, task outcome completeness, failure-memory linkage, gate
placement, boundary adherence, and first-pass verification.

It does not prove that harness adoption improved agent effectiveness.

### Human rework interpretation

Human rework is unknown, not 0. Future runs should record reviewer time or
review findings if the project wants to evaluate rework cost.

## Follow-Up

- Next review window: next 3-5 comparable Spring/Maven product tasks or a
  repeated ERP task set under a later harness revision.
- Owner or reviewer: maintainer or dogfood reviewer.
- Related decision or failure records: Harness ERP architecture decision,
  role-based access policy decision, Spring Boot coordinate failure record, and
  ERP-001 through ERP-005 task outcome records.
- Harness changes to make next: consider a consistency checker for aggregate
  effectiveness-report contradictions and template outcome inclusion flags.
