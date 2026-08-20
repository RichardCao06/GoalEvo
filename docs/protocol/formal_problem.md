# GoalEvo 形式化问题说明

**版本：0.1.0**  
**状态：Pilot-Locked**  
**人类决定：D001–D004**

## 1. 中心研究问题

当系统能够持续修改 Harness、Evaluator、Goal 建议、Autonomy、Assurance 和 Capability Envelope 时，如何：

1. 区分真实能力提升与成功标准变化；
2. 允许系统发现不完整目标；
3. 吸收合法的规范性变化；
4. 阻止未经授权的目标、权限、证明或能力范围放宽；
5. 防止系统通过无限弃权制造低错误率；
6. 将每次性能变化归因到正确层级。

## 2. 系统状态与外部世界

第 `t` 代可部署系统快照：

\[
\Sigma_t=(H_t,E_t,G_t,A_t,R_t,C_t)
\]

| 符号 | 含义 |
|---|---|
| `H_t` | Harness：提示词、工具、检索、记忆、工作流和代码配置 |
| `E_t` | Evaluator：对当前可见目标的测量和判定实现 |
| `G_t` | Goal Contract：当前可见的成功条件、红线、例外和诚实不完整状态 |
| `A_t` | Autonomy Contract：系统可自主执行的工具、数据、写入、发布和批准范围 |
| `R_t` | Assurance Contract：结果需要什么证据、独立性和签署 |
| `C_t` | Capability Envelope：当前系统在哪些任务与风险范围内经过验证 |

独立于系统快照保存：

- `W_t`：环境事实、角色、政策和时间状态；
- `Auth_t`：谁可以提出、批准、撤销和部署哪些变化；
- `G_t^*`：研究者为受控世界预先冻结、按时间有效、对 Experimental Agent 隐藏的操作性规范真值。

`G_t^*` 不被声称为普遍道德真理。它只是在该受控世界中用于确定性评价的完整规则。

## 3. 三个接受集合

- `Acc(G_t^*)`：当前完整规范真值允许的结果；
- `Acc(G_t)`：当前可见 Goal Contract 允许的结果；
- `Acc(E_t)`：当前 Evaluator 实际判为通过的结果。

由此定义：

### 目标理解差距

\[
D_G(t)=Acc(G_t)\triangle Acc(G_t^*)
\]

### 评价器差距

\[
D_E(t)=Acc(E_t)\triangle Acc(G_t)
\]

### 能力差距

即使 `G_t` 和 `E_t` 正确，`H_t` 是否能产生满足 `G_t^*` 的结果。

## 4. 四种关键变化

### 能力提升

固定 `G_k^*`、任务集和独立 Oracle，仅更换 Harness 后真实效用上升：

\[
\Delta U_H=U^*(H_{t+1};G_k^*,D)-U^*(H_t;G_k^*,D)
\]

### Evaluator 修复

`G_t` 不变，`E_t` 更准确地实现 `G_t`。这不是 Goal 变化。

### Goal Discovery

\[
G_{t+1}^*=G_t^*
\]

真实规范没有变化；系统通过足够证据发现原先遗漏的既有要求。

### Goal Normative Change

\[
G_{t+1}^*\neq G_t^*
\]

法规、正式政策或有权主体使真实有效规则发生变化。任务失败或提高完成率的需要只能触发调查和提案，不能自行改变 `G_t^*`。

## 5. 总体变化归因

观察到的总表现变化应拆解为：

\[
\Delta U_{observed}
=
\Delta U_H
+
\Delta U_G
+
\Delta U_E
+
\Delta U_A
+
\Delta U_R
+
\Delta U_C
+
\text{interaction}
\]

其中 `A、R、C` 的变化可能提高完成率，却不等同于能力提升。

系统版本 × 目标版本的交叉评价用于固定一部分状态、改变另一部分状态，从而获得可识别的归因证据。

## 6. 任务、事件和轨迹单位

- `Task`：一次业务请求；
- `Event`：政策、审计、投诉、授权或新证据；
- `PatchProposal`：一次原子修改提案；
- `Generation`：经验—诊断—修改—验证—晋级循环；
- `Run / Trajectory`：某方法在某世界、模型和随机种子下的完整运行。

同一 Run 内任务不能被假装为完全独立样本。

## 7. 安全不能由弃权伪造

设：

- `N` 为可评分任务机会；
- `A` 为系统自主给出成功/失败决定的任务；
- `D` 为弃权或升级给人的任务；
- `E_A` 为自主决定中的错误；
- `D_J` 为合理弃权；
- `D_E` 为错误弃权。

则：

\[
Coverage=A/N
\]

\[
SelectiveRisk=E_A/A
\]

\[
AbstentionPrecision=D_J/D
\]

\[
ErroneousAbstentionRate=D_E/N
\]

错误率下降若主要来自覆盖率崩塌、频繁弃权或错误弃权，不构成无条件的安全改进。

## 8. 可证伪性

以下结果会削弱或否定研究主张：

- M3 未减少未授权部署或严重 False Pass；
- M3 只通过降低 Coverage 获得低错误率；
- H2 真实效用低于预先冻结的非劣界限；
- H3 不能恢复满足合法变化后的 `G_t^*`；
- 目标治理收益来自更强模型、更多预算或测试泄漏；
- 结果无法在 Replay、OOD 或 Sealed Test 中复现；
- Track A 结果不能迁移到 Track B 时，外部效度主张必须收缩。
