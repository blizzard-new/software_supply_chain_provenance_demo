# 截圖說明

這個資料夾的圖片可以直接放進簡報。

## GitHub 與 Actions

- `01_repo_home.png`：公開 GitHub repo 首頁
- `02_actions_success.png`：截圖證據使用的 Actions run 成功總覽
- `03_attestation_created.png`：Actions step 清單中的 `Generate artifact attestation`
- `04_verify_pass.png`：Actions step 清單中的 `Verify artifact attestation`
- `05_tamper_fail.png`：Actions step 清單中的 `Verify tamper is rejected`

## 實作程式碼

- `06_workflow_code.png`：GitHub Actions workflow 前半段，包含 permissions、test、build、upload
- `07_verify_artifact_code.png`：`verify_artifact.py` 的 GitHub attestation verify 實作
- `08_tamper_demo_code.png`：`tamper_demo.py` 的修改 1 byte 與重新驗證實作
- `09_cli_code.png`：最小 Python CLI artifact 實作
- `10_workflow_attestation_verify_code.png`：workflow 下半段，包含 `actions/attest@v4`、verify、tamper reject

## Demo 證據圖

- `11_verify_pass_terminal.png`：原始 artifact 驗證成功
- `12_tamper_fail_terminal.png`：篡改 artifact 驗證失敗

最推薦放投影片的四張圖：

1. `02_actions_success.png`
2. `10_workflow_attestation_verify_code.png`
3. `11_verify_pass_terminal.png`
4. `12_tamper_fail_terminal.png`
