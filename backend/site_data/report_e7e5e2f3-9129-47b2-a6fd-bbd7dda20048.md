# FUTURESCOUT AI research report: quantum error correction

Generated: 2026-11-09 08:12 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, timing, scout, investment
- Agents NOT run in this version: patent, x. Conclusions therefore have no patent, social-media evidence.

## Verdict (forecast, computed from the report)
**Early and mixed: watch, do not assume** — score 35.5, confidence medium.
Qualifiers: high risk flagged by the Risk agent; research is running well ahead of commercial reality.

Quantum computers make mistakes, so error correction uses many imperfect physical qubits to build one reliable 'logical' qubit. In the laboratory this has now passed an important milestone: adding more qubits finally makes the result better instead of worse, though it still takes roughly a hundred physical qubits…

Why:
- Research Momentum rated 5/5: Publication counts for the exact phrase rose from 434 (2024) to 987 (2025) and the current partial year is running at roughly 3.7x the same period last year, i.e.
- Technical Feasibility rated 3/5: Below-threshold operation, GKP logical qudits beyond break-even and per-cycle leakage removal are genuine hardware results (S1, S3, S4), but the same evidence base carries high- and medium-severity challenges: decoder latency far above the cycle time (C1), conflated experiments (C2), and 101 physical qubits per logical qubit with hourly correlated error events (C3).
- Papers 2024→2025: 434→987 (+127%)
- So far in 2026 (to 10-10): 2452 papers vs 671 by the same date in 2025 (+265%, rising)

Watch out for:
- A high-severity challenge states the real-time decoder latency (63 microseconds) far exceeds the 1.1 microsecond code cycle, the opposite of what the science summary implies, so real-time decoding may not yet be compatible with fast QEC.
- The headline below-threshold result is merged from two experiments, and the source reports 101 physical qubits per logical qubit plus rare correlated error events roughly once per hour — the main barrier to scaling.
- Many headline overhead reductions are simulation or extrapolation, with the key logical error rate depending on assumed physical error rates.
- Low-overhead codes need dense long-range connectivity that is hard to build, and workarounds shift cost: removing up to 50% of long-range links roughly doubles syndrome circuit depth.

What would change this view:
- Stronger if: An independent, hardware-based demonstration in which reported decoder latency is verifiably below the code cycle time, directly addressing the reversal identified in the latency claim.
- Weaker if: Below-threshold behaviour failing to reproduce or improve at larger code distance in later hardware runs, which would break the central premise that error correction scales as demonstrated.
- Stronger if: A decoder demonstrated in a live hardware loop at latency below the code cycle time, rather than in GPU software benchmarks.
- Weaker if: Demonstrations showing that qubit-count savings from low-overhead codes are cancelled by added depth, rounds or connectivity requirements in measured space-time cost, which would remove the main appeal of this theme.

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
The evidence shows a genuine scientific milestone: a superconducting surface-code memory operated below the error-correction threshold (S1) and bosonic GKP logical qudits operated beyond break-even (S3), with leakage actively removed each cycle (S4). However, the Risk challenges show the two headline summaries overstate the sources: the reported real-time decoder latency is far longer than the code cycle, not shorter (C1), the real-time decoder and the distance-7 memory are different experiments (C2), and the same source reports 101 physical qubits per logical qubit with correlated error events about once per hour (C3). Most overhead-reduction claims are simulated or extrapolated rather than measured on hardware (R1, R4, R5, R6), and a proven lower bound limits geometrically local 2D architectures (R3). On the commercial side, the pure-play quantum filers all treat fault tolerance as the gating milestone but report no QEC revenue, and Xanadu states it has demonstrated only twelve logical qubits with photon loss not meeting required levels (M6). All five QEC-linked equities are in drawdown with annualised volatility above 100% (T1-T11), so any theme here carries substantial timing and volatility risk alongside the technical uncertainty.

## Technology Opportunity Score
**Score: 35.5 / 100** (confidence: medium; evidence coverage 90%)

Risk adjustment: rating 4/5 lowered the score by 24.0% (base 46.7).

Commercialization Gap (research momentum rating minus commercial readiness rating): +4


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S3, S4, S5, S7, S8, S9 | Publication counts for the exact phrase rose from 434 (2024) to 987 (2025) and the current partial year is running at roughly 3.7x the same period last year, i.e. momentum is still building rather than fading. The findings corroborate breadth across hardware demonstrations (S1, S3, S4), decoder and code design (S5, S7, S8) and theory (S9, S10, S11), with a caveat that several of these are simulations or preprints (C4, C5, C7). Research volume is not commercial success. |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 3 | S1, S3, S4, C1, C2, C3, R3 | Below-threshold operation, GKP logical qudits beyond break-even and per-cycle leakage removal are genuine hardware results (S1, S3, S4), but the same evidence base carries high- and medium-severity challenges: decoder latency far above the cycle time (C1), conflated experiments (C2), and 101 physical qubits per logical qubit with hourly correlated error events (C3). A proven lower bound limits geometrically local 2D layouts (R3). Feasible at prototype scale; not proven at useful scale. |
| Commercial Readiness | 15% | 1 | M1, M2, M5, M6 | No finding shows QEC-driven revenue, product shipments or production deployment. Pure-play filers describe fault tolerance as the goal of rising R&D spending, not as a current product (M2, M5), Quantinuum's logical-qubit milestones are dated 2027 and 2029 (M1), and Xanadu reports only twelve logical qubits demonstrated with photon loss not at required levels (M6). Early research stage with no commercial output. |
| Customer Adoption | 10% | 1 | M7 | The only customer-adjacent evidence is Quantinuum tying logical-qubit metrics to customer outcomes and commercial adoption, and IonQ positioning fault tolerance as the stage where quantum machines outcompete classical ones across many sectors (M7). No finding names a customer, contract or deployment, so adoption is aspirational rather than observed. |
| Industry Investment | 10% | 3 | M2, M3, M5, M7 | Company filings show sustained spending and programme support: Rigetti frames fault tolerance as its largest commercial opportunity behind rising R&D (M2) and won an Innovate UK QEC award (M3); Quantinuum, IonQ and Rigetti all treat QEC as the central gating milestone (M7); IonQ expects continued significant losses while scaling (M5). Investment is real but concentrated in a small number of pure-plays, and the findings give no dollar figures for QEC specifically. |
| Competitive Position | 10% | 2 | S1, S3, S4, S7, M1, M4, M6, M9 | Multiple hardware routes coexist (superconducting S1/S4, bosonic S3, neutral-atom Rydberg S7, photonic M6) with no evidence of a winner. Quantinuum claims a first (M1) and D-Wave claims a path to being first with fewer qubits per logical qubit (M4, unverified), while Xanadu's disclosed photon-loss shortfall is a concrete negative (M6). Positioning is claimed rather than demonstrated, and the incomplete filing coverage (M9) means no conclusions can be drawn about absent players. |
| Supply-Chain Readiness | 15% | 1 | R2, R3 | No finding addresses suppliers, fabrication capacity or component availability. The closest evidence is buildability of the required hardware: low-overhead codes need dense long-range connectivity that is hard to build, especially on superconducting processors, with workarounds roughly doubling syndrome circuit depth (R2), a constraint reinforced by the geometrically local 2D lower bound (R3). This is a design/manufacturing constraint, not supply-chain visibility, so confidence is low. |

Formula: base = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100; score = base x (1 - max_penalty x risk_rating/5). Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. The score is an explainable heuristic, not a validated prediction of stock performance.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.
- Confidence lowered to 'medium': coverage is 90%, but the cited ratings themselves are mostly of lower confidence.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Hardware-validated error correction: below-threshold memories, bosonic logical qubits and leakage control

Technologies: superconducting surface codes, bosonic / Gottesman-Kitaev-Preskill codes, logical qudits (qutrit, ququart), real-time decoding, leakage suppression, neutral-atom multiqubit Rydberg gates

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The near-term evidence is scientific, not commercial: below-threshold operation (S1), GKP qudits beyond break-even (S3) and per-cycle leakage removal (S4) are laboratory results, while the only company-level near-term signals are roadmap statements (M1, M2) and the fact that QEC-linked equities are all below their 50-day averages with 20-day annualised volatility above 100% (T1, T3, T5, T7, T9, T11). Nothing in the findings shows QEC revenue, customers or production output in this window. *(ai_interpretation)* [S1, S3, S4, M1, M2, T11] | medium |
| medium_1_3y | Company filings give specific but unproven dates: Quantinuum expects its Sol system in 2027 to reach up to 100 logical qubits (M1), and IonQ defines logical qubits as its path to fault tolerance while expecting continued significant losses (M5). The findings give no evidence that the laboratory below-threshold result scales to that level, and the same source reports 101 physical qubits per logical qubit with rare correlated error events roughly once per hour (C3); Xanadu reports only twelve logical qubits demonstrated with photon loss not meeting required levels (M6). *(forecast)* [M1, M5, M6, C3] | low |
| long_3_5y | This horizon rests almost entirely on forward-looking company statements: Quantinuum's Apollo (2029) targeting hundreds of logical qubits (M1) and Rigetti's statement that the industry believes early fault tolerance will require 10,000 to 1,000,000 physical qubits (M2). A proven lower bound implies that error correction restricted to geometrically local operations in 2D carries overhead growing with system size (R3), so the findings do not support assuming that planar-layout scaling alone reaches algorithm-scale machines. *(forecast)* [M1, M2, R3] | low |

**Bull case:** The core physics milestone has been crossed on real hardware: a superconducting surface-code memory was operated below threshold with logical error suppressed as code distance increased, and a distance-7 logical memory exceeded its best physical qubit's lifetime (S1); bosonic GKP logical qudits were operated beyond break-even with encoding optimised by reinforcement learning (S3); and leakage out of the computational subspace was actively removed every cycle, roughly a tenfold reduction (S4). If these behaviours persist as systems grow, error correction stops being the reason quantum computing cannot scale and becomes an engineering cost that falls with better hardware. *(ai_interpretation)* [S1, S3, S4]

