# 变更分类候选案例

- `candidates/*.jsonl`：由 Agent 生成的 84 个候选案例，按七类变更分文件保存；包含建议标签和理由，**不是 Gold Set**。
- `human_review_batch_01.yaml`：给两名人类编码者独立标注的 28 个盲化案例，不包含建议标签。

## 编码流程

1. 两名人类分别填写 `coder_label`、`confidence` 和 `notes`；
2. 在提交前不得打开 `candidates/` 中的建议标签；
3. Agent 汇总分歧和 Codebook 漏洞，但不得决定 Gold；
4. 第三名有权人类裁决；
5. 使用新案例复测后，才生成版本化 Gold Set。

Protocol v0.1 新增 `CAPABILITY_ENVELOPE_CHANGE`，用于记录经过验证的任务、风险、地域、系统版本或时间范围的扩大和收缩；它与实际工具/写入权限的 `AUTONOMY_CHANGE` 分开。
