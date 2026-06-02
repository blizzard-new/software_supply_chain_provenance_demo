# 軟體供應鏈簽章與可驗證 Provenance - 組員交接完整指南

公開 repo: https://github.com/blizzard-new/software_supply_chain_provenance_demo

最新 CI run: https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26842529539

主要截圖證據 run: https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975

## 一句話主軸

這次題目不是只證明程式碼存在，而是證明最後交出去的 artifact 是由指定 GitHub repo、指定 commit、指定 GitHub Actions workflow 建出來，並且任何一個 byte 被改掉都會驗證失敗。

## 題目重點

- Artifact: build 流程產出的檔案，例如本專案的 Python wheel。
- Digest: artifact 的 SHA-256 指紋，內容變 1 byte 就會改變。
- Provenance: artifact 的來源與 build 過程 metadata，例如 repo、commit、workflow、builder。
- Attestation: 對 artifact digest 和 provenance 的可驗證聲明。
- Verification policy: 驗證者接受 artifact 的條件，例如必須來自指定 repo 和 workflow。

## 本專案已完成

| 項目 | 狀態 | 證據 |
| --- | --- | --- |
| 公開 GitHub repo | 完成 | `01_repo_home.png` |
| GitHub Actions build | 完成 | run `26841214975` 和 `26842529539` 皆 success |
| Artifact attestation | 完成 | `03_attestation_created.png` |
| GitHub verify pass | 完成 | `11_verify_pass_terminal.png` |
| Tamper fail | 完成 | `12_tamper_fail_terminal.png` |
| 組員截圖資料夾 | 完成 | `team_handoff/screenshots/` |

## 每個資料夾有什麼

| 資料夾 | 內容 | 組員用途 |
| --- | --- | --- |
| `.github/workflows/` | `build-and-attest.yml`，正式 CI/CD：test、build、upload artifact、attest、verify、tamper reject | 簡報第 6 至 7 頁 |
| `src/hello_provenance/` | Python CLI source code | 說明 artifact 的 source |
| `scripts/` | `create_local_manifest.py`、`verify_artifact.py`、`tamper_demo.py`、`_common.py` | Demo 和程式碼實作畫面 |
| `tests/` | CLI unit test | 說明 workflow 有先跑測試 |
| `presentation_materials/` | 原本整理的摘要、大綱、研究資料、Q&A、diagram | 做 PPT 的文字資料 |
| `team_handoff/` | 給組員的交接資料、本 PDF/HTML、GitHub evidence | 直接傳給組員 |
| `team_handoff/screenshots/` | 12 張簡報截圖 | PPT 圖片來源 |
| `dist/` | build 或下載後的 wheel/sdist | demo 重跑時使用 |
| `.demo/` | local rehearsal 產物 | 練習用，不是正式 GitHub attestation |

## Demo 怎麼重跑

正式 GitHub attestation demo:

```powershell
gh auth login
gh run download 26841214975 --name python-distributions --dir dist --repo blizzard-new/software_supply_chain_provenance_demo
python scripts/verify_artifact.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo blizzard-new/software_supply_chain_provenance_demo
python scripts/tamper_demo.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo blizzard-new/software_supply_chain_provenance_demo
```

本地 rehearsal demo:

```powershell
.\demo.ps1
```

注意：本地 manifest 只是練習版，不是正式 attestation。正式證據是 GitHub Actions 產生的 artifact attestation。

## 截圖怎麼用

| 截圖 | 建議頁面 | 講法 |
| --- | --- | --- |
| `01_repo_home.png` | Slide 1 | 專案已 push 到公開 GitHub |
| `02_actions_success.png` | Slide 5 | CI 已跑完 test、build、attest、verify、tamper reject |
| `06_workflow_code.png` | Slide 6 | workflow 前半段：permissions、test、build、upload |
| `10_workflow_attestation_verify_code.png` | Slide 7 | workflow 後半段：attest、verify、tamper reject |
| `11_verify_pass_terminal.png` | Slide 8 | 原始 artifact 驗證通過 |
| `12_tamper_fail_terminal.png` | Slide 9 | 竄改 artifact 驗證失敗 |
| `07_verify_artifact_code.png` | Slide 10 | 驗證腳本實作 |
| `08_tamper_demo_code.png` | Slide 10 | 翻轉 1 byte 的 tamper demo |

## 簡報逐頁建議

1. 題目與一句話結論：放 `01_repo_home.png`，說明我們做的是可驗證 provenance demo。
2. 問題背景：source code 正常不代表下載到的 artifact 可信，攻擊點可能在 CI/CD 或 release artifact。
3. 核心概念：Artifact、Digest、Provenance、Attestation、Verification policy。
4. 現代趨勢：GitHub artifact attestations、SLSA、PEP 740、Sigstore。
5. 本專案架構：Python CLI package -> test -> build -> upload -> attest -> verify -> tamper fail。
6. Workflow 前半段：放 `06_workflow_code.png`，框出 permissions、test、build、upload。
7. Attestation/verify workflow：放 `10_workflow_attestation_verify_code.png`，框出 `actions/attest@v4`、verify、tamper reject。
8. Demo 1：放 `11_verify_pass_terminal.png`，說明原始 wheel digest 和 attestation subject digest 一致。
9. Demo 2：放 `12_tamper_fail_terminal.png`，說明翻轉 1 byte 後 digest 不一致，驗證失敗。
10. 實作程式碼畫面：放 `07_verify_artifact_code.png` 和 `08_tamper_demo_code.png`。
11. 解決了什麼：可驗證 artifact 是否來自指定 repo、workflow、commit，且內容未被竄改。
12. 沒解決什麼：source code 本身是否安全、dependency 是否安全、workflow 是否被合法惡意修改，仍需要其他控管。
13. 組員資料夾和分工：說明 `team_handoff/`、`presentation_materials/`、`screenshots/`。
14. 結論：從 source 到 artifact 到 verification 的端到端 demo 已完成。
15. Q&A 和參考資料：放 repo link 和官方參考來源。

## 老師可能問的問題

| 問題 | 建議回答 |
| --- | --- |
| attestation 跟 hash 有什麼不同？ | hash 只證明內容是否改變；attestation 會把 artifact digest 和 repo、commit、workflow、builder 等來源資訊綁在一起。 |
| source code 本來就惡意怎麼辦？ | attestation 不會解決這件事，它證明來源與 build context，不保證 source code 沒有惡意邏輯。 |
| 為什麼不用本機簽章？ | 本機簽章會有長期金鑰管理問題，也較難證明 build context。GitHub Actions 可用 OIDC 和 artifact attestations 建立 CI provenance。 |
| local manifest 是正式 attestation 嗎？ | 不是。local manifest 是 rehearsal。正式證據是公開 GitHub repo 的 workflow 產生 attestation，再用 GitHub CLI 驗證。 |
| 怎麼證明 tamper 被擋？ | `tamper_demo.py` 翻轉 artifact 的 1 byte，新的 SHA-256 對不上 GitHub attestation subject digest，因此 verify fail。 |

## 官方參考資料

- GitHub Docs - Using artifact attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- GitHub Action - actions/attest: https://github.com/actions/attest
- SLSA v1.2 Provenance: https://slsa.dev/spec/v1.2/provenance
- PEP 740 - Index support for digital attestations: https://peps.python.org/pep-0740/
- Sigstore Docs: https://docs.sigstore.dev/
