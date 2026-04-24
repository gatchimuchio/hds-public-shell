# Engineering Posture References

**Status: Engineering posture anchors, not proof of the framework.**

This file collects external references that help explain the engineering attitude behind this repository.

These references are **not** evidence that TCP, Closure Phase Ψ, DDP, or HDS are true.  
They are also **not** evidence of the author’s personal biography or competence.

They are included only as **orientation anchors** showing that the repository’s posture is aligned with well-known engineering practices:

- specification before assertion;
- conformance rather than metaphysical truth;
- verification and validation;
- risk management;
- auditability and traceability;
- responsibility boundary;
- safe stopping;
- public welfare and harm prevention;
- honest limitation disclosure;
- review, correction, and errata.

In short:

```text
This file does not prove the theory.
This file explains the engineering posture behind the theory.
```

---

## 1. Core Posture

The repository’s engineering posture can be summarized as follows:

```text
Do not claim truth when conformance is the target.
Do not assert what is unclosed.
Do not hide requirements, boundaries, or stopping rules.
Do not turn capability into superiority.
Do not convert black boxes into instruments of control.
Keep logs.
State responsibility.
Correct errors.
Stop when the domain becomes unsafe or underdefined.
```

This posture is not presented as morality theater.  
It is treated as an engineering constraint.

---

## 2. Concept Mapping

| Repository concept | Engineering posture | External anchor type |
|---|---|---|
| Conformance over truth | Evaluate by fit to specification, not metaphysical correctness | RFC/requirements engineering |
| `MUST / SHOULD / MAY` | Explicit requirement levels | BCP 14 / RFC 2119 / RFC 8174 |
| `W := (X, R, M)` | Scope, relation, and judging rule must be fixed | Requirements engineering / V&V |
| `SUSPEND` | Valid halt state under underdefinition or risk | Risk management / safety engineering |
| Logs over authority | Traceability and auditability | NIST controls / V&V planning |
| Responsibility boundary | Human operator/author bears final responsibility | IEEE / ACM ethics |
| Black-box respect | Do not claim full internal access when only I/O is observable | AI RMF / XAI / systems engineering |
| Sealed domains | Some implementation paths should not be disclosed | Safety / risk / harm-prevention practice |
| Errata | Correction is part of the system | Professional review / engineering lifecycle |
| Anti-superiority scoring | Avoid misuse of technical measures for human ranking | Ethics / harm prevention |

---

## 3. External Anchors

### A. Specification Discipline

#### 1. BCP 14 / RFC 2119 / RFC 8174

**Role:** Standard reference for requirement-level keywords such as `MUST`, `SHOULD`, and `MAY`.

**Connection to this repository:**  
Supports the repository’s use of explicit requirement language instead of vague philosophical assertion.

**Attached concept:**

```text
Engineering begins when terms stop floating and become requirements.
```

**Boundary:**  
This does not prove TCP. It only supports the use of normative specification language.

URLs:

- https://www.rfc-editor.org/bcp/bcp14
- https://datatracker.ietf.org/doc/rfc2119/
- https://www.ietf.org/rfc/rfc8174.html

---

#### 2. ISO/IEC/IEEE 29148:2018 — Requirements Engineering

**Role:** Standard reference for requirements engineering and specification practice.

**Connection to this repository:**  
Supports the idea that requirements, terms, scopes, and verification methods should be explicitly defined.

**Attached concept:**

```text
Unspecified requirements are not deep.
They are operational defects.
```

**Boundary:**  
This does not validate the repository’s conceptual framework. It only anchors the engineering habit of specifying requirements.

URLs:

- https://www.iso.org/standard/72089.html
- https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html

---

### B. Verification, Validation, and Logs

#### 3. NASA Systems Engineering Handbook — Verification and Validation

**Role:** NASA reference for systems engineering, verification, validation, requirements matrices, and responsibility/change authority.

**Connection to this repository:**  
Supports the repository’s emphasis on:

- verification;
- validation;
- requirements traceability;
- responsibility assignment;
- change authority;
- test/inspection/demonstration/analysis as verification methods.

**Attached concept:**

```text
A claim without verification conditions is not an engineering claim.
```

**Boundary:**  
NASA does not endorse this repository. The reference is used only to show the ordinary engineering background of V&V thinking.

URL:

- https://www.nasa.gov/reference/system-engineering-handbook-appendix/

---

#### 4. NIST SP 800-53 Rev. 5 — Security and Privacy Controls

**Role:** Catalog of security and privacy controls, including audit and accountability, assessment, authorization, monitoring, and risk assessment.

**Connection to this repository:**  
Supports the attitude that serious systems require:

- auditability;
- accountability;
- control families;
- assurance;
- organization-wide risk management.

**Attached concept:**

```text
If it cannot be audited, it should not be trusted as an operational layer.
```

**Boundary:**  
This does not prove the framework. It anchors the repository’s log-first and audit-first posture.

URL:

- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

---

#### 5. NIST SP 800-53A Rev. 5 — Assessing Security and Privacy Controls

**Role:** Methodology and procedures for assessing controls within a risk management framework.

**Connection to this repository:**  
Supports the idea that control claims require assessment procedures rather than mere assertion.

**Attached concept:**

```text
Controls without assessment procedures are decorative.
```

**Boundary:**  
This is not evidence for TCP/Ψ/DDP. It is a reference for assessment-oriented engineering posture.

URL:

- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

---

### C. Risk and Safety

#### 6. ISO 31000:2018 — Risk Management

**Role:** International standard for risk management principles and guidelines.

**Connection to this repository:**  
Supports the repository’s framing that uncertainty, misuse, and downstream harm must be treated as design constraints.

**Attached concept:**

```text
Risk is not an afterthought.
Risk is part of the design object.
```

**Boundary:**  
This does not prove DDP. It anchors the risk-management posture.

URL:

- https://www.iso.org/standard/65694.html

---

#### 7. IEC 61508 — Functional Safety of E/E/PE Safety-Related Systems

**Role:** International functional safety standard for electrical, electronic, and programmable electronic safety-related systems.

**Connection to this repository:**  
Supports the idea that safety functions, lifecycle thinking, risk reduction, and integrity levels are ordinary engineering concerns.

**Attached concept:**

```text
A system is not good because it works.
A system is good only when its failure modes are bounded.
```

**Boundary:**  
This is not an AI theory reference. It is a safety-engineering anchor for bounded failure and stoppability.

Reference page:

- https://61508.org/knowledge/what-is-iec-61508/

---

#### 8. NIST AI Risk Management Framework 1.0

**Role:** Public framework for managing AI risks and discussing trustworthy AI characteristics.

**Connection to this repository:**  
Supports the repository’s emphasis on:

- validity and reliability;
- safety;
- security and resilience;
- accountability and transparency;
- explainability and interpretability;
- harm and bias management.

**Attached concept:**

```text
AI should not be treated as magic.
It must be managed as a risk-bearing system.
```

**Boundary:**  
NIST AI RMF does not validate DDP. It provides general AI risk vocabulary.

URL:

- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- https://doi.org/10.6028/NIST.AI.100-1

---

### D. Trustworthy Systems and Black-Box Management

#### 9. NIST SP 800-160 Vol. 1 Rev. 1 — Engineering Trustworthy Secure Systems

**Role:** NIST publication on engineering trustworthy secure systems.

**Connection to this repository:**  
Supports the view that trustworthy systems require an engineering lifecycle, stakeholder requirements, assurance, and disciplined design rather than superficial output quality.

**Attached concept:**

```text
Trust is not a feeling.
Trust is an engineered property supported by lifecycle discipline.
```

**Boundary:**  
This does not prove the repository’s theory. It anchors the system-engineering stance.

URL:

- https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final

---

#### 10. NISTIR 8312 — Four Principles of Explainable Artificial Intelligence

