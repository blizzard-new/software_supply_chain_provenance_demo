# Software Supply Chain Provenance Demo

這個專案是資安與密碼學期末報告第一個題目「軟體供應鏈簽章與可驗證 Provenance」的實作底稿。它建立一個最小 Python CLI artifact，並提供兩種展示路線：

1. 本機教學版：用 SHA-256 manifest 先練習「原始 artifact 驗證成功、篡改 artifact 驗證失敗」的故事線。
2. 正式展示版：把專案推到公開 GitHub repo，讓 GitHub Actions 使用 `actions/attest@v4` 產生 signed artifact attestation，再用 `gh attestation verify` 驗證。

本機 manifest 不是正式 attestation，只是讓小組在 GitHub workflow 還沒跑完前可以先練 demo。正式報告要以 GitHub artifact attestation 的輸出為準。

## 專案結構

```text
.
├── .github/workflows/build-and-attest.yml
├── src/hello_provenance/
├── scripts/
│   ├── create_local_manifest.py
│   ├── verify_artifact.py
│   └── tamper_demo.py
├── presentation_materials/
├── pyproject.toml
├── Makefile
└── demo.ps1
```

## 本機快速 demo

在 PowerShell 執行：

```powershell
cd software_supply_chain_provenance_demo
.\demo.ps1
```

這會做五件事：

1. 安裝最少需要的 build 工具。
2. 跑單元測試。
3. 產生 `dist/*.whl` artifact。
4. 建立 `.demo/local_provenance.json`。
5. 驗證原始 artifact 成功，接著複製並修改 1 byte，確認篡改後驗證失敗。

也可以分段執行：

```powershell
python -m pip install build
python -m pip install -e .
python -m unittest discover -s tests
python -m build
python scripts/create_local_manifest.py
python scripts/verify_artifact.py --mode local
python scripts/tamper_demo.py --mode local
```

## 正式 GitHub attestation demo

1. 建立一個公開 GitHub repo。
2. 把這個資料夾內容 push 到 repo 的 `main` branch。
3. 到 Actions 頁面確認 `build-and-attest` workflow 成功。
4. 下載 `python-distributions` artifact，或用 GitHub CLI 下載：

```powershell
gh run download --name python-distributions --dir dist
```

5. 驗證 artifact：

```powershell
python scripts/verify_artifact.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo OWNER/REPO
```

6. 展示篡改失敗：

```powershell
python scripts/tamper_demo.py dist/hello_provenance_demo-0.1.0-py3-none-any.whl --mode github --repo OWNER/REPO
```

## Demo 要講的重點

- artifact 是最後給使用者下載、執行或安裝的產物。
- provenance 回答「這個 artifact 是從哪個 repo、哪個 commit、哪個 workflow build 出來的」。
- attestation 是對 provenance 的簽章式聲明。
- verification 會把 artifact 目前的 SHA-256 digest 和 attestation 裡記錄的 digest 對起來。
- artifact 被改掉 1 byte 後，digest 會完全不同，因此驗證失敗。
- attestation 不等於軟體沒有漏洞，也不等於可以無條件信任；它只提供來源與建置過程的可驗證證據。

## 簡報素材

`presentation_materials/` 已整理好給組員用的內容：

- `00_report_summary.md`：PDF 重點摘要與選題理由。
- `01_slide_outline.md`：每張投影片要放什麼。
- `02_research_facts.md`：可以引用的研究資料與來源。
- `03_demo_script.md`：現場 demo 流程與指令。
- `04_q_and_a.md`：可能被問的問題與回答。
- `05_team_handoff.md`：傳給組員的分工與交付清單。
- `06_mermaid_diagrams.md`：可轉成投影片圖的流程圖。
- `data/research_facts.csv`：資料表版本，方便貼到簡報或表格。
