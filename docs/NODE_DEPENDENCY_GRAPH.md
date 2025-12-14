# BAMD 節點依賴圖

## 節點總覽

```
Phase ID │ 名稱                  │ 類型      │ 預估時間
─────────┼───────────────────────┼───────────┼─────────
0        │ Experience Collector  │ Critical  │ 2-3 min
1        │ Content Analyst       │ Critical  │ 1-2 min
2a       │ Research Agent        │ Important │ 3-5 min
2b       │ Style Matcher         │ Important │ 2-3 min
3        │ Writer Agent          │ Critical  │ 3-5 min
3.4      │ Quality Predictor     │ Optional  │ 1 min
3.5      │ Editor Agent          │ Critical  │ 2-3 min
3.6      │ Fact Checker          │ Important │ 2-3 min
3.7      │ Humanizer             │ Important │ 2-3 min
3.8      │ Persuasion Agent      │ Optional  │ 2-3 min
3.9      │ Storyteller           │ Optional  │ 2-3 min
4        │ SEO Optimizer         │ Important │ 2-3 min
5        │ WordPress Publisher   │ Optional  │ 1-2 min
6        │ Marketing Assets      │ Optional  │ 2-3 min
12       │ Persona Adapter       │ Optional  │ 3-5 min
```

---

## 依賴關係圖

```
                    ┌─────────────────────────────────────────────┐
                    │              輸入: URL / 文章                 │
                    └─────────────────┬───────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │         Phase 1: Content Analyst             │
                    │         (分析原文結構) [REQUIRED]            │
                    └─────────────────┬───────────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Phase 0:           │  │  Phase 2a:          │  │  Phase 2b:          │
│  Experience         │  │  Research Agent     │  │  Style Matcher      │
│  Collector          │  │  (市場研究)          │  │  (風格學習)          │
│  (經驗收集)          │  │  [OPTIONAL]         │  │  [OPTIONAL]         │
│  [OPTIONAL]         │  └──────────┬──────────┘  └──────────┬──────────┘
└──────────┬──────────┘             │                        │
           │                        │                        │
           │   ┌────────────────────┴────────────────────────┘
           │   │
           ▼   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Phase 3: Writer Agent                           │
│                      (撰寫文章) [REQUIRED]                           │
│  依賴: Phase 1 (必須), Phase 0/2a/2b (可選，有則品質更好)              │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────────────────┐
                    │       Phase 3.4: Quality Predictor           │
                    │       (品質預測) [OPTIONAL]                  │
                    │       依賴: Phase 3                          │
                    └─────────────────┬───────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│ Phase 3.6:        │   │ Phase 3.7:        │   │ Phase 3.8:        │
│ Fact Checker      │   │ Humanizer         │   │ Persuasion        │
│ (事實驗證)         │   │ (人類化)           │   │ (說服力)           │
│ [OPTIONAL]        │   │ [OPTIONAL]        │   │ [OPTIONAL]        │
│ 依賴: Phase 3     │   │ 依賴: Phase 3     │   │ 依賴: Phase 3     │
└─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
          │                       │                       │
          │                       ▼                       │
          │             ┌───────────────────┐             │
          │             │ Phase 3.9:        │             │
          │             │ Storyteller       │             │
          │             │ (故事化)           │             │
          │             │ [OPTIONAL]        │             │
          │             │ 依賴: Phase 3     │             │
          │             └─────────┬─────────┘             │
          │                       │                       │
          └───────────────────────┼───────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────────────────┐
                    │         Phase 3.5: Editor Agent              │
                    │         (品質審查) [REQUIRED]                │
                    │         依賴: Phase 3 + 所有 3.x 增強         │
                    └─────────────────┬───────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────────┐
                    │         Phase 4: SEO Optimizer               │
                    │         (SEO 優化) [OPTIONAL]                │
                    │         依賴: Phase 3.5                      │
                    └─────────────────┬───────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
          ┌───────────────────┐             ┌───────────────────┐
          │ Phase 12:         │             │ Phase 5:          │
          │ Persona Adapter   │             │ WordPress         │
          │ (多讀者適配)       │             │ Publisher         │
          │ [OPTIONAL]        │             │ (發布)            │
          │ 依賴: Phase 4     │             │ [OPTIONAL]        │
          └───────────────────┘             │ 依賴: Phase 4     │
                                            └─────────┬─────────┘
                                                      │
                                                      ▼
                                            ┌───────────────────┐
                                            │ Phase 6:          │
                                            │ Marketing Assets  │
                                            │ (行銷素材)         │
                                            │ [OPTIONAL]        │
                                            │ 依賴: Phase 5     │
                                            └───────────────────┘
```