**Role:** Public report on explainable AI.

**Connection to this repository:**  
Supports the general need to distinguish system output from user understanding, explanation, and system limits.

**Attached concept:**

```text
A black box is not eliminated by naming it.
It must be bounded, observed, and handled with declared limits.
```

**Boundary:**  
This does not prove Closure Phase Ψ. It provides adjacent explainability vocabulary.

URL:

- https://www.nist.gov/publications/four-principles-explainable-artificial-intelligence
- https://doi.org/10.6028/NIST.IR.8312

---

### E. Professional Responsibility

#### 11. IEEE Code of Ethics

**Role:** Engineering ethics reference emphasizing public safety, responsibility, honest claims, competence, and disclosure of risks.

**Connection to this repository:**  
Supports the authorial posture of:

- public welfare first;
- honest claims based on available data;
- risk disclosure;
- correction and criticism;
- responsibility for engineering decisions.

**Attached concept:**

```text
Engineering authority is not permission to dominate.
It is a duty to disclose limits and prevent harm.
```

**Boundary:**  
This does not prove the framework. It anchors the author’s safety-first engineering posture in a conventional professional ethics frame.

URL:

- https://ieee-cas.org/about/ieee-code-ethics

---

#### 12. ACM Code of Ethics and Professional Conduct

**Role:** Computing ethics reference emphasizing avoiding harm, professional review, thorough evaluation, competence, and responsibility.

**Connection to this repository:**  
Supports the repository’s emphasis on:

- harm prevention;
- objective and thorough evaluation;
- review;
- professional limits;
- social impact analysis.

**Attached concept:**

```text
A system that produces clever outputs but hides harm is not intelligent engineering.
It is unmanaged risk.
```

**Boundary:**  
This does not prove the framework. It provides a conventional computing-ethics anchor.

URL:

- https://www.acm.org/code-of-ethics

---

## 4. Engineering Attitude Statement

The authorial engineering attitude of this repository can be stated as:

```text
The purpose of a framework is not to impress.
The purpose is to reduce ambiguity, expose boundaries, preserve responsibility, and make failure modes visible.

A claim that cannot state its scope, input, output, stopping condition, and audit path should not be treated as closed.

A powerful framework that cannot prohibit its own misuse is incomplete.
```

This attitude connects directly to:

- TCP: closure requires `X / R / M`;
- Closure Phase Ψ: stable signatures must be observed, not worshiped;
- DDP: dangerous domains must be sealed;
- HDS: operational use must remain subordinate to ethics, reversibility, and responsibility.

---

## 5. What These References Do and Do Not Support

### They support:

- the repository’s engineering style;
- the use of explicit specifications;
- the legitimacy of conformance-oriented reading;
- the importance of V&V, auditability, and risk management;
- the importance of professional responsibility and harm prevention.

### They do not support:

- a truth claim about TCP;
- a proof of Closure Phase Ψ;
- a proof of DDP;
- a claim that the author is endorsed by IEEE, ACM, NASA, NIST, ISO, IEC, or any cited institution;
- any superiority claim about individuals, groups, models, or cultures.

---

## 6. Suggested Placement in the Repository

Recommended file name:

```text
ENGINEERING_POSTURE_REFERENCES.md
```

Recommended relationship to other files:

```text
README.md
REFERENCES.md
ENGINEERING_POSTURE_REFERENCES.md
LICENSE
docs/
  01_Closure_Phase_Psi_v0_7_bilingual.md
  02_TCP_v0_7_bilingual.md
  03_DDP_v0_7_bilingual.md
```

Recommended README sentence:

```text
For external references explaining the engineering posture behind this repository, see ENGINEERING_POSTURE_REFERENCES.md. These references are orientation anchors, not evidence that the framework is true.
```

---

# 工学的態度・姿勢の参考資料

**位置づけ：フレームワークの証明ではなく、工学的態度の座標合わせ。**

本ファイルは、本リポジトリの背後にある工学的態度・姿勢を説明するための外部参照を整理する。

