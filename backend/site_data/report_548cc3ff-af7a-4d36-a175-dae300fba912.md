# FUTURESCOUT AI research report: post-quantum cryptography

Generated: 2026-11-09 06:04 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, scout, investment
- Agents NOT run in this version: patent, x. Conclusions therefore have no patent, social-media evidence.

## Summary
The evidence shows a field in rapid research expansion (exact-phrase papers rising from 847 in 2024 to 1,913 in 2025, +125.9% YoY) around three NIST-standardised algorithms (ML-KEM, ML-DSA, SLH-DSA) whose energy and speed on tested 32/64-bit platforms is reported comparable to classical ECC for key establishment and signing, except SLH-DSA signing on 32-bit hardware (S1-S3). Risk and challenge findings materially qualify this: the 'constrained' hardware tested was Raspberry Pi-class, not microcontrollers (C1), server-side, bandwidth and DDoS-amplification costs are measured elsewhere (R1, R3, C2), PQC security is described as conjectured rather than proven (R7, C6), and side-channel, PAKE-coverage and operational-inventory gaps remain open (R5, R6, R8). On the commercial side, PQC appears in SEC filings from network security vendors, an application-delivery vendor, a telecom and banks (M1, M2, M4, M5, M7), but these are product-marketing and risk statements, not evidence of paying customer adoption, and Cisco itself flags failure to drive adoption as a risk (M3). No patent evidence, no social/X evidence and no price-and-timing evidence were available in this version, and the Company Scout list is dominated by micro-cap filers with negligible or declining revenue whose PQC claims should be treated with heavy caution (K1, K4, K5). The main uncertainty is not whether PQC standards exist but how quickly heterogeneous estates migrate, at what operating cost, and with what residual cryptanalytic and implementation risk.

## Technology Opportunity Score
**Score: 43.1 / 100** (confidence: low; evidence coverage 90%)

Risk adjustment: rating 4/5 lowered the score by 24.0% (base 56.7).

Commercialization Gap (research momentum rating minus commercial readiness rating): +2


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S2, S5, S11, R1, R3, R8 | Code-computed OpenAlex counts of works containing the exact phrase rise from 265 (2020) to 847 (2024) and 1,913 (2025), a 125.9% YoY increase, and the retrieved findings show the literature spanning benchmarking, protocol integration, side channels and hybrid QKD-PQC work (S1-S12, R1-R9). Caveat: the count is exact-phrase only, not synonym-normalised and not adjusted for overall publishing growth, and high paper volume is not evidence of commercial success (rule 7). |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 3 | S1, S2, S3, S4, R1, R3, R5, R7 | The standards are finalised and benchmarked for real migration (S1, S4), and ML-KEM/ML-DSA are reported energy- and speed-comparable to classical ECC on the tested hardware (S2). This is offset by SLH-DSA signing being impractical on constrained 32-bit devices (S3), telemetry showing server CPU loaded up to 88 times longer in one PQC-TLS testbed (R1), structural bandwidth growth from signatures and hybrids (R3), contested security proof status (R7) and open side-channel work (R5). |
| Commercial Readiness | 15% | 3 | M1, M2, M4, M5, M7 | Multiple vendors already describe quantum-safe products in SEC filings: Fortinet within FortiOS (M1), Cisco in AI-ready switches (M2), F5 in application delivery and security (M4), and Chunghwa Telecom lists PQC certificates among its cybersecurity offerings (M5). Readiness is product-level only: no filing quantifies PQC revenue, and one large bank frames migration as complex because of legacy systems (M7). |
| Customer Adoption | 10% | 2 | M3, M7 | The evidence is about product marketing and risk framing, not adoption. Cisco flags failure to timely implement or drive customer adoption as a risk that could expose pre-quantum data (M3), and a large bank describes migration as complex due to legacy systems and interdependencies (M7). No finding reports a deployed customer, contract or adoption metric. |
| Industry Investment | 10% | 2 | K2, K3, M10, M7 | No finding quantifies investment specifically in PQC. Indirect signals are company-level R&D intensity from Company Scout (F5 at 17.5% of revenue, Cisco at 15.1%) (K2, K3) and PQC appearing across sectors in filings (M10, M7); none of this isolates PQC spending, so this is a weak, low-confidence rating rather than a measured one. |
| Competitive Position | 10% | 2 | M1, M2, M4, M5, M9, K2, K3 | Filings identify participants (Fortinet M1, Cisco M2, F5 M4, Chunghwa M5), and among the configured cybersecurity companies only Fortinet's retrieved excerpt mentions PQC (M9). There is no evidence of market share, differentiation, win rates or pricing, and the Company Scout scores are explicitly heuristics, not rankings of competitive strength. |
| Supply-Chain Readiness | 15% | 2 | S3, C1, R3, R6 | Constrained-device supply-chain readiness is not directly measured. The relevant evidence is that SLH-DSA signing is impractical on resource-constrained devices and 32-bit costs are substantially higher than 64-bit (S3), parity claims exclude microcontroller-class hardware (C1), signature and hybrid payloads expand bandwidth (R3), and organisations lack visibility into TLS configurations across heterogeneous estates (R6). These point to immature supply-chain readiness for embedded PQC. |

Formula: base = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100; score = base x (1 - max_penalty x risk_rating/5). Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. The score is an explainable heuristic, not a validated prediction of stock performance.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.
- Confidence lowered to 'low': coverage is 90%, but the cited ratings themselves are mostly of lower confidence.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Enterprise PQC migration in network security and application delivery

Technologies: ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205), hybrid classical+PQC TLS, PQC certificates

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Evidence for the next 12 months is limited to vendor product statements (M1, M2, M4, M5) and one explicit adoption risk (M3). No customer-deployment, revenue or pricing evidence exists, and the operational findings suggest inventory and configuration, not algorithm choice, is the near-term bottleneck (R6). There is no price-and-timing evidence at all in this version, so nothing can be said about how much of this is already reflected in any market. *(forecast)* [M1, M2, M3, M4, M5, R6] | low |
| medium_1_3y | Standards are final and benchmarking work is mature enough that migration planning is technically actionable (S1, S4, R3), which supports a 1-3 year migration window for large, well-resourced organisations; however the claims that governments are 'mandating' migration rest on one preprint abstract with no policy document retrieved (C3), so the regulatory timing cannot be relied on. Banks citing legacy-system complexity (M7) indicate migration stretches beyond this window for some sectors. *(forecast)* [S1, S4, R3, C3, M7] | medium |
| long_3_5y | Nothing in the retrieved evidence speaks directly to 3-5 year outcomes; the findings support only that standards exist and hybrid deployment is being studied (S1, S8). Long-run value depends on whether cryptanalytic and implementation risk is reduced (R7, R5) and whether adoption actually occurs (M3), neither of which the evidence resolves. *(forecast)* [S1, S8, R5, R7, M3] | low |

**Bull case:** PQC standards are finalised and the literature has shifted toward benchmarking real migration on real platforms, with ML-KEM and ML-DSA reported as broadly comparable to classical ECC in energy and speed on tested hardware (S1, S2). Vendors across networking, application delivery and telecom already describe quantum-safe products and PQC certificates in regulatory filings (M1, M2, M4, M5), and the topic appears across banking and insurance filings as a general enterprise risk item (M10, M7). A standards-driven, compliance-shaped refresh cycle could therefore pull through on a multi-year horizon. *(ai_interpretation)* [S1, S2, M1, M2, M4, M5, M7, M10]

**Base case:** Migration proceeds, but the binding constraints are operational and cost-related rather than algorithmic. Organisations lack visibility into TLS configurations across heterogeneous estates (R6), PQC signature payloads and hybrid modes expand bandwidth (R3), PQC-enabled TLS can amplify handshake-exhaustion attacks and intrusion detection degrades on PQC traffic (R1, R2), and SLH-DSA signing is impractical on constrained 32-bit devices (S3). The 'comparable to ECC' result was measured on Raspberry Pi-class hardware, not microcontrollers (C1), so parity claims should not be generalised. Value accrues to vendors with existing installed estates rather than as a step change in demand. *(ai_interpretation)* [R1, R2, R3, R6, S3, C1, S2]

**Bear case:** The case can fail on three fronts. First, security is asserted rather than proven: PQC security is described as conjectured and implementations are computationally expensive (R7), and the findings never state residual cryptanalytic risk (C6). Second, the measured penalty depends heavily on workload, threat model and hardware, with no common benchmark reconciling 'minimal cost' against 'severe amplification' reports (R4). Third, adoption may simply not happen on schedule - Cisco explicitly flags failure to implement or drive customer adoption as a risk (M3) - and protocol classes such as PAKE lack mature quantum-safe options (R8). The name-level evidence is also weak: the only company filings specifically centred on PQC include micro-cap filers with negligible revenue and negative growth (M8, K1, K4, K5). *(ai_interpretation)* [R7, R4, R8, M3, M8, K1, K4, K5]

**Catalysts:**
- Retrievable government mandate or regulatory text confirming the migration deadlines asserted in S1 would convert a preprint claim into a checkable driver (C3). *(assumption)* [S1, C3]
- A company filing that quantifies PQC-attributable revenue, bookings or a customer count rather than describing a capability (M1, M2, M4, M5). *(assumption)* [M1, M2, M4, M5]
- Publication of a common, reproducible benchmark reconciling the conflicting overhead results (R4). *(assumption)* [R4, R3, R1]
- Evidence that PQC traffic does not degrade intrusion detection or amplify handshake exhaustion in production (R1, R2). *(assumption)* [R1, R2]

