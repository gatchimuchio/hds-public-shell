# hds-public-shell

`hds-public-shell` は **公開API殻** です。
責務は、外部から来た候補行為を **F→M→C** の3相で受け、公開可能な範囲で
`ASSERT / SUSPEND / OUT_OF_SCOPE / FAIL` などに落とすことです。

## 役割

- **F (Frame)** — 目的・保護値・世界閉包 `W=(X,R,M)` を整える
- **M (Model)** — 抽象化と構造を出す
- **C (Commit)** — 倫理シェルで最終状態を返す

## 含むもの

- FastAPI エンドポイント
  - `GET /health`
  - `POST /decision`
  - `GET /audit`
  - `DELETE /audit`
  - `GET /policy`
- `HDSUpperController`
- `EthicsPolicy`
- in-memory / optional JSONL audit logger
- pytest 一式

## 含めないもの

- sealed evaluator logic
- threshold / detector / weight
- downstream execution
- operator UI

## deployment safety

`hds-public-shell` is the upstream control shell. Downstream systems such as
`blue-tanuki-core` should call `/decision` before local execution and fail
closed to `SUSPEND` if the shell is unavailable.

Public-safe additions:

- TCP `W=(X,R,M)` closure check.
- Source trust review: external `source` with missing or `untrusted` trust is
  `SUSPEND` with human review.
- Small inspectable tag inference for public tags such as `human_ranking`,
  `personality_scoring`, `manipulation`, `security`, and `mass_impact`.
- Audit payload redaction for secret-like keys.
- `GET /readiness` for deployment checks.

## quick start

```bash
pip install -e ".[dev,server]"
pytest -q
hds-public-shell
```

または

```bash
uvicorn hds_public_shell.main:app --host 127.0.0.1 --port 8000
```

## core との関係

- `blue-tanuki-core` = ローカル上流制御本体
- `hds-public-shell` = 外向け公開API殻

`blue-tanuki-core` がローカルで gate / suspend / audit / dispatch を持ち、
必要なら `hds-public-shell` に判断を問い合わせる構成に揃えています。

## ディレクトリ

```text
hds-public-shell/
├── README.md
├── LICENSE
├── pyproject.toml
├── src/hds_public_shell/
│   ├── __init__.py
│   ├── controller.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   └── policy.py
└── tests/
```
