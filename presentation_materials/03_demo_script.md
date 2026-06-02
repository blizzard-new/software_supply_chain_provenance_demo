# Demo 腳本

## A. 本機練習版

用途：正式 GitHub repo 還沒準備好前，先讓小組練習「驗證成功 -> 篡改失敗」的節奏。

```powershell
cd software_supply_chain_provenance_demo
python -m pip install build
python -m pip install -e .
python -m unittest
python -m build
python scripts/create_local_manifest.py
python scripts/verify_artifact.py --mode local
python scripts/tamper_demo.py --mode local
```

講法：
1. 我們先 build 出一個 Python wheel artifact。
2. 本機 manifest 記錄 artifact 的 SHA-256，這只是教學版，不是正式簽章。
3. 原始 artifact 驗證成功。
4. `tamper_demo.py` 複製 artifact 並修改 1 byte。
5. 篡改後 SHA-256 不同，所以驗證失敗。

## B. 正式 GitHub attestation 版

目前狀態：已完成。

- Public repo: https://github.com/blizzard-new/software_supply_chain_provenance_demo
- Verified run: https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975
- Commit: `c7ee14ad9699ec7a942ccc481d6be5aa87a622d9`
- `Generate artifact attestation`: success
- `Verify artifact attestation`: success
- `Verify tamper is rejected`: success

如果只做簡報，可以直接打開上面的 Actions run 截圖，不一定要在每位組員電腦重跑。

自己電腦重跑的事前準備：
- 本機要安裝 GitHub CLI：`gh`
- 要執行 `gh auth login`

流程：

```powershell
cd software_supply_chain_provenance_demo
gh run download 26841214975 --name python-distributions --dir dist --repo blizzard-new/software_supply_chain_provenance_demo
python scripts/verify_artifact.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo blizzard-new/software_supply_chain_provenance_demo
python scripts/tamper_demo.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo blizzard-new/software_supply_chain_provenance_demo
```

現場講法：
1. 先開 GitHub Actions，讓大家看到 test、build、attest、verify、tamper rejected 都成功。
2. 下載 workflow 產生的 artifact。
3. 跑 `verify_artifact.py`，它會呼叫 `gh attestation verify`。
4. 驗證通過代表 artifact digest 能對上 GitHub Actions 產生的 attestation。
5. 再跑 `tamper_demo.py`，改掉 artifact 一個 byte。
6. 第二次驗證失敗，表示 artifact 已經不是原本被 attested 的那份檔案。

## C. 預計截圖清單

正式簡報至少需要：
- GitHub Actions workflow 成功頁面。
- `Generate artifact attestation` step 成功頁面。
- 原始 artifact 驗證成功的終端機輸出。
- 篡改 artifact 驗證失敗的終端機輸出。
- 一張 provenance flow 圖。

## D. 現場備援

如果 GitHub 或網路當天出問題：
- 播預先錄好的 30 到 60 秒 demo 影片。
- 或改跑本機版 `python scripts/tamper_demo.py --mode local`，但要明講這是教學版完整性檢查，不是正式 GitHub signed attestation。