**Risks:**
- Operational complexity, not cryptography, may set the pace: lack of TLS configuration visibility across estates makes inventory and repeatable enablement hard (R6), and legacy interdependencies are cited by a large bank (M7). *(ai_interpretation)* [R6, M7]
- Reliability and cost penalty: PQC-enabled TLS can hold server CPU highly loaded for up to 88 times longer in one testbed, signature payloads dominate size growth, and hybrids add more (R1, R3). *(ai_interpretation)* [R1, R3]
- Security blind spot during migration: deep-learning intrusion detection degrading to near-random AU-ROC on PQC traffic (R2). *(ai_interpretation)* [R2]
- Unresolved security basis and side channels: security is conjectured rather than proven, and masking countermeasures for LWE schemes carry cost (R7, R5, C6). *(ai_interpretation)* [R7, R5, C6]
- Name-level quality risk: filings by micro-cap companies with negligible revenue and negative growth make PQC claims, including an unusual pairing with decentralised infrastructure (M8, K1, K4, K5). *(unverified_claim)* [M8, K1, K4, K5]
- Coverage gaps: password-authenticated key exchange has received little attention in migration efforts (R8). *(ai_interpretation)* [R8]

**What would invalidate this thesis:**
- Evidence that measured PQC overhead is not manageable in production networks, i.e. no benchmark reconciles the conflicting results and the severe-amplification cases generalise (R4, R1, R3). *(assumption)* [R4, R1, R3]
- Evidence that enterprises are not migrating: filings continuing to describe PQC only as a future capability with no customer deployment, consistent with the adoption risk Cisco itself flags (M3, M1, M4). *(assumption)* [M3, M1, M4]
- Discovery of practical cryptanalytic weaknesses in the standardised lattice or hash-based schemes, which the current evidence does not address (R7, C6). *(assumption)* [R7, C6]
- PQC mentions continuing to be confined to micro-cap filings with negligible revenue rather than established vendors with disclosed deployments (M8, K1, K4, K5). *(assumption)* [M8, K1, K4, K5]

**Conflicting evidence:**
- C1 weakens S2: the 'constrained IoT-class' hardware tested was Raspberry Pi 1/Zero/4 plus a laptop running OpenSSL 3.5, not microcontroller-class devices, and the parity result comes from a single preprint covering only energy and speed. *(ai_interpretation)* [C1, S2]
- C2 weakens S2 and S12: framing PQC cost as an energy/speed trade-off omits server-side and network costs, including handshake-exhaustion amplification and signature/hybrid bandwidth expansion measured elsewhere. *(ai_interpretation)* [C2, S2, S12, R1, R3]
- C3 challenges S1: the claim that US, UK and EU governments 'mandate' migration is an introductory assertion in one preprint abstract, no policy document was retrieved, and the abstract carries an anomalous future publication date. *(ai_interpretation)* [C3, S1]
- C4 challenges S4: the cited abstract describes a July 2022 four-candidate announcement, not the final FIPS 203/204/205 set, and omits code-based selection such as HQC and FN-DSA. *(ai_interpretation)* [C4, S4]
- C5 challenges S11: the claimed bifurcation of the field is likely an artefact of a small sample and ignores a third strand of deployment-security and operational studies (handshake DDoS, IDS blind spots, TLS inventory, side channels, PAKE gaps). *(ai_interpretation)* [C5, S11, R1, R2, R6, R8]
- C6 challenges S7 and S12: PQC security is treated as settled when retrieved work describes it as conjectured, with unresolved implementation risk such as side channels and masking cost. *(ai_interpretation)* [C6, S7, S12, R7, R5]
- C7 challenges S7: the QKD-versus-PQC verdict rests on a single non-peer-reviewed survey and is contested by work combining QKD and PQC in one deployed system. *(ai_interpretation)* [C7, S7, S8]

**Companies named by cited evidence:**
- F5, Inc.: Names post-quantum cryptography readiness in its application delivery and security portfolio (M4); Company Scout records 1 SEC report mentioning the topic, fiscal 2025 revenue 3.09B USD, growth +9.7%, R&D 17.5% of revenue, next-runner score 40/100 - a heuristic, not a prediction, and the PQC revenue contribution is not disclosed. [M4, K2]
- Cisco Systems, Inc.: States that AI-ready switches carry quantum-resistant security and PQC (M2) and separately flags failure to drive customer adoption of PQC as a risk (M3); Company Scout records 3 SEC reports mentioning the topic, fiscal 2026 revenue 63.33B USD, growth +11.8%, next-runner score 35/100 - heuristic only. [M2, M3, K3]
- Fortinet, Inc.: Describes quantum-safe tools and emerging quantum-resistant capabilities within FortiOS in both its 10-K and 10-Q (M1); it is the only company among the configured cybersecurity list whose retrieved filing excerpts mention PQC (M9). [M1, M9]
- Chunghwa Telecom Co Ltd: Lists PQC certificates among its cybersecurity technology areas alongside FIDO, zero trust and V2X (M5); Company Scout records 1 SEC report mentioning the topic, fiscal 2024 revenue 229.97B TWD, growth +3.0%, R&D 1.8% of revenue, next-runner score 25/100 - heuristic only. [M5, K6]
- Banco Santander (Brasil) S.A.: Describes the post-quantum transition as complex because of legacy systems and interdependencies, evidence that migration is an acknowledged operational challenge for a large financial institution (M7). Listed as a filer mention, not as a PQC vendor. [M7]
- Reliance Global Group, Inc.: States its business is focused on post-quantum cryptography and related data protection technologies (M6); Company Scout shows 2 SEC reports mentioning the topic, fiscal 2025 revenue 0.01B USD (micro by revenue), growth -11.6%, next-runner score 35/100. Small-cap, thinly covered, micro revenue: higher risk and less disclosure; the score is a heuristic, not a return forecast. [M6, K5]
- Cavitation Technologies, Inc.: Its filing claims use of PQC and decentralised infrastructure to protect transactions, an unusual pairing for a company with negligible revenue (M8); Company Scout shows 4 SEC reports mentioning the topic, fiscal 2026 revenue 0.00B USD, growth -98.5%, R&D 366.7% of revenue, next-runner score 45/100. Micro-cap with collapsing revenue and a promotional-sounding claim: treat with strong caution; the score is a heuristic, not a prediction. [M8, K1]
- Q/C Technologies, Inc.: Company Scout records 2 SEC reports mentioning post-quantum cryptography, fiscal 2018 revenue 0.00B USD and growth -50.4%, next-runner score 35/100. Micro-cap with no current revenue evidence and stale financials; higher risk and much less disclosure. The score is a heuristic, not a prediction of returns. [K4]

### Constrained-device and hardware-level PQC deployment

Technologies: ML-KEM on embedded/IoT hardware, ML-DSA on embedded/IoT hardware, SLH-DSA, LWE masking countermeasures, PQC-hardened network appliances

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The evidence supports only that benchmarking on constrained hardware is an active research area (S2, S3) with a measured signing penalty on 32-bit hardware; there is no finding on shipping embedded PQC products, volumes or customers, so nothing can be concluded for the next 12 months. *(forecast)* [S2, S3] | low |
| medium_1_3y | The reported trade-off between post-quantum security and deployment feasibility on resource-limited platforms is a recurring open issue (S12), with SLH-DSA signing flagged as impractical on constrained devices (S3) and masking countermeasures carrying cost for LWE schemes (R5). This suggests asymmetric progress: key establishment may port relatively easily, signing and side-channel protection are harder. *(forecast)* [S12, S3, R5] | low |
| long_3_5y | No retrieved finding addresses 3-5 year hardware outcomes. The claim that PQC is 'comparable to ECC' was measured on Raspberry Pi-class hardware rather than microcontrollers, so any long-run parity expectation is unsupported (C1). *(forecast)* [C1, S2] | low |

**Bull case:** Standards are fixed and benchmarking shows ML-KEM and ML-DSA performing at energy and speed levels comparable to classical elliptic-curve cryptography on the hardware tested, which if it holds on microcontroller-class devices would make embedded quantum-safe networking and IoT security a tractable engineering problem rather than a research one (S1, S2). Hardware vendors with existing appliance estates already market quantum-resistant security (M2, M4), giving a distribution channel for constrained-device PQC. *(ai_interpretation)* [S1, S2, M2, M4]

**Base case:** Progress is real but uneven and platform-dependent. SLH-DSA signing is impractical on resource-constrained devices and sign costs are substantially higher on 32-bit than 64-bit hardware (S3), the parity result was obtained on Raspberry Pi-class rather than microcontroller hardware (C1), and side-channel protection for lattice schemes remains an active research area with an associated cost (R5). The practical outcome is that some algorithm/operation combinations port to constrained devices well before others. *(ai_interpretation)* [S3, C1, R5, S12]

**Bear case:** The constrained-device case rests on thin and partly contradicted evidence. The headline parity claim comes from a single preprint, excludes microcontrollers and covers only energy and speed (C1), while server-side and network costs are excluded from the framing entirely (C2). Deployment-coverage gaps persist, including password-authenticated key exchange (R8), and operational inventory problems (R6) mean hardware upgrades may be sequenced behind configuration and visibility work. If signing costs and side-channel protections remain expensive, embedded PQC adoption stalls at the gateway/edge rather than reaching endpoint devices. *(ai_interpretation)* [C1, C2, R5, R6, R8, S3]

**Catalysts:**
- Independent measurements of ML-KEM and ML-DSA on microcontroller-class hardware rather than Raspberry Pi-class boards (C1). *(assumption)* [C1, S2, S3]
- A reconciled benchmark on signing cost and side-channel masking overhead across platforms (R4, R5). *(assumption)* [R4, R5]
- Vendor filings disclosing embedded or appliance-level PQC features with quantified shipment or customer evidence (M2, M4). *(assumption)* [M2, M4]

**Risks:**
- Signing operations, especially SLH-DSA, remain impractical on constrained 32-bit devices (S3, S12). *(ai_interpretation)* [S3, S12]
- Side-channel and hardware implementation constraints are open deployment risks, and masking countermeasures for LWE schemes imply added cost (R5). *(ai_interpretation)* [R5]
- Overhead is workload-, threat-model- and hardware-dependent with no common benchmark, so any single performance figure can mislead (R4, C2). *(ai_interpretation)* [R4, C2]
- Protocol-coverage gaps, notably PAKE, leave some hardware authentication paths without mature quantum-safe options (R8). *(ai_interpretation)* [R8]