**Base case:** Below-threshold operation is real but small and expensive in qubits: the headline memory uses 101 physical qubits for one logical qubit at 0.143% error per cycle, and repetition-code performance is capped by rare correlated error events about once per hour (C3). Decoding and latency remain the binding constraint, with the cited abstract reporting decoder latency far above the code cycle time rather than below it (C1), and company roadmaps to 100 or hundreds of logical qubits by 2027-2029 remain unproven plans rather than demonstrated capability (M1, M5). The visible commercial picture is of several companies spending more R&D while reporting no QEC-driven revenue (M2, M5). *(ai_interpretation)* [C1, C3, M1, M2, M5]

**Bear case:** Two of the strongest summaries in the evidence base do not accurately reflect their sources: the decoder latency claim is reversed (C1) and the distance-7 memory and the real-time decoder are conflated into one experiment (C2). The same source reports a large gap to algorithm-scale requirements (C3), and a proven lower bound shows geometrically local 2D layouts face overhead that grows with system size (R3). Meanwhile the pure-play filers themselves flag substantial scientific and engineering uncertainty (M8), Xanadu's photon-loss performance does not meet required levels (M6), and the listed equities are already in a sustained drawdown (T9, T10, T11) — so even a correct technical trajectory offers no protection against further price stress. *(forecast)* [C1, C2, C3, M6, M8, R3, T9, T10, T11]

**Catalysts:**
- An independent, hardware-based demonstration in which reported decoder latency is verifiably below the code cycle time, directly addressing the reversal identified in the latency claim. *(forecast)* [C1, S2]
- Evidence that below-threshold behaviour persists at larger code distance on the same device family with a stated number of physical qubits per logical qubit, rather than being inferred from different experiments. *(forecast)* [S1, C2, C3]
- Company filings or press releases showing logical-qubit counts delivered against the stated roadmap milestones (Quantinuum Sol 2027, Apollo 2029) or evidence of paying customers for error-corrected machines. *(forecast)* [M1, M7]

**Risks:**
- A high-severity challenge states the real-time decoder latency (63 microseconds) far exceeds the 1.1 microsecond code cycle, the opposite of what the science summary implies, so real-time decoding may not yet be compatible with fast QEC. *(ai_interpretation)* [C1, S2]
- The headline below-threshold result is merged from two experiments, and the source reports 101 physical qubits per logical qubit plus rare correlated error events roughly once per hour — the main barrier to scaling. *(ai_interpretation)* [C2, C3, S1]
- A proven lower bound implies geometrically local 2D error correction incurs overhead growing with system size, a structural limit that engineering cannot remove. *(ai_interpretation)* [R3]
- Company-reported roadmaps to 100 or hundreds of logical qubits are unverified forward statements, and one filer states it expects continued significant losses while pursuing them. *(unverified_claim)* [M1, M5]
- Timing and volatility risk: all five QEC-linked stocks are below their 50-day averages with 20-day annualised volatility above 100%, and Xanadu's 74.7% three-month decline and 50% gap below its 50-day average suggest company-specific stress as well as a theme-wide pullback. This is risk context only, not a timing signal. *(ai_interpretation)* [T1, T3, T5, T7, T9, T10, T11]

**What would invalidate this thesis:**
- Below-threshold behaviour failing to reproduce or improve at larger code distance in later hardware runs, which would break the central premise that error correction scales as demonstrated. *(forecast)* [S1, C3]
- Evidence that decoder latency on real hardware cannot be brought below the code cycle time, making fast real-time QEC impractical at scale. *(forecast)* [C1, S2]
- Roadmap milestones (e.g. Sol 2027, Apollo 2029) being missed or restated without delivered logical-qubit counts, which would remove the main medium-term commercial anchor in the findings. *(forecast)* [M1]

**Conflicting evidence:**
- C1 directly contradicts S2 on decoder latency, stating the cited abstract reports average real-time decoder latency of 63 microseconds against a 1.1 microsecond cycle time, the opposite of 'well under the code cycle time', and that the second cited source has no abstract and cannot support the claim. *(ai_interpretation)* [C1, S2]
- C2 and C3 weaken S1: the real-time decoder and the distance-7 memory are separate experiments, and the source's own limits (101 qubits per logical qubit, 0.143% error per cycle, correlated errors about hourly) are omitted. *(ai_interpretation)* [C2, C3, S1]
- C5 weakens S6: the quantum-autoencoder claim is a numerical proposal under an assumed noise model, not a hardware demonstration, despite being labelled a verified fact. *(ai_interpretation)* [C5, S6]

**Companies named by cited evidence:**
- Quantinuum Inc. (QNT): States it was first in the industry to implement logical qubits with higher accuracy than physical qubits and targets up to 100 logical qubits with its Sol system (2027) and hundreds with Apollo (2029); it also acknowledges substantial uncertainty in achieving fault tolerance at commercially viable scale. Small, newly listed, thinly covered, and its stock is in a steep drawdown with the highest measured volatility in the group — higher risk and less disclosure than a large incumbent. [M1, M8, K1, T7, T8]
- IonQ, Inc. (IONQ): Defines logical qubits via error-correction encoding as its path to fault tolerance and expects continued significant losses while scaling physical and logical qubit counts; a pure-play with no QEC revenue shown in the findings. [M5, M7]
- Rigetti Computing, Inc. (RGTI): Frames large-scale fault tolerance as the largest commercial opportunity behind rising R&D spend, states the industry view that early fault tolerance needs 10,000 to 1,000,000 physical qubits, and its UK subsidiary won an Innovate UK award to advance QEC on superconducting hardware. [M2, M3, M7]
- D-Wave Quantum Inc. (QBTS): Claims its gate-model roadmap with Quantum Circuits' dual-rail error-detecting qubits could deliver fully error-corrected gate-model computing using up to an order of magnitude fewer physical qubits per logical qubit; this is a company claim, unverified, and the stock is the steepest decliner in the group after Xanadu. [M4, T5, T6]
- Xanadu Quantum Technologies Ltd (XNDU): Reports having demonstrated only twelve logical qubits with photon loss not meeting required levels while its architecture targets 100,000 cores, and flags substantial barriers to fault tolerance; its shares are down 74.7% over three months, a decline far larger than peers. [M6, K2, T9, T10]

### Overhead reduction: codes, connectivity and machine-learning decoders (mostly simulated)

Technologies: quantum low-density parity-check (qLDPC) codes, hyperbolic-lattice CSS codes, soft-information decoding, machine-learning / sparse decoders, measurement-free fault tolerance with neutral-atom Rydberg gates

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The near-term evidence is almost entirely simulation, extrapolation or preprints: overhead reductions rest on assumed physical error rates or simulated gains (R1), soft-information decoding gives up to 11% (superconducting) and 20% (neutral atom) better suppression in simulation (R5), and one decoder result comes from GPU software benchmarks not shown in a live hardware loop (C4). No finding shows a product, customer or production deployment in this window. *(ai_interpretation)* [R1, R5, C4, S5] | medium |
| medium_1_3y | The findings point to connectivity as the gating difficulty rather than code design: low-overhead qLDPC codes need dense, long-range connectivity that is hard to build, and removing up to 50% of long-range links roughly doubles syndrome circuit depth (R2), consistent with the view that overhead reductions shift cost between axes rather than removing it (R4). Company filings tie QEC software codes to fault-tolerance goals but give no delivered result (M8), so this horizon is unsupported by evidence of deployment. *(forecast)* [R2, R4, M8] | low |
| long_3_5y | Beyond connectivity, an energy-cost argument (a Landauer-erasure floor per logical qubit per round, from a non-peer-reviewed preprint whose supporting test is a classical channel) suggests overhead metrics may understate true cost (R7); this is weak, low-confidence evidence and the findings contain no hardware validation of it. The diversification of code theory (hyperbolic codes and new formalisms) is real research activity but the sources are simulated or metadata-only (S8, S9, C7) and say nothing about long-run commercial scale. *(forecast)* [R7, S8, S9, C7] | low |

**Bull case:** If overhead can be cut without simply moving cost to depth or connectivity, fault tolerance becomes reachable with far fewer physical qubits. The findings show active work on defect-centric sparse decoders with near-linear complexity and reported speedups (S5), on soft-information decoding that is simulated to cut qubit footprint by 13% (superconducting) and 33% (neutral atom) (R5), on multiqubit Rydberg gates for measurement-free fault tolerance (S7), and on code design beyond Euclidean surface codes (S8, S9). Each of these is a real research direction that, if it survives hardware translation, lowers the cost of every logical qubit. *(ai_interpretation)* [S5, S7, S8, S9, R5]

**Base case:** The plausible reading is incremental improvement with cost shifting. Reported gains are modest where quantified (R5), many headline reductions depend on assumed physical error rates or simulation (R1), and low-overhead codes demand dense long-range connectivity whose workarounds roughly double syndrome circuit depth (R2). Decoder speedups measured in software are not shown in a live hardware loop and are above the relevant cycle time (C4). Net space-time savings therefore remain unclear (R4), and one code-design claim rests on a paper with no abstract plus a simulation (C7). *(ai_interpretation)* [R1, R2, R4, R5, C4, C7]

**Bear case:** Overhead reduction may be largely an accounting exercise. A proven lower bound shows geometrically local 2D error correction carries overhead growing with system size (R3), so planar designs cannot escape the problem by better engineering; dense-connectivity codes move the burden into hardware that is hard to build (R2); and gains that are real are incremental rather than order-of-magnitude (R5). One widely cited low-overhead result mixes real-device runs with simulation and is hard to reconcile with the field's usual picture, requiring independent replication (R6). An additional unverified preprint argues the metric itself ignores an irreducible energy cost (R7). *(forecast)* [R2, R3, R5, R6, R7]

