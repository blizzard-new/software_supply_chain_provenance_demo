# 給組員的入口文件

題目：軟體供應鏈簽章與可驗證 Provenance

我們要展示：同一個 build artifact 在有 GitHub artifact attestation 時可以驗證來源與完整性；如果 artifact 被改掉 1 byte，驗證會失敗。

## GitHub 已完成

- Public repo: https://github.com/blizzard-new/software_supply_chain_provenance_demo
- 最新成功 Actions run: https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26840712563
- 最新 commit: `f62d84ffb4a96ee5f85527f53d2f0e7badccb6dc`
- Artifact 名稱：`python-distributions`
- Attestation 頁面：在 Actions log 裡可以看到 `Attestation uploaded to repository`

最新版 Actions 已通過：

- `Run tests`
- `Build package artifact`
- `Upload package artifact`
- `Generate artifact attestation`
- `Verify artifact attestation`
- `Verify tamper is rejected`

## 組員要做什麼

1. 做簡報的人看 `../presentation_materials/01_slide_outline.md`。
2. 查資料的人看 `../presentation_materials/02_research_facts.md`。
3. 做 demo 截圖的人看 `github_evidence.md` 和 `demo_screenshot_checklist.md`。
4. 要貼到群組的文字看 `message_to_group.md`。

## 最重要的簡報主線

1. 供應鏈問題：下載到的 artifact 不一定能證明來源。
2. 解法：provenance + attestation + verification policy。
3. 實作：GitHub Actions build artifact，`actions/attest@v4` 產生 attestation。
4. Demo：原始 wheel 驗證成功。
5. Demo：改 1 byte 後驗證失敗。
6. 限制：attestation 不代表程式沒有漏洞，也不代表可以無條件信任。

## 建議分工

| 角色 | 負責內容 | 交付物 |
| --- | --- | --- |
| A | 實作與 demo 證據 | Actions 截圖、verify/tamper 截圖 |
| B | 研究內容 | GitHub/SLSA/PyPI/Sigstore 重點整理 |
| C | 投影片排版 | 流程圖、比較表、Q&A slide |

如果只有兩個人，B 和 C 合併。