**What would invalidate this thesis:**
- Evidence that parity with classical ECC does not hold on microcontroller-class hardware once measured (C1, S2). *(assumption)* [C1, S2]
- Evidence that signing cost and masking overhead are prohibitive in field deployments rather than merely non-trivial (S3, R5). *(assumption)* [S3, R5]
- Evidence that constrained deployments adopt hybrid QKD rather than PQC for the relevant use cases, which the retrieved work suggests is contested rather than settled (S8, C7). *(assumption)* [S8, C7]

**Conflicting evidence:**
- C1 directly weakens S2's application to constrained devices: tested hardware was Raspberry Pi-class plus a laptop, not microcontrollers, from a single preprint covering only energy and speed. *(ai_interpretation)* [C1, S2]
- C2 notes that framing the trade-off as energy and speed omits server-side and network costs, so constrained-device conclusions do not describe whole-system cost. *(ai_interpretation)* [C2, R1, R3]
- C5 argues the benchmarking-versus-immature-hybrids split is a sampling artefact and ignores a deployment-security strand that matters most for embedded rollouts. *(ai_interpretation)* [C5, S11]

**Companies named by cited evidence:**
- Cisco Systems, Inc.: Names quantum-resistant security and PQC in its AI-ready switch products (M2), the closest thing in the retrieved evidence to a hardware-adjacent PQC product claim; Company Scout shows 3 SEC reports mentioning the topic with fiscal 2026 revenue 63.33B USD and next-runner score 35/100 - heuristic only, and no PQC revenue is disclosed. [M2, K3]
- F5, Inc.: Positions PQC readiness within application delivery and security solutions (M4), relevant to the edge/appliance layer of a constrained deployment; Company Scout shows fiscal 2025 revenue 3.09B USD, R&D 17.5% of revenue, next-runner score 40/100 - a heuristic, not a prediction. [M4, K2]
- Fortinet, Inc.: Describes quantum-safe tools and quantum-resistant capabilities in FortiOS (M1), a platform that spans appliance and edge form factors; no PQC-specific revenue or unit evidence is disclosed. [M1]
- Chunghwa Telecom Co Ltd: Lists PQC certificates among its cybersecurity technology areas (M5), indicating a telecom operator role in certificate issuance and network-level deployment; Company Scout next-runner score 25/100 - heuristic only. [M5, K6]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 265, 2021: 287, 2022: 363, 2023: 528, 2024: 847, 2025: 1913, 2026: 3152}
Research Acceleration 2024->2025: 847 -> 1913 (125.9% YoY). OpenAlex works whose title or abstract contains the exact phrase "post-quantum cryptography", per publication year. Synonyms and abbreviations are not counted, and the number is not normalised for overall growth in publishing. The current (partial) year is excluded.

- **[S1]** *(verified_fact, confidence medium)* The three NIST-standardised post-quantum algorithms (FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA) are being benchmarked for real migration, and government mandates in the US, UK and EU are driving that migration.
  - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
  - excerpt: "governments across the US, UK and EU mandating migration to quantum-resistant standards"
  - reasoning: Single arXiv preprint covering only titles/abstract; the migration-mandate claim rests on one abstract.
- **[S2]** *(verified_fact, confidence medium)* Measured on constrained IoT-class and general-purpose hardware, ML-KEM and ML-DSA show energy and speed efficiency comparable to classical elliptic-curve cryptography.
  - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
  - excerpt: "results show that ML-KEM and ML-DSA achieve energy and speed efficiency comparable to classical elliptic-curve cryptography across all tested architectures."
  - reasoning: Directly stated in one arXiv abstract; not independently corroborated by other papers in this set.
- **[S3]** *(verified_fact, confidence medium)* SLH-DSA signing is flagged as impractical on resource-constrained devices, with signing energy costs on 32-bit hardware substantially higher than on 64-bit hardware.
  - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
  - excerpt: "SLH-DSA signing is inadvisable on constrained hardware"
  - reasoning: Stated in the same single preprint abstract; the numeric comparison is not corroborated elsewhere in this set.
