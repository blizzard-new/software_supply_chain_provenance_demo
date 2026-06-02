# PDF 報告重點摘要

原 PDF 比較了四個適合資安與密碼學期末報告的題目，評估標準是新穎性、15 分鐘 demo 可行性、學習價值、倫理風險與一週內完成度。

## 四個題目排序

| 優先度 | 題目 | PDF 給的判斷 |
| --- | --- | --- |
| 首選 | 軟體供應鏈簽章與可驗證 Provenance | demo 最穩、研究味道夠，可以完整展示 build -> attestation -> verify -> tamper fail |
| 次選 | Passkeys 與 WebAuthn 抗釣魚驗證 | 使用者容易理解，但現場 demo 可能依賴裝置、瀏覽器或安全金鑰狀態 |
| 第三 | 後量子密碼遷移與混合式 TLS | 密碼學味道最強，但環境與名詞負擔較重 |
| 第四 | 選擇性揭露數位憑證與隱私保護 | 題目很新，政策與隱私價值高，但部分規格仍在演進 |

## 為什麼最後選第一題

我們選「軟體供應鏈簽章與可驗證 Provenance」，原因是：

1. 一週內完成機率最高，不需要特殊硬體。
2. Demo 對比清楚：原始 artifact 驗證成功，篡改後驗證失敗。
3. 可連到 2025-2026 的真實趨勢：GitHub artifact attestations、SLSA v1.2、PyPI PEP 740、Sigstore。
4. 能同時講到 hash、簽章、OIDC、CI/CD、policy 與軟體供應鏈安全。
5. 風險低，屬於防禦型題目，適合課堂展示。

## 報告建議的 15 分鐘主線

1. 先定義問題：下載到的 artifact 不一定能證明來源。
2. 解釋概念：artifact、provenance、attestation、verification policy。
3. 說明為什麼現在重要：GitHub、SLSA、PyPI、Sigstore 都已把 attestation 納入實務流程。
4. 展示實作：用 GitHub Actions build artifact，再用 `actions/attest@v4` 產生 attestation。
5. 展示驗證：`gh attestation verify` 成功。
6. 展示篡改：改 1 byte 後 verify 失敗。
7. 收斂限制：attestation 不等於無漏洞，也不等於可以無條件信任。

## 這次已完成的實作方向

本資料夾已照 PDF 的第一題建好最小可展示專案：

- Python CLI artifact：`hello-provenance-demo`
- GitHub Actions workflow：build + test + upload + `actions/attest@v4`
- 本機 rehearsal：manifest 驗證原始 artifact 成功、篡改後失敗
- 正式 demo 指令：包裝 `gh attestation verify`
- 給簡報組員用的 slide outline、資料來源、demo 腳本、Q&A、流程圖
