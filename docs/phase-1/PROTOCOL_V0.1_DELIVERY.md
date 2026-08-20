# Protocol v0.1 交付说明

## 1. 交付定位

第一阶段交付物是 **Protocol v0.1（Pilot-Locked Engineering Baseline）**。

它是一份已经获得人类规范性决定、能够由程序校验、可用于工程试点的协议基线；它不是正式主实验的最终预注册，也不是研究结论。

## 2. 已完成

- 人类 D001–D014 决定的来源、原文和实施记录；
- 系统状态、外部 World State、Authority Graph 和 `G_t^*` 的形式化；
- 七类原子变更及 Capability Envelope 独立分类；
- T0–T3 工程试点风险分级授权；
- 六类不可补偿 Severe False Pass 原因；
- 反“通过弃权获得安全”的指标体系；
- Track A-H1、H2、H3 的工程试点 estimand；
- 层级结论和 Track A/Track B 外推边界；
- 版本化 JSON Schema 和跨对象不变量；
- 员工报销完整 Fixture；
- 84 个非 Gold 候选分类案例和 28 个盲化人工编码案例；
- CLI、单元测试、CI、追溯矩阵和 Pilot Lock Manifest；
- 人类—Agent 协作开发宪章。

## 3. 交付验收命令

```bash
python -m pip install -e '.[dev]'
python -m goalevo_protocol.cli validate
python -m goalevo_protocol.cli decisions
python -m goalevo_protocol.cli pilot-check
pytest -q
```

`pilot-check` 必须通过。

`freeze-check` 在 v0.1 必须继续失败，因为正式确认性条件尚未满足。CI 会把“意外通过 confirmatory freeze”视为错误，而不是进展。

## 4. 确认性冻结前的剩余工作

- 完成盲化工程试点；
- 冻结 H2 数值化 `delta`；
- 完成统计功效分析；
- 冻结正式模型公式、排除和重跑规则；
- 指定独立 Methods / Statistics Lead；
- 指定 Independent Custodian；
- 生成并密封最终测试；
- 形成新的 Confirmatory Freeze Manifest。

## 5. 版本边界

后续修复实现错误而不改变规范性含义，可以发布 `0.1.x`。

改变 D001–D013 的含义、主要 estimand、分母、非劣界限程序或风险红线，必须形成 Protocol Amendment；不能以普通代码修复名义悄悄生效。
