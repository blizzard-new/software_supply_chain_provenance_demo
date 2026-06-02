# Demo 截圖清單

簡報至少放 4 張圖。

## 1. GitHub repo 首頁

URL:

https://github.com/blizzard-new/software_supply_chain_provenance_demo

截圖重點：

- repo 是 public
- 有 `.github/workflows/build-and-attest.yml`
- 有 `presentation_materials/` 和 `team_handoff/`

## 2. Actions 成功總覽

URL:

https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26840712563

截圖重點：

- `build-and-attest`
- 綠色 success
- commit 是 `f62d84f`

## 3. Attestation 產生成功

在 run 裡打開 step：

`Generate artifact attestation`

截圖重點：

- `Attestation type: Build Provenance`
- `Attestation created for 2 subjects`
- `Attestation uploaded to repository`
- Rekor transparency log link

## 4. 原始 artifact 驗證成功

在 run 裡打開 step：

`Verify artifact attestation`

截圖重點：

- `[github] verification PASSED`
- subject 是 `hello_provenance_demo-0.1.0-py3-none-any.whl`
- workflow 是 `build-and-attest`
- commit 是 `f62d84ff...`

## 5. 篡改 artifact 驗證失敗

在 run 裡打開 step：

`Verify tamper is rejected`

截圖重點：

- original sha256 和 tampered sha256 不同
- tampered artifact 驗證失敗
- `[tamper] expected result: tampered artifact failed verification`

## 截圖命名建議

- `01_repo_home.png`
- `02_actions_success.png`
- `03_attestation_created.png`
- `04_verify_pass.png`
- `05_tamper_fail.png`
