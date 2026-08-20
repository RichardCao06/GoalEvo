# Phase 1 人类决定状态

**协议版本：Protocol v0.1 / 0.1.0**  
**状态：D001–D013 已记录并实施；D014 暂缓**  
**决定来源：** PR #1 comment `5351814513`

## 1. 当前结论

人类项目负责人已经完成本阶段的规范性判断。它们已被转写为：

- `governance/human-decisions/phase-1.yaml`：机器可读 Gate；
- `governance/decision-records/phase-1-v0.1.yaml`：保留人类原意和实施影响的决策记录；
- `docs/protocol/PROTOCOL_V0.1.md`：面向研究人员的统一协议；
- Schema、Fixture、不变量、指标和测试中的可执行约束。

本文件不再用于征集 D001–D013 的初次决定。后续改变其规范性含义必须提交 Protocol Amendment。

## 2. 已批准的核心方向

1. 安全底线优先，但不得通过无限弃权获得安全；
2. `H、E、G、A、R、C` 独立保存，World State 和 Authority Graph 位于系统之外；
3. `G_t^*` 是受控世界中的时间索引操作性规范真值；
4. Goal Discovery 与 Goal Normative Change 严格分开；
5. 不可补偿红线包含关键证据、授权和审计记录篡改；
6. 使用七类原子变更，Capability Envelope 独立成类；
7. 使用按风险分级的授权制度；
8. H1 以实际部署的未授权放宽为主要结果；
9. H2 先冻结 `delta` 的盲化确定程序；
10. H3 测量合法变化后的真实恢复，而不是 Patch 数量；
11. H1 是安全 Gate，H1–H3 全部成立也只支持 Track A；
12. 当前只授权工程试点，正式主实验前补齐独立统计负责人和密封测试保管人；
13. 首批微型世界为员工报销和数据访问权限；
14. 许可证决定暂缓，敏感、Gold 和 Sealed 材料不得上传。

## 3. 当前可以做什么

Protocol v0.1 允许：

- 开发和校验协议、Schema、Oracle、Fixture 与实验 Harness；
- 实现员工报销和数据访问权限微型世界；
- 运行明确标记为非确认性的工程试点；
- 估计任务方差、发现 Schema 缺陷、检验指标可计算性；
- 为下一阶段的功效分析和正式预注册准备数据。

## 4. 当前不能做什么

Protocol v0.1 不允许：

- 将工程试点结果作为 H1–H3 的正式确认性检验；
- 根据试点中的方法表现改变 H1–H3 的方向或主要分母；
- 宣称数值化非劣界限已经冻结；
- 创建、读取或解封正式 Sealed Test；
- 宣称 Track A 或 Track B 的科学主张已经得到支持；
- 将 D014 的暂缓解释为授予开源许可证。

## 5. 下一次需要人类介入的节点

在工程试点完成后，需要由人类完成或确认：

- 独立 Methods / Statistics Lead；
- H2 的数值化非劣界限；
- 样本规模、功效和正式统计公式；
- Independent Custodian；
- Sealed Test 的生成、保管与解封程序；
- 是否将协议晋级为正式确认性冻结版本。
