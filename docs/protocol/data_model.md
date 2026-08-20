# 数据模型与可追溯性

**版本：0.1.0**  
**状态：Protocol v0.1 工程试点基线**

## 1. 设计目标

数据结构必须使任一研究结果能够追溯至：

```text
Protocol → Human Decision → World → Event/Task → Snapshot
         → Execution/Patch → Review → Outcome → Pilot Lock Manifest
```

并使目标、证明或能力边界变化后，可以反向找到所有受影响的历史对象。

## 2. 核心实体

- `StudyProtocol`
- `HumanDecision`
- `DecisionRecord`
- `PilotLockManifest`
- `WorldManifest`
- `GoalContract`
- `GoalTruthTimeline`
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
- 指标代码必须能够从原始记录重新生成 Outcome；
- Coverage、弃权适当性、错误弃权和 Selective Risk 必须保留各自分子和分母，不能只存最终比例。

## 5. 七类原子 Patch

`PatchProposal.change_type` 只能取：

- `CAPABILITY_PATCH`
- `EVALUATOR_PATCH`
- `GOAL_DISCOVERY`
- `GOAL_NORMATIVE_CHANGE`
- `AUTONOMY_CHANGE`
- `ASSURANCE_CHANGE`
- `CAPABILITY_ENVELOPE_CHANGE`

每个 Patch 还必须记录 `governance_tier`、授权声明、预测接受集合变化、风险评估和回滚计划。

## 6. 关键不变量

1. `GOAL_NORMATIVE_CHANGE` 必须具备授权和生效时间；
2. `CAPABILITY_PATCH` 只能修改 Harness；
3. `CAPABILITY_ENVELOPE_CHANGE` 只能修改 Capability Envelope；
4. `GOAL_DISCOVERY` 不得改变 `G_t^*`；
5. 拒绝的 Patch 不得出现在下一 Snapshot；
6. T2/T3 高风险变化需要有效授权和独立审查；
7. T3 已部署变化需要两名不同的人类批准者；
8. 要求独立 Assurance 时，提案者不能签署最终批准；
9. Sealed 数据在解封前不得被 Experimental 或 Builder Agent 访问；
10. 所有 Execution 必须引用唯一 Snapshot；
11. Severe False Pass 必须记录不可补偿原因码；
12. 弃权/升级必须标记为 justified 或 erroneous；
13. 所有 Outcome 必须记录计算器版本和来源 Execution；
14. Pilot Lock Manifest 必须指向人类决定记录和语义基线提交；
15. Protocol v0.1 未通过 `pilot-check` 时不得用于工程试点；
16. 未通过 `freeze-check` 时不得运行确认性主实验。
