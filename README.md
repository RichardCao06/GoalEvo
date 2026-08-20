# GoalEvo

**Goal-Governed Self-Evolution / 目标治理的自进化**

GoalEvo 研究如何判断一个能够修改自身 Harness、评价器、目标建议、自治权限、证明规则和能力边界的智能系统，究竟是获得了真实能力提升，还是通过改变“什么算成功”制造了表面进步。

## 当前状态

第一阶段已交付 **Protocol v0.1（Pilot-Locked Engineering Baseline）**。人类 D001–D013 决定已经记录并实施，D014 许可证决定暂缓；工程试点基线由独立 Git 提交证明锁定。

- `protocol_version`: **0.1.0**
- `protocol_status`: **pilot_locked**
- `authorized_scope`: **engineering_pilot**
- `human_decision_gate`: **satisfied for pilot**
- `semantic_baseline_commit`: **5694556bda79ea14c9d3380969f688c8af7304cd**
- `confirmatory_experiment`: **not authorized**
- `sealed_test`: **not created**

## Protocol v0.1 的含义

v0.1 允许开发受控微型世界、Schema、Oracle、Harness 和运行器，也允许开展明确标记为非确认性的工程试点。

v0.1 **不是**正式主实验的最终预注册。以下事项仍会阻止 confirmatory freeze：

- H2 数值化非劣界限；
- 样本规模和功效方案；
- 正式统计公式、排除和重跑规则；
- 独立 Methods / Statistics Lead；
- Independent Custodian；
- Sealed Test。

## 已锁定的研究基础

1. 系统状态 `Σ_t=(H_t,E_t,G_t,A_t,R_t,C_t)` 与外部 World State、Authority Graph、`G_t^*` 分离；
2. 七类原子 Patch，包括独立的 `CAPABILITY_ENVELOPE_CHANGE`；
3. T0–T3 风险分级授权；
4. 不可补偿 Severe False Pass 与证据/授权/审计篡改红线；
5. H1 安全、H2 效用非劣、H3 合法适应的工程试点 estimand；
6. 反“通过无限弃权获得安全”的 Coverage、Abstention Precision、Erroneous Abstention Rate 和 Selective Risk；
7. 版本化、可审计、可重放的数据 Schema；
8. 人类—Agent 的决策权、审批和审计边界。

## 仓库结构

```text
docs/
  HUMAN_AGENT_COLLABORATION_CHARTER.md
  protocol/                    # 统一协议、形式化、分类、假设、指标与冻结策略
  phase-1/                     # 人类决定状态、交付说明、工作报告与追溯矩阵
governance/
  human-decisions/             # 机器可读人类决定 Gate
  decision-records/            # 人类决定来源与实施记录
  freeze-manifests/            # Pilot Lock / Confirmatory Freeze 证明
  templates/                   # Work Order、Decision Record、Amendment 模板
protocol/                      # 机器可读 StudyProtocol
schemas/                       # JSON Schema Draft 2020-12
fixtures/reimbursement-v0/     # 员工报销微型世界完整 Fixture
taxonomy_cases/                # 84 个非 Gold 候选案例与 28 个盲化人工编码案例
src/goalevo_protocol/          # 校验、Gate、派生指标与 CLI
tests/                         # 单元与跨对象不变量测试
```

## 验收命令

需要 Python 3.11+。

```bash
python -m pip install -e '.[dev]'
python -m goalevo_protocol.cli validate
python -m goalevo_protocol.cli decisions
python -m goalevo_protocol.cli pilot-check
pytest -q
```

正式确认性条件使用：

```bash
python -m goalevo_protocol.cli freeze-check
```

在 v0.1 中，`freeze-check` 应继续失败；它用于证明项目没有把工程试点误写成正式确认性实验。

## 关键文档

- [`docs/protocol/PROTOCOL_V0.1.md`](docs/protocol/PROTOCOL_V0.1.md)
- [`docs/phase-1/PROTOCOL_V0.1_DELIVERY.md`](docs/phase-1/PROTOCOL_V0.1_DELIVERY.md)
- [`governance/decision-records/phase-1-v0.1.yaml`](governance/decision-records/phase-1-v0.1.yaml)
- [`governance/freeze-manifests/protocol-v0.1.yaml`](governance/freeze-manifests/protocol-v0.1.yaml)
- [`docs/HUMAN_AGENT_COLLABORATION_CHARTER.md`](docs/HUMAN_AGENT_COLLABORATION_CHARTER.md)

## License

D014 已暂缓。在人类正式决定前，本仓库不新增许可证，也不授予超出适用法律默认范围的额外许可。代码许可证、公开数据许可、Gold 隐藏目标和 Sealed 材料分别治理。
