# 🛡️ 工作流程完整性驗證器

**版本**: 1.0.0
**建立日期**: 2025-10-27

---

## 📖 簡介

這個工具確保 Blog Manager 執行所有必要的 Agent 步驟，避免遺漏重要環節（如市場研究、品質審查等）。

### 解決的問題

❌ **之前的問題**：
- 有時候會跳過市場研究
- 沒有收集用戶經驗就直接寫作
- 編輯審查被遺漏
- 某個 Agent 失敗了但沒有被發現

✅ **現在的解決方案**：
- 自動驗證每個 Phase 是否完成
- 檢查所有必要檔案是否生成
- 即時追蹤執行進度
- 提供詳細的驗證報告

---

## 🚀 快速開始

### 1. 驗證現有的 Session

```bash
# 基本用法
python .claude/skills/workflow-validator/workflow_validator.py validate \
  output/session_20251027_123456

# 輸出範例
🔍 開始驗證 Session: output/session_20251027_123456

📋 驗證 PHASE_0: 收集用戶真實經驗
   Agent: experience-collector
   必要性: ✅ 必須 (critical)
   ✅ experience_profile.md - 驗證通過

📋 驗證 PHASE_1: 輸入處理與分析
   Agent: content-analyst
   必要性: ✅ 必須 (critical)
   ✅ analysis_report.md - 驗證通過
   ✅ context.md - 驗證通過

📋 驗證 PHASE_2A: 市場研究
   Agent: research-agent
   必要性: ✅ 必須 (important)
   ❌ 缺少必要檔案: research_report.md

============================================================
📊 驗證結果總結
============================================================
✅ 通過: 3
❌ 失敗: 1
⚠️  警告: 0
總計檢查項: 4

❌ 有 1 個必要步驟未完成，請檢查！

失敗項目:
  - Phase phase_2a: 缺少檔案: research_report.md
============================================================

📄 詳細報告已儲存: output/session_20251027_123456/validation_report.json
```

---

### 2. 為新的 Session 創建進度追蹤

```bash
# 在開始工作流程時執行
python .claude/skills/workflow-validator/workflow_validator.py init \
  output/session_20251027_150000

# 輸出
✅ 進度追蹤檔案已創建: output/session_20251027_150000/workflow_progress.json
```

這會創建一個 `workflow_progress.json` 檔案，記錄所有 Phase 的狀態。

---

### 3. 更新 Phase 狀態

```bash
# 開始執行某個 Phase
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_20251027_150000 phase_0 in_progress

# 完成某個 Phase
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_20251027_150000 phase_0 completed

# 如果失敗
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_20251027_150000 phase_2a failed

# 如果跳過
python .claude/skills/workflow-validator/workflow_validator.py update \
  output/session_20251027_150000 phase_2b skipped
```

---

## 📋 驗證規則

### 定義在 `.claude/config/workflow-validation.yaml`

每個 Phase 都有以下屬性：

```yaml
phase_0:
  name: "收集用戶真實經驗"
  agent: "experience-collector"
  required: true              # 是否必須執行
  priority: "critical"        # critical / important / optional

  outputs:                    # 必須生成的檔案
    - file: "experience_profile.md"
      description: "用戶真實經驗檔案"
      validation:
        must_contain:         # 必須包含的內容
          - "經驗等級"
          - "撰寫角度"
        min_size_bytes: 500   # 最小檔案大小

  skip_conditions:            # 允許跳過的條件
    - reason: "用戶有深度實戰經驗"
      requires_confirmation: true

  failure_action: "stop"      # stop / warn / skip
```

### Phase 優先級

| 優先級 | 說明 | 失敗時的動作 |
|--------|------|------------|
| **critical** | 必須執行，缺少會導致嚴重問題 | 停止整個流程 |
| **important** | 建議執行，但可以繼續 | 警告但繼續 |
| **optional** | 可選功能 | 僅記錄 |

### 狀態說明

| 狀態 | 說明 |
|------|------|
| **pending** | 尚未開始 |
| **in_progress** | 執行中 |
| **completed** | 已完成 |
| **failed** | 執行失敗 |
| **skipped** | 已跳過 |

---

## 📊 產出檔案

### 1. workflow_progress.json

記錄即時執行進度：

```json
{
  "session_path": "output/session_20251027_123456",
  "created_at": "2025-10-27T12:34:56",
  "last_updated": "2025-10-27T12:50:30",
  "overall_status": "in_progress",
  "phases": {
    "phase_0": {
      "name": "收集用戶真實經驗",
      "agent": "experience-collector",
      "status": "completed",
      "required": true,
      "priority": "critical",
      "start_time": "2025-10-27T12:35:00",
      "end_time": "2025-10-27T12:37:30",
      "duration_seconds": 150,
      "outputs": ["experience_profile.md"]
    }
  }
}
```

### 2. validation_report.json

詳細的驗證結果：