ここで挙げる資料は、**TCP・閉包位相Ψ・DDP・HDSが真であることの証拠ではない**。  
また、著者個人の経歴・能力・人格を証明するものでもない。

役割はあくまで、次の態度が既存の工学作法と同型であることを示すことである。

- 断定より仕様
- 真理より適合性
- 検証と妥当性確認
- リスク管理
- 監査可能性と追跡可能性
- 責任境界
- 安全な停止
- 公共安全と害の予防
- 限界の正直な開示
- レビュー・訂正・Errata

要するに：

```text
このファイルは理論を証明しない。
このファイルは理論の背後にある工学的態度を説明する。
```

---

## 1. 核となる態度

本リポジトリの工学的態度は、次のように要約できる。

```text
適合性が対象なら、真理を主張しない。
未閉包のものを断定しない。
要求・境界・停止規則を隠さない。
能力を優劣へ変換しない。
ブラックボックスを支配装置へ変換しない。
ログを残す。
責任主体を明示する。
誤りを訂正する。
危険領域・未定義領域では止まる。
```

これは道徳アピールではなく、工学制約である。

---

## 2. 概念対応表

| 本リポジトリの概念 | 工学的態度 | 外部参照の型 |
|---|---|---|
| 真理より適合性 | 仕様への合否で評価する | RFC / 要求工学 |
| `MUST / SHOULD / MAY` | 要求水準を明示する | BCP 14 / RFC 2119 / RFC 8174 |
| `W := (X, R, M)` | 対象・関係・判定規則を固定する | 要求工学 / V&V |
| `SUSPEND` | 未定義・危険時に止まる | リスク管理 / 安全工学 |
| 権威よりログ | 追跡可能性と監査可能性を優先 | NIST統制 / V&V計画 |
| 責任境界 | 最終責任を人間・著者・運用者へ置く | IEEE / ACM倫理 |
| ブラックボックス尊重 | I/Oしか見えない対象を完全同定したと主張しない | AI RMF / XAI / システム工学 |
| 封印領域 | 危険な実装経路を公開しない | 安全 / リスク / 害の予防 |
| Errata | 訂正をシステムの一部にする | 専門レビュー / 工学ライフサイクル |
| 優劣スコアリング禁止 | 技術指標を人間序列化に使わない | 倫理 / 害の予防 |

---

## 3. 外部参照

### A. 仕様規律

#### 1. BCP 14 / RFC 2119 / RFC 8174

**役割：** `MUST`、`SHOULD`、`MAY` などの要求水準語の標準的参照。

**本リポジトリとの接続：**  
曖昧な哲学的断定ではなく、明示的な要求語で仕様を書く姿勢を支える。

**接続する概念：**

```text
語が浮遊を止め、要求になった時点で工学が始まる。
```

**境界：**  
TCPの証明ではない。規格語使用の一般的根拠である。

URLs:

- https://www.rfc-editor.org/bcp/bcp14
- https://datatracker.ietf.org/doc/rfc2119/
- https://www.ietf.org/rfc/rfc8174.html

---

#### 2. ISO/IEC/IEEE 29148:2018 — Requirements Engineering

**役割：** 要求工学・仕様作法の国際標準。

**本リポジトリとの接続：**  
要求、用語、射程、検証方法を明示する態度を支える。

**接続する概念：**

```text
未指定の要求は深遠なのではない。
運用上の欠陥である。
```

**境界：**  
本フレームワークの妥当性を証明しない。仕様化姿勢の座標である。

URLs:

- https://www.iso.org/standard/72089.html
- https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html

---

### B. 検証・妥当性確認・ログ

#### 3. NASA Systems Engineering Handbook — Verification and Validation

**役割：** システム工学、V&V、要求検証マトリクス、責任・変更権限に関する参照。

**本リポジトリとの接続：**  
以下の態度を支える。