---

## 節點定義 (JSON Schema)

```json
{
  "nodes": {
    "phase_1": {
      "id": "phase_1",
      "name": "Content Analyst",
      "description": "分析原文結構和內容",
      "required": true,
      "dependencies": [],
      "parallel_group": null,
      "estimated_time_seconds": 120,
      "inputs": ["url", "raw_content"],
      "outputs": ["analysis_report"]
    },
    "phase_0": {
      "id": "phase_0",
      "name": "Experience Collector",
      "description": "收集用戶真實經驗",
      "required": false,
      "dependencies": ["phase_1"],
      "parallel_group": "pre_write",
      "estimated_time_seconds": 180,
      "inputs": ["analysis_report"],
      "outputs": ["experience_profile"]
    },
    "phase_2a": {
      "id": "phase_2a",
      "name": "Research Agent",
      "description": "市場研究和競品分析",
      "required": false,
      "dependencies": ["phase_1"],
      "parallel_group": "pre_write",
      "estimated_time_seconds": 240,
      "inputs": ["analysis_report"],
      "outputs": ["research_report"]
    },
    "phase_2b": {
      "id": "phase_2b",
      "name": "Style Matcher",
      "description": "學習參考作者風格",
      "required": false,
      "dependencies": ["phase_1"],
      "parallel_group": "pre_write",
      "estimated_time_seconds": 180,
      "inputs": ["analysis_report"],
      "outputs": ["style_guide"]
    },
    "phase_3": {
      "id": "phase_3",
      "name": "Writer Agent",
      "description": "撰寫文章初稿",
      "required": true,
      "dependencies": ["phase_1"],
      "optional_dependencies": ["phase_0", "phase_2a", "phase_2b"],
      "parallel_group": null,
      "estimated_time_seconds": 300,
      "inputs": ["analysis_report", "experience_profile?", "research_report?", "style_guide?"],
      "outputs": ["draft"]
    },
    "phase_3_4": {
      "id": "phase_3_4",
      "name": "Quality Predictor",
      "description": "預測文章品質分數",
      "required": false,
      "dependencies": ["phase_3"],
      "parallel_group": null,
      "estimated_time_seconds": 60,
      "inputs": ["draft"],
      "outputs": ["quality_prediction"]
    },
    "phase_3_6": {
      "id": "phase_3_6",
      "name": "Fact Checker",
      "description": "驗證事實正確性",
      "required": false,
      "dependencies": ["phase_3"],
      "parallel_group": "enhance",
      "estimated_time_seconds": 180,
      "inputs": ["draft"],
      "outputs": ["fact_check_report", "verified_draft"]
    },
    "phase_3_7": {
      "id": "phase_3_7",
      "name": "Humanizer",
      "description": "人類化內容處理",
      "required": false,
      "dependencies": ["phase_3"],
      "parallel_group": "enhance",
      "estimated_time_seconds": 180,
      "inputs": ["draft"],
      "outputs": ["humanized_draft"]
    },
    "phase_3_8": {
      "id": "phase_3_8",
      "name": "Persuasion Agent",
      "description": "強化說服力",
      "required": false,
      "dependencies": ["phase_3"],
      "parallel_group": "enhance",
      "estimated_time_seconds": 180,
      "inputs": ["draft"],
      "outputs": ["persuasive_draft"]
    },
    "phase_3_9": {
      "id": "phase_3_9",
      "name": "Storyteller",
      "description": "故事化敘事增強",
      "required": false,
      "dependencies": ["phase_3"],
      "parallel_group": "enhance",
      "estimated_time_seconds": 180,
      "inputs": ["draft"],
      "outputs": ["story_enhanced_draft"]
    },
    "phase_3_5": {
      "id": "phase_3_5",
      "name": "Editor Agent",
      "description": "品質審查和整合",
      "required": true,
      "dependencies": ["phase_3"],
      "optional_dependencies": ["phase_3_6", "phase_3_7", "phase_3_8", "phase_3_9"],
      "parallel_group": null,
      "estimated_time_seconds": 180,
      "inputs": ["draft", "verified_draft?", "humanized_draft?", "persuasive_draft?", "story_enhanced_draft?"],
      "outputs": ["reviewed_draft"]
    },
    "phase_4": {
      "id": "phase_4",
      "name": "SEO Optimizer",
      "description": "SEO 優化",
      "required": false,
      "dependencies": ["phase_3_5"],
      "parallel_group": null,
      "estimated_time_seconds": 180,
      "inputs": ["reviewed_draft"],
      "outputs": ["final_article", "seo_report"]
    },
    "phase_12": {
      "id": "phase_12",
      "name": "Persona Adapter",
      "description": "多讀者版本適配",
      "required": false,
      "dependencies": ["phase_4"],
      "parallel_group": null,
      "estimated_time_seconds": 300,
      "inputs": ["final_article"],
      "outputs": ["adapted_versions"]
    },
    "phase_5": {
      "id": "phase_5",
      "name": "WordPress Publisher",
      "description": "發布到 WordPress",
      "required": false,
      "dependencies": ["phase_4"],
      "parallel_group": null,
      "estimated_time_seconds": 120,
      "inputs": ["final_article"],
      "outputs": ["publish_report"]
    },
    "phase_6": {
      "id": "phase_6",
      "name": "Marketing Assets",
      "description": "生成行銷素材",
      "required": false,
      "dependencies": ["phase_5"],
      "parallel_group": null,
      "estimated_time_seconds": 180,
      "inputs": ["final_article", "publish_report"],
      "outputs": ["marketing_assets"]
    }
  }
}
```