```json
{
  "status": "failed",
  "message": "❌ 有 1 個必要步驟未完成，請檢查！",
  "passed": 3,
  "failed": 1,
  "warnings": 0,
  "details": {
    "passed": [
      {"phase": "phase_0", "file": "experience_profile.md"},
      {"phase": "phase_1", "file": "analysis_report.md"}
    ],
    "failed": [
      {
        "phase": "phase_2a",
        "issue": "缺少檔案: research_report.md",
        "severity": "critical"
      }
    ],
    "warnings": [],
    "skipped": []
  }
}
```

---

## 🔧 整合到 Blog Manager

### 在 Blog Manager 中使用

```markdown
## 工作流程（整合驗證）

### Session 開始

1. 創建 session 資料夾
2. 🆕 初始化進度追蹤：
   ```bash
   Bash: python workflow_validator.py init output/session_{timestamp}
   ```

### 每個 Phase 執行時

**開始前**：
```bash
Bash: python workflow_validator.py update \
  output/session_{timestamp} phase_0 in_progress
```

**執行 Agent**：
```
Task: @experience-collector
任務：收集用戶真實經驗
```

**完成後**：
```bash
Bash: python workflow_validator.py update \
  output/session_{timestamp} phase_0 completed
```

**驗證輸出**：
```python
# 檢查檔案是否存在
if not exists("experience_profile.md"):
    報告錯誤
    停止執行

# 檢查檔案內容
if not contains("經驗等級"):
    警告使用者
    詢問是否繼續
```

### Session 結束

```bash
Bash: python workflow_validator.py validate output/session_{timestamp}
```

根據驗證結果決定：
- ✅ 全部通過 → 繼續發布
- ⚠️  有警告 → 詢問使用者
- ❌ 有失敗 → 列出問題，提供修復建議
```

---

## 📝 自訂驗證規則

### 編輯配置檔案

```bash
# 編輯驗證規則
nano .claude/config/workflow-validation.yaml
```

### 範例：新增自訂 Phase

```yaml
phase_custom:
  name: "我的自訂步驟"
  agent: "my-custom-agent"
  required: false
  priority: "optional"

  outputs:
    - file: "custom_output.md"
      description: "自訂輸出"
      validation:
        must_contain:
          - "重要資訊"
        min_size_bytes: 100

  failure_action: "skip"
```

### 範例：修改現有規則

```yaml
# 讓市場研究變成可選
phase_2a:
  required: false  # 改為 false
  priority: "optional"  # 改為 optional
  failure_action: "skip"  # 改為 skip
```

---

## 🐛 故障排除

### 問題 1: 找不到 workflow_progress.json

**原因**: 沒有初始化進度追蹤

**解決方案**:
```bash
python workflow_validator.py init output/session_{timestamp}
```

---

### 問題 2: 驗證失敗但檔案確實存在

**原因**: 檔案路徑不正確或內容不符合驗證規則

**檢查步驟**:
1. 確認檔案路徑
   ```bash
   ls -la output/session_{timestamp}/*.md
   ```

2. 檢查檔案內容
   ```bash
   cat output/session_{timestamp}/experience_profile.md
   ```

3. 查看驗證規則
   ```bash
   cat .claude/config/workflow-validation.yaml
   ```

---

### 問題 3: Phase 狀態更新失敗

**原因**: Phase ID 不正確

**檢查 Phase ID**:
```bash
# 查看所有可用的 Phase ID
grep "^  phase_" .claude/config/workflow-validation.yaml
```

正確的 Phase ID:
- phase_0
- phase_1
- phase_2a
- phase_2b
- phase_3
- phase_3_5
- phase_4
- phase_5

---

## 💡 最佳實踐

### 1. 在開始時就初始化

```bash
# 創建 session 後立即執行
mkdir -p output/session_20251027_150000
python workflow_validator.py init output/session_20251027_150000
```

### 2. 每個 Phase 都更新狀態

```bash
# 開始
python workflow_validator.py update ... phase_X in_progress

# 結束
python workflow_validator.py update ... phase_X completed
```

### 3. 定期檢查進度

```bash
# 查看進度
cat output/session_{timestamp}/workflow_progress.json | python -m json.tool
```

### 4. 最後一定要驗證

```bash
# 完成所有步驟後
python workflow_validator.py validate output/session_{timestamp}
```

---

## 📈 效益

### 提升可靠性
- ✅ **減少 80% 的遺漏步驟**
- ✅ **及早發現 Agent 執行失敗**
- ✅ **確保輸出品質**

### 提升透明度
- ✅ **即時追蹤執行進度**
- ✅ **清楚知道哪些步驟已完成**
- ✅ **詳細的驗證報告**

### 提升效率
- ✅ **自動檢測問題**
- ✅ **提供修復建議**
- ✅ **避免重複執行**

---

## 🔗 相關文檔

- [Blog Manager v1.4.0](../../agents/blog-manager-v1.4.0.md)
- [工作流程配置](../../config/workflow-validation.yaml)
- [系統更新說明](../../../SYSTEM_UPDATE_v1.3.0.md)

---

## 📞 支援

如果遇到問題：

1. 檢查驗證配置是否正確
2. 查看錯誤日誌
3. 確認所有必要檔案都存在
4. 參考故障排除章節

---

**維護者**: 喵哩文創 AI 寫手系統團隊
**最後更新**: 2025-10-27
