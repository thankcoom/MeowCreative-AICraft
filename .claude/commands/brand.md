# 品牌管理

管理品牌知識庫，查看、建立、切換品牌 Profile。

## 參數
- `$ARGUMENTS`: 子命令 (list | show | create | use)

---

## 子命令

### `/brand` 或 `/brand list`

列出所有品牌。讀取 `.claude/memory/brands/` 目錄：

```bash
ls -la .claude/memory/brands/
```

顯示每個品牌的：
- 名稱
- 產業
- 語調
- 知識庫數量

### `/brand show <name>`

顯示品牌詳情。讀取 `.claude/memory/brands/<name>.yaml`：

```
Read: .claude/memory/brands/<name>.yaml
```

格式化顯示：
- 基本資訊 (名稱、標語、官網)
- 品牌設定 (語調、價值觀)
- 目標受眾
- 知識庫內容摘要

### `/brand create`

互動式建立品牌。使用 AskUserQuestion 收集資訊：

**Step 1: 基本資訊**
```
questions:
  - question: "品牌名稱？"
    header: "名稱"
    options: [] # 讓用戶輸入
```

**Step 2: 產業類別**
```
questions:
  - question: "產業類別？"
    header: "產業"
    options:
      - label: "科技/軟體"
      - label: "電商/零售"
      - label: "媒體/內容"
      - label: "教育/培訓"
```

**Step 3: 品牌語調**
```
questions:
  - question: "品牌語調？"
    header: "語調"
    options:
      - label: "專業權威"
        description: "正式、數據導向"
      - label: "親和友善"
        description: "對話式、有溫度"
      - label: "年輕活力"
        description: "活潑、網路感"
      - label: "自然樸實"
        description: "真實、不做作"
```

**Step 4: 目標受眾**
讓用戶描述目標受眾。

**Step 5: 品牌價值觀**
讓用戶輸入 3-5 個核心價值。

**Step 6: 儲存**
將資料儲存到 `.claude/memory/brands/<brand_id>.yaml`

### `/brand use <name>`

設定當前使用的品牌。更新 `.claude/memory/current_brand.txt`。

後續 `/write` 命令會自動載入此品牌。

---

## 品牌資料結構

```yaml
# .claude/memory/brands/miaoli.yaml
brand_id: miaoli
brand_name: 喵哩文創
brand_name_en: Miaoli Creative
tagline: 用故事連結世界
website: https://miaolicreative.com

industry: 媒體/內容
brand_voice: friendly_approachable
brand_voice_name: 親和友善

target_audience: 25-45歲的創業者、行銷人員

brand_values:
  - 真實 - 不虛構、不誇大
  - 創意 - 用新視角說故事
  - 專業 - 紮實的內容品質

writing_guidelines:
  do:
    - 使用對話式語調
    - 分享真實經驗
    - 提供實用建議
  dont:
    - 虛構數據或案例
    - 過度誇大效果
    - 使用艱澀術語
```
