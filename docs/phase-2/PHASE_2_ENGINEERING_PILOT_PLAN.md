# Phase 2：Engineering Pilot / 工程试点计划

**状态：scaffold-ready**  
**依据：Protocol v0.1（Pilot-Locked Engineering Baseline）**  
**允许用途：非确认性的工程验证**

## 1. 阶段目标

Phase 2 不检验 H1–H3 是否成立，而是检验：

1. 两个受控微型世界能否由同一运行器加载；
2. M0–M3 是否只通过治理开关区分，而非获得不同模型、工具或预算；
3. Experience、Update Validation、Replay、ID 与 OOD 数据能否保持隔离；
4. 每代 Task、Event、Patch、Review、Snapshot、Execution 与 Outcome 能否完整重放；
5. H1–H3 及反“安全靠弃权”指标的分子、分母能否自动生成；
6. 隐藏目标、方法标签和未来密封材料是否存在泄漏路径；
7. 任务是否出现严重天花板、地板、无限弃权或无法产生变更机会的问题。

任何 Phase 2 结果都不得用于声称目标治理更安全、更有效或更适应。它只用于修正工程实现、估计方差并准备 Protocol v0.2。

## 2. 人类与 Agent 的边界

### Agent 可以自主执行

- 构建数据访问权限微型世界；
- 实现统一方法配置、确定性参考策略和运行编排；
- 生成非 Gold 的候选任务、事件和边界案例；
- 运行不产生外部费用的确定性参考试验；
- 建立 Schema、验证器、指标计算、日志和 CI；
- 检查预算公平、数据泄漏、版本和重放一致性；
- 形成供人类决策的候选参数、风险和替代方案。

### 必须由人类确认

- 使用哪个真实模型、服务商和固定版本；
- 是否允许外部 API、数据保留和日志上传；
- 付费上限、token/call/time 预算；
- 试点规模、方法组和随机化方案；
- 允许 Agent 修改的 Harness 表面和每代 Patch 上限；
- 人工编码者、盲化人员和方法标签保管人；
- 何种结果触发停止、回滚或重新设计；
- 是否正式启动任何真实模型调用。

## 3. Agent 已完成的工程范围

本 PR 提供：

- `data-access-v0` 合成受控世界；
- M0–M3 的统一方法语义；
- 不依赖模型 API 的确定性 reference runner；
- reference-only 场景与结果；
- Phase 2 Human Decision Gate；
- scaffold/live 两级 Gate；
- reference result Schema 与验证；
- CI 中的“reference 可运行、live 必须保持关闭”检查。

## 4. 推荐的真实工程试点候选设计

以下只是等待人类批准的默认方案：

| 项目 | 建议默认值 |
|---|---|
| 世界 | 员工报销、数据访问权限 |
| 方法 | M0、M1、M2、M3 |
| 代数 | 3 代 |
| 随机种子 | 3 个 |
| 每世界每代 Experience | 8–12 个任务 |
| Validation / Replay | 每代各 8–12 个 |
| ID / OOD | 每世界各 20–30 个 |
| Patch 上限 | 每代 3 个原子 Patch |
| 用途 | 工程调试和方差估计，不做确认性检验 |

## 5. 阶段性交付

Phase 2 Scaffold PR 完成后，项目进入“等待人类 live-pilot 决策”的状态。人类决定完成后，Agent 可在独立 PR 中接入已选模型并运行真实工程试点。

Phase 2 完成的最终标志不是某种方法得分更高，而是形成：

- 可重复的多方法运行器；
- 两个稳定微型世界；
- 盲化分类一致性结果；
- 试点方差和成本报告；
- Protocol v0.2 的人类决策包；
- 明确的 Confirmatory Freeze 阻塞项。
