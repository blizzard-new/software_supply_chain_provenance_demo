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

https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975

截圖重點：

- `build-and-attest`
- 綠色 success
- commit 是 `c7ee14a`

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
- commit 是 `c7ee14ad...`

## 5. 篡改 artifact 驗證失敗

在 run 裡打開 step：

`Verify tamper is rejected`

截圖重點：

- original sha256 和 tampered sha256 不同
- tampered artifact 驗證失敗
- `[tamper] expected result: tampered artifact failed verification`

## 截圖命名建議

已經放在 `team_handoff/screenshots/`：

- `01_repo_home.png`：GitHub repo 首頁
- `02_actions_success.png`：Actions 成功總覽
- `03_attestation_created.png`：Actions step 清單中的 attestation step
- `04_verify_pass.png`：Actions step 清單中的 verify step
- `05_tamper_fail.png`：Actions step 清單中的 tamper step
- `06_workflow_code.png`：workflow 前半段，包含 permissions、test、build、upload
- `07_verify_artifact_code.png`：`verify_artifact.py` 實作
- `08_tamper_demo_code.png`：`tamper_demo.py` 實作
- `09_cli_code.png`：最小 CLI artifact 實作
- `10_workflow_attestation_verify_code.png`：workflow 下半段，包含 attest、verify、tamper
- `11_verify_pass_terminal.png`：可直接放簡報的 verify pass 終端機圖
- `12_tamper_fail_terminal.png`：可直接放簡報的 tamper fail 終端機圖

簡報最推薦使用：`02_actions_success.png`、`10_workflow_attestation_verify_code.png`、`11_verify_pass_terminal.png`、`12_tamper_fail_terminal.png`。
