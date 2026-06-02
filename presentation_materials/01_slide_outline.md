# 投影片內容大綱

建議總長 12 到 15 分鐘，主線只講一件事：同一個 artifact，在 provenance 驗證下可以確認來源；被篡改後驗證會失敗。

## Slide 1 - 題目與一句話結論

標題：Software Supply Chain Attestation：讓 build artifact 的來源可以被驗證

要放：
- 題目名稱
- 小組成員
- 一句話主張：安全不只看程式碼，也要能證明下載到的 artifact 是誰、在哪裡、用哪個流程 build 出來的。

講者備註：
- 先用「我下載到的檔案到底是不是 GitHub Actions build 出來的？」切入。

## Slide 2 - 問題背景：供應鏈攻擊不是只改 source code

要放：
- 攻擊者可能改 CI/CD、release artifact、上傳流程或套件倉庫。
- 傳統 hash 只能確認「這份檔案有沒有變」，不能回答「它從哪裡來」。
- provenance 的價值是把 artifact 和 source repo / commit / workflow 綁在一起。

建議視覺：
- 左邊放「source code」，中間放「build」，右邊放「artifact」。
- 在 build 到 artifact 之間標出可能被替換或篡改的位置。

## Slide 3 - 核心概念

要放四個名詞：
- Artifact：最後被下載、安裝、執行的 build 產物，例如 wheel、binary、container image。
- Provenance：描述 artifact 從哪個 repo、commit、workflow、builder 產生。
- Attestation：對 provenance 的可驗證聲明，通常含簽章與 digest。
- Verification policy：消費者檢查 artifact digest、來源 repo、workflow、身分是否符合預期。

講者備註：
- 不要把 attestation 講成「保證安全」；它保證的是來源與完整性證據。

## Slide 4 - 為什麼 2026 適合做這題

要放資料：
- GitHub artifact attestations 已支援 `actions/attest@v4`，workflow 權限需要 `id-token: write`、`contents: read`、`attestations: write`。
- GitHub 文件寫明 artifact attestations 會包含 workflow、repo、organization、commit SHA、trigger event 與 OIDC token 相關資訊。
- SLSA v1.2 在 2025-11-24 發布，新增 Source Track，把焦點從 build 擴展到 source 管理、審核與保護。
- PyPI 的 PEP 740 attestation 文件已支援 SLSA Provenance 與 PyPI Publish attestations。

建議視覺：
- 做成「GitHub / SLSA / PyPI / Sigstore」四格表。

## Slide 5 - 我們的實作架構

要放：
- 最小 Python CLI package：`hello-provenance-demo`
- GitHub Actions：test -> build -> upload artifact -> `actions/attest@v4`
- Verify script：包裝 `gh attestation verify`
- Tamper script：複製 artifact，改 1 byte，再驗證失敗

建議視覺：
- 使用 `06_mermaid_diagrams.md` 裡的 provenance flow。

## Slide 6 - Demo：成功驗證

要放：
- Actions workflow 成功截圖
- `dist/*.whl` artifact
- `python scripts/verify_artifact.py ... --mode github --repo OWNER/REPO`
- 終端機輸出中的 PASS 或 GitHub CLI verified result

講者備註：
- 強調 verification 不是只看檔名，而是看 artifact digest 與 attestation 內容。

## Slide 7 - Demo：篡改後失敗

要放：
- `tamper_demo.py` 指令
- 原始 SHA-256 與篡改後 SHA-256
- 驗證失敗截圖

講者備註：
- 改 1 byte 就會讓 SHA-256 完全不同，所以 attestation 中的 subject digest 對不上。

## Slide 8 - 限制與風險

要放：
- Attestation 不保證 artifact 沒有漏洞或惡意行為。
- 如果 workflow 本身有問題，attestation 只會誠實證明「有問題的 workflow 產出了這個 artifact」。
- 有 attestation 但沒有 verify policy，安全價值會大幅降低。
- GitHub Free / Pro / Team 要用公開 repo 才能穩定展示 artifact attestations。

## Slide 9 - 結論

要放：
- Provenance 讓軟體消費者能問：它從哪裡來？誰 build 的？有沒有被改？
- Demo 顯示：原始 artifact 驗證成功；篡改 artifact 驗證失敗。
- 最重要的安全觀念：簽章與 attestation 是供應鏈決策的證據，不是「無條件信任」。
