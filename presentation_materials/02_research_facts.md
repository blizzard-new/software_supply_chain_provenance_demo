# 研究資料與可引用重點

這份資料表是給簡報用的，不需要整段照念。每張投影片挑 1 到 2 個最有用的事實即可。

| 主題 | 可放進簡報的資料 | 用法 |
| --- | --- | --- |
| GitHub artifact attestations 的目的 | GitHub 文件說 artifact attestations 可建立 build artifact 的 provenance 與 integrity guarantees，讓消費者驗證軟體在哪裡、如何 build。 | Slide 3 或 Slide 4 的定義 |
| Attestation 內容 | GitHub attestation 會包含 workflow、repository、organization、environment、commit SHA、triggering event，以及 OIDC token 相關資訊。 | 說明 provenance 不是單純 hash |
| SLSA Level | GitHub 文件指出 artifact attestations 本身可提供 SLSA v1.0 Build Level 2；搭配 reusable workflows 可往 Build Level 3。 | 說明這題與標準框架相關 |
| Workflow 權限 | 產生 binary attestation 需要 `id-token: write`、`contents: read`、`attestations: write`，並使用 `actions/attest@v4`。 | Slide 5 實作架構 |
| Verify 指令 | GitHub CLI 可用 `gh attestation verify PATH -R OWNER/REPO` 驗證 binary artifact。 | Demo slide |
| 限制 | GitHub 文件明確提醒：attestation 不保證 artifact 是安全的；消費者仍要定義 policy 並評估內容。 | 風險與限制 slide |
| 使用門檻 | GitHub Free / Pro / Team 方案中，artifact attestations 對公開 repo 可用；private/internal repo 需要 Enterprise Cloud。 | Demo 事前提醒 |
| SLSA v1.2 | SLSA v1.2 在 2025-11-24 發布，新增 Source Track，涵蓋 source code 的撰寫、審查與管理威脅。 | 為什麼這題是 2025-2026 新趨勢 |
| PyPI / PEP 740 | PyPI 文件說它的 digital attestations 實作 PEP 740，支援 SLSA Provenance 與 PyPI Publish attestations。 | 說明不是只有 GitHub，在套件生態也落地 |
| Sigstore | Sigstore Cosign bundle 包含 signature、certificate、timestamp 和 transparency log inclusion proof。 | 補充背後的簽章生態 |

## 建議引用來源

- GitHub Docs - Artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations
- GitHub Docs - Using artifact attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- SLSA - Announcing SLSA v1.2: https://slsa.dev/blog/2025/11/announce-slsa-v1.2
- PyPI Docs - Digital attestations: https://docs.pypi.org/attestations/
- PEP 740 - Index support for digital attestations: https://peps.python.org/pep-0740/
- Sigstore Cosign Quickstart: https://docs.sigstore.dev/quickstart/quickstart-cosign/

## 簡報中要避免的錯誤說法

- 不要說「有 attestation 就代表軟體安全」。
- 不要說「簽章可以找出漏洞」。
- 不要只講 hash，因為 hash 不能回答來源與 build 身分。
- 不要把本機 `.demo/local_provenance.json` 當成正式 attestation；它只是練習 demo 用。