- 検証
- 妥当性確認
- 要求の追跡可能性
- 責任割当
- 変更権限
- 分析・検査・実証・試験による検証

**接続する概念：**

```text
検証条件を持たない主張は、工学的主張ではない。
```

**境界：**  
NASAが本リポジトリを支持しているわけではない。V&V思考の一般的背景として使う。

URL:

- https://www.nasa.gov/reference/system-engineering-handbook-appendix/

---

#### 4. NIST SP 800-53 Rev. 5 — Security and Privacy Controls

**役割：** セキュリティ・プライバシー統制のカタログ。Audit and Accountability、Assessment、Authorization、Monitoring、Risk Assessment 等を含む。

**本リポジトリとの接続：**  
重大なシステムには以下が必要であるという態度を支える。

- 監査可能性
- 説明責任
- 統制群
- assurance
- 組織的リスク管理

**接続する概念：**

```text
監査できないものを、運用層として信頼してはならない。
```

**境界：**  
フレームワークの証明ではない。ログ優先・監査優先の態度の座標である。

URL:

- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

---

#### 5. NIST SP 800-53A Rev. 5 — Assessing Security and Privacy Controls

**役割：** リスク管理フレームワーク内で統制を評価するための方法論と手順。

**本リポジトリとの接続：**  
統制主張には評価手順が必要であり、主張だけでは不十分であるという態度を支える。

**接続する概念：**

```text
評価手順を持たない統制は、飾りである。
```

**境界：**  
TCP/Ψ/DDPの証明ではない。評価手順志向の工学姿勢の参照である。

URL:

- https://csrc.nist.gov/pubs/sp/800/53/a/r5/final

---

### C. リスクと安全

#### 6. ISO 31000:2018 — Risk Management

**役割：** リスク管理の原則とガイドラインを示す国際標準。

**本リポジトリとの接続：**  
不確実性、誤用、下流被害を設計制約として扱う姿勢を支える。

**接続する概念：**

```text
リスクは後処理ではない。
リスクは設計対象の一部である。
```

**境界：**  
DDPの証明ではない。リスク管理姿勢の座標である。

URL:

- https://www.iso.org/standard/65694.html

---

#### 7. IEC 61508 — Functional Safety

**役割：** 電気・電子・プログラマブル電子安全関連システムの機能安全に関する国際標準。

**本リポジトリとの接続：**  
安全機能、ライフサイクル思考、リスク低減、完全性水準が通常の工学関心であることを示す。

**接続する概念：**

```text
動くから良いシステムなのではない。
故障モードが境界づけられて初めて良いシステムである。
```

**境界：**  
AI理論の参照ではない。停止可能性・故障境界のための安全工学的座標である。

Reference page:

- https://61508.org/knowledge/what-is-iec-61508/

---

#### 8. NIST AI Risk Management Framework 1.0

**役割：** AIリスク管理と信頼可能AI特性に関する公開フレームワーク。

**本リポジトリとの接続：**  
以下の観点を支える。

- valid and reliable
- safe
- secure and resilient
- accountable and transparent
- explainable and interpretable
- harmful bias managed

**接続する概念：**

```text
AIを魔法として扱ってはならない。
AIはリスクを持つシステムとして管理されるべきである。
```

**境界：**  
NIST AI RMFはDDPを証明しない。AIリスク語彙の一般参照である。

URL:

- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- https://doi.org/10.6028/NIST.AI.100-1

---

### D. 信頼可能システムとブラックボックス管理

#### 9. NIST SP 800-160 Vol. 1 Rev. 1 — Engineering Trustworthy Secure Systems

**役割：** 信頼可能でセキュアなシステムを工学するためのNIST文書。

**本リポジトリとの接続：**  
信頼可能性は表面的な出力品質ではなく、ライフサイクル、ステークホルダー要求、保証、設計規律によって支えられるという態度を補強する。

**接続する概念：**

```text
信頼は気分ではない。
信頼はライフサイクル規律に支えられた工学的性質である。
```

