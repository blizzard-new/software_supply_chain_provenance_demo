# 可以直接貼給組員的訊息

我們期末報告先做第一個題目：「軟體供應鏈簽章與可驗證 Provenance」。

GitHub 和 demo 已經建好了：

https://github.com/blizzard-new/software_supply_chain_provenance_demo

截圖證據使用的 Actions 已經成功：

https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975

這個 run 已經完成：

- build Python artifact
- 用 `actions/attest@v4` 產生 artifact attestation
- 用 `gh attestation verify` 驗證原始 wheel 成功
- 改 1 byte 後驗證失敗

做簡報可以看：

- `team_handoff/README.md`
- `team_handoff/github_evidence.md`
- `team_handoff/demo_screenshot_checklist.md`
- `team_handoff/screenshots/`
- `presentation_materials/01_slide_outline.md`
- `presentation_materials/02_research_facts.md`
- `presentation_materials/04_q_and_a.md`

簡報主線就是：下載到的 artifact 需要能證明來源；GitHub attestation 可以把 artifact 和 repo、commit、workflow 綁起來；原始 artifact 驗證成功，篡改 artifact 驗證失敗。
