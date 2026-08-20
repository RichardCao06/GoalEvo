# 数据模型与可追溯性

**版本：0.1-draft**

## 1. 设计目标

数据结构必须使任一研究结果能够追溯至：

```text
Protocol → World → Event/Task → Snapshot → Execution/Patch → Review → Outcome
```

并使目标变化后可以反向找到所有受影响的历史对象。

## 2. 核心实体

- `StudyProtocol`
- `HumanDecision`
- `WorldManifest`
- `GoalContract`
- `AuthorityGraph`
- `Event`
- `TaskInstance`
- `PatchProposal`
- `ReviewDecision`
- `Snapshot`
- `Run`
- `TaskExecution`
- `OutcomeRecord`

对应 Schema 位于 `schemas/`。

## 3. 通用字段

所有版本化对象应尽量具有：

```text
id, version, parent_version, status, created_at, effective_from,
effective_until, created_by, source_ids, content_hash, visibility
```

## 4. 原始与派生数据

- Task、Event、Patch、Review、Snapshot 和 Execution 是原始研究记录；
- `OutcomeRecord` 是可重算的派生结果；
- 派生数据不得覆盖原始记录；
- 指标代码必须能够从原始记录重新生成 Outcome。

## 5. 关键不变量

1. `GOAL_NORMATIVE_CHANGE` 必须具备授权和生效时间；
2. `CAPABILITY_PATCH` 只能修改 Harness；
3. `GOAL_DISCOVERY` 不得改变 `G_t^*`；
4. 拒绝的 Patch 不得出现在下一 Snapshot；
5. 要求独立 Assurance 时，提案者不能签署最终批准；
6. Sealed 数据在解封前不得被 Experimental 或 Builder Agent 访问；
7. 所有 Execution 必须引用唯一 Snapshot；
8. 所有 Outcome 必须记录计算器版本和来源 Execution；
9. 协议未通过 Human Decision Gate 时不得标为 `frozen`。
