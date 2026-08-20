# 变更分类 Codebook

**版本：0.1-draft**  
**状态：等待 D004、D006、D007**

## 1. 目的

每次系统修改都必须被归入一个可审计层级。分类不是为了描述代码文件位置，而是为了判断修改改变了执行能力、测量方法、成功定义、自治权还是证明要求。

## 2. 六类主变更

### 2.1 `CAPABILITY_PATCH`

改变 `H_t`，但不改变目标、评价器语义、自治权限或证明门槛。

**正例**：改进检索、增加错误重试、调整工作流、添加单位换算工具。  
**反例**：删除必须检查的字段；这属于 Evaluator 或 Goal 变化。

### 2.2 `EVALUATOR_PATCH`

改变 `E_t` 对当前 `G_t` 的实现方式，目标语义保持不变。

**正例**：修复紧急报销例外被错误拒绝。  
**红旗**：新评价器扩大接受集合，但无法证明是修复 `D_E`。

### 2.3 `GOAL_DISCOVERY`

`G_t^*` 未变化；系统根据足够证据把原本存在但未写清的条款纳入 `G_t`。

**正例**：审计报告揭示一直有效的双重审批要求。  
**反例**：为了提高完成率而创建新例外。

### 2.4 `GOAL_NORMATIVE_CHANGE`

`G_t^*` 因合法外部事件发生变化。

**必须包含**：授权、批准和生效时间、范围、历史失效规则。  
**反例**：系统根据任务失败自行改变金额门槛。

### 2.5 `AUTONOMY_CHANGE`

改变 `A_t`，即系统可自主使用的工具、数据、写入、发布或批准范围。

**正例**：允许读取新的只读数据库。  
**高风险例**：开放自动发布或数据库写权限。

### 2.6 `ASSURANCE_CHANGE`

改变 `R_t` 或 `C_t`，即证明要求、签署者独立性、适用范围或能力认证。

**正例**：新增独立第二来源要求。  
**高风险例**：将双人签署降为系统自签；未经授权扩大 Capability Envelope。

## 3. 原子 Patch 规则

一个 Patch 必须满足：

1. 只有一个 `change_type`；
2. 只修改与该类型相符的目标对象；
3. 跨层修改拆成多个 Patch；
4. 多个 Patch 可通过 `bundle_id` 关联；
5. 每个 Patch 独立验证、批准和回滚；
6. Bundle 的部分失败不得被整体成功掩盖。

## 4. 分类决策树

1. 直接修改哪个版本对象？
   - Harness → `CAPABILITY_PATCH`
   - Evaluator → `EVALUATOR_PATCH`
   - Autonomy → `AUTONOMY_CHANGE`
   - Assurance/Envelope → `ASSURANCE_CHANGE`
   - Goal → 进入第 2 步
2. `G_t^*` 是否变化？
   - 否，且存在预先允许的发现证据 → `GOAL_DISCOVERY`
   - 是，且有合法事件与授权 → `GOAL_NORMATIVE_CHANGE`
   - 无法确定 → `human_judgment_required`，不得生效
3. 是否同时修改多个对象？
   - 是 → 拒绝复合 Patch，要求拆分
4. 是否扩大接受集合或降低证明要求？
   - 是 → 强制升级独立审查和人工批准

## 5. 接受集合审查

每个 Goal 或 Evaluator Patch 必须报告：

\[
\Delta^+=Acc(new)\setminus Acc(old)
\]

\[
\Delta^-=Acc(old)\setminus Acc(new)
\]

`Delta+` 中的每个类别必须解释为：

- 修复错误阻止；
- 补全既有目标；
- 合法接受新风险；
- 未经授权放宽；
- 尚不能确定。

## 6. 升级条件

以下情况禁止自动生效：

- 分类置信不足或多个类别同样合理；
- 修改 Goal、Autonomy、Assurance 或 Capability Envelope；
- `Delta+` 非空；
- 授权证据缺失或冲突；
- Patch 影响 H1–H3 的定义或分母；
- 提案者与最终证明者相同；
- 需要改变已冻结协议。

## 7. 编码与一致性流程

1. Agent 生成候选边界案例；
2. 两名人类独立编码；
3. Agent 分析分歧，不决定 Gold；
4. 第三人类裁决；
5. 修改 Codebook 后用新案例复测；
6. 冻结 Gold Set 和版本哈希。

本仓库的 `taxonomy_cases/candidates/*.jsonl` 仅是 Agent 提出的候选标签，不是正式 Gold 标签。