**Catalysts:**
- A decoder demonstrated in a live hardware loop at latency below the code cycle time, rather than in GPU software benchmarks. *(forecast)* [C4, S5]
- Hardware results for low-overhead codes (qLDPC or hyperbolic) on a device with the required long-range connectivity, with stated depth and round counts rather than qubit-count savings alone. *(forecast)* [R2, R4, S8]
- Independent replication of the disputed low-overhead NISQ claims under a clearly stated noise model. *(forecast)* [R6]

**Risks:**
- Many headline overhead reductions are simulation or extrapolation, with the key logical error rate depending on assumed physical error rates. *(ai_interpretation)* [R1]
- Low-overhead codes need dense long-range connectivity that is hard to build, and workarounds shift cost: removing up to 50% of long-range links roughly doubles syndrome circuit depth. *(ai_interpretation)* [R2]
- A decoder presented as a field-wide trend was benchmarked in software, with latencies above a 1.1 microsecond superconducting cycle time, so real-time compatibility is not established. *(ai_interpretation)* [C4, S5]
- Reported gains are platform-dependent and incremental (up to 11% and 20% better suppression, equal to 13% and 33% footprint reductions), not order-of-magnitude. *(ai_interpretation)* [R5]
- A code-design claim relies partly on a metadata-only paper with no abstract plus a simulated hyperbolic-code paper, while related evidence shows savings shifting to depth or connectivity. *(ai_interpretation)* [C7, S8]

**What would invalidate this thesis:**
- Demonstrations showing that qubit-count savings from low-overhead codes are cancelled by added depth, rounds or connectivity requirements in measured space-time cost, which would remove the main appeal of this theme. *(forecast)* [R2, R4]
- Failure of claims such as the reported 60% overhead reduction and 2.7x suppression to replicate independently, which would reduce confidence in the whole class of results. *(forecast)* [R6]
- Continued reliance on simulation and metadata-only papers rather than hardware measurement, leaving the central overhead question unresolved. *(forecast)* [R1, C7]

**Conflicting evidence:**
- C4 challenges S5: the sparse decoder result is a single preprint generalised into a field-wide trend, benchmarked on simulated noise plus one dataset, not demonstrated in a live hardware loop. *(ai_interpretation)* [C4, S5]
- C7 challenges S8: one cited paper has no abstract and the other simulates the codes, so claims of higher encoding rates and lower overhead are the paper's own framing and the connectivity/layout problem is unaddressed. *(ai_interpretation)* [C7, S8]
- R6 flags a low-overhead NISQ result mixing real-device runs with simulation that is hard to reconcile with the field's usual picture and needs replication — an unverified claim that pulls against the bull case. *(unverified_claim)* [R6]

**Companies named by cited evidence:**
- Quantinuum Inc. (QNT): Its filing names effective QEC software codes as one of the uncertainties in reaching fault tolerance at commercially viable scale, and it is flagged by the company-scout pass as active on the topic (next-runner score 20/100, a heuristic, not a prediction). Small, thinly covered, high volatility. [M8, K1, T7]
- Rigetti Computing, Inc. (RGTI): Won an Innovate UK Quantum Missions Pilot award specifically to advance quantum error correction on superconducting quantum computers, and funds it through rising R&D spending; no delivered result is shown in the findings. [M2, M3]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 222, 2021: 260, 2022: 283, 2023: 335, 2024: 434, 2025: 987, 2026: 2689}
Research Acceleration 2024->2025: 434 -> 987 (127.4% YoY). OpenAlex works whose title or abstract contains the exact phrase "quantum error correction", per publication year. Synonyms and abbreviations are not counted, and the number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-10): 2025 671 -> 2026 2452 (265.4%, trend: rising). OpenAlex works with the exact phrase 'quantum error correction' in title or abstract published 1 Jan–10 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence high)* A superconducting surface-code memory has been operated below the error-correction threshold with a real-time decoder, with logical error suppressed by increasing code distance and a distance-7 logical memory exceeding its best physical qubit's lifetime.
  - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
  - excerpt: "we present two below-threshold surface code memories on our newest generation of superconducting processors, Willow: a distance-7 code, and a distance-5 code integrated with a real-time decoder."
  - reasoning: Peer-reviewed Nature article; the abstract states below-threshold operation, distance scaling and break-even explicitly. Single source, but direct and quantitative.
