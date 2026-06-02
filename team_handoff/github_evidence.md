# GitHub 證據整理

## Repo

https://github.com/blizzard-new/software_supply_chain_provenance_demo

## 截圖證據使用的成功 workflow

https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26841214975

Run 資訊：

- Workflow: `build-and-attest`
- Branch: `main`
- Commit: `c7ee14ad9699ec7a942ccc481d6be5aa87a622d9`
- Artifact: `python-distributions`
- Artifact ID: `7367022299`
- Artifact zip digest: `sha256:89325abc3ee0cd5bc171a265e64443cc715effc67d949fce8852c1b448d28156`

## Workflow 成功步驟

- `Run tests`: success
- `Build package artifact`: success
- `Upload package artifact`: success
- `Generate artifact attestation`: success
- `Verify artifact attestation`: success
- `Verify tamper is rejected`: success

## 可截圖的 verify 成功輸出

```text
[github] verification PASSED
[github] subject  = hello_provenance_demo-0.1.0-py3-none-any.whl
[github] digest   = 7e1631c43d5ba0743c62a79df5b469df55a73f9c00a972ea1358ba55b3b4a7d5
[github] builder  = https://github.com/blizzard-new/software_supply_chain_provenance_demo/.github/workflows/build-and-attest.yml@refs/heads/main
[github] workflow = build-and-attest
[github] commit   = c7ee14ad9699ec7a942ccc481d6be5aa87a622d9
[github] tlog     = https://rekor.sigstore.dev
```

## 可截圖的 tamper 失敗輸出

```text
[tamper] original sha256 = 7e1631c43d5ba0743c62a79df5b469df55a73f9c00a972ea1358ba55b3b4a7d5
[tamper] tampered sha256 = 34b3d6cc07aaa300c8ed0723e29dfe107c811f16f49472393162d1df53971242
[tamper] Step 2: verify tampered artifact. Expected: FAIL
[github] verification FAILED
[tamper] expected result: tampered artifact failed verification
```

## 報告時要怎麼講

- 原始 wheel 的 digest 和 attestation 裡的 subject digest 一樣，所以 verify pass。
- 篡改後 wheel 的 digest 變成另一個值，GitHub 找不到對應 attestation，所以 verify fail。
- 這證明 attestation 可以偵測 release artifact 被替換或被改掉。
- 但它不保證程式碼沒有漏洞，只能證明來源與建置流程。
