# GoalEvo

**Goal-Governed Self-Evolution / 目标治理的自进化**

GoalEvo 研究如何判断一个能够修改自身 Harness、评价器、目标建议、自治权限和证明规则的智能系统，究竟是获得了真实能力提升，还是通过改变“什么算成功”制造了表面进步。

本仓库当前处于 **Phase 1：研究协议与数据语义冻结前的 Draft 阶段**。本阶段不运行确认性主实验，也不声称任何研究假设已得到支持。

## 当前阶段目标

Phase 1 建立后续 Track A 受控 Benchmark 的共同测量基础：

1. 形式化系统状态、真实目标、可见目标、评价器和能力变化；
2. 冻结六类变更分类与原子 Patch 规则；
3. 将 Track A-H1、H2、H3 写成可证伪的 estimand；
4. 建立版本化、可审计、可重放的数据 Schema；
5. 建立人类—Agent 决策权、审批、审计与 Protocol Freeze 机制。

## 重要状态

- `protocol_status`: **draft**
- `human_decision_gate`: **open**
- `sealed_test`: **not_created**
- `confirmatory_experiment`: **not_authorized**

只有当 `governance/human-decisions/phase-1.yaml` 中所有阻塞性决定得到有权人类批准，并通过独立审查后，协议才可以从 `draft` 晋级为 `frozen`。

## 仓库结构

```text
docs/
  HUMAN_AGENT_COLLABORATION_CHARTER.md
  protocol/                 # 形式化、分类、假设、指标与冻结策略
  phase-1/                  # 人类决策包、Agent 工作报告与追溯矩阵
governance/
  human-decisions/          # 规范性决定及签署状态
  templates/                # Work Order、Decision Record、Amendment 模板
schemas/                    # JSON Schema Draft 2020-12
fixtures/reimbursement-v0/  # 员工报销微型世界的最小完整 Fixture
taxonomy_cases/             # 变更分类候选案例与人工编码批次
src/goalevo_protocol/       # 校验、决策 Gate、派生指标与 CLI
tests/                      # 单元与跨对象不变量测试
```

## 你现在需要完成的工作

请先阅读：

- [`docs/phase-1/HUMAN_DECISION_PACKET.md`](docs/phase-1/HUMAN_DECISION_PACKET.md)
- [`governance/human-decisions/phase-1.yaml`](governance/human-decisions/phase-1.yaml)

对每个决定填写：

```yaml
decision: approve | modify | reject | defer
human_rationale: "你的理由"
approved_by: "姓名或 GitHub 账号"
approved_at: "ISO-8601 时间"
```

`defer` 不等于批准；阻塞性决定仍为 `defer` 时，协议不得冻结。

## 本地验证

需要 Python 3.11+。

```bash
python -m pip install -e '.[dev]'
goalevo decisions
goalevo validate
pytest
```

标准命令：

```bash
python -m goalevo_protocol.cli decisions
python -m goalevo_protocol.cli validate
pytest -q
```

当前 Draft 的预期行为是：Schema、Fixture 和测试通过，但 `decisions` 会报告尚未完成的人类决定，`freeze-check` 会失败。

## 科学与治理原则

- 目标、自治权限、证明标准和能力边界分开治理；
- 提出、执行、评价、批准不得由同一主体独占；
- 可由程序判断的事项优先使用固定程序；
- 失败运行、不利证据和被拒绝 Patch 必须保留；
- Experimental Agent 不得访问隐藏真实目标、Gold 标签或密封测试；
- 任何正式结论必须与预注册范围和证据覆盖相匹配。

详见 [`docs/HUMAN_AGENT_COLLABORATION_CHARTER.md`](docs/HUMAN_AGENT_COLLABORATION_CHARTER.md)。

## License

尚未由人类项目负责人决定。本仓库在许可证明确前不授予额外许可。
