# Protocol Freeze 与 Amendment 策略

## 1. 三个阶段

### v0.1 Concept Draft

允许修改概念、分类和 Schema，但每次修改必须留记录。不得运行确认性主实验。

### v0.2 Pilot-Locked

完成工程试点后冻结：

- 主要 estimand；
- 非劣界限数值；
- 样本与功效方案；
- 正式统计公式；
- 排除与重跑规则；
- Sealed Test 生成和保管程序。

### v1.0 Confirmatory Frozen

正式主实验前冻结所有确认性内容和代码哈希。之后改变主要假设、指标、分母、样本或测试，只能通过 Protocol Amendment，并将受影响结果降为探索性或重新开展独立确认。

## 2. Freeze Gate

`goalevo freeze-check` 至少检查：

- 所有阻塞性人类决定已批准或明确修改；
- 角色签署完整；
- Schema 和 Fixture 通过；
- 测试通过；
- 无未解决高风险审计项；
- 协议状态与版本一致；
- Sealed 数据访问策略已记录。

## 3. Amendment

每项 Amendment 必须说明：

- 为什么修改；
- 修改了哪些文件、Schema、指标和测试；
- 是否查看过主结果；
- 对确认性结论的影响；
- 是否需要重新分析或新密封测试；
- 谁提出、谁审查、谁批准。