**境界：**  
本リポジトリの理論を証明しない。システム工学姿勢の座標である。

URL:

- https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final

---

#### 10. NISTIR 8312 — Four Principles of Explainable Artificial Intelligence

**役割：** 説明可能AIに関する公開報告書。

**本リポジトリとの接続：**  
システム出力、利用者理解、説明、限界を区別する必要性を支える。

**接続する概念：**

```text
ブラックボックスは、名前を付けても消えない。
境界づけ、観測し、限界を明示して扱うしかない。
```

**境界：**  
閉包位相Ψを証明しない。説明可能性の隣接語彙を与える。

URL:

- https://www.nist.gov/publications/four-principles-explainable-artificial-intelligence
- https://doi.org/10.6028/NIST.IR.8312

---

### E. 専門職責任

#### 11. IEEE Code of Ethics

**役割：** 公共安全、責任、正直な主張、能力、リスク開示を重視する工学倫理の参照。

**本リポジトリとの接続：**  
以下の著者姿勢を支える。

- 公共安全優先
- 利用可能データに基づく正直な主張
- リスク開示
- 批判と訂正
- 工学判断への責任

**接続する概念：**

```text
工学的権威は、支配の許可ではない。
限界を開示し、害を防ぐ責任である。
```

**境界：**  
本フレームワークの証明ではない。安全優先の工学姿勢の一般参照である。

URL:

- https://ieee-cas.org/about/ieee-code-ethics

---

#### 12. ACM Code of Ethics and Professional Conduct

**役割：** 害の回避、専門レビュー、徹底した評価、能力、責任を重視するコンピューティング倫理の参照。

**本リポジトリとの接続：**  
以下の態度を支える。

- 害の予防
- 客観的・徹底的な評価
- レビュー
- 専門的限界
- 社会的影響の分析

**接続する概念：**

```text
賢い出力を出しても、害を隠すシステムは知的工学ではない。
それは管理されていないリスクである。
```

**境界：**  
本フレームワークの証明ではない。計算機倫理の一般参照である。

URL:

- https://www.acm.org/code-of-ethics

---

## 4. 工学的態度の宣言文

本リポジトリの著者姿勢は、次のように記述できる。

```text
フレームワークの目的は、感心させることではない。
曖昧さを減らし、境界を露出させ、責任を保存し、失敗モードを可視化することである。

射程、入力、出力、停止条件、監査経路を示せない主張は、閉包済みとして扱ってはならない。

自分自身の誤用を禁止できない強力なフレームワークは、未完成である。
```

この態度は以下へ直結する。

- TCP：閉包には `X / R / M` が必要
- 閉包位相Ψ：安定署名は観測するものであり、崇拝するものではない
- DDP：危険領域は封印する
- HDS：運用は倫理・可逆性・責任の下位に置かれる

---

## 5. これらの参照が支えるもの・支えないもの

### 支えるもの

- 本リポジトリの工学的文体
- 明示的仕様の使用
- 適合性ベースの読み方の妥当性
- V&V・監査可能性・リスク管理の重要性
- 専門職責任と害の予防

### 支えないもの

- TCPの真理性
- 閉包位相Ψの証明
- DDPの証明
- IEEE・ACM・NASA・NIST・ISO・IEC等による著者または本理論の支持
- 個人・集団・モデル・文化に関する優劣主張

---

## 6. リポジトリ内での配置案

推奨ファイル名：

```text
ENGINEERING_POSTURE_REFERENCES.md
```

配置例：

```text
README.md
REFERENCES.md
ENGINEERING_POSTURE_REFERENCES.md
LICENSE
docs/
  01_Closure_Phase_Psi_v0_7_bilingual.md
  02_TCP_v0_7_bilingual.md
  03_DDP_v0_7_bilingual.md
```

READMEへの追記例：

```text
For external references explaining the engineering posture behind this repository, see ENGINEERING_POSTURE_REFERENCES.md. These references are orientation anchors, not evidence that the framework is true.
```
