# Writing Wisdom Database

**版本**: 1.0.0
**建立日期**: 2025-12-11
**目的**: 整合世界級寫作智慧，作為 AI 寫手系統的知識基礎

---

## 目錄結構

```
.claude/wisdom/
├── README.md              # 本文件
│
├── masters/               # 大師原則
│   ├── schwartz.yaml      # Eugene Schwartz - 文案之王
│   ├── ogilvy.yaml        # David Ogilvy - 現代廣告之父
│   ├── cialdini.yaml      # Robert Cialdini - 說服心理學
│   ├── heath.yaml         # Chip & Dan Heath - 記憶黏著
│   └── patel.yaml         # Neil Patel - 現代內容行銷
│
├── frameworks/            # 核心框架
│   ├── awareness_stages.yaml    # 讀者認知 5 階段
│   ├── persuasion_principles.yaml  # 說服原理整合
│   ├── success_framework.yaml   # SUCCESs 記憶框架
│   └── argument_structure.yaml  # 論證結構模板
│
├── psychology/            # 心理學原理
│   ├── cognitive_load.yaml      # 認知負荷理論
│   ├── mental_models.yaml       # 心智模型
│   ├── decision_making.yaml     # 決策心理學
│   └── emotion_triggers.yaml    # 情緒觸發機制
│
├── examples/              # 頂級範例庫
│   ├── headlines/         # 標題範例
│   ├── openings/          # 開頭範例
│   ├── arguments/         # 論證範例
│   └── closings/          # 結尾範例
│
└── anti-patterns/         # 反模式 (避免)
    ├── logic_fallacies.yaml     # 邏輯謬誤
    ├── weak_arguments.yaml      # 弱論證模式
    └── cognitive_traps.yaml     # 認知陷阱
```

---

## 使用方式

### 1. Writer Agent 參考

在撰寫文章前，載入相關知識：

```bash
# 根據文章類型載入
Read: .claude/wisdom/frameworks/awareness_stages.yaml
Read: .claude/wisdom/masters/schwartz.yaml
```

### 2. Editor Agent 驗證

在審查文章時，對照檢查：

```bash
# 檢查邏輯謬誤
Read: .claude/wisdom/anti-patterns/logic_fallacies.yaml

# 驗證說服原理
Read: .claude/wisdom/frameworks/persuasion_principles.yaml
```

### 3. Writing Benchmark Agent 對標

在對標分析時，參考頂級範例：

```bash
# 對標標題
Read: .claude/wisdom/examples/headlines/
```

---

## 核心原則

### 1. 知其然，更知其所以然

每個原則都包含：
- **What**: 具體做法
- **Why**: 背後原理
- **How**: 應用方法
- **When**: 適用情境
- **Example**: 實際範例

### 2. 可驗證，可操作

每個框架都包含：
- 檢查清單
- 評分標準
- 反面案例

### 3. 持續進化

知識庫會透過以下方式更新：
- 分析頂級內容提取新模式
- 用戶反饋調整權重
- 新研究整合

---

## 版本歷史

| 版本 | 日期 | 更新內容 |
|------|------|----------|
| 1.0.0 | 2025-12-11 | 初始版本，建立目錄結構 |

---

**維護者**: AI 寫手系統團隊