- **[S2]** *(verified_fact, confidence medium)* Real-time decoding has been demonstrated as compatible with below-threshold surface-code operation, with reported decoder latency well under the code cycle time.
  - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
  - source: [Real-time quantum error correction beyond break-even](https://doi.org/10.1038/s41586-023-05782-6) (OpenAlex, 2023-03-22, metadata_only)
  - excerpt: "Our system maintains below-threshold performance when decoding in real time, achieving an average decoder latency of 63 μs at distance-5 up to a million cycles, with a cycle time of 1.1 μs."
  - reasoning: Quantitative claim from the Willow paper; a second Nature paper on real-time QEC beyond break-even is present but has no abstract available, so it is only weakly corroborating context.
- **[S3]** *(verified_fact, confidence high)* Error-corrected logical qudits (qutrit and ququart) using a bosonic Gottesman-Kitaev-Preskill code have been experimentally operated beyond break-even, with the encoding optimized by a reinforcement-learning agent.
  - source: [Quantum error correction of qudits beyond break-even](https://doi.org/10.1038/s41586-025-08899-y) (OpenAlex, 2025-05-14, abstract_only)
  - excerpt: "we report the experimental realization of an error-corrected logical qutrit (d = 3) and ququart (d = 4), which was achieved with the Gottesman–Kitaev–Preskill bosonic code"
  - reasoning: Peer-reviewed Nature article stating experimental realization and beyond-break-even gain; single source but direct.
- **[S4]** *(verified_fact, confidence high)* Leakage out of the computational subspace has been actively removed each cycle in surface-code and bit-flip-code experiments, reducing steady-state leakage population roughly tenfold and limiting leakage-induced correlated errors.
  - source: [Overcoming leakage in quantum error correction](https://doi.org/10.1038/s41567-023-02226-w) (OpenAlex, 2023-10-05, abstract_only)
  - excerpt: "we demonstrate a distance-3 surface code and distance-21 bit-flip code on a quantum processor for which leakage is removed from all qubits in each cycle."
  - reasoning: Peer-reviewed Nature Physics article with explicit quantitative reduction stated in the abstract.
- **[S5]** *(verified_fact, confidence medium)* Machine-learning decoders for QEC are moving toward defect-centric, sparse processing architectures, with one reported design processing only active syndrome detection events at near-linear complexity and reporting large speedups over near-maximum-likelihood and matching-based decoders.
  - source: [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) (arXiv, 2026-05-16, abstract_only)
  - excerpt: "We introduce the Sparse Mamba Decoder (SMD), a defect-centric neural decoder that processes only the k active detection events using a 13-dimensional feature representation per defect and a Mamba state-space backbone, achieving $O(k)$ complexity."
  - reasoning: Numerical benchmarks are reported in the abstract, but this is an arXiv preprint and has not been peer reviewed; the speedup and accuracy figures are self-reported.
- **[S6]** *(verified_fact, confidence medium)* Quantum autoencoders have been trained to detect and correct errors, including spatially correlated errors and qubit loss, and can extend logical-qubit lifetime even when the autoencoder itself is moderately noisy.
  - source: [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) (OpenAlex, 2023-03-09, abstract_only)
  - excerpt: "we demonstrate how quantum neural networks, in the form of quantum autoencoders, can be trained to learn optimal strategies for active detection and correction of errors, including spatially correlated computational errors as well as qubit losses."
  - reasoning: Peer-reviewed article in Quantum; the abstract describes demonstrated capability but the evidence base here is a single work.
- **[S7]** *(verified_fact, confidence medium)* Multiqubit neutral-atom Rydberg gates implemented with global laser pulses are being explored for measurement-free fault-tolerant QEC and for Floquet codes built from two-body stabilizer measurements.
  - source: [Multiqubit Rydberg Gates for Quantum Error Correction](https://arxiv.org/abs/2512.00843v2) (arXiv, 2025-11-30, abstract_only)
  - excerpt: "we investigate multiqubit Rydberg gates that are useful for fault-tolerant quantum error correction in single-species neutral-atom platforms and can be implemented with global laser pulses that do not individually address atomic sites."
  - reasoning: Published in PRX Quantum (listed venue) but provided here as a preprint-style record without a peer-review statement in the metadata; abstract reports break-even analysis.
- **[S8]** *(verified_fact, confidence low)* Code-design research is diversifying beyond Euclidean surface codes toward hyperbolic-lattice CSS codes, which are claimed to raise encoding rates and lower qubit overhead.
  - source: [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) (arXiv, 2025-04-10, abstract_only)
  - source: [Demonstration of low-overhead quantum error correction codes](https://doi.org/10.1038/s41567-025-03157-4) (OpenAlex, 2026-01-22, metadata_only)
  - excerpt: "By embedding qubits in hyperbolic lattices, these codes achieve higher encoding rates and lower qubit overhead compared to those defined on conventional Euclidean lattices."
  - reasoning: The hyperbolic-code claim is from an arXiv preprint with simulation-based metrics; a second paper on low-overhead QEC codes exists but has no abstract available, so corroboration is weak.
- **[S9]** *(ai_interpretation, confidence medium)* Theoretical QEC work is extending the formalism itself: a stabilizer framework now covers operator-algebra quantum error correction, and an approximate-QEC theory addresses non-isometric encodings relevant to energy-constrained continuous-variable codes.
  - source: [Stabilizer Formalism for Operator Algebra Quantum Error Correction](https://arxiv.org/abs/2304.11442v2) (arXiv, 2023-04-22, abstract_only)
  - source: [Approximate quantum error correction theory of non-isometric codes](https://arxiv.org/abs/2606.13559v1) (arXiv, 2026-06-11, abstract_only)
  - reasoning: Both are arXiv papers; the first was later published in Quantum. Reading them together shows formalism-level generalization work rather than hardware demonstrations.
- **[S10]** *(ai_interpretation, confidence low)* QEC concepts are being borrowed outside mainstream hardware routes, including lattice gauge theory simulations, where Gauss-law constraints supply redundancy, and thermodynamic recycling of algorithmic failure branches on superconducting hardware.
  - source: [Quantum error correction with gauge symmetries](https://doi.org/10.1038/s41534-023-00706-8) (OpenAlex, 2023-04-25, abstract_only)
  - source: [Thermodynamic Recycling of Algorithmic Failure Branches: Quantum-Computer Demonstration with Quantum Error Correction](https://arxiv.org/abs/2601.07522v2) (arXiv, 2026-01-12, abstract_only)
  - reasoning: Two separate papers from different subfields; the thermodynamic work is an arXiv preprint and both are single demonstrations, so this is a weak cross-domain signal.
- **[S11]** *(verified_fact, confidence low)* A quaternionic extension of quantum error correction has been proposed, constructing a quaternionic analogue of the five-qubit code with a reported logical error threshold of about 0.015 claimed to exceed the complex-valued code.
  - source: [Quantum Error Correction in Quaternionic Hilbert Spaces](https://arxiv.org/abs/2504.19833v1) (arXiv, 2025-04-28, abstract_only)
  - excerpt: "Numerical estimates show that the quaternionic five-qubit code achieves a logical error threshold of approximately $p_{th} \approx 0.015$"
  - reasoning: Single arXiv preprint with numerical estimates only; no independent reproduction or peer review, and the claim of improvement over the standard code rests on the authors' own simulation.

**Emerging directions:**
- defect-centric / sparse neural decoders with near-constant latency across code distances
- machine-learning-optimized bosonic (GKP) logical qudits
- measurement-free fault-tolerant QEC with multiqubit neutral-atom gates
- hyperbolic-lattice and other non-Euclidean CSS code families
- Floquet codes and low-overhead code constructions
- approximate QEC theory for non-isometric and energy-constrained encodings
- cross-domain reuse of QEC primitives in lattice gauge theory simulation and quantum thermodynamics

**Open problems:**
- Rare correlated error events appear to limit logical performance at large code distances even when operating below threshold.
- Leakage must be continuously removed or it builds over time and spreads into correlated errors.
- Practical fault tolerance still requires hardware-efficient encodings that avoid exponentially large physical-qubit overhead.
- Energy and non-isometric constraints degrade the accuracy of continuous-variable code implementations.
- Neural decoder accuracy, latency and scalability must be achieved simultaneously, and most high-accuracy decoders process full dense syndrome arrays.

**Limitations:**
- All statements are based on titles and abstracts only; no full texts were read.
- Several arXiv items are preprints and have not been peer reviewed; their numerical benchmarks are self-reported.
- Two retrieved records (one on real-time QEC beyond break-even, one on low-overhead QEC codes) have no abstract available, so they could not be used as evidence beyond their existence.
- The sample mixes hardware demonstrations, code theory, decoders and speculative formalisms, so findings are not directly comparable and paper counts are not used as evidence.
- No commercial or investment conclusions can be drawn; a research demonstration is not evidence of commercial viability.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['quantum error correction overhead', 'syndrome extraction latency', 'physical error rate threshold', 'quantum error correction cross-talk', 'error mitigation vs correction', 'cryogenic decoder constraints']

- **[R1]** *(verified_fact, confidence medium)* Many headline overhead reductions rest on simulation or extrapolation rather than hardware. The Cornucopia result is an extrapolated logical error rate that depends on assumed physical error rates, and the soft-information gains are simulated.
  - source: [Quantum error correction at ultra-low overhead](https://doi.org/10.48550/arxiv.2608.02773) (OpenAlex, 2026-08-03, abstract_only)
  - source: [Reducing quantum error correction overhead using soft information](https://arxiv.org/abs/2504.03504v3) (arXiv, 2025-04-04, abstract_only)
  - source: [Reducing Quantum Error Correction Overhead with Versatile Flag-Sharing Syndrome Extraction Circuits](https://arxiv.org/abs/2407.00607v1) (arXiv, 2024-06-30, abstract_only)
  - excerpt: "achieving an extrapolated logical error rate of $2.6\times10^{-16}$ ($1.9\times10^{-31}$) per logical qubit per cycle, assuming the physical error rate of $0.1\%$ ($0.01\%$)"
  - reasoning: The abstracts of src_43430297cb, src_905c50a9ad and src_aebf5c7a43 describe extrapolation or numerical simulation (circuit-level noise models). All three are arXiv-origin preprints and are not peer reviewed as retrieved. The abstracts do not show whether the assumed noise models hold on real devices, including correlated errors, leakage and drift. That is a gap rather than a demonstrated failure.
- **[R2]** *(verified_fact, confidence medium)* Low-overhead qLDPC codes need dense, long-range connectivity that is hard to build, especially on superconducting processors. Workarounds shift the cost elsewhere: removing up to 50% of long-range links roughly doubles syndrome circuit depth.
  - source: [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) (arXiv, 2025-08-31, abstract_only)
  - source: [Simulation and Design of Quantum Processors for Low‑Overhead Quantum Error Correction](https://hdl.handle.net/1721.1/163685) (OpenAlex, 2025-05-01, abstract_only)
  - excerpt: "Quantum low-density parity-check codes reduce quantum error correction overhead but require dense, long-range connectivity that challenges hardware implementation, particularly for superconducting processors."
  - reasoning: src_c0058675c2 is an arXiv preprint. src_ec87473193 is an MIT thesis that designs a long-range coupler spanning five lattice sites, but only for a nine-qubit prototype. The abstracts give no evidence of scaling long-range coupling to thousands of qubits.
- **[R3]** *(verified_fact, confidence medium)* A proven lower bound says that error correction restricted to geometrically local operations in 2D incurs overhead that grows with system size, even with free classical computation. Planar-layout architectures therefore face a structural limit that engineering alone cannot remove.
  - source: [A lower bound on the overhead of quantum error correction in low dimensions](https://doi.org/10.48550/arxiv.2302.04317) (OpenAlex, 2023-02-08, abstract_only)
  - excerpt: "We show that a quantum architecture with an error correction procedure limited to geometrically local operations incurs an overhead that grows with the system size"
  - reasoning: This is a single theoretical preprint, not peer reviewed as retrieved. It applies to strictly local architectures, so non-local codes and reconfigurable-atom approaches are outside the bound. This is also the reason connectivity-heavy alternatives are being pursued, which exposes them to the connectivity risk above.
- **[R4]** *(ai_interpretation, confidence medium)* Overhead reductions often move cost between resource axes instead of removing it. Qubit-count savings come with extra circuit depth, extra rounds or code-specific restrictions, so net savings in space-time cost are unclear.
  - source: [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) (arXiv, 2025-08-31, abstract_only)
  - source: [Quantum Prometheus: Defying Overhead with Recycled Ancillas in Quantum Error Correction](https://doi.org/10.1109/isqed65160.2025.11014328) (OpenAlex, 2025-04-23, abstract_only)
  - source: [Reducing Quantum Error Correction Overhead with Versatile Flag-Sharing Syndrome Extraction Circuits](https://arxiv.org/abs/2407.00607v1) (arXiv, 2024-06-30, abstract_only)
  - reasoning: src_c0058675c2 reports about 2x circuit depth for a 50% cut in long-range connections. src_93b8f532fe cuts ancillas by alternating X and Z measurements per half-round and reports about 25% less qubit overhead for rotated surface codes only. Its abstract does not discuss the time or idle-error cost. src_aebf5c7a43 defines circuit area as depth times qubits, which implies that qubit count alone is incomplete. The tradeoff is my inference across the abstracts. These are preprints and a conference paper, and src_93b8f532fe gives no hardware validation in its abstract.
- **[R5]** *(verified_fact, confidence low)* Reported gains depend on the platform and are modest in places. Soft-information decoding is simulated to give up to 11% (superconducting) and up to 20% (neutral atom) better error suppression, equal to 13% and 33% qubit-footprint reductions. These are incremental, not order-of-magnitude, gains.
  - source: [Reducing quantum error correction overhead using soft information](https://arxiv.org/abs/2504.03504v3) (arXiv, 2025-04-04, abstract_only)
  - excerpt: "Our simulations show that soft information decoding on near-term devices can provide up to 11% higher error suppression on superconducting qubits and up to 20% stronger error suppression on neutral atom qubits."
  - reasoning: This rests on one arXiv preprint (later listed in Quantum Sci. Technol.) with simulation only. Soft information needs analog readout data and decoders that can use it in real time, and the abstract does not address that cost. The Cornucopia codes similarly depend on reconfigurable neutral-atom rearrangement (src_43430297cb), so benefits are tied to specific hardware.
- **[R6]** *(unverified_claim, confidence low)* The NISQ low-overhead paper reports strong results (60% overhead reduction, 2.7x suppression, break-even at 0.8% physical error rate) that mix real-device runs with simulation and are hard to reconcile with the field's usual picture. These claims need independent replication.
  - source: [Low-Overhead Quantum Error Correction Codes for Noisy Intermediate-Scale Quantum Devices](https://doi.org/10.1051/epjconf/202636001013/pdf) (OpenAlex, 2026-03-23, abstract_only)
  - reasoning: The abstract lists IBM Eagle and IonQ experiments alongside 'Google Sycamore simulation', so it is unclear which results are measured. It also reports a logical error rate of 0.0065 from 10 physical qubits, which is a weak absolute level. It claims 94.3% ML-decoder accuracy at 12 µs latency. The abstract gives no code distance, no shot counts and no error bars. The venue is an unusual metadata record, there are 0 citations, and I could not tell whether it was peer reviewed. This is a reproducibility gap, not proof of error.
- **[R7]** *(ai_interpretation, confidence low)* A non-peer-reviewed preprint argues that error correction has an energy cost set by Landauer erasure (a floor of (n−k)/k · kT·ln2 per logical qubit per round), which standard overhead metrics ignore. Its evidence is a classical NAND-like channel comparison, not quantum hardware, and one test gave a partial null.
  - source: [Error Correction Is a Landauer Machine: The Thermodynamic Floor of Quantum Error-Correction Overhead](https://doi.org/10.5281/zenodo.22115862) (OpenAlex, 2026-08-26, abstract_only)
  - excerpt: "a partial null that leaves the floor claim intact and defines the protocol for an industrial flash-memory test"
  - reasoning: The source is a Zenodo preprint with 0 citations and abstract-only access. It states a partial null: a naive nested construction pays a residual-error penalty. The industrial flash-memory test is still to be done. Its biology argument (photosynthesis, magnetoreception) is an analogy, not evidence about engineered qubits. The abstract gives no comparison of the floor against real cryogenic or control-electronics power, so the practical importance of this floor is unknown. This is a gap.

**Possible hype:**
- 'Ultra-low overhead' (src_43430297cb): the headline logical error rates of 10^-16 to 10^-31 are extrapolations under assumed physical error rates, not measurements.
- 'Defying Overhead' (src_93b8f532fe): the ~25% qubit saving is for rotated surface codes only, and the abstract does not address time or depth cost.
- 'Experimental validation' with '60% overhead reduction' (src_020cace84d): the abstract mixes hardware and simulation and gives no statistical detail.
- 'Error Correction Is a Landauer Machine' and the biological 'no correction needed' framing (src_0df71ca0a9): the conclusions come from a classical-channel analogy, an unreviewed preprint and an untested protocol.
- Generic 'low-overhead' labels across the set: overhead is often measured in only one dimension (qubit count), while depth, connectivity and decoder cost go unquantified.

**Challenges to the Science findings:**
- Targets ['S2'], severity high:
  - **[C1]** *(ai_interpretation, confidence high)* S2 says decoder latency was 'well under the code cycle time'. The cited abstract reports the opposite: average real-time decoder latency of 63 μs against a 1.1 μs cycle time. The latency is much longer than the cycle, not shorter. The abstract shows only that the decoder kept pace for up to a million cycles at distance-5. It says nothing about the latency being under the cycle time. The second cited paper (src_3ee790e4ad) has no abstract, so it cannot support the claim.
    - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
    - source: [Real-time quantum error correction beyond break-even](https://doi.org/10.1038/s41586-023-05782-6) (OpenAlex, 2023-03-22, metadata_only)
    - excerpt: "achieving an average decoder latency of 63 μs at distance-5 up to a million cycles, with a cycle time of 1.1 μs"
    - reasoning: 63 μs is about 57 times the 1.1 μs cycle time. S2's quantitative characterisation therefore contradicts its own source. The src_3ee790e4ad citation is metadata-only and adds no support.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S1'], severity medium:
  - **[C2]** *(ai_interpretation, confidence high)* S1 merges two separate experiments into one. The real-time decoder was used with the distance-5 code. The distance-7 memory that beats its best physical qubit by 2.4x is a different code. The finding implies a distance-7 memory operated with a real-time decoder, and the abstract does not say this.
    - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
    - excerpt: "a distance-7 code, and a distance-5 code integrated with a real-time decoder"
    - reasoning: The abstract lists two memories, and only the distance-5 one is tied to real-time decoding. Combining them overstates what has been shown.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S1'], severity medium:
  - **[C3]** *(ai_interpretation, confidence medium)* S1 omits the limits the same abstract reports. The headline memory uses 101 qubits for one logical qubit, with 0.143% error per cycle and Λ of about 2.14. Repetition-code performance is capped by rare correlated error events roughly once per hour, about 3×10^9 cycles. A confident 'verified fact, high' summary leaves out the main barrier to scaling and the large gap to algorithm-scale requirements.
    - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
    - excerpt: "logical performance is limited by rare correlated error events occurring approximately once every hour, or $$3$$ $$\times $$ $${10}^{9}$$ cycles"
    - reasoning: The authors say the result 'if scaled' could meet requirements. That is conditional, and S1 does not carry the condition. Correlated-error floors are the kind of issue that can break exponential suppression at larger scale.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S5'], severity medium:
  - **[C4]** *(ai_interpretation, confidence medium)* S5 is labelled verified_fact and generalises from one preprint to a field-wide 'moving toward' trend. The reported speedups come from software benchmarks (simulated noise models plus one Sycamore dataset) on GPUs, against other decoders. The 24-57 μs latencies are not shown on hardware in a live loop. They are also well above a 1.1 μs superconducting cycle time. The abstract does not establish that this decoder is real-time compatible with fast QEC.
    - source: [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) (arXiv, 2026-05-16, abstract_only)
    - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
    - reasoning: The preprint is unreviewed and offline in nature (GPU, benchmark datasets). Its latency figures sit against the 63 μs / 1.1 μs figures in the Willow paper. The evidence base is a single paper, and it does not show deployment feasibility.
- Targets ['S6'], severity medium:
  - **[C5]** *(ai_interpretation, confidence medium)* S6 is labelled verified_fact, but the abstract describes quantum autoencoders as trained and investigated, and says 'we find' that they may extend lifetime. It reports no hardware experiment. 'Have been trained to detect and correct errors' and 'can extend logical-qubit lifetime' read as demonstrated capability, but the abstract supports only a proposal studied numerically, under an assumed noise model.
    - source: [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) (OpenAlex, 2023-03-09, abstract_only)
    - excerpt: "we investigate the potential of quantum machine learning for quantum error correction in a quantum memory"
    - reasoning: The abstract uses 'potential' and 'may still be successfully used' and mentions no device. The confidence label should be lower. Comparison against standard decoders is also not stated in the abstract.
- Targets ['S11'], severity medium:
  - **[C6]** *(ai_interpretation, confidence medium)* S11 presents a quaternionic QEC threshold of about 0.015 as a trend in QEC research. The source is a single preprint with 'numerical estimates' only. It gives no stated noise model, no comparison conditions, and no route to a physical quaternionic system. Whether the threshold 'exceeds' the complex-valued code is not comparable to hardware-relevant thresholds. It should not be grouped with the hardware demonstrations (S1, S3, S4).
    - source: [Quantum Error Correction in Quaternionic Hilbert Spaces](https://arxiv.org/abs/2504.19833v1) (arXiv, 2025-04-28, abstract_only)
    - excerpt: "Numerical estimates show that the quaternionic five-qubit code achieves a logical error threshold of approximately $p_{th} \approx 0.015$"
    - reasoning: Quaternionic quantum mechanics is not an established physical platform. A threshold from numerical estimates on a five-qubit code is not evidence of practical improvement.
- Targets ['S8'], severity low:
  - **[C7]** *(ai_interpretation, confidence medium)* S8 relies on a metadata-only paper (src_0192635a40), which has no abstract and cannot support the claim. Its other citation, the hyperbolic-code paper, simulates the codes. Statements about higher encoding rates and lower overhead are the paper's own framing. The abstract does not report hardware results, and the problem of connectivity and layout for hyperbolic codes is not addressed. Related evidence shows overhead savings often shift cost to depth or connectivity.
    - source: [Demonstration of low-overhead quantum error correction codes](https://doi.org/10.1038/s41567-025-03157-4) (OpenAlex, 2026-01-22, metadata_only)
    - source: [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) (arXiv, 2025-04-10, abstract_only)
    - source: [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) (arXiv, 2025-08-31, abstract_only)
    - reasoning: One cited source has no abstract, so the claim rests on a single simulation-based preprint. Overhead trade-offs in the qLDPC routing paper (about 50% fewer long-range links for roughly twice the depth) suggest caution about 'lower overhead' claims.

**Limitations:**
- Only abstracts or metadata were available; no full text was read, so methods, noise models and error bars were not checked.
- src_0192635a40 (Nature Physics, 'Demonstration of low-overhead quantum error correction codes', 66 citations) and src_c9bb5e9898 (a calculator) had no abstract. The one apparent experimental demonstration therefore could not be assessed, and nothing here should be read as contradicting it.
- Several sources are arXiv or Zenodo preprints and are not peer reviewed as retrieved. Two are MIT theses with prototype-scale scope.
- The set of 12 papers is narrow. It centres on 'low overhead' and omits decoder latency, real-time classical control, cryogenic power, fabrication yield, magic-state cost and leakage or correlated errors, so the risk coverage is incomplete.
- The set has no direct competing results that contradict each other. The contradictions identified (e.g. the 2D locality bound versus connectivity-heavy codes) are my inferences.
- No company-level evidence was retrieved; this analysis concerns technical risk only.
- Only titles, metadata and abstracts were reviewed. Full-text details such as noise models, decoder pipelining and baselines could change some challenges, especially on S2 and S5.
- src_3ee790e4ad and src_0192635a40 have no abstracts, so I could not check what they report. I only noted that they cannot support the claims attributed to them.
- I did not challenge S3, S4, S7, S9 and S10 because their abstracts appear consistent with the findings, apart from minor hedging issues such as distance-3 scale and simulation-based performance claims.
- The evidence set has no independent replications or critical commentary on the Willow result, so the risk review rests on the abstracts themselves.

## Evidence: company filings and news
Status: ok. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: quantum error correction, logical qubit, surface code, fault-tolerant quantum, bosonic code, quantum LDPC

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| IonQ (IONQ) | 2 | 1 | small: 0.1B USD | +201.9% | 235.1% of revenue | 2 press release(s) read |
| Rigetti Computing (RGTI) | 2 | 2 | micro: 0.0B USD | +59.9% | 457.6% of revenue | 2 press release(s) read |
| D-Wave Quantum (QBTS) | 2 | 1 | micro: 0.0B USD | +178.5% | 206.3% of revenue |  |
| International Business Machines (IBM) | 2 | 0 | large: 67.5B USD | +7.6% | 12.3% of revenue | 2 press release(s) read |
| Honeywell International (HON) | 2 | 0 | large: 37.4B USD | +7.8% | 4.8% of revenue |  |
| Quantinuum Inc. (QNT) | 1 | 1 | n/a | n/a | n/a | discovered by full-text search |
| Xanadu Quantum Technologies Ltd (XNDU) | 1 | 1 | n/a | n/a | n/a | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence medium)* Quantinuum states it was the first in the industry to implement logical qubits with higher accuracy than physical qubits, citing the 2021 Ryan-Anderson et al. Study, and expects its Sol system (2027) to achieve up to 100 logical qubits and Apollo (2029) to achieve hundreds of logical qubits.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - excerpt: "we were the first in the industry to implement logical qubits with a higher accuracy than physical qubits, according to the 2021 Ryan-Anderson et al. Study."
  - reasoning: Directly stated in Quantinuum's 10-Q excerpt; the future system timelines are the company's own expectations, but the excerpt is quoted verbatim.
- **[M2]** *(verified_fact, confidence medium)* Rigetti frames large-scale fault-tolerant quantum computing as the goal of its rising R&D spending, and states that the industry believes early fault tolerance will likely require systems with 10,000 to 1,000,000 physical qubits.
  - source: [Rigetti Computing, Inc. Form 10-K, filed 2026-03-04](https://www.sec.gov/Archives/edgar/data/1838359/000110465926023454/rgti-20251231x10k.htm) (SEC EDGAR, 2026-03-04, excerpt_only)
  - source: [Rigetti Computing, Inc. Form 10-Q, filed 2026-08-06](https://www.sec.gov/Archives/edgar/data/1838359/000110465926091993/rgti-20260630x10q.htm) (SEC EDGAR, 2026-08-06, excerpt_only)
  - excerpt: "It is currently believed in the quantum computing industry that this is likely to require systems with 10,000 to 1,000,000 physical qubits."
  - reasoning: Both Rigetti filings explicitly tie R&D growth to fault-tolerant quantum computing goals; the physical-qubit requirement is stated as industry belief in the 10-K.
- **[M3]** *(verified_fact, confidence medium)* Rigetti's UK subsidiary was selected in April 2025 as one of the winners of Innovate UK's Quantum Missions Pilot Competition to advance quantum error correction capabilities on superconducting quantum computers.
  - source: [Rigetti Computing, Inc. Form 10-K, filed 2026-03-04](https://www.sec.gov/Archives/edgar/data/1838359/000110465926023454/rgti-20251231x10k.htm) (SEC EDGAR, 2026-03-04, excerpt_only)
  - excerpt: "In April 2025, Rigetti UK Limited, our wholly owned subsidiary, announced that it was selected as one of the winners of Innovate UK’s Quantum Missions Pilot Competition to advance quantum error correction capabilities on superconducting quantum computers."
  - reasoning: Stated directly in Rigetti's 10-K excerpt.
- **[M4]** *(unverified_claim, confidence medium)* D-Wave claims its gate-model roadmap, combining its technology with Quantum Circuits' dual-rail error-detecting qubits, could enable it to be the first to deliver fully error-corrected, scaled gate-model quantum computing, using up to an order of magnitude fewer physical qubits per logical qubit.
  - source: [D-Wave Quantum Inc. Form 10-K, filed 2026-02-26](https://www.sec.gov/Archives/edgar/data/1907982/000190798226000026/qbts-20251231.htm) (SEC EDGAR, 2026-02-26, excerpt_only)
  - excerpt: "Combining these technologies is expected to facilitate an accelerated commercial gate-model product roadmap that D-Wave believes will enable it to be the first to deliver fully error-corrected, scaled gate-model quantum computing."
  - reasoning: The excerpt is a verbatim company expectation ('D-Wave believes'), not an achieved result; the competitive 'first to deliver' claim is the company's own forward-looking statement.
- **[M5]** *(verified_fact, confidence medium)* IonQ defines logical qubits via error correction encoding as its path to fault-tolerant quantum computing, and expects to continue incurring significant losses while pursuing higher numbers of physical and logical qubits as prerequisites for broad quantum advantage.
  - source: [Ionq, Inc. Form 10-K, filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1824920/000119312526071562/ionq-20251231.htm) (SEC EDGAR, 2026-02-25, excerpt_only)
  - excerpt: "We expect to continue to incur significant losses for the foreseeable future as we prioritize reaching the technical milestones necessary to achieve an increasingly higher number of physical and logical qubits"
  - reasoning: Direct statements in IonQ's 10-K; the loss expectation is the company's own forward-looking statement quoted verbatim.
- **[M6]** *(verified_fact, confidence medium)* Xanadu has so far demonstrated only twelve logical qubits with photon loss not meeting required levels, while its architecture targets scaling to 100,000 cores; it flags substantial barriers to building a fault-tolerant quantum computer.
  - source: [Xanadu Quantum Technologies Ltd Form 20-F, filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) (SEC EDGAR, 2026-04-09, excerpt_only)
  - excerpt: "twelve logical qubits with photon loss not meeting the required levels. Our architecture is designed with a target to scale up to 100,000"
  - reasoning: Stated in Xanadu's 20-F excerpt; the 100,000-core figure is a stated design target, not an achieved capability.
- **[M7]** *(ai_interpretation, confidence medium)* Across the pure-play quantum companies, quantum error correction is the central technical milestone gating commercialization: Rigetti calls full-scale fault tolerance 'the largest commercial opportunity,' Quantinuum ties logical-qubit metrics to customer outcomes and commercial adoption, and IonQ positions FTQC as the stage where quantum computers outcompete classical machines across many sectors.
  - source: [Rigetti Computing, Inc. Form 10-K, filed 2026-03-04](https://www.sec.gov/Archives/edgar/data/1838359/000110465926023454/rgti-20251231x10k.htm) (SEC EDGAR, 2026-03-04, excerpt_only)
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - source: [Ionq, Inc. Form 10-K, filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1824920/000119312526071562/ionq-20251231.htm) (SEC EDGAR, 2026-02-25, excerpt_only)
  - reasoning: Pattern across three independent filings: each company explicitly links error correction / logical qubits to commercial payoff, though none claims full fault tolerance is achieved today.
- **[M8]** *(verified_fact, confidence medium)* Quantinuum acknowledges substantial scientific and engineering uncertainty in achieving fault tolerance at commercially viable scale, including low error rates across many qubits, effective QEC software codes, coherence management, and scaling with maintained gate fidelities.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - excerpt: "Achieving fault-tolerance at commercially viable scale involves substantial scientific and engineering uncertainty, including achieving sufficiently low error rates across large numbers of qubits, developing effective quantum error correction software codes"
  - reasoning: Risk disclosure quoted verbatim from Quantinuum's 10-Q.
- **[M9]** *(assumption, confidence low)* IBM and Honeywell filings retrieved did not mention the quantum error correction keywords, so this analysis provides no direct filing evidence of their QEC activities; their absence from the excerpts does not mean absence from the market.
  - reasoning: Per retrieval summary, 0 of 2 reports for each company mentioned the keywords; excerpt-only coverage cannot establish market absence.
  - citation check: company name(s) not found in the cited sources removed: IBM, Honeywell International Inc.

**Limitations:**
- Only 6 sources were available, all excerpt-only SEC filings; no full filings were read and no news headlines were provided despite press releases being retrieved for IONQ, RGTI and IBM.
- Coverage is limited to the configured company list plus two discovered companies (Quantinuum, Xanadu); other significant QEC players (e.g., Google, Microsoft, Alice & Bob, AWS) are not covered.
- No evidence on customers, revenue attributable to QEC, supply chain, or manufacturing capacity for error correction specifically; the filings discuss technology roadmaps and risk factors.
- Quantinuum and Xanadu report no annual revenue in SEC XBRL data, limiting commercial-scale assessment of these discovered companies.
- Company forward-looking milestones (e.g., Quantinuum's 2027 Sol system, D-Wave's 'first to deliver' claim) are unverified expectations, not demonstrated results.

## Evidence: patents
Status: partial. Worldwide patent publications from Google Patents (SerpApi) matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: ok. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.

| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |
|---|---|---|---|---|---|---|---|
| Rigetti Computing (RGTI) | 11.75 (2026-11-06) | -16.9% | -33.4% | -15.8% | 109.4% | -47.9% | **subdued**: 15.8% below its 50-day average and -33.4% over 3 months; high volatility (109.4% annualised, 20-day) |
| IonQ (IONQ) | 32.62 (2026-11-06) | -17.3% | -23.3% | -11.7% | 121.9% | -47.4% | **subdued**: 11.7% below its 50-day average and -23.3% over 3 months; high volatility (121.9% annualised, 20-day) |
| D-Wave Quantum (QBTS) | 10.68 (2026-11-06) | -26.8% | -47.1% | -26.8% | 105.9% | -60.0% | **subdued**: 26.8% below its 50-day average and -47.1% over 3 months; high volatility (105.9% annualised, 20-day) |
| Quantinuum Inc. (QNT) | 37.57 (2026-11-06) | -9.5% | -33.6% | -13.4% | 134.1% | -56.7% | **subdued**: 13.4% below its 50-day average and -33.6% over 3 months; high volatility (134.1% annualised, 20-day) |
| Xanadu Quantum Technologies Ltd (XNDU) | 2.67 (2026-11-06) | -35.2% | -74.7% | -50.0% | 115.2% | -81.6% | **subdued**: 50.0% below its 50-day average and -74.7% over 3 months; high volatility (115.2% annualised, 20-day) |

- **[T1]** *(verified_fact, confidence medium)* Rigetti Computing (RGTI) has pulled back sharply: -33.4% over 3 months and 15.8% below its 50-day average, with 20-day annualised volatility of 109.4%.
  - source: [Rigetti Computing (RGTI) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RGTI&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -33.4%. Price vs 50-day average -15.8%. 20-day annualised volatility 109.4%."
- **[T2]** *(ai_interpretation, confidence medium)* RGTI's rule-based timing risk is subdued, meaning little recent run-up; however, volatility above 100% annualised means large daily swings remain likely in either direction, and a subdued level does not imply the price will rise.
  - source: [Rigetti Computing (RGTI) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RGTI&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T3]** *(verified_fact, confidence medium)* IonQ (IONQ) is down 23.3% over 3 months and 11.7% below its 50-day average, with 20-day annualised volatility of 121.9% — the timing-risk reading is subdued but volatility is very high.
  - source: [IonQ (IONQ) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IONQ&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -23.3%. Price vs 50-day average -11.7%. 20-day annualised volatility 121.9%."
- **[T4]** *(ai_interpretation, confidence medium)* IONQ sits roughly midway between its 100-day low (+30.9%) and high (-47.4%); the pullback reduces run-up risk but the extreme volatility makes any timing assessment unstable over even short horizons.
  - source: [IonQ (IONQ) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IONQ&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T5]** *(verified_fact, confidence medium)* D-Wave Quantum (QBTS) shows the steepest decline among the group apart from Xanadu: -47.1% over 3 months and 26.8% below its 50-day average, with 105.9% annualised volatility.
  - source: [D-Wave Quantum (QBTS) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QBTS&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -47.1%. Price vs 50-day average -26.8%. 20-day annualised volatility 105.9%."
- **[T6]** *(ai_interpretation, confidence medium)* QBTS trades 60.0% below its 100-day high; such a deep drawdown signals sustained selling pressure rather than a stretched valuation, and the timing risk here is more about continued downside momentum than about buying into an overheated price.
  - source: [D-Wave Quantum (QBTS) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QBTS&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T7]** *(verified_fact, confidence medium)* Quantinuum (QNT) is down 33.6% over 3 months and 13.4% below its 50-day average, and carries the highest measured volatility in the group at 134.1% annualised (20-day).
  - source: [Quantinuum Inc. (QNT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QNT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -33.6%. Price vs 50-day average -13.4%. 20-day annualised volatility 134.1%."
- **[T8]** *(ai_interpretation, confidence medium)* QNT's subdued timing-risk reading reflects the pullback, but volatility of 134% annualised means price levels can change materially within days; the short 100-day window limits how much the drawdown tells us about longer-term positioning.
  - source: [Quantinuum Inc. (QNT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QNT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T9]** *(verified_fact, confidence medium)* Xanadu (XNDU) has fallen 74.7% over 3 months and trades 50.0% below its 50-day average and 81.6% below its 100-day high, with 115.2% annualised volatility.
  - source: [Xanadu Quantum Technologies Ltd (XNDU) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=XNDU&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -74.7%. Price vs 50-day average -50.0%."
- **[T10]** *(ai_interpretation, confidence medium)* XNDU's decline is far larger than the rest of the theme; a price 50% below its 50-day average is an unusual statistical deviation that can indicate company- or stock-specific stress beyond the theme-wide pullback, warranting investigation of causes before drawing timing conclusions.
  - source: [Xanadu Quantum Technologies Ltd (XNDU) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=XNDU&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T11]** *(ai_interpretation, confidence medium)* Cross-company: all five quantum-error-correction-linked stocks show subdued rule-based timing risk — every one is below its 50-day average and down over 3 months — so the theme as a whole is in a drawdown phase rather than a run-up phase, but all carry 20-day annualised volatility above 100%.
  - source: [Rigetti Computing (RGTI) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RGTI&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [IonQ (IONQ) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IONQ&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [D-Wave Quantum (QBTS) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QBTS&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Quantinuum Inc. (QNT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QNT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Xanadu Quantum Technologies Ltd (XNDU) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=XNDU&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)

**Limitations:**
- The ~100-trading-day window is short; drawdown and volatility readings may not reflect longer-term positioning of these stocks.
- Analysis uses price metrics only — no fundamentals, valuation, or company-specific news are considered, and prices may have moved for reasons unrelated to quantum error correction.
- 'Subdued' timing risk describes the absence of recent run-up, not an expectation of recovery; past prices do not predict future prices.
- Volatility above 100% annualised for all five names means any timing assessment can become stale within days.
- Rule-based timing labels are heuristic and not a substitute for full risk analysis.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 7 distinct company names from 0 patent publications, 4 company-affiliated papers and 5 SEC filers; 5 matched to the SEC ticker file (2 outside the configured list), 2 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Quantinuum Inc. (QNT) · Services-Computer Integrated Systems Design | 0 | 0 | 1 | n/a | n/a | n/a | **20** |
| Xanadu Quantum Technologies Ltd (XNDU) · Electronic Computers | 0 | 0 | 1 | n/a | n/a | n/a | **20** |

- Quantinuum Inc.: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); size unknown from SEC XBRL (+5, neutral)
- Xanadu Quantum Technologies Ltd: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); size unknown from SEC XBRL (+5, neutral)

**Configured incumbents that also showed up:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Rigetti Computing (RGTI) | 0 | 0 | 2 | micro: 0.01B USD | +59.9% | 457.6% | **55** |
| IonQ (IONQ) | 0 | 0 | 1 | small: 0.13B USD | +201.9% | 235.1% | **50** |
| D-Wave Quantum (QBTS) | 0 | 0 | 1 | micro: 0.02B USD | +178.5% | 206.3% | **50** |

**Found but not in the SEC ticker file (private, foreign, or name not matched):** Google (United States) (0P/4A/0F), Google DeepMind (United Kingdom) (0P/1A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* Quantinuum Inc. (QNT) is active on quantum error correction: 1 of its SEC report(s) mention the topic. Next-runner score 20/100 (heuristic).
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Xanadu Quantum Technologies Ltd (XNDU) is active on quantum error correction: 1 of its SEC report(s) mention the topic. Next-runner score 20/100 (heuristic).
  - source: [Xanadu Quantum Technologies Ltd Form 20-F, filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) (SEC EDGAR, 2026-04-09, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [Rigetti Computing (RGTI) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RGTI&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_9cf244422f
- [IonQ (IONQ) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IONQ&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_d1ccdce8a2
- [D-Wave Quantum (QBTS) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QBTS&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_90f4865172
- [Quantinuum Inc. (QNT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QNT&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_0507e3a3ca
- [Xanadu Quantum Technologies Ltd (XNDU) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=XNDU&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_456f2181c2
- [Error Correction Is a Landauer Machine: The Thermodynamic Floor of Quantum Error-Correction Overhead](https://doi.org/10.5281/zenodo.22115862) | OpenAlex | 2026-08-26 | retrieved 2026-11-09 | abstract_only | id src_0df71ca0a9
- [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) | SEC EDGAR | 2026-08-13 | retrieved 2026-11-09 | excerpt_only | id src_bf91003520
- [Rigetti Computing, Inc. Form 10-Q, filed 2026-08-06](https://www.sec.gov/Archives/edgar/data/1838359/000110465926091993/rgti-20260630x10q.htm) | SEC EDGAR | 2026-08-06 | retrieved 2026-11-09 | excerpt_only | id src_20458a699c
- [Quantum error correction at ultra-low overhead](https://doi.org/10.48550/arxiv.2608.02773) | OpenAlex | 2026-08-03 | retrieved 2026-11-09 | abstract_only | id src_43430297cb
- [Surface-Code Overhead Tech4Biz Solutions A Lightweight, Exact, and Reproducible Calculator for Surface-Code Quantum Error Correction Overhead](https://doi.org/10.13140/rg.2.2.21425.95846) | OpenAlex | 2026-07-12 | retrieved 2026-11-09 | metadata_only | id src_c9bb5e9898
- [Approximate quantum error correction theory of non-isometric codes](https://arxiv.org/abs/2606.13559v1) | arXiv | 2026-06-11 | retrieved 2026-11-09 | abstract_only | id src_7c1902090a
- [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) | arXiv | 2026-05-16 | retrieved 2026-11-09 | abstract_only | id src_844afd8b30
- [Xanadu Quantum Technologies Ltd Form 20-F, filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) | SEC EDGAR | 2026-04-09 | retrieved 2026-11-09 | excerpt_only | id src_b80a7885a6
- [Low-Overhead Quantum Error Correction Codes for Noisy Intermediate-Scale Quantum Devices](https://doi.org/10.1051/epjconf/202636001013/pdf) | OpenAlex | 2026-03-23 | retrieved 2026-11-09 | abstract_only | id src_020cace84d
- [Rigetti Computing, Inc. Form 10-K, filed 2026-03-04](https://www.sec.gov/Archives/edgar/data/1838359/000110465926023454/rgti-20251231x10k.htm) | SEC EDGAR | 2026-03-04 | retrieved 2026-11-09 | excerpt_only | id src_22473e9149
- [D-Wave Quantum Inc. Form 10-K, filed 2026-02-26](https://www.sec.gov/Archives/edgar/data/1907982/000190798226000026/qbts-20251231.htm) | SEC EDGAR | 2026-02-26 | retrieved 2026-11-09 | excerpt_only | id src_c7a34f495b
- [Ionq, Inc. Form 10-K, filed 2026-02-25](https://www.sec.gov/Archives/edgar/data/1824920/000119312526071562/ionq-20251231.htm) | SEC EDGAR | 2026-02-25 | retrieved 2026-11-09 | excerpt_only | id src_475cac8770
- [Demonstration of low-overhead quantum error correction codes](https://doi.org/10.1038/s41567-025-03157-4) | OpenAlex | 2026-01-22 | retrieved 2026-11-09 | metadata_only | id src_0192635a40
- [Thermodynamic Recycling of Algorithmic Failure Branches: Quantum-Computer Demonstration with Quantum Error Correction](https://arxiv.org/abs/2601.07522v2) | arXiv | 2026-01-12 | retrieved 2026-11-09 | abstract_only | id src_800ebaba67
- [Multiqubit Rydberg Gates for Quantum Error Correction](https://arxiv.org/abs/2512.00843v2) | arXiv | 2025-11-30 | retrieved 2026-11-09 | abstract_only | id src_c56bc32c98
- [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) | arXiv | 2025-08-31 | retrieved 2026-11-09 | abstract_only | id src_c0058675c2
- [Quantum error correction of qudits beyond break-even](https://doi.org/10.1038/s41586-025-08899-y) | OpenAlex | 2025-05-14 | retrieved 2026-11-09 | abstract_only | id src_97a5bbcd85
- [Simulation and Design of Quantum Processors for Low‑Overhead Quantum Error Correction](https://hdl.handle.net/1721.1/163685) | OpenAlex | 2025-05-01 | retrieved 2026-11-09 | abstract_only | id src_ec87473193
- [Calibration and Control of Superconducting Qubits for Low‑Overhead Quantum Error Correction](https://hdl.handle.net/1721.1/163676) | OpenAlex | 2025-05-01 | retrieved 2026-11-09 | abstract_only | id src_c050153b28
- [Quantum Error Correction in Quaternionic Hilbert Spaces](https://arxiv.org/abs/2504.19833v1) | arXiv | 2025-04-28 | retrieved 2026-11-09 | abstract_only | id src_afb5833d56
- [Quantum Prometheus: Defying Overhead with Recycled Ancillas in Quantum Error Correction](https://doi.org/10.1109/isqed65160.2025.11014328) | OpenAlex | 2025-04-23 | retrieved 2026-11-09 | abstract_only | id src_93b8f532fe
- [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) | arXiv | 2025-04-10 | retrieved 2026-11-09 | abstract_only | id src_90875088aa
- [Reducing quantum error correction overhead using soft information](https://arxiv.org/abs/2504.03504v3) | arXiv | 2025-04-04 | retrieved 2026-11-09 | abstract_only | id src_905c50a9ad
- [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) | OpenAlex | 2024-12-09 | retrieved 2026-11-09 | abstract_only | id src_9f4129c761
- [Reducing Quantum Error Correction Overhead with Versatile Flag-Sharing Syndrome Extraction Circuits](https://arxiv.org/abs/2407.00607v1) | arXiv | 2024-06-30 | retrieved 2026-11-09 | abstract_only | id src_aebf5c7a43
- [Overcoming leakage in quantum error correction](https://doi.org/10.1038/s41567-023-02226-w) | OpenAlex | 2023-10-05 | retrieved 2026-11-09 | abstract_only | id src_7c98bcb9a8
- [Quantum Error Correction For Dummies](https://doi.org/10.1109/qce57702.2023.00017) | OpenAlex | 2023-09-17 | retrieved 2026-11-09 | abstract_only | id src_fff72088a9
- [Introduction to quantum error correction and fault tolerance](https://doi.org/10.21468/scipostphyslectnotes.70) | OpenAlex | 2023-06-12 | retrieved 2026-11-09 | abstract_only | id src_789d3ecd8d
- [Quantum error correction with gauge symmetries](https://doi.org/10.1038/s41534-023-00706-8) | OpenAlex | 2023-04-25 | retrieved 2026-11-09 | abstract_only | id src_28c1bcb706
- [Stabilizer Formalism for Operator Algebra Quantum Error Correction](https://arxiv.org/abs/2304.11442v2) | arXiv | 2023-04-22 | retrieved 2026-11-09 | abstract_only | id src_d2b8ad6673
- [Real-time quantum error correction beyond break-even](https://doi.org/10.1038/s41586-023-05782-6) | OpenAlex | 2023-03-22 | retrieved 2026-11-09 | metadata_only | id src_3ee790e4ad
- [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) | OpenAlex | 2023-03-09 | retrieved 2026-11-09 | abstract_only | id src_31eadc54ac
- [A lower bound on the overhead of quantum error correction in low dimensions](https://doi.org/10.48550/arxiv.2302.04317) | OpenAlex | 2023-02-08 | retrieved 2026-11-09 | abstract_only | id src_631d3a610f

## Gaps, limitations and errors
- Missing data: Patent evidence: the patent agent did not run, so there is no assignee, filing-trend or geography data and patent_momentum cannot be rated.
- Missing data: Social/X evidence: the X agent did not run, so there are no company, standards-body or press posts from the last 7 days and no catalyst signal from that source.
- Missing data: Independent verification: no finding reports third-party replication of the below-threshold result (S1) or of the disputed low-overhead claims (R6).
- Missing data: Hardware-in-the-loop decoder data: no finding shows a machine-learning decoder running live on hardware below the code cycle time (C4).
- Missing data: Customer and commercial evidence: no named customer, contract, order book, price or revenue attributable to quantum error correction appears in any finding.
- Missing data: Dollar figures for QEC-specific R&D spend; findings state direction (rising R&D) but no amounts (M2).
- Missing data: IBM and Honeywell: their retrieved filings did not mention the QEC keywords, so this analysis has no direct filing evidence of their QEC activity, and absence from the excerpts is not absence from the market (M9).
- Missing data: Cause of the extreme price deviation in Xanadu (50% below its 50-day average, -74.7% over three months): no finding explains it (T10).
- Missing data: No evidence on cryogenics, fabrication supply chains or component availability.
- Limitation: Assessment is based on abstracts and filing excerpts; several cited sources have no abstract at all (C1, C7), which caps how much can be concluded from them.
- Limitation: Several science findings labelled verified_fact are shown by the Risk challenges to overstate their sources (C1, C2, C4, C5, C6, C7); this report reflects the challenged reading rather than the original labels.
- Limitation: Market findings are short passages from annual/quarterly reports plus news headlines; headline-based items such as the D-Wave claim are unverified and given little weight.
- Limitation: Publication counts use the exact phrase 'quantum error correction' only, are not normalised for overall publishing growth, exclude synonyms and abbreviations, and the current year is partial.
- Limitation: Price and timing findings cover only about 100 trading days for five stocks and are used solely as risk context, never as entry points, timing signals or price expectations.
- Limitation: Company Scout next-runner scores are code-computed heuristics, not predictions of returns, and two of the listed names are small with limited disclosure.
- Limitation: No patent or social evidence exists in this version, so any conclusion about intellectual-property positioning or market sentiment would be unsupported.
- Limitation: No valuation, financial-statement or balance-sheet analysis was performed; nothing here is a recommendation or a forecast of returns.
- Chief review gap: No dedicated science finding on quantum LDPC code performance or recent constant-overhead results; the planned query 'quantum LDPC codes' appears not to have yielded a relevant paper in the retrieved set, yet qLDPC is a major theoretical advance that could reshape the overhead picture
- Chief review gap: Patent agent was not run: no IP landscape, freedom-to-operate, or code-family patent positioning available
- Chief review gap: X agent was not run: no community or researcher sentiment signals to complement the filing-based market picture
- Chief review gap: No systematic comparison of logical error thresholds across code families (surface code vs. qLDPC vs. bosonic) under comparable noise models
- Chief review gap: Real-time decoding coverage is limited to one low-confidence finding (Sparse Mamba); no evidence on FPGA or cryogenic decoder implementations at scale
- Chief review gap: No evidence on fault-tolerant logical gate demonstrations (e.g., logical CNOT, logical T gates) beyond logical memory; the field's next milestone after below-threshold storage is not directly covered by retrieved papers.
- Chief review gap: Patent agent was not run, so IP landscape, freedom-to-operate, and competitive moat analysis are absent; this cannot be filled by paper search.
- Chief review gap: X/social agent was not run, so no community sentiment or expert commentary signals are available.
- Chief review gap: No direct cross-platform comparison of logical error rates or overhead between superconducting, trapped-ion, bosonic, and neutral-atom QEC implementations.
- Chief review gap: Several retrieved papers are peripheral to the core topic (quaternionic QEC, thermodynamic recycling, gauge symmetries, 'QEC for Dummies'), diluting the signal-to-noise ratio of the paper set.
- Reference checks changed 1 statement(s) in the assessment (see notes in italics above).
- ERROR [patent/Google Patents (SerpApi)]: counts: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [patent/Google Patents (SerpApi)]: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 3 | 9047 | 4033 | 0.00578 |
| market | z-ai/glm-5.3 | 1 | 3575 | 1887 | 0.01564 |
| science | deepseek/deepseek-v4.1-flash | 2 | 10029 | 8749 | 0.01351 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 23616 | 9265 | 0.13988 |
| timing | z-ai/glm-5.3-flash | 1 | 1701 | 1277 | 0.00077 |
| investment | deepseek/deepseek-v4.1-flash | 1 | 8546 | 9606 | 0.01349 |
| investment (rescore) | deepseek/deepseek-v4.1-flash | 1 | 8907 | 9958 | 0.01203 |

Total estimated cost: $0.20111 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
