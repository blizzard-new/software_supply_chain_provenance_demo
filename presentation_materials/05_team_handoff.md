# 組員交接文件

正式題目：軟體供應鏈簽章與可驗證 Provenance

一句話說明：我們要展示同一個 build artifact 在有 attestation 時可以驗證來源與完整性；被篡改後驗證會失敗。

## GitHub 已完成

- Public repo: https://github.com/blizzard-new/software_supply_chain_provenance_demo
- Evidence Actions run: https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975
- Evidence commit: `c7ee14ad9699ec7a942ccc481d6be5aa87a622d9`
- `Generate artifact attestation`: success
- `Verify artifact attestation`: success
- `Verify tamper is rejected`: success

## 已準備好的東西

- 可 build 的 Python CLI artifact：`hello-provenance-demo`
- GitHub Actions workflow：`.github/workflows/build-and-attest.yml`
- 本機驗證腳本：`scripts/verify_artifact.py`
- 篡改測試腳本：`scripts/tamper_demo.py`
- 本機練習用 manifest：`scripts/create_local_manifest.py`
- PDF 重點摘要：`presentation_materials/00_report_summary.md`
- 簡報大綱：`presentation_materials/01_slide_outline.md`
- 研究資料與來源：`presentation_materials/02_research_facts.md`
- Demo 腳本：`presentation_materials/03_demo_script.md`
- Q&A：`presentation_materials/04_q_and_a.md`
- Mermaid 流程圖：`presentation_materials/06_mermaid_diagrams.md`

## 建議分工

| 角色 | 責任 | 交付物 |
| --- | --- | --- |
| 組員 A | 實作與 demo | GitHub repo、Actions 成功頁面、verify/tamper 終端機截圖 |
| 組員 B | 研究與講稿 | 背景、名詞解釋、SLSA/GitHub/PyPI/Sigstore 資料整理 |
| 組員 C | 簡報與視覺 | 投影片、流程圖、截圖排版、備援影片 |

如果只有兩個人，組員 B 和 C 合併。

## 最短完成順序

1. 打開已完成的 Actions run。
2. 截圖 `Generate artifact attestation` 成功。
3. 截圖 `Verify artifact attestation` 成功。
4. 截圖 `Verify tamper is rejected` 成功。
5. 把 `06_mermaid_diagrams.md` 的流程圖轉成投影片圖。
6. 照 `01_slide_outline.md` 做 8 到 9 張投影片。

## 一週排程

| 日期 | 里程碑 | 驗收標準 |
| --- | --- | --- |
| 2026-06-03 | 題目定稿與 repo 建立 | GitHub repo 建好，README 可讀 |
| 2026-06-04 | build 成功 | `dist/*.whl` 能產生 |
| 2026-06-05 | provenance 成功 | Actions 頁面可看到 attestation step 成功 |
| 2026-06-06 | verify/tamper 完成 | 一張成功驗證截圖，一張失敗驗證截圖 |
| 2026-06-07 | 投影片初稿 | 至少 8 張 slide 有內容 |
| 2026-06-08 | 第一次彩排 | 主內容 12 到 13 分鐘講完 |
| 2026-06-09 | 最終修正 | demo 有備援影片，Q&A 有準備 |

## 簡報必放內容

- 問題：下載到的 artifact 不一定能證明來源。
- 概念：artifact、provenance、attestation、verification policy。
- 新穎性：GitHub artifact attestations、SLSA v1.2、PyPI PEP 740、Sigstore。
- 實作：Python artifact + GitHub Actions + actions/attest@v4 + gh verify。
- Demo：原始 artifact 成功；篡改後失敗。
- 限制：attestation 不保證無漏洞，不保證 workflow 本身安全，必須真的 verify。

## 傳給組員時可以附上的訊息

我們這組先做第一個題目「軟體供應鏈簽章與可驗證 Provenance」。資料夾裡已經有 demo 程式、GitHub Actions workflow、驗證/篡改腳本，還有簡報大綱、研究資料、demo 腳本和 Q&A。簡報可以照 `presentation_materials/01_slide_outline.md` 做，demo 指令看 `presentation_materials/03_demo_script.md`。
