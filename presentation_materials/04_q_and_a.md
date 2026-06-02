# Q&A 準備

## Q1. Attestation 和 hash 有什麼不同？

Hash 只能回答「這份檔案有沒有變」。Attestation 還能把 artifact 和 build 身分綁起來，例如 repo、commit、workflow、builder 與 OIDC identity。

## Q2. 有 attestation 是否代表軟體沒有漏洞？

不是。Attestation 不做弱點掃描，也不保證沒有惡意邏輯。它提供的是來源與建置流程證據。要不要信任，仍然要搭配 policy、code review、dependency scan、SBOM 或其他安全檢查。

## Q3. 如果 GitHub Actions workflow 本身被攻擊怎麼辦？

Attestation 會證明 artifact 是由該 workflow 產生，但如果 workflow 本身不安全，attestation 不能自動修好這件事。因此實務上要保護 branch、review workflow changes、限制 token permission，並用 reusable workflow 或更嚴格的 SLSA 控制提高可信度。

## Q4. 為什麼篡改 1 byte 就驗證失敗？

Attestation 裡會記錄 artifact 的 digest。SHA-256 對輸入非常敏感，改 1 byte 就會產生完全不同的 digest，所以驗證時對不上。

## Q5. 這和程式碼簽章一樣嗎？

概念相近，都是讓消費者能驗證某種聲明。但這裡重點不是只簽單一 binary，而是把 artifact 和 build provenance 綁在一起，讓消費者知道它是從哪個 workflow 與 source 產生。

## Q6. 這題和密碼學有什麼關係？

它用到 hash、簽章、短效身分、OIDC、透明日誌與 supply-chain policy。它不是純理論密碼學，但很適合展示密碼學如何落地到 CI/CD 與軟體供應鏈安全。

## Q7. 為什麼不用只檢查 GitHub release 上的檔案？

Release 頁面可以放檔案，但檔案本身還是可能被替換或來源不明。Attestation 的價值是讓下載者可以獨立驗證 artifact 是否對應到預期 repo 和 workflow。

## Q8. 本機 manifest demo 算不算正式成果？

不算正式 attestation。它只用來練習流程與備援。正式成果應該展示 GitHub Actions 產生的 signed artifact attestation，並用 `gh attestation verify` 驗證。