---

## 預設模式定義

### 快速模式 (Quick)

```json
{
  "name": "quick",
  "description": "快速產出，最小化流程",
  "estimated_time": "5 分鐘",
  "nodes": ["phase_1", "phase_3", "phase_3_5", "phase_4"],
  "skip_if_missing": []
}
```

執行順序：
```
Phase 1 → Phase 3 → Phase 3.5 → Phase 4
```

### 標準模式 (Standard)

```json
{
  "name": "standard",
  "description": "平衡品質和效率",
  "estimated_time": "15 分鐘",
  "nodes": [
    "phase_1",
    "phase_0", "phase_2a", "phase_2b",  // 並行
    "phase_3",
    "phase_3_6", "phase_3_7",            // 並行
    "phase_3_5",
    "phase_4"
  ],
  "parallel_execution": {
    "pre_write": ["phase_0", "phase_2a", "phase_2b"],
    "enhance": ["phase_3_6", "phase_3_7"]
  }
}
```

執行順序：
```
Phase 1 → [Phase 0, 2a, 2b 並行] → Phase 3 → [Phase 3.6, 3.7 並行] → Phase 3.5 → Phase 4
```

### 完整模式 (Full)

```json
{
  "name": "full",
  "description": "最高品質，完整流程",
  "estimated_time": "30 分鐘",
  "nodes": [
    "phase_1",
    "phase_0", "phase_2a", "phase_2b",
    "phase_3",
    "phase_3_4",
    "phase_3_6", "phase_3_7", "phase_3_8", "phase_3_9",
    "phase_3_5",
    "phase_4",
    "phase_12"
  ],
  "parallel_execution": {
    "pre_write": ["phase_0", "phase_2a", "phase_2b"],
    "enhance": ["phase_3_6", "phase_3_7", "phase_3_8", "phase_3_9"]
  }
}
```

### 發布模式 (Publish)

```json
{
  "name": "publish",
  "description": "標準模式 + 發布",
  "extends": "standard",
  "additional_nodes": ["phase_5", "phase_6"]
}
```

---

## Node Selector 演算法

```python
def resolve_execution_plan(selected_nodes: List[str], all_nodes: Dict) -> List[List[str]]:
    """
    解析選中的節點，生成執行計劃

    Returns:
        List of parallel groups, each containing nodes that can run together
        Example: [["phase_1"], ["phase_0", "phase_2a", "phase_2b"], ["phase_3"], ...]
    """

    # 1. 自動加入必要依賴
    resolved = set(selected_nodes)
    for node_id in selected_nodes:
        node = all_nodes[node_id]
        for dep in node.get("dependencies", []):
            resolved.add(dep)

    # 2. 拓撲排序
    sorted_nodes = topological_sort(resolved, all_nodes)

    # 3. 分組並行節點
    execution_plan = []
    current_group = []

    for node_id in sorted_nodes:
        node = all_nodes[node_id]
        parallel_group = node.get("parallel_group")

        if parallel_group:
            # 找到同組的其他節點
            same_group = [n for n in sorted_nodes
                         if all_nodes[n].get("parallel_group") == parallel_group
                         and n in resolved]

            if same_group not in execution_plan:
                execution_plan.append(same_group)
        else:
            execution_plan.append([node_id])

    return execution_plan
```

---

## 下一步

1. **實作 Node Selector 模組** (`bamd/core/node_selector.py`)
2. **建立節點配置檔** (`bamd/config/nodes.json`)
3. **實作預設模式** (`bamd/config/modes.json`)
4. **CLI 整合**

---

**建立日期**: 2025-12-12
**版本**: v0.1
