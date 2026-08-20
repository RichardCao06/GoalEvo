# Protocol Lock、Freeze 与 Amendment 策略

## 1. 两个不同 Gate

### Protocol v0.1 — Pilot-Locked Engineering Baseline

在人类 D001–D013 决定完成并被一致地落实到文档、Schema、Fixture 和测试后，v0.1 可以锁定为工程试点基线。

它冻结：

- 研究对象和状态本体；
- 七类变更及原子 Patch；
- Severe False Pass 红线；
- 风险分级授权的工程默认规则；
- H1–H3 的问题方向、主要比较和工程试点 estimand；
- 反无限弃权的指标和分母；
- 数据语义、追溯和角色边界。

它不授权正式确认性主实验。

### Confirmatory Frozen

正式主实验前还必须冻结：

- H2 数值化非劣界限；
- 样本与功效方案；
- 正式统计公式；
- 排除与重跑规则；
- 独立 Methods / Statistics Lead；
- Independent Custodian；
- Sealed Test 生成、保管和解封程序；
- 所有确认性代码与配置哈希。

## 2. `pilot-check`

`goalevo pilot-check` 至少检查：

- 所有阻塞性人类决定已批准或明确修改；
- Research Owner、工程试点 Domain Lead 和 Data Steward 已有可追责身份；
- 协议状态为 `pilot_locked`；
- Schema 和 Fixture 通过；
- 测试通过；
- Pilot Lock Manifest 指向语义基线 Git 提交；
- 当前授权范围仅为 `engineering_pilot`。

## 3. `freeze-check`

`goalevo freeze-check` 用于正式确认性冻结，除全部 Pilot Gate 外还检查：

- 全部独立角色已补齐；
- Research Owner 与 Independent Custodian 不同；
- 数值化非劣界限已冻结；
- 正式统计和样本方案已冻结；
- Sealed Test 已创建并处于密封状态；
- 当前授权范围为 `confirmatory_experiment`；
- 协议状态为 `frozen`。

v0.1 应通过 `pilot-check`，但应继续无法通过 `freeze-check`。

## 4. Amendment

每项 Amendment 必须说明：

- 为什么修改；
- 修改了哪些人类决定、文件、Schema、指标和测试；
- 是否查看过试点或主结果；
- 对工程试点和确认性结论的影响；
- 是否需要重新分析或新 Sealed Test；
- 谁提出、谁审查、谁批准。

改变 D001–D013 的规范性含义不能作为普通代码修复静默生效。
