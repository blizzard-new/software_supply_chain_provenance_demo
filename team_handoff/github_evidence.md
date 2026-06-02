# GitHub 證據整理

## Repo

https://github.com/blizzard-new/software_supply_chain_provenance_demo

## 最新成功 workflow

https://github.com/blizzard-new/software_supply_chain_provenance_demo/actions/runs/26840712563

Run 資訊：

- Workflow: `build-and-attest`
- Branch: `main`
- Commit: `f62d84ffb4a96ee5f85527f53d2f0e7badccb6dc`
- Artifact: `python-distributions`
- Artifact ID: `7366816744`
- Artifact zip digest: `sha256:f6a0e1ab0e48d2ad9d708e5b7763c61844619ddbc0ae85d31e81ba4d983e0a7a`

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
[github] digest   = 25b9c77d2215753d2b54ee213d114484a14d91421c8997357470c3d597faed82
[github] builder  = https://github.com/blizzard-new/software_supply_chain_provenance_demo/.github/workflows/build-and-attest.yml@refs/heads/main
[github] workflow = build-and-attest
[github] commit   = f62d84ffb4a96ee5f85527f53d2f0e7badccb6dc
[github] tlog     = https://rekor.sigstore.dev
```

## 可截圖的 tamper 失敗輸出

```text
[tamper] original sha256 = 25b9c77d2215753d2b54ee213d114484a14d91421c8997357470c3d597faed82
[tamper] tampered sha256 = 7bf7bbba5e8b2729436c7f0c5c56d62a2d102bf03826c0e4382efcb2582c481e
[tamper] Step 2: verify tampered artifact. Expected: FAIL
[github] verification FAILED
[tamper] expected result: tampered artifact failed verification
```

## 報告時要怎麼講

- 原始 wheel 的 digest 和 attestation 裡的 subject digest 一樣，所以 verify pass。
- 篡改後 wheel 的 digest 變成另一個值，GitHub 找不到對應 attestation，所以 verify fail。
- 這證明 attestation 可以偵測 release artifact 被替換或被改掉。
- 但它不保證程式碼沒有漏洞，只能證明來源與建置流程。