- **[S4]** *(verified_fact, confidence medium)* Lattice-based constructions dominate current NIST-standardised post-quantum cryptography, with hash-based schemes the other main selected family.
  - source: [The Mathematical Foundation of Post-Quantum Cryptography](https://arxiv.org/abs/2404.19186v1) (arXiv, 2024-04-30, abstract_only)
  - excerpt: "three of them are based on lattice theory and the other one is based on Hash function."
  - reasoning: Stated in one arXiv preprint abstract describing the July 2022 NIST announcement.
- **[S5]** *(verified_fact, confidence medium)* The post-quantum literature spans several distinct cryptographic families: lattice-based, hash-based, code-based, multivariate polynomial, and isogeny-based cryptography.
  - source: [Applications of Post-Quantum Cryptography](https://doi.org/10.34190/eccws.23.1.2247) (OpenAlex, 2024-06-21, abstract_only)
  - source: [A Survey of Post-Quantum Cryptography: Start of a New Race](https://doi.org/10.3390/cryptography7030040) (OpenAlex, 2023-08-14, abstract_only)
  - source: [Post Quantum Cryptography: A Review of Techniques, Challenges and Standardizations](https://doi.org/10.1109/icoin56518.2023.10048976) (OpenAlex, 2023-01-11, abstract_only)
  - excerpt: "including lattice-based, hash-based, code-based, multivariate polynomial, and isogeny-based cryptography"
  - reasoning: Multiple reviews enumerate the same family taxonomy, though all are abstracts only.
- **[S6]** *(verified_fact, confidence medium)* The motivating threat model is consistent across reviews: Shor-type quantum algorithms would break widely deployed asymmetric cryptosystems (RSA, Diffie-Hellman, ECC), while Grover's algorithm weakens symmetric schemes.
  - source: [Post Quantum Cryptography: A Review of Techniques, Challenges and Standardizations](https://doi.org/10.1109/icoin56518.2023.10048976) (OpenAlex, 2023-01-11, abstract_only)
  - source: [A Survey on Post-Quantum Cryptography: State-of-the-Art and Challenges](https://arxiv.org/abs/2312.10430v1) (arXiv, 2023-12-16, abstract_only)
  - source: [Post-Quantum Cryptography Neural Network](https://arxiv.org/abs/2402.16002v1) (arXiv, 2024-02-25, abstract_only)
  - excerpt: "Major breakthroughs in quantum computing will render all the present-day widely used asymmetric cryptosystems insecure."
  - reasoning: Same threat framing appears in several abstracts, but none reports new cryptanalytic results.
- **[S7]** *(verified_fact, confidence low)* At least one paper argues quantum-resistant (post-quantum) cryptography is currently the more viable path than quantum key distribution, given present limitations of quantum cryptography.
  - source: [A Survey on Post-Quantum Cryptography: State-of-the-Art and Challenges](https://arxiv.org/abs/2312.10430v1) (arXiv, 2023-12-16, abstract_only)
  - excerpt: "it is currently better to use quantum-resistant cryptography."
  - reasoning: A single arXiv preprint abstract; it is a position stated by the authors, not a demonstrated comparative result.
- **[S8]** *(verified_fact, confidence low)* Work exists on combining QKD with PQC in a single deployed system, using dynamic obfuscation of the operation sequence and a GPS-free quantum synchronisation protocol.
  - source: [Obfuscated Quantum and Post-Quantum Cryptography](https://arxiv.org/abs/2508.07635v2) (arXiv, 2025-08-11, abstract_only)
  - excerpt: "we present an experimental deployment of a new design for combined quantum key distribution (QKD) and post-quantum cryptography (PQC)"
  - reasoning: Single preprint abstract describing one experimental deployment; no independent replication in this set.
- **[S9]** *(verified_fact, confidence low)* Quantum technologies are also proposed as an enhancement to cybersecurity itself, with reported experimental demonstrations of device-independent random number generators, device-independent QKD, quantum memories and analog quantum simulators.
  - source: [Post-quantum cryptography and the quantum future of cybersecurity](https://doi.org/10.1103/physrevapplied.21.040501) (OpenAlex, 2024-04-09, abstract_only)
  - excerpt: "experimental demonstrations of device-independent random number generators, device-independent quantum key distribution, quantum memories, and analog quantum simulators"
  - reasoning: A single review abstract lists these demonstrations without quantitative detail.
- **[S10]** *(verified_fact, confidence low)* An exploratory direction maps a code-based PQC scheme onto a neural network structure, using non-linear activation and ciphertext perturbation to harden encryption.
  - source: [Post-Quantum Cryptography Neural Network](https://arxiv.org/abs/2402.16002v1) (arXiv, 2024-02-25, abstract_only)
  - excerpt: "this study proposes a PQC-based neural network that maps a code-based PQC method to a neural network structure"
  - reasoning: Single preprint abstract; the demonstration is described only on cellular network signals and is far from standardised use.
- **[S11]** *(ai_interpretation, confidence medium)* Across this sample the field has bifurcated into (a) performance/energy benchmarking of the already-standardised algorithms against migration constraints, and (b) exploratory or hybrid schemes (QKD-PQC, neural-network PQC) that are much less mature.
  - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
  - source: [A Comparative Performance Evaluation of Kyber, sntrup761, and FrodoKEM for Post-Quantum Cryptography](https://arxiv.org/abs/2508.10023v1) (arXiv, 2025-08-07, abstract_only)
  - source: [A Survey of Post-Quantum Cryptography: Start of a New Race](https://doi.org/10.3390/cryptography7030040) (OpenAlex, 2023-08-14, abstract_only)
  - source: [Post Quantum Cryptography: A Review of Techniques, Challenges and Standardizations](https://doi.org/10.1109/icoin56518.2023.10048976) (OpenAlex, 2023-01-11, abstract_only)
  - source: [Obfuscated Quantum and Post-Quantum Cryptography](https://arxiv.org/abs/2508.07635v2) (arXiv, 2025-08-11, abstract_only)
  - source: [Post-Quantum Cryptography Neural Network](https://arxiv.org/abs/2402.16002v1) (arXiv, 2024-02-25, abstract_only)
  - reasoning: The benchmarking paper and the surveys treat standardised algorithms as the deployment target, while the QKD-PQC and neural-network papers describe novel designs; several of the latter are arXiv preprints and unreviewed.
- **[S12]** *(ai_interpretation, confidence medium)* A recurring open issue is the trade-off between post-quantum security and deployment feasibility on resource-limited platforms, particularly signing operations and IoT-class hardware.
  - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
  - source: [Applications of Post-Quantum Cryptography](https://doi.org/10.34190/eccws.23.1.2247) (OpenAlex, 2024-06-21, abstract_only)
  - source: [A Comparative Performance Evaluation of Kyber, sntrup761, and FrodoKEM for Post-Quantum Cryptography](https://arxiv.org/abs/2508.10023v1) (arXiv, 2025-08-07, abstract_only)
  - source: [A Survey of Post-Quantum Cryptography: Start of a New Race](https://doi.org/10.3390/cryptography7030040) (OpenAlex, 2023-08-14, abstract_only)
  - reasoning: The energy benchmark reports concrete hardware penalties, and the comparative/survey papers frame transition challenges and algorithm trade-offs; evidence is abstract-level only.

**Emerging directions:**
- Energy-aware benchmarking of NIST-standard algorithms on constrained and general-purpose hardware
- Combined QKD + PQC deployments with dynamically obfuscated operation sequences and quantum synchronisation
- Quantum-assisted security primitives (device-independent RNG, DI-QKD, quantum memories) as complements to classical PQC
- Non-standard constructions such as neural-network-mapped code-based encryption
- Mathematical unification of lattice security with sphere packing/covering and quadratic forms

**Open problems:**
- SLH-DSA signing is reported as impractical on 32-bit constrained devices
- Transitioning legacy classical systems to post-quantum standards remains a stated challenge
- Quantum key distribution's present limitations are argued to make it less viable than quantum-resistant cryptography today
- Unclear robustness/performance trade-offs across algorithm families for specific application domains
- Whether novel constructions such as neural-network PQC provide genuine security is not established in these abstracts

**Limitations:**
- Most items are abstracts or metadata only; no full texts were available to this analysis.
- Several key sources are arXiv preprints that are not peer reviewed (e.g. the energy benchmark, the QKD-PQC deployment, the neural-network PQC paper).
- Two entries (the Springer reference entry and the transition report) have no abstract, so they could not be assessed beyond their titles.
- The sample is small and dominated by reviews and surveys rather than primary experimental results.
- No paper reports cryptanalytic breaks of the standardised algorithms, and no commercial or adoption outcome data are present.
- Findings about deployment feasibility rest largely on a single benchmarking preprint and should not be generalised.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['PQC performance overhead', 'lattice side-channel attacks', 'PQC key size overhead', 'hybrid cryptography limitations', 'PQC implementation vulnerabilities', 'quantum computer timeline uncertainty']

- **[R1]** *(verified_fact, confidence low)* PQC-enabled TLS handshakes may amplify handshake-exhaustion DDoS attacks. In one testbed, server CPU stayed highly loaded for up to 88 times longer.
  - source: [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) (OpenAlex, 2026-07-14, abstract_only)
  - excerpt: "PQC-TLS can prolong periods of sustained high CPU utilization on the server by up to 88 times"
  - reasoning: This is an arXiv preprint and not peer reviewed. The testbed is small (one server, ten attacking nodes). The abstract does not say which PQC parameters or hardware were used, so generalisation is uncertain.
- **[R2]** *(verified_fact, confidence low)* Deep-learning intrusion detection systems degrade sharply on PQC traffic. One system reached near-random AU-ROC, which suggests a security blind spot during migration.
  - source: [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) (OpenAlex, 2026-07-14, abstract_only)
  - excerpt: "HyperVision's AU-ROC degrades to near-random levels (0.49)"
  - reasoning: The result comes from a single preprint with a specific dataset and specific IDS models. It is not independently replicated. The abstract does not say whether retraining on PQC traffic would fix the problem.
- **[R3]** *(verified_fact, confidence medium)* PQC raises bandwidth and handshake size. Signature payloads are the main cost, and hybrid (classical plus PQC) deployments add more. This is a structural cost for constrained networks and devices.
  - source: [Secure Computation After Quantum: PQC, Confidential Clouds, and Policy-Grade Auditability](https://doi.org/10.62311/nesx/rp-dp925) (OpenAlex, 2025-12-24, abstract_only)
  - source: [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) (OpenAlex, 2026-07-15, abstract_only)
  - source: [PQC Protection for AI Workloads - A Performance-Aware Migration Framework](https://doi.org/10.21203/rs.3.rs-10945203/v1) (OpenAlex, 2026-09-09, abstract_only)
  - excerpt: "digital signature payloads frequently dominating bandwidth budgets relative to key encapsulation"
  - reasoning: The evidence is mainly a review or analysis built on published parameter sizes, not new measurements. src_9987e02f40 also flags latency, memory and signature-size constraints on heterogeneous AI platforms, but its abstract is truncated. The sources support the direction of the overhead, not its magnitude in production.
- **[R4]** *(ai_interpretation, confidence low)* The papers disagree on overhead. Some report minimal or manageable cost, while others report severe amplification under attack or large size expansion. The measured penalty seems to depend heavily on workload, threat model and hardware, and no common benchmark reconciles the results.
  - source: [NoisePQC++: A Unified NIST-Compliant PQC and Hybrid-PQC Implementation of the Noise Protocol](https://doi.org/10.48550/arxiv.2608.00954) (OpenAlex, 2026-08-02, abstract_only)
  - source: [Integrating PQC into standard industry protocols](https://hdl.handle.net/11012/257260) (OpenAlex, 2026-01-01, abstract_only)
  - source: [Exploration of PQC-Based Digital Signature Schemes in TLS Certificates](https://doi.org/10.62019/abbdm.v4i3.189) (OpenAlex, 2024-08-01, abstract_only)
  - source: [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) (OpenAlex, 2026-07-14, abstract_only)
  - source: [Secure Computation After Quantum: PQC, Confidential Clouds, and Policy-Grade Auditability](https://doi.org/10.62311/nesx/rp-dp925) (OpenAlex, 2025-12-24, abstract_only)
  - reasoning: src_93fbebde13 reports minimal overhead under normal conditions, and src_971eca27d6 (a thesis) found no major increase in server compute. src_360d24bdaa calls trade-offs manageable. src_ae754525d8 reports 88x CPU persistence under attack, and src_36248af4c5 reports substantial size expansion. Several of these are preprints or low-citation works with small, setup-specific tests. The apparent conflict may reflect different scenarios rather than true contradiction.
- **[R5]** *(ai_interpretation, confidence low)* Side-channel attacks and hardware-level implementation constraints are open deployment risks for the NIST PQC algorithms. Masking countermeasures for lattice (LWE) schemes are an active research area, which suggests protection has a cost.
  - source: [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) (OpenAlex, 2026-07-15, abstract_only)
  - source: [A Novel Masking Scheme with Low Additional Overhead for LWE-Based PQC Family](https://doi.org/10.1007/978-3-032-22931-1_6) (OpenAlex, 2026-01-01, metadata_only)
  - reasoning: src_10a7c54025 names side-channel vulnerabilities as a real-world challenge. src_85fc0e903a has only a title and no abstract, so the claim that masking carries overhead is inferred from the title alone. The papers give no data on how severe the exposure is.
- **[R6]** *(verified_fact, confidence low)* Migration may be limited more by operations than by algorithms. Organisations lack visibility into TLS configurations across heterogeneous estates, which makes inventory and repeatable enablement hard.
  - source: [Operationalising Post Quantum TLS Automated Configuration Profiling and Hybrid PQC Deployment in Financial Infrastructure](https://doi.org/10.48550/arxiv.2605.17955) (OpenAlex, 2026-05-18, abstract_only)
  - excerpt: "security teams lack precise visibility into TLS configurations and repeatable methods for enabling PQC compatible settings across a heterogeneous estate."
  - reasoning: This is an arXiv preprint. The sample is Nginx configs from public repositories, which may not represent enterprise estates, plus one financial-institution proof of concept. The 'operational bottleneck' is the authors' own argument.
- **[R7]** *(verified_fact, confidence low)* The security of PQC is conjectured, not rigorously proven, and implementations are computationally expensive. The authors present QKD as a possible complement, but it has its own limit of transmission loss over distance. Both routes carry unresolved limits.
  - source: [Practical hybrid PQC-QKD protocols with enhanced security and performance](https://doi.org/10.48550/arxiv.2411.01086) (OpenAlex, 2024-11-02, abstract_only)
  - excerpt: "but it is yet to be rigorously proven, and its current implementations are computationally expensive"
  - reasoning: This is a preprint that frames the problem to motivate its own hybrid protocols, so the framing may be favourable to that approach. The abstract gives no quantitative evidence on cost or on cryptanalysis progress.
- **[R8]** *(verified_fact, confidence low)* Coverage of PQC is uneven. Password-authenticated key exchange (PAKE) has received little attention in migration efforts, so some protocol classes may lack mature quantum-safe options.
  - source: [SoK: PQC PAKEs Design, Security and Performance](https://doi.org/10.62056/a6n5txl7s) (OpenAlex, 2026-08-03, abstract_only)
  - excerpt: "they did not receive much attention from the ongoing Post-Quantum Cryptography (PQC) integration efforts."
  - reasoning: This is a single survey (SoK) abstract. It identifies an awareness gap and unexplored designs. It does not show that the gap causes security failures.
- **[R9]** *(ai_interpretation, confidence low)* Adaptive, learned selection of PQC parameters, such as the DRL approach for Kyber in ITS, may add complexity and attack surface. The abstract shows no adversarial or security-downgrade analysis.
  - source: [PDRL-PQCS: Proactive Deep Reinforcement Learning for Real-Time PQC Configuration in ITS with Edge Collaboration](https://doi.org/10.26599/tst.2026.90100035) (OpenAlex, 2026-03-01, abstract_only)
  - reasoning: The abstract is truncated and the evaluation results are not visible. The absence of a security-downgrade analysis in the visible text is a gap, not proof of a flaw. The security bounds the authors mention are not described.

**Possible hype:**
- 'Harvest now, decrypt later' described as already occurring (src_9987e02f40): the abstract gives no evidence for this, and nothing in the papers dates when a quantum computer capable of breaking RSA or ECC will exist.
- 'Future-proof' or 'robust' security claims (src_360d24bdaa): PQC hardness is conjectured (src_6a33060056), and side-channel exposure remains (src_10a7c54025).
- 'Minimal overhead' and 'practical' handshakes (src_93fbebde13): measured under normal network conditions, while src_ae754525d8 shows large degradation under attack.
- 'Manageable trade-offs' for hybrid certificate chains (src_360d24bdaa): this sits against reported size expansion and added hybrid overhead (src_36248af4c5).
- Framing PQC migration as mainly an algorithm swap: src_8b5ec17baf and src_36248af4c5 point to operational and systems-level barriers.

**Challenges to the Science findings:**
- Targets ['S2'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S2 generalises beyond what was tested. The 'constrained IoT-class' hardware is Raspberry Pi 1, Zero and 4 plus a laptop, running OpenSSL 3.5. It does not include microcontroller-class devices. The 'comparable to elliptic-curve cryptography' result comes from a single preprint and covers only energy and speed, so it should not be read as general parity with classical ECC on constrained devices.
    - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
    - excerpt: "measuring both computational performance and energy consumption on a range of constrained IoT-class devices, from the 32-bit Raspberry Pi 1 and Zero to the 64-bit Raspberry Pi 4, as well as commodity laptop hardware."
    - reasoning: The abstract documents a narrow hardware set (Linux-capable single-board computers and a laptop). Only the abstract was reviewed, so any further caveats in the paper are not visible. The finding should state this scope and that it rests on a single preprint.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S2', 'S12'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S2 and S12 frame PQC cost as an energy and speed trade-off on resource-limited devices. This leaves out server-side and network costs that other retrieved papers measure. PQC-enabled TLS may amplify handshake-exhaustion DDoS, and signature payloads and hybrid modes expand bandwidth. A 'comparable to ECC' headline can therefore mislead about deployment cost.
    - source: [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) (OpenAlex, 2026-07-14, abstract_only)
    - source: [Secure Computation After Quantum: PQC, Confidential Clouds, and Policy-Grade Auditability](https://doi.org/10.62311/nesx/rp-dp925) (OpenAlex, 2025-12-24, abstract_only)
    - excerpt: "PQC-TLS can prolong periods of sustained high CPU utilization on the server by up to 88 times, significantly amplifying the effectiveness of such attacks."
    - reasoning: The 88x figure comes from one preprint testbed. It still contradicts a benign reading of S2 under attack conditions. src_36248af4c5 separately reports that signature payloads dominate bandwidth and hybrid profiles increase overhead. Both are costs that S2's energy and speed metrics do not capture.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S1'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S1 is labelled verified_fact, but the statement that US, UK and EU governments are 'mandating' migration is an introductory assertion in one preprint's abstract. No policy document was retrieved to verify it. The abstract also carries an anomalous future publication date (2026-10-19). S1 should be downgraded or sourced to the actual mandates.
    - source: [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) (arXiv, 2026-10-19, abstract_only)
    - excerpt: "with governments across the US, UK and EU mandating migration to quantum-resistant standards."
    - reasoning: The abstract establishes only that the authors assert this. It does not establish the scope or force of the mandates, or that they are what drives migration. Verification would need primary policy sources, which are absent from the evidence.
- Targets ['S4'], severity low:
  - **[C4]** *(ai_interpretation, confidence medium)* S4 gives an incomplete and dated picture of the standardised families. The cited abstract describes a July 2022 announcement of four candidates, three lattice and one hash-based. It is not a statement about the final FIPS 203/204/205 set. Another retrieved paper lists HQC (a code-based scheme) and FN-DSA as further key algorithms. 'Hash-based the other main selected family' omits code-based selection.
    - source: [The Mathematical Foundation of Post-Quantum Cryptography](https://arxiv.org/abs/2404.19186v1) (arXiv, 2024-04-30, abstract_only)
    - source: [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) (OpenAlex, 2026-07-15, abstract_only)
    - excerpt: "On July 5, 2022, the National Institute of Standards and Technology announced four possible post-quantum cryptography standards, three of them are based on lattice theory and the other one is based on Hash function."
    - reasoning: The cited source is a 2022 snapshot of candidates. src_10a7c54025 names 'key finalists (FN-DSA and HQC)', so code-based schemes are part of the standards landscape. The abstract does not say HQC's formal status, so this caveat is moderate.
- Targets ['S11'], severity medium:
  - **[C5]** *(ai_interpretation, confidence medium)* S11's 'bifurcation' of the field is likely an artefact of the small retrieved sample. It ignores a third strand visible in the risk search: deployment-security and operational studies. These cover handshake-exhaustion DDoS, IDS blind spots, TLS inventory and configuration problems, side channels and protocol-coverage gaps (PAKE). The claim that the field splits into benchmarking and immature hybrids is not supported by a systematic sample.
    - source: [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) (OpenAlex, 2026-07-14, abstract_only)
    - source: [Operationalising Post Quantum TLS Automated Configuration Profiling and Hybrid PQC Deployment in Financial Infrastructure](https://doi.org/10.48550/arxiv.2605.17955) (OpenAlex, 2026-05-18, abstract_only)
    - source: [SoK: PQC PAKEs Design, Security and Performance](https://doi.org/10.62056/a6n5txl7s) (OpenAlex, 2026-08-03, abstract_only)
    - source: [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) (OpenAlex, 2026-07-15, abstract_only)
    - excerpt: "We argue that the bottleneck is operational rather than algorithmic"
    - reasoning: The excerpt is from src_8b5ec17baf. A handful of search hits cannot show the structure of a field. Papers on operations, attack surface and coverage gaps do not fit either of S11's two buckets. This weakens the generalisation 'across this sample'.
- Targets ['S7', 'S12'], severity medium:
  - **[C6]** *(ai_interpretation, confidence medium)* S7 and the surrounding findings treat PQC's security as settled, with only deployment feasibility as the open issue. Retrieved work states that PQC security is conjectured rather than proven. Implementation-level risks such as side channels and masking costs are also active concerns. The findings never state the residual cryptanalytic and implementation risk of the standardised algorithms.
    - source: [Practical hybrid PQC-QKD protocols with enhanced security and performance](https://doi.org/10.48550/arxiv.2411.01086) (OpenAlex, 2024-11-02, abstract_only)
    - source: [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) (OpenAlex, 2026-07-15, abstract_only)
    - excerpt: "but it is yet to be rigorously proven, and its current implementations are computationally expensive."
    - reasoning: This is a general gap rather than a refutation. The statement comes from a preprint arguing for hybrid PQC-QKD, so it is partisan. src_10a7c54025 separately flags side-channel vulnerabilities and hardware-level constraints. Both bear on how S7's 'more viable path' conclusion should be read.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S7'], severity low:
  - **[C7]** *(ai_interpretation, confidence medium)* S7 rests on a single non-peer-reviewed arXiv survey's conclusion and is stated without qualification. Other retrieved work argues QKD and PQC are complementary and combines them (S8), so the QKD-versus-PQC verdict is contested rather than established.
    - source: [A Survey on Post-Quantum Cryptography: State-of-the-Art and Challenges](https://arxiv.org/abs/2312.10430v1) (arXiv, 2023-12-16, abstract_only)
    - source: [Practical hybrid PQC-QKD protocols with enhanced security and performance](https://doi.org/10.48550/arxiv.2411.01086) (OpenAlex, 2024-11-02, abstract_only)
    - excerpt: "we conclude that due to quantum cryptography's present limitations it is not a viable solution like it is often presented to be"
    - reasoning: The finding correctly says 'at least one paper argues', but it omits that the position conflicts with hybrid-approach papers. Both sides are only abstract-level evidence.

**Limitations:**
- Only titles and abstracts were available. Several abstracts are truncated, and src_85fc0e903a has no abstract, so the numbers and conclusions behind many claims could not be checked.
- Only 12 papers were retrieved, and many are low-citation, newly published or preprints (arXiv, Research Square) that are not peer reviewed.
- There is no evidence in the set on quantum hardware timelines, cryptanalysis of the NIST standards, supply-chain or single-vendor dependence, or cost data. Absence of such evidence here is a coverage gap, not evidence of safety or risk.
- Experiments are mostly small testbeds or proofs of concept, such as one financial institution, one STM32 client and one ten-node attack setup. Results may not generalise.
- src_971eca27d6 is a Czech-language thesis, read from its abstract only, and its measurement details are not visible.
- Search results skew toward TLS and protocol integration, so hardware, embedded and side-channel risks are underrepresented.
- Only titles, metadata and abstracts were reviewed. Caveats or methods in the full papers may soften or strengthen the challenges.
- Several evidence items are single preprints or have zero citations. These include the 88x DDoS result and the IDS degradation result, so they are suggestive rather than established.
- The evidence set is a small retrieved sample, so claims about the field's overall structure or about standards status cannot be fully checked.
- No primary policy or NIST documents were retrieved, so the mandate and standardisation-status points are flagged as unverified rather than refuted.
- S5, S6, S8, S9 and S10 were left unchallenged because they are narrow and consistent with the abstracts cited.

## Evidence: company filings and news
Status: partial. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: post-quantum cryptography, PQC, quantum-resistant, cryptographic agility, quantum threat
News headline search: "post-quantum cryptography" (GDELT)

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| CrowdStrike Holdings (CRWD) | 2 | 0 | n/a | n/a | n/a | 1 press release(s) read |
| Palo Alto Networks (PANW) | 2 | 0 | large: 11.5B USD | +24.5% | 22.2% of revenue | 1 press release(s) read |
| Zscaler (ZS) | 2 | 0 | mid: 3.4B USD | +25.4% | 26.9% of revenue |  |
| Cloudflare (NET) | 2 | 0 | mid: 2.2B USD | +29.8% | 23.6% of revenue | 2 press release(s) read |
| Fortinet (FTNT) | 2 | 2 | mid: 6.8B USD | +14.2% | 12.0% of revenue | 2 press release(s) read |
| Okta (OKTA) | 2 | 0 | mid: 2.9B USD | +11.8% | 21.9% of revenue | 2 press release(s) read |
| Cavitation Technologies, Inc. (CVAT) | 1 | 1 | micro: 0.0B USD | -98.5% | 366.7% of revenue | discovered by full-text search |
| Cisco Systems, Inc. (CSCO) | 1 | 1 | large: 63.3B USD | +11.8% | 15.1% of revenue | discovered by full-text search |
| Q/C Technologies, Inc. (QCLS) | 1 | 1 | micro: 0.0B USD | -50.4% | n/a | discovered by full-text search |
| Reliance Global Group, Inc. (EZRA) | 1 | 1 | micro: 0.0B USD | -11.6% | n/a | discovered by full-text search |
| Banco Santander (Brasil) S.A. (BSBR) | 1 | 1 | n/a | n/a | n/a | discovered by full-text search |
| Chunghwa Telecom Co Ltd (CHT) | 1 | 1 | None: 230.0B TWD | +3.0% | 1.8% of revenue | discovered by full-text search |
| F5, Inc. (FFIV) | 1 | 1 | mid: 3.1B USD | +9.7% | 17.5% of revenue | discovered by full-text search |
| Grupo Cibest S.A. (CIB) | 1 | 1 | n/a | n/a | n/a | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Fortinet describes quantum-safe tools and emerging quantum-resistant cryptographic capabilities as part of its FortiOS platform in both its 10-K and 10-Q filings.
  - source: [Fortinet, Inc. Form 10-Q (FORM 10-Q), filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000027/ftnt-20260930.htm) (SEC EDGAR, 2026-10-30, excerpt_only)
  - source: [Fortinet, Inc. Form 10-K (FORM 10-K), filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm) (SEC EDGAR, 2026-02-25, excerpt_only)
  - excerpt: "FortiOS includes advanced encryption, quantum safe tools, and other security technologies designed to address evolving cybersecurity threats, including emerging quantum-resistant cryptographic capabilities."
  - reasoning: Two separate Fortinet filings (10-K and 10-Q) contain near-identical language embedding quantum-resistant capabilities in the FortiOS product description, indicating a shipping product feature rather than a one-off mention.
- **[M2]** *(verified_fact, confidence high)* Cisco states that its AI-ready switches are equipped with quantum-resistant security and post-quantum cryptography to protect against future threats.
  - source: [Cisco Systems, Inc. Form 10-K, filed 2026-09-02](https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm) (SEC EDGAR, 2026-09-02, excerpt_only)
  - excerpt: "These switches are AI-ready with advanced telemetry and assurance capabilities, equipped with quantum-resistant security and post-quantum cryptography to protect against future threats."
  - reasoning: Direct filing excerpt tying PQC to a specific Cisco product line (switches).
- **[M3]** *(verified_fact, confidence high)* Cisco flags failure to timely implement or drive customer adoption of post-quantum cryptography as a risk that could expose pre-quantum encrypted data and systems to compromise once viable quantum computing emerges.
  - source: [Cisco Systems, Inc. Form 10-K, filed 2026-09-02](https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm) (SEC EDGAR, 2026-09-02, excerpt_only)
  - excerpt: "any failure by us to timely implement, or by our customers to timely adopt, post-quantum cryptography in our solutions or IT systems as it becomes available could render existing cryptographic protections ineffective upon the emergence of viable quantum computing"
  - reasoning: Explicit risk-factor language in Cisco's 10-K; the excerpt is quoted verbatim.
- **[M4]** *(verified_fact, confidence medium)* F5 markets post-quantum cryptography readiness as part of its application delivery and security solutions portfolio.
  - source: [F5, Inc. Form 10-K, filed 2025-11-25](https://www.sec.gov/Archives/edgar/data/1048695/000104869525000157/ffiv-20250930.htm) (SEC EDGAR, 2025-11-25, excerpt_only)
  - excerpt: "We sell application delivery and security solutions for web application and API protection, hybrid multicloud networking, enterprise AI delivery and security, application migration, application modernization, zero trust architecture and post quantum cryptography readiness."
  - reasoning: F5's 10-K lists PQC readiness among its sold solution categories, suggesting commercial positioning rather than pure risk disclosure.
- **[M5]** *(verified_fact, confidence medium)* Chunghwa Telecom lists Post-Quantum Cryptography (PQC) certificates among its cybersecurity technology areas, alongside FIDO, zero trust and V2X security.
  - source: [Chunghwa Telecom Co Ltd Form 20-F, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1132924/000119312526155848/cht-20251231.htm) (SEC EDGAR, 2026-04-15, excerpt_only)
  - excerpt: "Cybersecurity: Post-Quantum Cryptography (PQC) certificates, AI fraud prevention, Fast Identity Online (FIDO), mobile authentication, blockchain and smart contracts, zero trust security"
  - reasoning: Filing excerpt names PQC certificates as a technology area, indicating a telecom operator's involvement in PQC deployment.
- **[M6]** *(verified_fact, confidence low)* Reliance Global Group states its business is focused on post-quantum cryptography and related data protection technologies.
  - source: [Reliance Global Group, Inc. Form 10-Q, filed 2026-07-30](https://www.sec.gov/Archives/edgar/data/1812727/000149315226035504/form10-q.htm) (SEC EDGAR, 2026-07-30, excerpt_only)
  - excerpt: "business is focused on post-quantum cryptography and related data protection technologies."
  - reasoning: The excerpt is truncated mid-sentence ('The market for post-quantum cryptography is'), so the exact scope of the business focus and any market claims cannot be confirmed; the company is micro-cap with declining revenue per XBRL data.
- **[M7]** *(verified_fact, confidence medium)* Banco Santander (Brasil) describes the transition to post-quantum cryptography as complex due to legacy systems and interdependencies, indicating PQC migration is a recognized operational challenge for large financial institutions.
  - source: [Banco Santander (Brasil) S.A. Form 20-F, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1471055/000129281426000592/bsbrform20f_2025.htm) (SEC EDGAR, 2026-02-27, excerpt_only)
  - excerpt: "The transition to post-quantum cryptography is complex due to legacy systems, interdependent"
  - reasoning: Filing excerpt shows a major bank discussing PQC transition complexity; excerpt is truncated so full context is unknown.
- **[M8]** *(unverified_claim, confidence low)* Cavitation Technologies' filing claims use of post-quantum cryptography and decentralized infrastructure to protect transactions, an unusual pairing for a company with negligible revenue.
  - source: [Cavitation Technologies, Inc. Form 10-Q, filed 2026-10-27](https://www.sec.gov/Archives/edgar/data/1376793/000168316826008112/cavitation_i10q-093026.htm) (SEC EDGAR, 2026-10-27, excerpt_only)
  - reasoning: The claim is the company's own assertion in a 10-Q; XBRL data shows micro-scale revenue (~USD 3,000) and losses, so the claim's substance cannot be assessed from the excerpt alone.
- **[M9]** *(ai_interpretation, confidence low)* Among the configured cybersecurity companies (CrowdStrike, Palo Alto Networks, Zscaler, Cloudflare, Okta), none of the retrieved filing excerpts mention PQC keywords; only Fortinet among the configured list does.
  - source: [Fortinet, Inc. Form 10-Q (FORM 10-Q), filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000027/ftnt-20260930.htm) (SEC EDGAR, 2026-10-30, excerpt_only)
  - source: [Fortinet, Inc. Form 10-K (FORM 10-K), filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm) (SEC EDGAR, 2026-02-25, excerpt_only)
  - reasoning: Per the retrieval summary, CRWD, PANW, ZS, NET and OKTA filings had zero keyword mentions. Because only excerpts were read, this indicates absence of PQC language in the retrieved passages, not absence from the market.
  - citation check: company name(s) not found in the cited sources removed: CrowdStrike Holdings, Palo Alto Networks, Zscaler, Cloudflare, Okta
- **[M10]** *(ai_interpretation, confidence medium)* PQC appears in filings across diverse sectors (networking, telecom, banking, insurance, application delivery), suggesting the topic has moved beyond pure security vendors into general enterprise risk and product discussions.
  - source: [Cisco Systems, Inc. Form 10-K, filed 2026-09-02](https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm) (SEC EDGAR, 2026-09-02, excerpt_only)
  - source: [Chunghwa Telecom Co Ltd Form 20-F, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1132924/000119312526155848/cht-20251231.htm) (SEC EDGAR, 2026-04-15, excerpt_only)
  - source: [Banco Santander (Brasil) S.A. Form 20-F, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1471055/000129281426000592/bsbrform20f_2025.htm) (SEC EDGAR, 2026-02-27, excerpt_only)
  - source: [F5, Inc. Form 10-K, filed 2025-11-25](https://www.sec.gov/Archives/edgar/data/1048695/000104869525000157/ffiv-20250930.htm) (SEC EDGAR, 2025-11-25, excerpt_only)
  - source: [Reliance Global Group, Inc. Form 10-Q, filed 2026-07-30](https://www.sec.gov/Archives/edgar/data/1812727/000149315226035504/form10-q.htm) (SEC EDGAR, 2026-07-30, excerpt_only)
  - source: [Grupo Cibest S.A. Form 20-F, filed 2026-04-08](https://www.sec.gov/Archives/edgar/data/2058897/000205889726000125/cib-20251231.htm) (SEC EDGAR, 2026-04-08, excerpt_only)
  - reasoning: Pattern across multiple independent filings from different industries: PQC is cited both as a product capability (Cisco, F5, Chunghwa) and as a risk/transition topic (Santander Brasil, Grupo Cibest, Reliance). Each source is only an excerpt, so depth of engagement is unknown.

**Limitations:**
- Only excerpt passages from filings were available; full filings were not read, so absence of PQC keywords in CRWD, PANW, ZS, NET and OKTA excerpts does not mean those companies are absent from the PQC market.
- No news headlines were retrieved for this topic, so no media-reported developments (e.g., NIST standard adoption, product launches) could be assessed.
- Several excerpts are truncated mid-sentence (Reliance Global Group, Banco Santander Brasil, Q/C Technologies), limiting what can be concluded from them.
- No evidence on customers, revenue attributable to PQC products, pricing, or competitive positioning was found in any source.
- Discovered companies (CVAT, QCLS, EZRA, CIB) are micro-cap or data-limited; their PQC mentions may be incidental or aspirational and cannot be verified further from the provided excerpts.
- The analysis covers only 13 companies; major PQC players outside the retrieved set (e.g., dedicated cryptography vendors, chipmakers) are not covered.

## Social signals from X
Status: no_data. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 30 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (37): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie
Posts read: 0 (estimated X cost $0.000)


**Limitations:**
- No post from the approved accounts mentioned the keywords in the last 7 days.

## Evidence: patents
Status: partial. Worldwide patent publications from Google Patents (SerpApi) matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 9 distinct company names from 0 patent publications, 0 company-affiliated papers and 9 SEC filers; 9 matched to the SEC ticker file (8 outside the configured list), 0 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| F5, Inc. (FFIV) · Computer Communications Equipment | 0 | 0 | 1 | mid: 3.09B USD | +9.7% | 17.5% | **40** |
| Cisco Systems, Inc. (CSCO) · Computer Communications Equipment | 0 | 0 | 3 | large: 63.33B USD | +11.8% | 15.1% | **35** |
| Q/C Technologies, Inc. (QCLS) · In Vitro & In Vivo Diagnostic Substances | 0 | 0 | 2 | micro: 0.00B USD | -50.4% | n/a | **35** |
| Chunghwa Telecom Co Ltd (CHT) · Radiotelephone Communications | 0 | 0 | 1 | n/a: 229.97B TWD | +3.0% | 1.8% | **25** |
| Cavitation Technologies, Inc. (CVAT) · Agricultural Services · OUTSIDE TECHNOLOGY: mentions likely boilerplate | 0 | 0 | 4 | micro: 0.00B USD | -98.5% | 366.7% | **20** |
| Reliance Global Group, Inc. (EZRA) · Insurance Agents, Brokers & Service · OUTSIDE TECHNOLOGY: mentions likely boilerplate | 0 | 0 | 2 | micro: 0.01B USD | -11.6% | n/a | **10** |
| Banco Santander (Brasil) S.A. (BSBR) · Commercial Banks, NEC · OUTSIDE TECHNOLOGY: mentions likely boilerplate | 0 | 0 | 1 | n/a | n/a | n/a | **0** |
| Grupo Cibest S.A. (CIB) · Commercial Banks, NEC · OUTSIDE TECHNOLOGY: mentions likely boilerplate | 0 | 0 | 1 | n/a | n/a | n/a | **0** |

- F5, Inc.: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +10% (+5); R&D 18% of revenue (+10)
- Cisco Systems, Inc.: 3 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth +12% (+5); R&D 15% of revenue (+10)
- Q/C Technologies, Inc.: 2 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth -50% (+0)
- Chunghwa Telecom Co Ltd: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); size unknown from SEC XBRL (+5, neutral); revenue growth +3% (+5)
- Cavitation Technologies, Inc.: 4 SEC report(s) mentioning the topic (+20); filer outside technology (Agricultural Services): topic mentions are usually risk-factor boilerplate (-25); micro company by revenue (+15): more room to grow, more risk; revenue growth -98% (+0); R&D 367% of revenue (+10)
- Reliance Global Group, Inc.: 2 SEC report(s) mentioning the topic (+20); filer outside technology (Insurance Agents, Brokers & Service): topic mentions are usually risk-factor boilerplate (-25); micro company by revenue (+15): more room to grow, more risk; revenue growth -12% (+0)

**Configured incumbents that also showed up:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Fortinet (FTNT) | 0 | 0 | 2 | mid: 6.80B USD | +14.2% | 12.0% | **40** |

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* F5, Inc. (FFIV) is active on post-quantum cryptography: 1 of its SEC report(s) mention the topic; fiscal 2025 revenue 3.09B USD (mid by revenue), growth +9.7%, R&D 17.5% of revenue. Next-runner score 40/100 (heuristic).
  - source: [F5, Inc. Form 10-K, filed 2025-11-25](https://www.sec.gov/Archives/edgar/data/1048695/000104869525000157/ffiv-20250930.htm) (SEC EDGAR, 2025-11-25, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Cisco Systems, Inc. (CSCO) is active on post-quantum cryptography: 3 of its SEC report(s) mention the topic; fiscal 2026 revenue 63.33B USD (large by revenue), growth +11.8%, R&D 15.1% of revenue. Next-runner score 35/100 (heuristic).
  - source: [Cisco Systems, Inc. Form 10-K, filed 2026-09-02](https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm) (SEC EDGAR, 2026-09-02, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Q/C Technologies, Inc. (QCLS) is active on post-quantum cryptography: 2 of its SEC report(s) mention the topic; fiscal 2018 revenue 0.00B USD (micro by revenue), growth -50.4%. Next-runner score 35/100 (heuristic).
  - source: [Q/C Technologies, Inc. Form 10-K, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1321834/000149315226016872/form10-k.htm) (SEC EDGAR, 2026-04-15, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Chunghwa Telecom Co Ltd (CHT) is active on post-quantum cryptography: 1 of its SEC report(s) mention the topic; fiscal 2024 revenue 229.97B TWD, growth +3.0%, R&D 1.8% of revenue. Next-runner score 25/100 (heuristic).
  - source: [Chunghwa Telecom Co Ltd Form 20-F, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1132924/000119312526155848/cht-20251231.htm) (SEC EDGAR, 2026-04-15, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- No retrieved paper carried a company-type author affiliation (most are universities).
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [Fortinet, Inc. Form 10-Q (FORM 10-Q), filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000027/ftnt-20260930.htm) | SEC EDGAR | 2026-10-30 | retrieved 2026-11-09 | excerpt_only | id src_9653491d1d
- [Cavitation Technologies, Inc. Form 10-Q, filed 2026-10-27](https://www.sec.gov/Archives/edgar/data/1376793/000168316826008112/cavitation_i10q-093026.htm) | SEC EDGAR | 2026-10-27 | retrieved 2026-11-09 | excerpt_only | id src_7336271320
- [Energy Consumption of Post-Quantum Cryptography on Constrained and General-Purpose Architectures](https://arxiv.org/abs/2610.27111v2) | arXiv | 2026-10-19 | retrieved 2026-11-09 | abstract_only | id src_9d1161e3bc
- [PQC Protection for AI Workloads - A Performance-Aware Migration Framework](https://doi.org/10.21203/rs.3.rs-10945203/v1) | OpenAlex | 2026-09-09 | retrieved 2026-11-09 | abstract_only | id src_9987e02f40
- [Cisco Systems, Inc. Form 10-K, filed 2026-09-02](https://www.sec.gov/Archives/edgar/data/858877/000085887726000132/csco-20260725.htm) | SEC EDGAR | 2026-09-02 | retrieved 2026-11-09 | excerpt_only | id src_e9a79fe1dd
- [SoK: PQC PAKEs Design, Security and Performance](https://doi.org/10.62056/a6n5txl7s) | OpenAlex | 2026-08-03 | retrieved 2026-11-09 | abstract_only | id src_45a730fcff
- [NoisePQC++: A Unified NIST-Compliant PQC and Hybrid-PQC Implementation of the Noise Protocol](https://doi.org/10.48550/arxiv.2608.00954) | OpenAlex | 2026-08-02 | retrieved 2026-11-09 | abstract_only | id src_93fbebde13
- [Reliance Global Group, Inc. Form 10-Q, filed 2026-07-30](https://www.sec.gov/Archives/edgar/data/1812727/000149315226035504/form10-q.htm) | SEC EDGAR | 2026-07-30 | retrieved 2026-11-09 | excerpt_only | id src_dd2d2cbffb
- [Navigating the NIST PQC Standards: Trade-offs and Case Studies](https://doi.org/10.60097/acig/221494) | OpenAlex | 2026-07-15 | retrieved 2026-11-09 | abstract_only | id src_10a7c54025
- [On the Security Implications of PQC in TLS: Handshake Exhaustion and IDS Degradation](https://doi.org/10.48550/arxiv.2607.12504) | OpenAlex | 2026-07-14 | retrieved 2026-11-09 | abstract_only | id src_ae754525d8
- [Operationalising Post Quantum TLS Automated Configuration Profiling and Hybrid PQC Deployment in Financial Infrastructure](https://doi.org/10.48550/arxiv.2605.17955) | OpenAlex | 2026-05-18 | retrieved 2026-11-09 | abstract_only | id src_8b5ec17baf
- [Q/C Technologies, Inc. Form 10-K, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1321834/000149315226016872/form10-k.htm) | SEC EDGAR | 2026-04-15 | retrieved 2026-11-09 | excerpt_only | id src_4723f8b46b
- [Chunghwa Telecom Co Ltd Form 20-F, filed 2026-04-15](https://www.sec.gov/Archives/edgar/data/1132924/000119312526155848/cht-20251231.htm) | SEC EDGAR | 2026-04-15 | retrieved 2026-11-09 | excerpt_only | id src_26a3d9a125
- [Grupo Cibest S.A. Form 20-F, filed 2026-04-08](https://www.sec.gov/Archives/edgar/data/2058897/000205889726000125/cib-20251231.htm) | SEC EDGAR | 2026-04-08 | retrieved 2026-11-09 | excerpt_only | id src_a04d3371d5
- [PDRL-PQCS: Proactive Deep Reinforcement Learning for Real-Time PQC Configuration in ITS with Edge Collaboration](https://doi.org/10.26599/tst.2026.90100035) | OpenAlex | 2026-03-01 | retrieved 2026-11-09 | abstract_only | id src_5c4c39a5eb
- [Banco Santander (Brasil) S.A. Form 20-F, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1471055/000129281426000592/bsbrform20f_2025.htm) | SEC EDGAR | 2026-02-27 | retrieved 2026-11-09 | excerpt_only | id src_1e86f4f4a7
- [Fortinet, Inc. Form 10-K (FORM 10-K), filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1262039/000126203926000007/ftnt-20251231.htm) | SEC EDGAR | 2026-02-25 | retrieved 2026-11-09 | excerpt_only | id src_29aa926699
- [A Novel Masking Scheme with Low Additional Overhead for LWE-Based PQC Family](https://doi.org/10.1007/978-3-032-22931-1_6) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | metadata_only | id src_85fc0e903a
- [Integrating PQC into standard industry protocols](https://hdl.handle.net/11012/257260) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | abstract_only | id src_971eca27d6
- [Secure Computation After Quantum: PQC, Confidential Clouds, and Policy-Grade Auditability](https://doi.org/10.62311/nesx/rp-dp925) | OpenAlex | 2025-12-24 | retrieved 2026-11-09 | abstract_only | id src_36248af4c5
- [F5, Inc. Form 10-K, filed 2025-11-25](https://www.sec.gov/Archives/edgar/data/1048695/000104869525000157/ffiv-20250930.htm) | SEC EDGAR | 2025-11-25 | retrieved 2026-11-09 | excerpt_only | id src_4a3bacb051
- [Obfuscated Quantum and Post-Quantum Cryptography](https://arxiv.org/abs/2508.07635v2) | arXiv | 2025-08-11 | retrieved 2026-11-09 | abstract_only | id src_bcc27a5fdd
- [A Comparative Performance Evaluation of Kyber, sntrup761, and FrodoKEM for Post-Quantum Cryptography](https://arxiv.org/abs/2508.10023v1) | arXiv | 2025-08-07 | retrieved 2026-11-09 | abstract_only | id src_7af56bdfd5
- [Post-quantum Cryptography](https://doi.org/10.1007/978-3-030-71522-9_386) | OpenAlex | 2025-01-01 | retrieved 2026-11-09 | metadata_only | id src_cb78f8fd6c
- [Practical hybrid PQC-QKD protocols with enhanced security and performance](https://doi.org/10.48550/arxiv.2411.01086) | OpenAlex | 2024-11-02 | retrieved 2026-11-09 | abstract_only | id src_6a33060056
- [Exploration of PQC-Based Digital Signature Schemes in TLS Certificates](https://doi.org/10.62019/abbdm.v4i3.189) | OpenAlex | 2024-08-01 | retrieved 2026-11-09 | abstract_only | id src_360d24bdaa
- [Applications of Post-Quantum Cryptography](https://doi.org/10.34190/eccws.23.1.2247) | OpenAlex | 2024-06-21 | retrieved 2026-11-09 | abstract_only | id src_4f617d8a3a
- [The Mathematical Foundation of Post-Quantum Cryptography](https://arxiv.org/abs/2404.19186v1) | arXiv | 2024-04-30 | retrieved 2026-11-09 | abstract_only | id src_4aefcdcced
- [Post-quantum cryptography and the quantum future of cybersecurity](https://doi.org/10.1103/physrevapplied.21.040501) | OpenAlex | 2024-04-09 | retrieved 2026-11-09 | abstract_only | id src_2a1b2216b3
- [Post-Quantum Cryptography Neural Network](https://arxiv.org/abs/2402.16002v1) | arXiv | 2024-02-25 | retrieved 2026-11-09 | abstract_only | id src_be6f30f54b
- [Transition to Post-Quantum Cryptography Standards](https://doi.org/10.6028/nist.ir.8547) | OpenAlex | 2024-01-01 | retrieved 2026-11-09 | metadata_only | id src_6a440a8da3
- [A Survey on Post-Quantum Cryptography: State-of-the-Art and Challenges](https://arxiv.org/abs/2312.10430v1) | arXiv | 2023-12-16 | retrieved 2026-11-09 | abstract_only | id src_5625041338
- [A Survey of Post-Quantum Cryptography: Start of a New Race](https://doi.org/10.3390/cryptography7030040) | OpenAlex | 2023-08-14 | retrieved 2026-11-09 | abstract_only | id src_518c5be7fe
- [Post Quantum Cryptography: A Review of Techniques, Challenges and Standardizations](https://doi.org/10.1109/icoin56518.2023.10048976) | OpenAlex | 2023-01-11 | retrieved 2026-11-09 | abstract_only | id src_5fbbdb1b17

## Gaps, limitations and errors
- Missing data: Patent agent did not run: no patent filings, assignees or code-computed patent counts, so patent_momentum cannot be rated and company patent activity cannot be checked.
- Missing data: X agent did not run: no company, standards-body or press social signals for catalysts or launch context.
- Missing data: Price & timing agent did not run: no ~100-day price metrics, so no assessment of how far related names have already moved (rule 5b cannot be applied quantitatively).
- Missing data: No retrieved government policy or mandate document: the assertion that US, UK and EU governments mandate PQC migration remains unverified (C3).
- Missing data: No customer-adoption evidence: no deployments, contract values, seat counts, certificates issued or migration completions are cited by any finding.
- Missing data: No PQC-specific financial disclosure: no filing in the evidence isolates PQC revenue, bookings or R&D spend (K2, K3 give company-wide R&D only).
- Missing data: No independent cryptanalytic assessment of the standardised algorithms, and no finding states residual cryptanalytic risk (C6).
- Missing data: No common benchmark reconciling the conflicting overhead measurements (R4).
- Missing data: No company evidence on which established security vendors beyond Fortinet embed PQC, since the other configured cybersecurity companies' retrieved excerpts do not mention it (M9).
- Missing data: No coverage of hardware/HSM or secure-element vendors, contract manufacturers or silicon supply chain, beyond general constrained-device constraints (S3, C1).
- Limitation: This is a research assessment for a 1-5 year view, not investment advice; it contains no price targets, entry points, timing signals or buy/sell/hold recommendations.
- Limitation: Every statement is bounded by the cited findings; where no finding exists the item was placed in missing_data rather than inferred.
- Limitation: The research-activity metric is an exact-phrase OpenAlex count, excludes synonyms and abbreviations, is not normalised for overall publishing growth, and excludes the partial current year; it measures academic attention only, not commercial success (rule 7).
- Limitation: Several findings rest on single preprints or arXiv surveys with low confidence, and the challenge findings C1-C7 materially weaken S1, S2, S4, S7, S11 and S12; confidence is set accordingly.
- Limitation: Market evidence is drawn from SEC filing excerpts describing capabilities and risks, which is not proof that customers buy, deploy or pay for the technology (rule 6).
- Limitation: The M8 and K1/K4/K5 company mentions come from micro-cap filings with negligible or negative revenue and, for M8, a promotional-sounding claim; Company Scout next-runner scores are transparent heuristics, not predictions of returns, and smaller companies carry more risk and less disclosure.
- Limitation: Headline-based findings, if any existed, would be unverified claims; no X findings were provided at all in this version.
- Limitation: No patent, social or price evidence was available, so the assessment under-represents intellectual-property positioning, near-term catalysts and timing risk.
- Chief review gap: Patent agent was not run, so there is no IP landscape or freedom-to-operate analysis; this limits conclusions about competitive moats and licensing risk but cannot be filled by paper search.
- Chief review gap: X agent was not run, so no community or practitioner sentiment signals are available; this is a limitation on gauging real-world deployment friction beyond what filings and papers show.
- Chief review gap: No science finding addresses PKI/X.509 certificate management migration (e.g., certificate size inflation, chain validation with PQC signatures), which is a major practical deployment bottleneck mentioned indirectly in market findings (M5, M7).
- Chief review gap: Several retrieved science papers are broad surveys (3 of 12), reducing the density of novel technical evidence; the specific benchmark papers (energy, comparative KEM) are the strongest but limited in number.
- Chief review gap: No evidence on PQC deployment in cloud/hyperscaler contexts (AWS, Azure, GCP), which are major migration vectors.
- Reference checks changed 1 statement(s) in the assessment (see notes in italics above).
- ERROR [market/GDELT news]: rate limited by GDELT (limit: about 1 request / 5 s)
- ERROR [patent/Google Patents (SerpApi)]: counts: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [patent/Google Patents (SerpApi)]: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 2 | 5159 | 2208 | 0.00319 |
| science | deepseek/deepseek-v4.1-flash | 1 | 4026 | 3675 | 0.00562 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 23878 | 9747 | 0.14523 |
| market | z-ai/glm-5.3 | 1 | 3947 | 1937 | 0.01824 |
| investment | deepseek/deepseek-v4.1-flash | 1 | 7888 | 8517 | 0.01259 |
| x (data) | X API pay-per-use | 2 | 0 | 0 | 0.00000 |

Total estimated cost: $0.18486 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
