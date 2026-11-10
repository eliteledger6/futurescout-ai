# FUTURESCOUT AI research report: quantum error correction

Generated: 2026-11-10 04:21 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, x, patent, scout, investment

## Verdict (forecast, computed from the report)
**Building: real activity, not yet proven commercially** — score 67.7, confidence low.
Qualifiers: low confidence 28%, below the 70% that counts as confident; high risk flagged by the Risk agent; research is running well ahead of commercial reality.

Quantum error correction is a way of protecting fragile quantum computers from the mistakes they constantly make, and it is needed before they can do useful work. Scientific papers and patents on it are growing very fast, and one laboratory test showed errors can be reduced as the system grows. The big question is…

Why:
- Research Momentum rated 5/5: Code-computed counts of works rose from 703 (2024) to 1,383 (2025), +96.7%, and 2026 year-to-date is 3,538 versus 945 a year earlier, a rising trend.
- Patent Momentum rated 4/5: Publications grew from 1,399 (2024) to 2,271 (2025), +62.3%, and 2,544 so far in 2026 versus 1,585 at the same date in 2025.
- Papers 2024→2025: 703→1383 (+97%)
- So far in 2026 (to 10-11): 3538 papers vs 945 by the same date in 2025 (+274%, rising)

Watch out for:
- Rare correlated error events, about once per hour in repetition codes, may limit logical performance at scale.
- Photon loss has not yet met required levels in Xanadu's architecture, and fault tolerance at scale is described by companies as scientifically and technically uncertain.
- The patent search returns many classical 'fault-tolerant' filings, so patent counts may overstate quantum-specific activity.
- Social-media performance claims (20% improvements) are preliminary and unverified.

What would change this view:
- Stronger if: Logical-gate (not just memory) demonstrations below threshold at distance greater than 7, with real-time decoding at the same distance.
- Weaker if: Larger-distance surface-code experiments show logical error suppression stalling or reversing, for example because of correlated errors or leakage.
- Stronger if: Peer-reviewed, hardware-based benchmarks of neural decoders at distance greater than 5 with real-time latency.
- Weaker if: Hardware benchmarks show learned decoders offer no real advantage over established decoders under real noise.

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
Research on quantum error correction is accelerating sharply: the OpenAlex count rose from 703 works in 2024 to 1,383 in 2025 (+96.7%), and 2026 year-to-date is 3,538 against 945 at the same point of 2025. Patent publications are also rising, though the patent search picks up classical 'fault-tolerant' patents, so that signal is noisy [P4]. The strongest experimental evidence is a superconducting surface-code memory operated below threshold and beyond break-even [S1, S2]. The Risk agent's challenges limit what this shows: it is a memory only, has no logical gates, and the suppression factor is modest [C1]. Structural overhead and connectivity limits remain open [R1, R2, C6]. Company evidence is mostly roadmaps and unverified claims, with Quantinuum targeting up to 100 logical qubits in 2027 [M2] and Xanadu having demonstrated only twelve [M4]. The main uncertainty is whether laboratory below-threshold results can scale to useful fault-tolerant machines at acceptable qubit cost and on a commercially relevant timeline. Research activity is not evidence of commercial success.

## Technology Opportunity Score
**Opportunity score: 67.7 / 100** · **Confidence: 28%** (low; evidence 46% x risk multiplier 0.6) · evidence coverage 65%

Risk: rating 4/5 does not change the score; it multiplies confidence by 0.6.

Commercialization Gap (research momentum rating minus commercial readiness rating): +3


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S3, S4, S7, S8 | Code-computed counts of works rose from 703 (2024) to 1,383 (2025), +96.7%, and 2026 year-to-date is 3,538 versus 945 a year earlier, a rising trend. The counts are not normalised for overall publishing growth. Experimental and theoretical work covers multiple directions [S1, S3, S4, S7, S8]. Research activity does not equal commercial success. |
| Patent Momentum | 10% | 4 | P1, P2, P3, P4, P5 | Publications grew from 1,399 (2024) to 2,271 (2025), +62.3%, and 2,544 so far in 2026 versus 1,585 at the same date in 2025. Applications focus on decoders, surface codes, hardware noise management and fault-tolerant protocols [P1, P2, P3, P5]. The search includes classical 'fault-tolerant' patents, so counts overstate quantum-specific filings [P4]. Applications are claims, not proof. |
| Technical Feasibility | 15% | 3 | S1, S2, S3, S4, C1, C2, R1, R2, C6, M5 | Below-threshold memory, beyond break-even operation and leakage containment are experimentally shown [S1, S2, S3, S4]. These are memory-only, small-scale results with a modest suppression factor and correlated-error limits [C1, C2]. Structural overhead and connectivity limits remain [R1, R2, C6], and fault tolerance at scale is described by companies as uncertain [M5]. |
| Commercial Readiness | 15% | 2 | M2, M3, M4, M5, X7 | Company evidence is largely forward-looking: Quantinuum's Sol (2027) and Apollo (2029) are expectations [M2], Xanadu has twelve logical qubits and unresolved photon loss [M4], and both describe scaling as uncertain [M5]. Quantinuum names logical-qubit metrics as drivers of adoption [M3], which is a framing and not evidence of sales. Revenue growth is reported only through an unverified post [X7]. |
| Customer Adoption | 10% | missing | none | no valid 0-5 rating given |
| Industry Investment | 10% | 3 | P1, M2, X1, X2, X8 | Major technology firms and startups file patents on error correction [P1], and company roadmaps target logical-qubit milestones [M2]. An AMD/IBM/ORNL co-design platform and a €9.1M funding round for Quint Computing are reported only through unverified posts or headlines [X1, X2, X8]. Actual spending levels are not evidenced. |
| Competitive Position | 10% | missing | none | no valid 0-5 rating given |
| Supply-Chain Readiness | 15% | missing | none | no valid 0-5 rating given |

Formula: score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a validated prediction of stock performance; confidence is not a probability of profit.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Surface-code and bosonic logical-qubit demonstrations moving toward fault tolerance

Technologies: surface code, superconducting qubits, leakage mitigation, GKP bosonic codes, real-time decoding

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Experiments show below-threshold memory, beyond break-even operation, tenfold leakage reduction and beyond break-even qudits [S1, S2, S3, S4]. They are small-scale memory demonstrations without logical gates, and the correlated-error and scale caveats remain [C1, C2]. Vendor claims of logical-qubit milestones are company statements, and the X-reported earnings figures are unverified [M1, X7]. Expect incremental demonstrations rather than useful fault-tolerant computation. *(forecast)* [S1, S2, S3, S4, C1, C2, M1, X7] | medium |
| medium_1_3y | Quantinuum states it expects Sol in 2027 with up to 100 logical qubits, an unverified company expectation [M2]. Both Quantinuum and Xanadu describe fault tolerance at scale as subject to substantial scientific and engineering uncertainty [M5]. Xanadu has so far shown twelve logical qubits and has unresolved photon loss [M4]. The evidence does not show whether these roadmaps will be met. *(forecast)* [M2, M4, M5] | low |
| long_3_5y | Quantinuum's Apollo (hundreds of logical qubits, 2029) is a company target only [M2]. The authors of the below-threshold result say large-scale requirements would be met only 'if scaled' [C1]. A proven 2D locality overhead bound and connectivity trade-offs create structural headwinds [R1, R2, C6]. The evidence cannot support a confident long-term view. *(forecast)* [M2, C1, R1, R2, C6] | low |

**Bull case:** Below-threshold scaling, leakage control and bosonic beyond break-even results compound into logical-gate demonstrations. Vendor roadmaps to tens and then hundreds of logical qubits are met, and fault-tolerant machines gain commercial traction. *(forecast)* [S1, S2, S3, S4, M2]

**Base case:** Laboratory progress continues with modest suppression factors and small logical-qubit counts. Real-time decoding and leakage handling improve, but scaling cost and engineering uncertainty slow commercial milestones, consistent with company risk disclosures. *(forecast)* [S1, C1, C2, M4, M5]

**Bear case:** Rare correlated errors, leakage at larger distances and the overhead growth of locality-limited architectures prevent practical scaling. Company roadmaps slip, and demonstrations remain memories rather than computers. *(forecast)* [C1, C2, R1, C6, M5]

**Catalysts:**
- Logical-gate (not just memory) demonstrations below threshold at distance greater than 7, with real-time decoding at the same distance. *(forecast)* [C1, S1, S2]
- Delivery of Quantinuum's stated 2027 Sol milestone, which is currently only a company expectation. *(forecast)* [M2]
- Independent confirmation that leakage removal restores exponential logical suppression in larger surface codes. *(forecast)* [S3, C2]

**Risks:**
- Rare correlated error events, about once per hour in repetition codes, may limit logical performance at scale. *(ai_interpretation)* [C1]
- Photon loss has not yet met required levels in Xanadu's architecture, and fault tolerance at scale is described by companies as scientifically and technically uncertain. *(ai_interpretation)* [M4, M5]
- Locality-limited 2D error correction has a proven space overhead that grows with system size. *(ai_interpretation)* [R1]

**What would invalidate this thesis:**
- Larger-distance surface-code experiments show logical error suppression stalling or reversing, for example because of correlated errors or leakage. *(forecast)* [C1, C2]
- Major vendors withdraw or substantially delay logical-qubit roadmaps citing error-correction limits. *(forecast)* [M2, M5]

**Conflicting evidence:**
- S1/S2 present below-threshold, beyond-break-even results, but C1 notes the result is a memory only, Λ=2.14 is modest, real-time decoding was at distance-5 rather than 7, and scalability is conditional. *(ai_interpretation)* [S1, S2, C1]
- S3 reads as leakage largely solved, but C2 notes the demonstration is small-scale and does not show restored exponential suppression in a larger surface code. *(ai_interpretation)* [S3, C2]

**Companies named by cited evidence:**
- Quantinuum Inc. (QNT): SEC 10-Q states it was first to show logical qubits more accurate than physical ones and targets Sol (2027) and Apollo (2029); the roadmap is an unverified company expectation. Cash losses reported only via an unverified social post. [M1, M2, K2, X7]
- Xanadu Quantum Technologies (XNDU): Has demonstrated only twelve logical qubits, with photon loss not yet at required levels; 1 patent as assignee and a 20-F mention. Smaller company with higher risk. [M4, K1]
- Google: Named by the scout as an assignee/author affiliation (2 patents, 4 papers). The cited below-threshold paper is the one reviewed in S1, but the findings do not name the authors' employer. [K1]

### Decoding, noise modelling and HPC co-design software layer

Technologies: real-time decoders, neural/ML decoders, detector error models, HPC-quantum co-design

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Patent applications concentrate on decoding and detector error modelling [P1, P2], and AMD, IBM and ORNL announced a co-design platform for error correction, an unverified social-media claim [X1, X2, X5]. Reported 20% gains from Riverlane and Quantum X Labs are preliminary and unverified [X3, X4]. ML decoder gains are mostly simulation, and there is only one preprint behind the 'trend' [S5, C3]. Activity is real but the performance evidence is thin. *(forecast)* [P1, P2, X1, X2, X5, X3, X4, S5, C3] | low |
| medium_1_3y | Real-time decoding at 63 µs average latency has been shown at distance-5 [S2], and patent filings address the decoder bottleneck [P2]. Whether ML decoders hold their simulated gains on real hardware is unproven, since on the only experimental dataset the new decoder only matched an existing one [C3]. The evidence does not show who captures value. *(forecast)* [S2, P2, C3] | low |
| long_3_5y | The evidence says nothing direct about the 3-5 year position of decoding software. Machine learning is also being applied to discover noise-adapted codes, but only in simulation [S6, C4]. No supported long-term conclusion. *(forecast)* [S6, C4] | low |

**Bull case:** Decoders and noise models prove portable across hardware and keep up with real-time latency at larger distances, making the software layer a bottleneck-removing component with industry co-design backing. *(forecast)* [S2, S5, P2, X1]

**Base case:** Decoder and noise-model patenting and preprints keep growing, with incremental real-hardware gains. Simulation advantages partly erode on real device noise. *(forecast)* [P1, P2, C3, R5]

**Bear case:** Simulated decoder advantages do not carry over to experimental noise, and the co-design announcements produce no measurable benefit. Value accrues to hardware makers rather than software suppliers. *(forecast)* [C3, R5, X5]

**Catalysts:**
- Peer-reviewed, hardware-based benchmarks of neural decoders at distance greater than 5 with real-time latency. *(forecast)* [S5, C3, S2]
- Published results from the AMD/IBM/ORNL co-design platform, currently only announced. *(forecast)* [X1, X2]

**Risks:**
- The patent search returns many classical 'fault-tolerant' filings, so patent counts may overstate quantum-specific activity. *(ai_interpretation)* [P4]
- Social-media performance claims (20% improvements) are preliminary and unverified. *(unverified_claim)* [X3, X4]

**What would invalidate this thesis:**
- Hardware benchmarks show learned decoders offer no real advantage over established decoders under real noise. *(forecast)* [C3]

**Conflicting evidence:**
- S5 calls neural decoders 'a clearly emerging direction', but C3 notes this rests on one non-peer-reviewed preprint, with simulation gains and only parity on experimental data. Patent filings do show decoder interest [P2]. *(ai_interpretation)* [S5, C3, P2]

**Companies named by cited evidence:**
- AMD: Announced a co-design platform with IBM and ORNL for error correction, per its own social posts; an unverified announcement, with no evidence yet of results. [X1, X5]
- IBM: Named in the co-design announcement and by the scout with 2 patents as assignee; not SEC-financial-checked here. [X2, K1]
- Riverlane: Reportedly achieved a 20% improvement using data-driven error models, per one social post; unverified. [X3]
- Dell Technologies (DELL): 1 retrieved patent as assignee (adaptive canary qubit noise mapping); very large company where quantum is unlikely to be a main driver. Its filings are not shown to mention the topic. [K3, P3, M7]

### Low-overhead codes (qLDPC, hyperbolic, bosonic) and the scaling-cost problem

Technologies: qLDPC codes, hyperbolic codes, hardware-efficient/continuous-variable QEC, magic-state distillation, neutral-atom architectures

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Overhead-reduction claims are mostly simulation and narrow in scope [R5], and hyperbolic and autoencoder results lack hardware validation [C4]. Headline qLDPC error rates are extrapolated and platform-specific [R3]. Expect papers and patents, not deployed low-overhead systems. *(forecast)* [R5, C4, R3] | medium |
| medium_1_3y | qLDPC codes need dense long-range connectivity that is hard to build, and routing workarounds roughly double circuit depth [R2]. Magic-state distillation remains a major overhead, with alternatives shown only numerically [R6]. Patents describe distillation and logical-gate protocols [P5], but the evidence does not show whether any of this reaches hardware in this window. *(forecast)* [R2, R6, P5] | low |
| long_3_5y | A proven lower bound says local 2D QEC overhead grows with system size [R1], so progress depends on non-local or alternative architectures that are unproven at scale [R2, R3]. The evidence does not allow a confident long-term view. *(forecast)* [R1, R2, R3] | low |

**Bull case:** Low-overhead or hardware-efficient codes are demonstrated on hardware and cut the physical qubits per logical qubit substantially, making large systems practical sooner than the surface-code path alone implies. *(forecast)* [S7, S10, R3, R5]

**Base case:** Overhead reductions are real but modest and platform-specific, and connectivity and distillation costs keep scaling expensive. *(forecast)* [R2, R5, R6]

**Bear case:** Simulation gains vanish under real noise and connectivity constraints, so overhead remains prohibitive for locality-limited architectures. *(forecast)* [R1, R2, R5, C6]

**Catalysts:**
- Experimental demonstration of a high-rate qLDPC code on hardware, measuring rather than extrapolating logical error rates. *(forecast)* [R3]
- A hardware demonstration of a cheaper non-Clifford gate than magic-state distillation. *(forecast)* [R6]

**Risks:**
- Results often depend on one hardware platform and its control stack. *(ai_interpretation)* [R3]
- Crosstalk from parallel gates can raise the needed code distance and therefore qubit cost. *(ai_interpretation)* [R4]

**What would invalidate this thesis:**
- Hardware experiments show that simulated overhead savings do not survive real-device noise and connectivity limits. *(forecast)* [R5, R2]

**Conflicting evidence:**
- Review literature points to hardware-efficient directions [S10], but C5 notes this rests on one source from a 2019 summer-school lecture, not a surveyed consensus. S7's lower-overhead hyperbolic claims are simulation only [C4]. *(ai_interpretation)* [S10, C5, S7, C4]

**Companies named by cited evidence:**
- Pasqal Holding SA (PSQL): 1 retrieved patent as assignee (multiple rounds of error correction); its filings do not mention the topic keywords, so no commercial activity can be inferred. Smaller company with higher risk and less disclosure. [K4, M7]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 382, 2021: 424, 2022: 447, 2023: 517, 2024: 703, 2025: 1383, 2026: 3956}
Research Acceleration 2024->2025: 703 -> 1383 (96.7% YoY). OpenAlex works whose title or abstract contains any of the exact phrases "quantum error correction", "quantum error-correcting codes", "stabilizer codes", "surface code", per publication year (singular and plural forms match; each work counted once). The synonyms and abbreviations were kept only after an AI check of sampled papers. The number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-11): 2025 945 -> 2026 3538 (274.4%, trend: rising). OpenAlex works with any of the exact phrases "quantum error correction", "quantum error-correcting codes", "stabilizer codes", "surface code" in title or abstract published 1 Jan–11 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence medium)* A superconducting surface-code memory has been operated below the error-correction threshold, with logical error rate suppressed as code distance increases and with a 101-qubit distance-7 code reaching 0.143% ± 0.003% error per cycle.
  - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
  - excerpt: "culminating in a 101-qubit distance-7 code with 0.143% ± 0.003% error per cycle of error correction"
- **[S2]** *(verified_fact, confidence medium)* The logical memory in that system exceeds the lifetime of its best physical qubit (beyond break-even) by a factor of 2.4 ± 0.3 and maintains below-threshold performance under real-time decoding with 63 µs average decoder latency at distance-5.
  - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
  - excerpt: "This logical memory is also beyond break-even, exceeding its best physical qubit’s lifetime by a factor of $$2.4\pm 0.3$$"
- **[S3]** *(verified_fact, confidence medium)* Leakage out of the computational states, a major source of correlated errors for QEC, was experimentally contained by removing leakage from all qubits each cycle, yielding a tenfold reduction in steady-state leakage population.
  - source: [Overcoming leakage in quantum error correction](https://doi.org/10.1038/s41567-023-02226-w) (OpenAlex, 2023-10-05, abstract_only)
  - excerpt: "We report a tenfold reduction in the steady-state leakage population of the data qubits encoding the logical state and an average leakage population of less than 1 × 10 −3 throughout the entire device."
- **[S4]** *(verified_fact, confidence medium)* Error-corrected logical qudits (qutrit d=3 and ququart d=4) have been experimentally realized with a bosonic Gottesman–Kitaev–Preskill code, achieving beyond break-even operation.
  - source: [Quantum error correction of qudits beyond break-even](https://doi.org/10.1038/s41586-025-08899-y) (OpenAlex, 2025-05-14, abstract_only)
  - excerpt: "achieved beyond break-even error correction with a gain of 1.82 ± 0.03 (1.87 ± 0.03)"
- **[S5]** *(ai_interpretation, confidence low)* Data-driven and neural decoders are a clearly emerging direction, with claims of defect-centric sparse processing achieving lower logical error rates than minimum-weight matching and large runtime speedups over near-maximum-likelihood decoders.
  - source: [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) (arXiv, 2026-05-16, abstract_only)
  - reasoning: Single arXiv preprint (not peer reviewed); reported numbers concern specific noise models and code distances so cannot be generalized to all decoders.
- **[S6]** *(verified_fact, confidence low)* Machine learning is being applied not only to decoding but to discovering new logical encodings adapted to a device's underlying noise, with quantum autoencoders claimed to extend logical-qubit lifetime even when the autoencoders themselves are noisy.
  - source: [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) (OpenAlex, 2023-03-09, abstract_only)
  - excerpt: "We also show that quantum neural networks can be used to discover new logical encodings that are optimally adapted to the underlying noise."
- **[S7]** *(verified_fact, confidence low)* Alternative code geometries beyond the standard Euclidean surface code are being pursued, including hyperbolic lattices claimed to offer higher encoding rates and lower qubit overhead, with a unified graph-theoretic framework proposed for their systematic benchmarking.
  - source: [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) (arXiv, 2025-04-10, abstract_only)
  - excerpt: "these codes achieve higher encoding rates and lower qubit overhead compared to those defined on conventional Euclidean lattices"
- **[S8]** *(verified_fact, confidence low)* Theoretical work is formalizing the limits of non-isometric encodings (relevant to continuous-variable codes and holography) using the approximate quantum error correction framework, applied to GKP and tiger codes under energy constraints.
  - source: [Approximate quantum error correction theory of non-isometric codes](https://arxiv.org/abs/2606.13559v1) (arXiv, 2026-06-11, abstract_only)
  - excerpt: "we employ the approximate quantum error correction framework to quantitatively study the fundamental limitations imposed by non-isometric encodings on the accuracy of quantum error correction"
- **[S9]** *(ai_interpretation, confidence low)* Several mathematically unconventional QEC proposals have appeared (quaternionic Hilbert-space codes, thermodynamic recycling of algorithm failure branches), but these are single-source, non-peer-reviewed preprints making performance claims that are not independently corroborated here.
  - source: [Quantum Error Correction in Quaternionic Hilbert Spaces](https://arxiv.org/abs/2504.19833v1) (arXiv, 2025-04-28, abstract_only)
  - source: [Thermodynamic Recycling of Algorithmic Failure Branches: Quantum-Computer Demonstration with Quantum Error Correction](https://arxiv.org/abs/2601.07522v2) (arXiv, 2026-01-12, abstract_only)
  - reasoning: Both are arXiv preprints without independent replication in this set; the quaternionic threshold and Landauer-limit claims are abstract-level only.
- **[S10]** *(ai_interpretation, confidence medium)* A recurring theme across the review/tutorial literature is the goal of 'hardware-efficient' QEC that avoids exponentially large hardware overhead, with continuous-variable and modular superconducting-photon architectures highlighted as near-term practical directions.
  - source: [Introduction to quantum error correction and fault tolerance](https://doi.org/10.21468/scipostphyslectnotes.70) (OpenAlex, 2023-06-12, abstract_only)
  - source: [Quantum Error Correction For Dummies](https://doi.org/10.1109/qce57702.2023.00017) (OpenAlex, 2023-09-17, abstract_only)
  - reasoning: Two independent review-style sources point the same way; both are secondary/overview material rather than new experimental results.

**Emerging directions:**
- Defect-centric sparse neural decoders for real-time, low-latency decoding
- Machine-learned and autoencoder-based discovery of noise-adapted encodings
- Bosonic/qudit logical memories (GKP qutrit and ququart) beyond break-even
- Codes on hyperbolic lattices and generalized CSS benchmarking frameworks
- Approximate QEC theory for non-isometric and energy-constrained continuous-variable codes
- Leakage removal as a routine per-cycle operation
- Unconventional mathematical frameworks for QEC (quaternionic Hilbert spaces)
- Coupling QEC with quantum thermodynamics (failure-branch recycling)

**Open problems:**
- Rare correlated error events (e.g., leakage and its spreading) limit logical performance over long runs
- Decoder latency and scalability must keep pace with real-time error-correction cycles
- Fundamental accuracy limits imposed by non-isometric encodings under energy constraints remain to be quantified
- NISQ-era hardware imperfections (gate error, decoherence/dephasing, measurement error, crosstalk, leakage) still constrain error-free computation
- Experimental error correction of logical qudits and bosonic codes is only nascent
- Achieving practical fault tolerance without exponential hardware overhead

**Limitations:**
- Analysis is based on titles and abstracts only; no full texts were read.
- One retrieved item (src_3ee790e4ad, 'Real-time quantum error correction beyond break-even') has metadata only with no abstract and could not be assessed.
- Several items are arXiv preprints and are not peer reviewed; their reported numbers and thresholds are not independently verified here.
- The sample is small and mixes experimental results, theory, review/tutorial material and unconventional proposals, limiting cross-paper generalization.
- No citation or publication-count statistics are used; evidence strength reflects abstract-level content only.
- No commercial or investment conclusions are drawn; laboratory demonstrations are not evidence of commercial viability.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['quantum error correction overhead', 'surface code scalability limits', 'qubit crosstalk error', 'quantum error correction latency', 'decoherence rate limits', 'quantum error mitigation alternatives']

- **[R1]** *(verified_fact, confidence medium)* A proven lower bound says QEC restricted to geometrically local operations in 2D carries a space overhead that grows with system size, even when classical computation is free and error-free. This is a structural limit on planar, nearest-neighbour architectures.
  - source: [A lower bound on the overhead of quantum error correction in low dimensions](https://doi.org/10.48550/arxiv.2302.04317) (OpenAlex, 2023-02-08, abstract_only)
  - excerpt: "incurs an overhead that grows with the system size, even if arbitrary error-free classical computation is allowed"
  - reasoning: This is a theoretical result from one arXiv preprint (not peer reviewed). The abstract gives the asymptotic scaling, Ω(√log(1/δ)), but not the constants or the point at which it becomes practically binding. Overhead 'reduction' claims made for local 2D layouts should be read against this bound.
- **[R2]** *(verified_fact, confidence medium)* Low-overhead qLDPC codes depend on dense, long-range connectivity that is hard to build, especially on superconducting chips. A proposed workaround removes up to 50% of long-range links but roughly doubles syndrome-extraction circuit depth. The connectivity problem is traded for time cost, not removed.
  - source: [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) (arXiv, 2025-08-31, abstract_only)
  - excerpt: "remove up to 50% of long-range connections while approximately doubling the circuit depth"
  - reasoning: arXiv preprint with no hardware demonstration in the abstract. Deeper circuits give physical errors more time to accumulate. The abstract says circuit-level distance is 'largely preserved' but does not give logical error rates under realistic noise, so the net effect is a gap.
- **[R3]** *(verified_fact, confidence medium)* Headline performance for the new high-rate 'Cornucopia' qLDPC codes is extrapolated, not measured. The logical error rates of 2.6e-16 and 1.9e-31 assume physical error rates of 0.1% and 0.01%. The scheme also relies on reconfigurable neutral-atom rearrangement, so one hardware platform and its control stack carry the result.
  - source: [Quantum error correction at ultra-low overhead](https://doi.org/10.48550/arxiv.2608.02773) (OpenAlex, 2026-08-03, abstract_only)
  - excerpt: "achieving an extrapolated logical error rate of $2.6\times10^{-16}$ ($1.9\times10^{-31}$) per logical qubit per cycle, assuming the physical error rate of $0.1\%$ ($0.01\%$)"
  - reasoning: Single arXiv preprint (OpenAlex lists 11 citations). The abstract does not report atom-movement time, loss, or the effect of correlated errors on the extrapolation. Those are gaps, not demonstrated failures. The pseudo-threshold of >0.4% is described as comparable to the surface code and bivariate bicycle codes, so the claimed advantage is mainly in rate, not threshold.
- **[R4]** *(verified_fact, confidence medium)* In trapped-ion 2D crystals, crosstalk between parallel entangling gates raises the needed surface-code distance from 3 to 5. Parallelism, which QEC needs in order to have a threshold, therefore increases qubit cost. The paper reports a break-even point under 'realistic parameters', but this comes from numerical modelling.
  - source: [Performance Analysis for Crosstalk Errors between Parallel Entangling Gates in Trapped Ion Quantum Error Correction](https://arxiv.org/abs/2501.09554v2) (arXiv, 2025-01-16, abstract_only)
  - excerpt: "a distance-5 code is necessary to correct the two-qubit crosstalk error"
  - reasoning: arXiv preprint, numerical only. The abstract treats the 10^-10 logical-error goal as a long-term target and does not claim it has been reached. Whether the 'realistic parameters' match current ion hardware at scale is not checked in the abstract.
- **[R5]** *(ai_interpretation, confidence medium)* Most of the overhead-reduction results in this set come from simulation or numerics, not hardware. They give modest or narrow gains: soft information (up to 11% and 20% better suppression, 13% and 33% fewer physical qubits), flag-sharing on small codes ([[17,1,5]], [[19,1,5]], [[5,1,3]]), and ancilla recycling (~25% fewer qubits in rotated surface codes). Real-device noise could erode these gains.
  - source: [Reducing quantum error correction overhead using soft information](https://arxiv.org/abs/2504.03504v3) (arXiv, 2025-04-04, abstract_only)
  - source: [Reducing Quantum Error Correction Overhead with Versatile Flag-Sharing Syndrome Extraction Circuits](https://arxiv.org/abs/2407.00607v1) (arXiv, 2024-06-30, abstract_only)
  - source: [Quantum Prometheus: Defying Overhead with Recycled Ancillas in Quantum Error Correction](https://doi.org/10.1109/isqed65160.2025.11014328) (OpenAlex, 2025-04-23, abstract_only)
  - reasoning: Judgement across three abstracts. Soft information and flag-sharing are explicitly simulation-based, and the ancilla-reuse paper presents only an analysis. The soft-information paper is an arXiv preprint (also listed with a Quantum Sci. Technol. venue) and the flag-sharing paper is also an arXiv preprint. The abstracts do not show whether the gains hold with real correlated noise, readout limits, or added classical-decoding load. That is a gap, not a contradiction. The flag-sharing 'order of magnitude' pseudothreshold gain is relative to prior schemes for very small codes.
- **[R6]** *(verified_fact, confidence low)* The cost of non-Clifford (T) gates through magic-state distillation is described as a major overhead, needing many physical qubits and complex measurement and feedback. The proposed alternative, a DFS-encoded geometric logical T gate, has only been shown numerically in superconducting circuits. It is not yet a proven replacement.
  - source: [Suppression of Universal Errors in DFS-Encoded Superconducting Geometric Logical \emph{T} Gate](https://arxiv.org/abs/2605.00552v1) (arXiv, 2026-05-01, abstract_only)
  - excerpt: "conventional magic state distillation requires massive physical qubit overhead across successive distillation rounds, alongside sophisticated measurement and feedback control"
  - reasoning: arXiv preprint (the abstract is truncated). The abstract's account of distillation cost is the authors' framing, not an independent measurement. The alternative is evaluated by numerical simulation against other gate protocols. Whether it fits inside a fault-tolerant logical stack is not addressed in the abstract.
- **[R7]** *(ai_interpretation, confidence low)* A non-peer-reviewed Zenodo preprint argues that active QEC has a Landauer thermodynamic floor of (n−k)/k·kT·ln2 per logical qubit per round, and that biology avoids it through structure. Its own code comparison returned a 'partial null', and it is not evidence of a practical energy bottleneck. Autonomous and dissipative correction is named as the boundary of the claim.
  - source: [Error Correction Is a Landauer Machine: The Thermodynamic Floor of Quantum Error-Correction Overhead](https://doi.org/10.5281/zenodo.22115862) (OpenAlex, 2026-08-26, abstract_only)
  - reasoning: A single zero-citation preprint on Zenodo. Its test is a classical NAND-like flash channel, not a quantum device. The abstract does not compare the floor with real cryogenic control power, so I cannot judge whether the floor matters in practice. The biology analogy is speculative. The paper also defines its own metric (JPCUB), which has no independent validation. I treat it as a possible theoretical constraint to monitor, not an established limit.

**Possible hype:**
- 'Ultra-low overhead' / 'low-overhead' codes: the headline logical error rates are extrapolated from assumed physical error rates and rest on simulation, not hardware.
- 'Defying overhead' (ancilla recycling): the evidence is an analysis on rotated surface codes, with about 25% fewer qubits at most; this reduces overhead but does not remove it.
- 'Thermodynamic floor' for QEC and the biological 'correction-free' analogy: this is a single unreviewed preprint with a partial null result and classical test channels.
- 'Error suppressed to the fourth order' for geometric T gates: numerical results only, with no demonstrated fault-tolerant integration.
- Overhead 'reduction' framings that ignore trade-offs such as doubled circuit depth, long-range connectivity needs, and decoder or readout complexity.

**Challenges to the Science findings:**
- Targets ['S1', 'S2'], severity medium:
  - **[C1]** *(ai_interpretation, confidence high)* S1 and S2 present the Willow result as evidence of scalable fault tolerance but leave out caveats from the same abstract. Logical performance of the repetition codes is limited by rare correlated error events, about once per hour (3×10^9 cycles). The result is a memory only, with no logical gates. The real-time decoding result is at distance-5, not at the distance-7 code that supplies the headline 0.143% figure. Λ=2.14 is a modest suppression factor per distance step. The authors themselves say the performance would meet large-scale requirements only 'if scaled'.
    - source: [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) (OpenAlex, 2024-12-09, abstract_only)
    - excerpt: "logical performance is limited by rare correlated error events occurring approximately once every hour, or $$3$$ $$\times $$ $${10}^{9}$$ cycles."
    - reasoning: The correlated-error floor and the memory-only scope bound how far the findings can be extrapolated. The Science summary omits both.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S3'], severity low:
  - **[C2]** *(ai_interpretation, confidence medium)* S3 reads as though leakage is solved. The cited demonstration is a distance-3 surface code plus a distance-21 bit-flip code. The abstract reports reduced leakage populations, not restored exponential suppression of the logical error rate in a larger surface code. The 'resolved a key challenge' framing is the authors' own claim from a small-scale demonstration. It is not an independently established result.
    - source: [Overcoming leakage in quantum error correction](https://doi.org/10.1038/s41567-023-02226-w) (OpenAlex, 2023-10-05, abstract_only)
    - reasoning: The abstract supports a tenfold reduction in steady-state leakage at small code distance. It does not show that leakage no longer limits scaling. Labelling S3 'verified_fact' with medium confidence overstates what the abstract establishes.
- Targets ['S5'], severity medium:
  - **[C3]** *(ai_interpretation, confidence medium)* S5 calls neural decoders 'a clearly emerging direction' on the strength of one 2026 preprint. The headline gains are simulation benchmarks: up to 49% lower MWPM logical error rate at d≤5 under SI1000 noise, and speedups over specific decoders. On the only experimental dataset, Sycamore, the new decoder merely matches or slightly surpasses an existing dense neural decoder. A trend claim needs more than one non-peer-reviewed paper.
    - source: [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) (arXiv, 2026-05-16, abstract_only)
    - excerpt: "SMD reduces the MWPM logical error rate by up to 49% at $d \le 5$ under SI1000 noise"
    - reasoning: The abstract shows simulated gains at small distance. The experimental result is only parity with a prior neural decoder. This supports a single-preprint claim, not a 'clearly emerging' field-level trend.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S6', 'S7'], severity low:
  - **[C4]** *(ai_interpretation, confidence medium)* S6 and S7 are labelled verified_fact, but the abstracts describe numerical or simulation-based work with no hardware demonstration. The hyperbolic-code paper says its codes were simulated. The quantum-autoencoder paper shows learned strategies and 'moderate noise' tolerance with no experimental device mentioned. The 'higher encoding rates and lower overhead' and 'extend logical-qubit lifetime' claims are therefore model-level, and they are not hardware-validated facts.
    - source: [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) (arXiv, 2025-04-10, abstract_only)
    - source: [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) (OpenAlex, 2023-03-09, abstract_only)
    - excerpt: "We apply this framework to construct and simulate two representative hyperbolic quantum error correction codes (HQECCs)"
    - reasoning: The excerpt confirms the hyperbolic-code results are simulated. The autoencoder abstract likewise reports no hardware run. These findings should be treated as simulation-level, with the 'verified' label limited to 'the authors claim'.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S10'], severity medium:
  - **[C5]** *(ai_interpretation, confidence medium)* S10 generalises to 'a recurring theme across the review/tutorial literature' from only two sources, and only one of them supports it. The hardware-efficient, continuous-variable, modular superconducting-photon emphasis comes from lecture notes from a 2019 summer school, a specific research group's perspective. The 'For Dummies' abstract is a generic NISQ-era review and mentions none of this. 'Near-term practical directions' is the notes' vision statement and is not a surveyed consensus.
    - source: [Introduction to quantum error correction and fault tolerance](https://doi.org/10.21468/scipostphyslectnotes.70) (OpenAlex, 2023-06-12, abstract_only)
    - source: [Quantum Error Correction For Dummies](https://doi.org/10.1109/qce57702.2023.00017) (OpenAlex, 2023-09-17, abstract_only)
    - excerpt: "The goal and vision is “hardware-efficient” quantum error correction that does not require exponentially large hardware overhead"
    - reasoning: A single group's lecture-note vision does not make a recurring theme across the literature. The second cited abstract does not corroborate it.
- Targets general, severity medium:
  - **[C6]** *(ai_interpretation, confidence medium)* General gap: the findings S1–S4 are experimental successes, but nothing weighs the structural cost of scaling them. A proven lower bound shows that locality-limited 2D error correction has a space overhead growing with system size. Alternatives such as qLDPC codes demand hard-to-build long-range connectivity, and routing workarounds trade it for roughly doubled circuit depth. Without this counterweight, the surface-code and bosonic demonstrations may be read as nearer to practical scale than the evidence supports.
    - source: [A lower bound on the overhead of quantum error correction in low dimensions](https://doi.org/10.48550/arxiv.2302.04317) (OpenAlex, 2023-02-08, abstract_only)
    - source: [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) (arXiv, 2025-08-31, abstract_only)
    - excerpt: "in order to operate a quantum error correcting code in 2D at a logical error rate of $δ$, a space overhead of $Ω(\sqrt{\log(1/δ)})$ is needed"
    - reasoning: The cited lower bound applies to 2D local architectures, and the routing preprint shows connectivity can be traded for circuit depth. Together they show scale-up is constrained by overhead and connectivity. The Science findings do not address these constraints.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source

**Limitations:**
- Only 12 papers, and only titles/abstracts (mostly abstract_only; some truncated). No full-text methods, noise models or error bars were checked.
- Most evidence is arXiv or Zenodo preprints that are not peer reviewed. Several results are simulation-only, so hardware reproducibility is mostly unassessed.
- Two items have no abstract (src_0192635a40, a Nature Physics demonstration of low-overhead codes with 67 citations, and src_c9bb5e9898, an overhead calculator). I cannot assess their results or caveats, and I drew no conclusions from them.
- The decoherence paper on random Lindbladians (src_67e9b52016) is generic theory on random open systems and only loosely tied to QEC engineering, so I did not use it as a risk finding.
- The search was oriented to overhead and so under-covers other risks: decoder latency and classical compute, leakage and correlated errors such as cosmic rays, cryogenic wiring and power, and supply-chain concentration. Absence from this set does not mean these are not problems.
- No company-level information was available, so I attribute no risks to specific firms.
- Only titles and abstracts were reviewed. Caveats may be addressed in full texts that were not read.
- src_3ee790e4ad, src_0192635a40 and src_c9bb5e9898 have no abstracts, so I could not assess or use them. For example, the low-overhead code demonstration could bear on the overhead-related findings.
- I did not challenge S4, S8 or S9. S4 and S8 are consistent with their abstracts, and S9 already carries the appropriate preprint caveats.
- The review cannot independently check experimental numbers beyond the abstract text.

## Evidence: company filings and news
Status: ok. Companies are chosen from the evidence: SEC-listed patent assignees and employers of paper authors found by the Patent and Science agents (23 company name(s) in the patents and papers; 3 matched to the SEC ticker file; the top 3 by patents + papers are read), plus filers whose reports mention the topic. Company evidence is limited to short verbatim passages from their latest SEC annual/quarterly reports that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase only; no patent or paper of theirs was found, they are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: quantum error correction, logical qubit, fault-tolerant, surface code, qubit coherence

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Dell Technologies Inc. (DELL) | 2 | 0 | large: 113.5B USD | +18.8% | 2.8% of revenue |  |
| Pasqal Holding SA (PSQL) | 1 | 0 | n/a | n/a | n/a |  |
| Xanadu Quantum Technologies Ltd (XNDU) | 1 | 1 | n/a | n/a | n/a |  |
| Quantinuum Inc. (QNT) | 1 | 1 | n/a | n/a | n/a | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence medium)* Quantinuum states it was the first in the industry to implement logical qubits with higher accuracy than physical qubits, citing the 2021 Ryan-Anderson et al. Study.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - excerpt: "we were the first in the industry to implement logical qubits with a higher accuracy than physical qubits, according to the 2021 Ryan-Anderson et al. Study."
  - reasoning: Direct restatement of a Quantinuum 10-Q excerpt; the company's own claim about industry precedence.
- **[M2]** *(unverified_claim, confidence medium)* Quantinuum expects to introduce its Sol system in 2027 with up to 100 logical qubits, and Apollo in 2029 with hundreds of logical qubits, as milestones toward fault-tolerant computing.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - reasoning: These are the company's own forward-looking expectations stated in its 10-Q; the excerpt is exact but the achievement is not verified.
- **[M3]** *(verified_fact, confidence medium)* Quantinuum frames logical qubit count, fidelity, scalability, time-to-solution and full-stack performance as the metrics it believes drive customer outcomes and commercial adoption.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - excerpt: "The metrics and performance drivers that best showcase our ability to achieve results include fidelity, number of logical qubits, system scalability, time-to-solution and full-stack performance."
  - reasoning: Exact restatement of the filing excerpt describing the company's commercial framing.
- **[M4]** *(verified_fact, confidence medium)* Xanadu has demonstrated only twelve logical qubits, with photon loss not yet meeting required levels, while designing its architecture toward a target of 100,000 cores.
  - source: [Xanadu Quantum Technologies Ltd Form 20-F (ANNUAL REPORT), filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) (SEC EDGAR, 2026-04-09, excerpt_only)
  - excerpt: "twelve logical qubits with photon loss not meeting the required levels. Our architecture is designed with a target to scale up to 100,000"
  - reasoning: Exact restatement of Xanadu's 20-F excerpt describing its current demonstration status and scaling target.
- **[M5]** *(ai_interpretation, confidence medium)* Both Xanadu and Quantinuum describe fault tolerance at scale as subject to substantial scientific and engineering uncertainty, including error rates, error-correction codes and qubit coherence.
  - source: [Xanadu Quantum Technologies Ltd Form 20-F (ANNUAL REPORT), filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) (SEC EDGAR, 2026-04-09, excerpt_only)
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - reasoning: Both filings' excerpts independently flag fault-tolerance barriers (Xanadu: 'significant barriers in our development and manufacturing efforts'; Quantinuum: 'substantial scientific and engineering uncertainty'), a shared risk pattern across the two companies.
- **[M6]** *(verified_fact, confidence medium)* Quantinuum identifies developing effective quantum error correction software codes and managing qubit coherence times as key engineering challenges for commercially viable fault tolerance.
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - excerpt: "developing effective quantum error correction software codes, managing qubit coherence times and scaling our systems while maintaining or improving gate fidelities."
  - reasoning: Exact restatement of the 10-Q excerpt on fault-tolerance challenges.
- **[M7]** *(assumption, confidence low)* Dell and Pasqal hold patents related to quantum error correction per the evidence set, but their retrieved filings do not mention the topic keywords, so no commercial activity can be inferred from this evidence.
  - reasoning: The retrieval metadata names them as patent assignees, but no filing excerpts were provided; absence of keyword mentions in excerpts does not prove absence from the market.
  - citation check: company name(s) not found in the cited sources removed: Dell Technologies Inc., Pasqal Holding SA

**Limitations:**
- Only two filing excerpts (Xanadu 20-F, Quantinuum 10-Q) mention the topic; no news headlines were provided, so no market-coverage claims could be made.
- Filings are excerpt-only; full reports were not read, so statements about each company's broader commercial position, customers or revenue are unavailable.
- Dell and Pasqal appear only as patent assignees with no keyword-matching excerpts; their role in quantum error correction cannot be assessed.
- No revenue data in SEC XBRL for Xanadu, Quantinuum or Pasqal, limiting commercial-scale assessment.
- Quantinuum's system roadmap (Sol, Apollo) is company expectation only, not verified performance.

## Social signals from X
Status: ok. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 50 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (130): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie, @SemiconductorsX, @KirkDBorne, @kyleichan, @thePandaily, @HPCwire, @WarGuy_, @PIBKohima, @robvank, @LifeboatHQ, @zhaoweiasu, @BlackEngineer, @ShapesXR, @engadget, @Gadgets360, @eeNewsEurope, @machinelearnflx, @dez_blanchfield, @0xRicker, @Lance_Edelman, @Techmeme, @chr1sa, @Romka2x, @OWW, @CyberRobooo, @Decoded08, @techniahqrobot, @liuziwei7, @johnkoetsier, @preskill, @gp_pulipaka, @QuantumStateX, @Scholarshipps, @QuantumDaily, @scitechgirl, @Amandasatiro07, @thatoptometrist, @QuantumPapers, @the_hindu, @IndiaToday, @EconomicTimes, @ETNOWlive, @GreaterKashmir, @DDIndialive, @c_aashish, @TheQuietSensei, @CBCRajouri, @india_plus_, @alphaaffairsf2f, @dayalugurubjp, @Prabinmen, @PsuWatch, @aseemmanchanda, @bhagwantkhuba, @SUDHIRb9661, @governancenow, @PIB_India, @marinaj4q, @Finsee_main, @skathire, @singularityhub, @ahier, @MolecularCell, @RevvityLifeSci, @idtdna, @NaturePlants, @SimbokeSarah, @ChEnected, @RZubiranS, @BioinfoAdv, @srqstockpicker, @ShorterLab, @nabil125125125, @ThalesDigiSec, @ThejesterVerse, @WOCTechnology, @QuantSecXYZ, @Ronald_vanLoon, @PrameyaEnglish, @craigapplecom, @BLU_Products, @PragativadiNews, @HimanshiTech, @NyongesaSande, @gadgetbytenepal, @bobbymorris280, @TechieUltimatum, @PaidFreeDroid, @nitin_gadkari, @MIB_India, @kishanreddybjp, @IndiaInGuate, @PIBDehradun, @CISACyber
Posts read: 18 (estimated X cost $0.090)

- **[X1]** *(unverified_claim, confidence medium)* AMD announced (via @AMD) a new co-design platform with IBM and Oak Ridge National Laboratory to advance quantum error correction, built on 'Umbra', an HPC system powered by AMD Instinct MI355X GPUs and 5th Gen AMD CPUs.
  - source: [@AMD: Quantum progress. Powered by collaboration. We're excited to announce we're launching a ne…](https://x.com/AMD/status/2118330823803851060) (X API, 2026-11-05, full_text)
  - source: [@AMD: Quantum’s future takes teamwork. Swipe to see how AMD, @IBM and @ORNL are advancing quantu…](https://x.com/AMD/status/2118819338849571023) (X API, 2026-11-06, full_text)
  - excerpt: "We're excited to announce we're launching a new co-design platform with @IBM and @ORNL's @QuantumSciCtr to advance quantum error correction. At its foundation: Umbra, an HPC system powered by AMD Instinct MI355X GPUs..."
  - reasoning: Direct company announcement from AMD, corroborated by HPCwire's headline and an agent post describing the same AMD/IBM/ORNL platform and Umbra MI355X details. Still promotional/unverified; linked article not read.
  - citation check: company name(s) not found in the cited posts removed: Oak Ridge National Laboratory
- **[X2]** *(unverified_claim, confidence medium)* HPCwire separately reports that ORNL, IBM and AMD launched a co-design platform for quantum error correction, and that Quantinuum outlined a 'Nexus' roadmap for fault-tolerant quantum computing.
  - source: [@HPCwire: ORNL, IBM, and AMD Launch New Co-Design Platform for Quantum Error Correction @ORNL @IBM @…](https://x.com/HPCwire/status/2118362762849951888) (X API, 2026-11-05, full_text)
  - source: [@HPCwire: Quantinuum Outlines Nexus Roadmap for Fault-Tolerant Quantum Computing @QuantinuumQC #Quan…](https://x.com/HPCwire/status/2118349895836844520) (X API, 2026-11-05, full_text)
  - excerpt: "ORNL, IBM, and AMD Launch New Co-Design Platform for Quantum Error Correction ... Quantinuum Outlines Nexus Roadmap for Fault-Tolerant Quantum Computing"
  - reasoning: Specialist press headlines corroborate the AMD/IBM/ORNL launch and add a Quantinuum fault-tolerance roadmap item; article bodies unread, so details are limited to headlines.
  - citation check: company name(s) not found in the cited posts removed: Oak Ridge National Laboratory
- **[X3]** *(unverified_claim, confidence low)* Riverlane researchers reportedly achieved a 20 percent improvement in quantum error correction performance using a data-driven method to model errors, per @QuantumStateX.
  - source: [@QuantumStateX: Data-driven error models lift quantum error correction by 20 percent Riverlane researchers…](https://x.com/QuantumStateX/status/2119908980721897819) (X API, 2026-11-09, full_text)
  - reasoning: Single owner-added aggregator account; the '20 percent' figure and Riverlane attribution cannot be checked from the post alone, and the hashtag references GoogleQuantumAI without explanation.
- **[X4]** *(unverified_claim, confidence low)* Quantum X Labs reports up to 20% fewer logical decoding failures in preliminary benchmarks on IBM quantum processors, per @QuantumStateX.
  - source: [@QuantumStateX: Quantum X Labs reports achieving up to 20% fewer logical decoding failures in preliminary …](https://x.com/QuantumStateX/status/2119851539606986772) (X API, 2026-11-09, full_text)
  - reasoning: Self-reported preliminary benchmark from a single low-engagement post with a stock ticker hashtag; promotional in nature and unverified.
- **[X5]** *(ai_interpretation, confidence medium)* Several accounts this week emphasised quantum error correction as an active HPC-industry collaboration area: AMD/IBM/ORNL co-design platform posts, an ORNL-IBM co-design platform mention by @gp_pulipaka, and Quantinuum fault-tolerance coverage.
  - source: [@AMD: Quantum progress. Powered by collaboration. We're excited to announce we're launching a ne…](https://x.com/AMD/status/2118330823803851060) (X API, 2026-11-05, full_text)
  - source: [@AMD: Quantum’s future takes teamwork. Swipe to see how AMD, @IBM and @ORNL are advancing quantu…](https://x.com/AMD/status/2118819338849571023) (X API, 2026-11-06, full_text)
  - source: [@gp_pulipaka: Oak Ridge National Laboratory, IBM Launch New Co Design Platform for Quantum Error Correct…](https://x.com/gp_pulipaka/status/2119097576653783322) (X API, 2026-11-07, full_text)
  - source: [@HPCwire: ORNL, IBM, and AMD Launch New Co-Design Platform for Quantum Error Correction @ORNL @IBM @…](https://x.com/HPCwire/status/2118362762849951888) (X API, 2026-11-05, full_text)
  - source: [@HPCwire: Quantinuum Outlines Nexus Roadmap for Fault-Tolerant Quantum Computing @QuantinuumQC #Quan…](https://x.com/HPCwire/status/2118349895836844520) (X API, 2026-11-05, full_text)
  - source: [@WarGuy_: AMD, IBM and Oak Ridge National Laboratory are launching a joint platform to advance quant…](https://x.com/WarGuy_/status/2118337327575548019) (X API, 2026-11-05, full_text)
  - reasoning: Multiple independent accounts (company, press, agent) posted about the same AMD/IBM/ORNL QEC platform and Quantinuum's fault-tolerant roadmap within days, indicating QEC co-design with HPC is the dominant theme in this week's sample.
- **[X6]** *(unverified_claim, confidence low)* New preprints this week address fault-tolerant quantum computing building blocks, including surface-code patch connection via entanglement distillation, dynamic measurement scheduling to accelerate fault-tolerant programs, formal QEC theory in Lean, fast verification of magic-state preparation, and attack detection on the QEC/control layer, per @QuantumPapers.
  - source: [@QuantumPapers: Connection of surface code patches based on entanglement distillation without postselectio…](https://x.com/QuantumPapers/status/2119390707597107599) (X API, 2026-11-08, full_text)
  - source: [@QuantumPapers: DynaMite: Dynamic Measurement Scheduling To Accelerate Fault-Tolerant Quantum Programs Don…](https://x.com/QuantumPapers/status/2119091869514641855) (X API, 2026-11-07, full_text)
  - source: [@QuantumPapers: QECert: Formal Foundations for Quantum Error-Correction Theory in Lean Keming He, Jiahan C…](https://x.com/QuantumPapers/status/2119059727178944793) (X API, 2026-11-07, full_text)
  - source: [@QuantumPapers: Fast verification of fault tolerant magic state preparation circuits with the CNOT + T gat…](https://x.com/QuantumPapers/status/2119008337777840596) (X API, 2026-11-07, full_text)
  - source: [@QuantumPapers: Trinetra.Q: Statistical and Behavioral Detection of Attacks on the Quantum-Error-Correctio…](https://x.com/QuantumPapers/status/2119268112826531973) (X API, 2026-11-08, full_text)
  - source: [@QuantumPapers: Finite-temperature transition-window weights on a fault-tolerant quantum computer: duplex …](https://x.com/QuantumPapers/status/2119545191656730878) (X API, 2026-11-08, full_text)
  - reasoning: ArXiv-style paper listings show research activity across surface codes, fault-tolerant scheduling, formal verification and QEC security, but preprints are unreviewed and only titles were observed.
- **[X7]** *(unverified_claim, confidence low)* Quantinuum's Q3 2026 revenue reportedly rose 13% quarter-over-quarter with a raised sales outlook but widening cash losses, and the company 'hit key accuracy targets', per @Finsee_main.
  - source: [@Finsee_main: $QNT Q3 2026 earnings: Quantinuum raises its sales outlook, but cash losses widen Quantinu…](https://x.com/Finsee_main/status/2118664276495810699) (X API, 2026-11-06, full_text)
  - reasoning: Single aggregator post summarising earnings; figures truncated in the post and the underlying report unread. Included as context on fault-tolerance-focused vendors, not as verified financials.
- **[X8]** *(unverified_claim, confidence low)* Quint Computing reportedly raised €9.1M to advance fault-tolerant quantum computing, per an HPCwire headline.
  - source: [@HPCwire: Quint Computing Raises €9.1M to Advance Fault-Tolerant Quantum Computing #QuintComputing #…](https://x.com/HPCwire/status/2117645179414876593) (X API, 2026-11-03, full_text)
  - reasoning: Funding amount appears only in a headline from one press account; article body unread.

**Limitations:**
- Only posts from a fixed, owner-approved account list over the last 7 days were analysed; most core quantum-computing companies (IBM, Google, Riverlane, Quantinuum directly) are not in the list, so coverage is indirect.
- All claims are what accounts said, not verified facts; linked articles and papers were not read, so figures like '20 percent' or '€9.1M' rest on headlines and summaries.
- Company posts (AMD) are promotional announcements; engagement counts (e.g., 467 on AMD's launch post) indicate attention, not accuracy.
- Several sources are owner-added aggregator or agent accounts with low engagement and unclear editorial standards.
- The 7-day window is short; quiet weeks elsewhere should not be read as absence of QEC activity.
- No timing commitments beyond Quantinuum's roadmap headline were stated, so horizons are largely not applicable.

## Evidence: patents
Status: ok. Worldwide patent publications from EPO OPS matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.

Patent publications per year (EPO, terms ['quantum error correction', 'logical qubit', 'fault-tolerant', 'surface code']): {2022: 1201, 2023: 1266, 2024: 1399, 2025: 2271, 2026: 2564}
Patent Acceleration 2024->2025: 1399 -> 2271 (62.3% YoY). EPO OPS publications per publication year matching any of ['quantum error correction', 'logical qubit', 'fault-tolerant', 'surface code'] (worldwide, applications and grants, one family can count several times). Recent years are undercounted because of the ~18-month publication delay. The current partial year is excluded.
Most frequent first applicants among retrieved publications: GOOGLE LLC (2), IBM (2), RIVIAN IP HOLDINGS LLC (2), RTX BBN TECH INC (1), RAKUTEN SYMPHONY INC (1), ABB SCHWEIZ AG (1), PARITY QUANTUM COMPUTING GMBH (1), DELL PRODUCTS LP (1)

- **[P1]** *(ai_interpretation, confidence medium)* Major technology companies and specialized quantum startups are actively filing for quantum error correction (QEC) methods, with a strong emphasis on decoding algorithms, surface codes, and hardware-level noise management.
  - source: [CROSS-HAIR SURFACE CODES FOR QUANTUM COMPUTING [WO2026232094A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026232094A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [FAULT-TOLERANT QUBITS VIA MULTIMODE RESONATORS [WO2026231161A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026231161A2) (EPO OPS, 2026-11-05, abstract_only)
  - source: [DECODER FOR AN ERROR CORRECTING CODE [WO2026223892A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026223892A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [DECISION-TREE DECODERS FOR QUANTUM LOW-DENSITY PARITY-CHECK CODES [US20260340471A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340471A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [ADAPTIVE CANARY QUBIT SYSTEM WITH REAL-TIME NOISE MAPPING AND TELEMETRY INTEGRATION FOR QUANTUM ERROR MANAGEMENT [US20260340472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340472A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [SCALABLE TRAINING OF IMPROVED DETECTOR ERROR MODELS FOR DECODERS OF QUANTUM ERROR CORRECTION CODES [WO2026217118A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026217118A2) (EPO OPS, 2026-10-15, abstract_only)
  - reasoning: The retrieved publications show filings from both large tech firms (Google, IBM, Dell) and quantum-focused entities (Parity, BBN Tech) targeting different layers of the QEC stack, from physical qubit control to classical decoding software.
- **[P2]** *(ai_interpretation, confidence medium)* Decoding optimization and detector error modeling represent a concentrated area of innovation, as evidenced by multiple applications addressing syndrome measurement processing and logical state recovery.
  - source: [DECISION-TREE DECODERS FOR QUANTUM LOW-DENSITY PARITY-CHECK CODES [US20260340471A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340471A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [Quantum Error Correction Decoding via Block-and-Cycle Feasibility Checking [US20260300797A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300797A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [SCALABLE TRAINING OF IMPROVED DETECTOR ERROR MODELS FOR DECODERS OF QUANTUM ERROR CORRECTION CODES [WO2026217118A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026217118A2) (EPO OPS, 2026-10-15, abstract_only)
  - source: [COMPUTER PROGRAM, QUANTUM COMPUTATION SUPPORT METHOD, AND INFORMATION PROCESSING APPARATUS [EP4826604A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4826604A1) (EPO OPS, 2026-10-21, abstract_only)
  - reasoning: IBM and Google have filed multiple recent applications focusing on decision-tree decoders, block-and-cycle feasibility checking, and scalable training of detector error models, indicating a strategic push to improve the speed and accuracy of classical post-processing for quantum systems.
- **[P3]** *(ai_interpretation, confidence medium)* Novel physical implementations and hardware-level error management strategies are being described in patent applications, including adaptive canary qubits for real-time noise mapping and multi-mode resonators for cat qubits.
  - source: [ADAPTIVE CANARY QUBIT SYSTEM WITH REAL-TIME NOISE MAPPING AND TELEMETRY INTEGRATION FOR QUANTUM ERROR MANAGEMENT [US20260340472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340472A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [FAULT-TOLERANT QUBITS VIA MULTIMODE RESONATORS [WO2026231161A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026231161A2) (EPO OPS, 2026-11-05, abstract_only)
  - source: [MODULAR PHOTONIC QUANTUM COMPUTER WITH AUTONOMOUS AI CONTROL AND ROOM-TEMPERATURE OPERATION [WO2026210195A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026210195A1) (EPO OPS, 2026-10-08, abstract_only)
  - reasoning: These filings describe moving beyond abstract codes to integrate error management directly into hardware control loops, using telemetry data and AI-driven fault correction to dynamically reassign qubits or manage thermal environments.
- **[P4]** *(verified_fact, confidence low)* The search results include a substantial number of non-quantum patents using overlapping terminology such as fault-tolerant and error correction in classical contexts like automotive power systems, financial ledgers, and AI security.
  - source: [HETEROGENEOUS DISKS UTILIZATION IN FAULT TOLERANT STORAGE SYSTEMS [US20260339797A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339797A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [FAULT-TOLERANT OPERATION OF SERIES-CONNECTED INVERTERS TOPOLOGY [WO2026224503A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026224503A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [ENHANCED REDUNDANCY IN MIXED-VOLTAGE LOW VOLTAGE SYSTEM [US20260336466A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260336466A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [FAULT-TOLERANT AI ARCHITECTURE WITH DISTRIBUTED PROCESSING AND AUTONOMOUS TASK TRANSITION [US20260319898A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260319898A1) (EPO OPS, 2026-10-15, abstract_only)
  - source: [BYZANTINE-FAULT-TOLERANT FEDERATED THREAT MODEL TRAINING FOR ADVERSARIALLY ROBUST AI SECURITY SYSTEMS [US20260312975A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260312975A1) (EPO OPS, 2026-10-08, abstract_only)
  - excerpt: "A system for fault tolerant storage includes a network environment including a plurality of computing devices and a plurality of storage devices."
  - reasoning: The abstracts explicitly describe classical systems, confirming that keyword matching captures broad fault-tolerance concepts beyond quantum computing.
- **[P5]** *(ai_interpretation, confidence medium)* Protocols for fault-tolerant logical operations and memory access, including magic state distillation and QRAM, are being described to support scalable quantum computing architectures.
  - source: [DISTILLATION-TELEPORTATION PROTOCOL FOR FAULT-TOLERANT QUANTUM RANDOM ACCESS MEMORY (QRAM) [US20260299819A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260299819A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [QUANTUM COMPUTER AND METHOD FOR IMPLEMENTING A LOGICAL GATE USING A MAGIC STATE [WO2026195576A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026195576A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [SYSTEMS AND METHODS FOR TROTTER-BASED UNIVERSAL FAULT TOLERANCE [WO2026222032A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026222032A1) (EPO OPS, 2026-10-22, abstract_only)
  - reasoning: Filings from Amazon, Alice & Bob, and the University of Arizona describe methods for preparing logical resource states, implementing logical T gates via magic states, and executing Trotter-based universal fault tolerance, highlighting efforts to enable complex logical operations on error-corrected hardware.

**Limitations:**
- Analysis is restricted to titles and abstracts of 25 recent publications; full claims and specifications are not available.
- Keyword matching captures classical fault-tolerance patents, reducing precision for strictly quantum topics.
- Publication delay of approximately 18 months means recent filing trends may be undercounted.
- The sample represents only a fraction of the 7,263 total publications since 2023, and keyword variations may miss relevant patents.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: partial. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.


**Limitations:**
- No price series could be retrieved.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 24 distinct company names from 25 patent publications, 4 company-affiliated papers and 2 SEC filers; 4 matched to the SEC ticker file (4 outside the configured list), 10 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| XANADU QUANTUM TECH INC (XNDU) · Electronic Computers | 1 | 0 | 1 | n/a | n/a | n/a | **30** |
| Quantinuum Inc. (QNT) · Services-Computer Integrated Systems Design | 0 | 0 | 1 | n/a | n/a | n/a | **20** |
| Dell Technologies Inc. (DELL) · Electronic Computers | 1 | 0 | 0 | large: 113.54B USD | +18.8% | 2.8% | **15** |
| Pasqal Holding SA (PSQL) · Services-Computer Processing & Data Preparation | 1 | 0 | 0 | n/a | n/a | n/a | **15** |

- XANADU QUANTUM TECH INC: 1 patent publication(s) as assignee (+10); 1 SEC report(s) mentioning the topic (+15); size unknown from SEC XBRL (+5, neutral)
- Quantinuum Inc.: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); size unknown from SEC XBRL (+5, neutral)
- Dell Technologies Inc.: 1 patent publication(s) as assignee (+10); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth +19% (+5)
- Pasqal Holding SA: 1 patent publication(s) as assignee (+10); size unknown from SEC XBRL (+5, neutral)

**Found but not in the SEC ticker file (private, foreign, or name not matched):** GOOGLE LLC (2P/4A/0F), IBM (2P/0A/0F), RIVIAN IP HOLDINGS LLC (2P/0A/0F), RTX BBN TECH INC (1P/0A/0F), RAKUTEN SYMPHONY INC (1P/0A/0F), ABB SCHWEIZ AG (1P/0A/0F), PARITY QUANTUM COMPUTING GMBH (1P/0A/0F), POLAMREDDY VIVEKANANDA REDDY (1P/0A/0F), DUSTOSS LTD (1P/0A/0F), WASHBURN JONATHAN (1P/0A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence medium)* XANADU QUANTUM TECH INC (XNDU) is active on quantum error correction: 1 retrieved patent publication(s) name it as assignee; 1 of its SEC report(s) mention the topic. Next-runner score 30/100 (heuristic).
  - source: [METHOD FOR PERFORMING QUANTUM ERROR CORRECTION [US20260300796A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300796A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [Xanadu Quantum Technologies Ltd Form 20-F (ANNUAL REPORT), filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) (SEC EDGAR, 2026-04-09, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Quantinuum Inc. (QNT) is active on quantum error correction: 1 of its SEC report(s) mention the topic. Next-runner score 20/100 (heuristic).
  - source: [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) (SEC EDGAR, 2026-08-13, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Dell Technologies Inc. (DELL) is active on quantum error correction: 1 retrieved patent publication(s) name it as assignee; fiscal 2025 revenue 113.54B USD (large by revenue), growth +18.8%, R&D 2.8% of revenue. Next-runner score 15/100 (heuristic).
  - source: [ADAPTIVE CANARY QUBIT SYSTEM WITH REAL-TIME NOISE MAPPING AND TELEMETRY INTEGRATION FOR QUANTUM ERROR MANAGEMENT [US20260340472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340472A1) (EPO OPS, 2026-10-29, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Pasqal Holding SA (PSQL) is active on quantum error correction: 1 retrieved patent publication(s) name it as assignee. Next-runner score 15/100 (heuristic).
  - source: [A METHOD FOR PROVIDING MULTIPLE ROUNDS OF ERROR CORRECTIONS FOR A QUANTUM ERROR CORRECTION CODE [EP4818990A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4818990A1) (EPO OPS, 2026-10-07, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [@QuantumStateX: Data-driven error models lift quantum error correction by 20 percent Riverlane researchers…](https://x.com/QuantumStateX/status/2119908980721897819) | X API | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_18c4693510
- [@QuantumStateX: A 3D code twist creates a logical gate without extra qubits Po-Shen Hsin of King’s College…](https://x.com/QuantumStateX/status/2119851580132344100) | X API | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_462fc9779b
- [@QuantumStateX: Quantum X Labs reports achieving up to 20% fewer logical decoding failures in preliminary …](https://x.com/QuantumStateX/status/2119851539606986772) | X API | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_b60ed5c5a2
- [@QuantumPapers: Finite-temperature transition-window weights on a fault-tolerant quantum computer: duplex …](https://x.com/QuantumPapers/status/2119545191656730878) | X API | 2026-11-08 | retrieved 2026-11-10 | full_text | id src_ac04d56806
- [@QuantumPapers: Connection of surface code patches based on entanglement distillation without postselectio…](https://x.com/QuantumPapers/status/2119390707597107599) | X API | 2026-11-08 | retrieved 2026-11-10 | full_text | id src_ebac4aec1b
- [@QuantumPapers: Trinetra.Q: Statistical and Behavioral Detection of Attacks on the Quantum-Error-Correctio…](https://x.com/QuantumPapers/status/2119268112826531973) | X API | 2026-11-08 | retrieved 2026-11-10 | full_text | id src_872dc24a7a
- [@gp_pulipaka: Oak Ridge National Laboratory, IBM Launch New Co Design Platform for Quantum Error Correct…](https://x.com/gp_pulipaka/status/2119097576653783322) | X API | 2026-11-07 | retrieved 2026-11-10 | full_text | id src_26e528a9cc
- [@QuantumPapers: DynaMite: Dynamic Measurement Scheduling To Accelerate Fault-Tolerant Quantum Programs Don…](https://x.com/QuantumPapers/status/2119091869514641855) | X API | 2026-11-07 | retrieved 2026-11-10 | full_text | id src_8cc60f90cf
- [@QuantumPapers: QECert: Formal Foundations for Quantum Error-Correction Theory in Lean Keming He, Jiahan C…](https://x.com/QuantumPapers/status/2119059727178944793) | X API | 2026-11-07 | retrieved 2026-11-10 | full_text | id src_eeda9dfdb8
- [@QuantumPapers: Fast verification of fault tolerant magic state preparation circuits with the CNOT + T gat…](https://x.com/QuantumPapers/status/2119008337777840596) | X API | 2026-11-07 | retrieved 2026-11-10 | full_text | id src_0f6fc5d47a
- [@AMD: Quantum’s future takes teamwork. Swipe to see how AMD, @IBM and @ORNL are advancing quantu…](https://x.com/AMD/status/2118819338849571023) | X API | 2026-11-06 | retrieved 2026-11-10 | full_text | id src_f0d60f9d15
- [@Finsee_main: $QNT Q3 2026 earnings: Quantinuum raises its sales outlook, but cash losses widen Quantinu…](https://x.com/Finsee_main/status/2118664276495810699) | X API | 2026-11-06 | retrieved 2026-11-10 | full_text | id src_eac51813be
- [@AMD: Quantum progress. Powered by collaboration. We're excited to announce we're launching a ne…](https://x.com/AMD/status/2118330823803851060) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_bec85ebea4
- [@HPCwire: ORNL, IBM, and AMD Launch New Co-Design Platform for Quantum Error Correction @ORNL @IBM @…](https://x.com/HPCwire/status/2118362762849951888) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_1a6cd0614c
- [@HPCwire: Quantinuum Outlines Nexus Roadmap for Fault-Tolerant Quantum Computing @QuantinuumQC #Quan…](https://x.com/HPCwire/status/2118349895836844520) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_29e1414d00
- [@WarGuy_: AMD, IBM and Oak Ridge National Laboratory are launching a joint platform to advance quant…](https://x.com/WarGuy_/status/2118337327575548019) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_036166b6f8
- [CROSS-HAIR SURFACE CODES FOR QUANTUM COMPUTING [WO2026232094A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026232094A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-10 | abstract_only | id src_8b07a2461a
- [FAULT-TOLERANT QUBITS VIA MULTIMODE RESONATORS [WO2026231161A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026231161A2) | EPO OPS | 2026-11-05 | retrieved 2026-11-10 | abstract_only | id src_f5f024d51d
- [@KirkDBorne: 💥574 information-packed pages from @PacktPublishing at https://t.co/nxWY6AOB50 🚀 "Agentic …](https://x.com/KirkDBorne/status/2117750458915631386) | X API | 2026-11-03 | retrieved 2026-11-10 | full_text | id src_f6da75ce94
- [@HPCwire: Quint Computing Raises €9.1M to Advance Fault-Tolerant Quantum Computing #QuintComputing #…](https://x.com/HPCwire/status/2117645179414876593) | X API | 2026-11-03 | retrieved 2026-11-10 | full_text | id src_1dd128c5f9
- [HETEROGENEOUS DISKS UTILIZATION IN FAULT TOLERANT STORAGE SYSTEMS [US20260339797A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339797A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_7fd5526725
- [FAULT-TOLERANT OPERATION OF SERIES-CONNECTED INVERTERS TOPOLOGY [WO2026224503A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026224503A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_0e99992c9b
- [DECODER FOR AN ERROR CORRECTING CODE [WO2026223892A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026223892A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_330f18f157
- [DECISION-TREE DECODERS FOR QUANTUM LOW-DENSITY PARITY-CHECK CODES [US20260340471A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340471A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_f88f9886e0
- [ADAPTIVE CANARY QUBIT SYSTEM WITH REAL-TIME NOISE MAPPING AND TELEMETRY INTEGRATION FOR QUANTUM ERROR MANAGEMENT [US20260340472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340472A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_ec81aaf08f
- [ENHANCED REDUNDANCY IN MIXED-VOLTAGE LOW VOLTAGE SYSTEM [US20260336466A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260336466A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_e276cf2ac6
- [EVENT-DRIVEN FINANCIAL TRANSACTION PROCESSING SYSTEM WITH ATOMIC CONSISTENCY ACROSS DISTRIBUTED LEDGERS [US20260340643A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340643A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_75f739420c
- [SYSTEM AND METHOD FOR PHOTOVOLTAIC PERFORMANCE ENHANCEMENT VIA WIND-RESPONSIVE MICROFILAMENTS AND PARTIAL SPATIAL MITIGATION [WO2026224614A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026224614A2) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_cdcb4da01b
- [PATTERN-LOCK TOPOLOGICAL BOUNDARY DEVICES METHODS AND APPARATUS FOR LOSSLESS EDGE CHANNELS AND GOLDEN-RATIO TILED SURFACE-CODE QUBITS USING RECOGNITION-PHYSICS PATTERN-CHARGE INVARIANT [US20260340469A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260340469A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-10 | abstract_only | id src_707462e73d
- [SYSTEMS AND METHODS FOR TROTTER-BASED UNIVERSAL FAULT TOLERANCE [WO2026222032A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026222032A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-10 | abstract_only | id src_5119567960
- [COMPUTER PROGRAM, QUANTUM COMPUTATION SUPPORT METHOD, AND INFORMATION PROCESSING APPARATUS [EP4826604A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4826604A1) | EPO OPS | 2026-10-21 | retrieved 2026-11-10 | abstract_only | id src_8302751b7b
- [SCALABLE TRAINING OF IMPROVED DETECTOR ERROR MODELS FOR DECODERS OF QUANTUM ERROR CORRECTION CODES [WO2026217118A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026217118A2) | EPO OPS | 2026-10-15 | retrieved 2026-11-10 | abstract_only | id src_6179fcf6cf
- [FAULT-TOLERANT AI ARCHITECTURE WITH DISTRIBUTED PROCESSING AND AUTONOMOUS TASK TRANSITION [US20260319898A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260319898A1) | EPO OPS | 2026-10-15 | retrieved 2026-11-10 | abstract_only | id src_cad5e0a530
- [FAULT-TOLERANT TRANSITION TO DRIVER-OPERATED STEERING [US20260316823A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260316823A1) | EPO OPS | 2026-10-15 | retrieved 2026-11-10 | abstract_only | id src_5e3d0593c0
- [BYZANTINE-FAULT-TOLERANT FEDERATED THREAT MODEL TRAINING FOR ADVERSARIALLY ROBUST AI SECURITY SYSTEMS [US20260312975A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260312975A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-10 | abstract_only | id src_bd51618394
- [MODULAR PHOTONIC QUANTUM COMPUTER WITH AUTONOMOUS AI CONTROL AND ROOM-TEMPERATURE OPERATION [WO2026210195A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026210195A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-10 | abstract_only | id src_dbc646ed06
- [METHODS AND SYSTEMS FOR SELF-HEALING ARTIFICIAL INTELLIGENCE [US20260310497A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260310497A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-10 | abstract_only | id src_5b6999df89
- [A METHOD FOR PROVIDING MULTIPLE ROUNDS OF ERROR CORRECTIONS FOR A QUANTUM ERROR CORRECTION CODE [EP4818990A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4818990A1) | EPO OPS | 2026-10-07 | retrieved 2026-11-10 | abstract_only | id src_a5c07d3d40
- [Quantum Error Correction Decoding via Block-and-Cycle Feasibility Checking [US20260300797A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300797A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-10 | abstract_only | id src_1c49edc518
- [METHOD FOR PERFORMING QUANTUM ERROR CORRECTION [US20260300796A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300796A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-10 | abstract_only | id src_85ba8026bb
- [DISTILLATION-TELEPORTATION PROTOCOL FOR FAULT-TOLERANT QUANTUM RANDOM ACCESS MEMORY (QRAM) [US20260299819A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260299819A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-10 | abstract_only | id src_1470770fc7
- [QUANTUM COMPUTER AND METHOD FOR IMPLEMENTING A LOGICAL GATE USING A MAGIC STATE [WO2026195576A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026195576A1) | EPO OPS | 2026-09-24 | retrieved 2026-11-10 | abstract_only | id src_bbba2313c5
- [PEER-TO-PEER ENDPOINT MANAGEMENT SYSTEM AND METHOD FOR DECENTRALIZED DEVICE SECURITY AND ORCHESTRATION [US20260291995A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260291995A1) | EPO OPS | 2026-09-24 | retrieved 2026-11-10 | abstract_only | id src_169eb2cf86
- [Error Correction Is a Landauer Machine: The Thermodynamic Floor of Quantum Error-Correction Overhead](https://doi.org/10.5281/zenodo.22115862) | OpenAlex | 2026-08-26 | retrieved 2026-11-10 | abstract_only | id src_0df71ca0a9
- [Quantinuum Inc. Form 10-Q, filed 2026-08-13](https://www.sec.gov/Archives/edgar/data/2110105/000162828026056743/qnt-20260630.htm) | SEC EDGAR | 2026-08-13 | retrieved 2026-11-10 | excerpt_only | id src_bf91003520
- [Quantum error correction at ultra-low overhead](https://doi.org/10.48550/arxiv.2608.02773) | OpenAlex | 2026-08-03 | retrieved 2026-11-10 | abstract_only | id src_43430297cb
- [Surface-Code Overhead Tech4Biz Solutions A Lightweight, Exact, and Reproducible Calculator for Surface-Code Quantum Error Correction Overhead](https://doi.org/10.13140/rg.2.2.21425.95846) | OpenAlex | 2026-07-12 | retrieved 2026-11-10 | metadata_only | id src_c9bb5e9898
- [Approximate quantum error correction theory of non-isometric codes](https://arxiv.org/abs/2606.13559v1) | arXiv | 2026-06-11 | retrieved 2026-11-10 | abstract_only | id src_7c1902090a
- [Sparse Mamba Decoder for Quantum Error Correction: Efficient Defect-Centric Processing of Surface Code Syndromes](https://arxiv.org/abs/2605.17156v2) | arXiv | 2026-05-16 | retrieved 2026-11-10 | abstract_only | id src_844afd8b30
- [Suppression of Universal Errors in DFS-Encoded Superconducting Geometric Logical \emph{T} Gate](https://arxiv.org/abs/2605.00552v1) | arXiv | 2026-05-01 | retrieved 2026-11-10 | abstract_only | id src_c06098bc64
- [Xanadu Quantum Technologies Ltd Form 20-F (ANNUAL REPORT), filed 2026-04-09](https://www.sec.gov/Archives/edgar/data/2097163/000121390026042080/ea0285152-20f_xanadu.htm) | SEC EDGAR | 2026-04-09 | retrieved 2026-11-10 | excerpt_only | id src_b80a7885a6
- [Demonstration of low-overhead quantum error correction codes](https://doi.org/10.1038/s41567-025-03157-4) | OpenAlex | 2026-01-22 | retrieved 2026-11-10 | metadata_only | id src_0192635a40
- [Thermodynamic Recycling of Algorithmic Failure Branches: Quantum-Computer Demonstration with Quantum Error Correction](https://arxiv.org/abs/2601.07522v2) | arXiv | 2026-01-12 | retrieved 2026-11-10 | abstract_only | id src_800ebaba67
- [A simple universal routing strategy for reducing the connectivity requirements of quantum LDPC codes](https://arxiv.org/abs/2509.00850v1) | arXiv | 2025-08-31 | retrieved 2026-11-10 | abstract_only | id src_c0058675c2
- [Quantum error correction of qudits beyond break-even](https://doi.org/10.1038/s41586-025-08899-y) | OpenAlex | 2025-05-14 | retrieved 2026-11-10 | abstract_only | id src_97a5bbcd85
- [Quantum Error Correction in Quaternionic Hilbert Spaces](https://arxiv.org/abs/2504.19833v1) | arXiv | 2025-04-28 | retrieved 2026-11-10 | abstract_only | id src_afb5833d56
- [Quantum Prometheus: Defying Overhead with Recycled Ancillas in Quantum Error Correction](https://doi.org/10.1109/isqed65160.2025.11014328) | OpenAlex | 2025-04-23 | retrieved 2026-11-10 | abstract_only | id src_93b8f532fe
- [Systematic Approach to Hyperbolic Quantum Error Correction Codes](https://arxiv.org/abs/2504.07800v2) | arXiv | 2025-04-10 | retrieved 2026-11-10 | abstract_only | id src_90875088aa
- [Reducing quantum error correction overhead using soft information](https://arxiv.org/abs/2504.03504v3) | arXiv | 2025-04-04 | retrieved 2026-11-10 | abstract_only | id src_905c50a9ad
- [Performance Analysis for Crosstalk Errors between Parallel Entangling Gates in Trapped Ion Quantum Error Correction](https://arxiv.org/abs/2501.09554v2) | arXiv | 2025-01-16 | retrieved 2026-11-10 | abstract_only | id src_35b3dcabb7
- [Quantum error correction below the surface code threshold](https://doi.org/10.1038/s41586-024-08449-y) | OpenAlex | 2024-12-09 | retrieved 2026-11-10 | abstract_only | id src_9f4129c761
- [Reducing Quantum Error Correction Overhead with Versatile Flag-Sharing Syndrome Extraction Circuits](https://arxiv.org/abs/2407.00607v1) | arXiv | 2024-06-30 | retrieved 2026-11-10 | abstract_only | id src_aebf5c7a43
- [Decoherence rate in random Lindblad dynamics](https://arxiv.org/abs/2402.04705v3) | arXiv | 2024-02-07 | retrieved 2026-11-10 | abstract_only | id src_67e9b52016
- [Overcoming leakage in quantum error correction](https://doi.org/10.1038/s41567-023-02226-w) | OpenAlex | 2023-10-05 | retrieved 2026-11-10 | abstract_only | id src_7c98bcb9a8
- [Quantum Error Correction For Dummies](https://doi.org/10.1109/qce57702.2023.00017) | OpenAlex | 2023-09-17 | retrieved 2026-11-10 | abstract_only | id src_fff72088a9
- [Introduction to quantum error correction and fault tolerance](https://doi.org/10.21468/scipostphyslectnotes.70) | OpenAlex | 2023-06-12 | retrieved 2026-11-10 | abstract_only | id src_789d3ecd8d
- [Real-time quantum error correction beyond break-even](https://doi.org/10.1038/s41586-023-05782-6) | OpenAlex | 2023-03-22 | retrieved 2026-11-10 | metadata_only | id src_3ee790e4ad
- [Quantum Error Correction with Quantum Autoencoders](https://doi.org/10.22331/q-2023-03-09-942) | OpenAlex | 2023-03-09 | retrieved 2026-11-10 | abstract_only | id src_31eadc54ac
- [A lower bound on the overhead of quantum error correction in low dimensions](https://doi.org/10.48550/arxiv.2302.04317) | OpenAlex | 2023-02-08 | retrieved 2026-11-10 | abstract_only | id src_631d3a610f

## Gaps, limitations and errors
- Missing data: No price and timing (T) findings, so valuation and stretched-stock risk is not assessed
- Missing data: No evidence of paying customers, contracts or revenue attributable to error correction
- Missing data: No supply-chain or manufacturing evidence (components, cryogenics, control electronics, fabs)
- Missing data: No peer-reviewed independent replication of below-threshold, leakage or decoder results beyond the cited papers
- Missing data: No hardware demonstrations of logical gates below threshold, qLDPC codes, hyperbolic codes or learned encodings
- Missing data: Normalised research-growth figures (OpenAlex counts are not adjusted for overall publishing growth)
- Missing data: Verified financials for most named companies (Google, IBM and other non-SEC names have no financial data; Quantinuum and Xanadu data come only from selected filing excerpts)
- Missing data: Patents are filtered imperfectly: classical fault-tolerant patents contaminate the counts, and grant or quality status is unknown
- Limitation: Based only on supplied findings, mostly paper abstracts and short filing excerpts; no full-text review
- Limitation: X findings are social signals and unverified; market headlines were not read
- Limitation: Research and patent counts measure activity, not quality or commercial value, and the recent-year patent counts are undercounted by publication delay
- Limitation: Many cited papers are non-peer-reviewed preprints and simulation studies
- Limitation: The company list is limited to those named in the findings and is not exhaustive; smaller companies carry more risk and less disclosure
- Limitation: This is a research assessment, not investment advice, and contains no price targets or recommendations; all forward-looking statements are forecasts
- Chief review gap: Evidence is heavily weighted toward superconducting surface-code and bosonic GKP platforms; trapped-ion, neutral-atom, and photonic QEC progress is underrepresented in the science findings (only R4 touches trapped ions, M4 touches photonics).
- Chief review gap: The 'beyond break-even' results (S1, S2, S4) demonstrate logical memory lifetime exceeding physical qubit lifetime, but the gap to full fault-tolerant computation (arbitrary circuits, logical gates) is not directly addressed by any single finding; the report must be careful not to overstate readiness.
- Chief review gap: Decoder performance at large code distances (d≥9) is not well characterized; S2 gives 63 µs latency at d=5 but no data at the distances needed for practical fault tolerance.
- Chief review gap: Most overhead-reduction and alternative-code results (R3, R5, S7) are simulation-based or extrapolated, not hardware-validated; this is noted in the findings but the report should make the simulation-to-hardware gap explicit.
- Chief review gap: X findings are all unverified social signals and cannot be used as factual evidence in the report.
- ERROR [timing/Alpha Vantage]: XNDU: Alpha Vantage limit or notice: We have detected your API key as *** and our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphava
- ERROR [timing/Alpha Vantage]: QNT: Alpha Vantage limit or notice: We have detected your API key as *** and our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphava

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 2 | 6142 | 2523 | 0.00365 |
| x | z-ai/glm-5.3-flash | 1 | 4419 | 1625 | 0.00117 |
| patent | Qwen/Qwen3.6-35B-A3B-FP8 | 1 | 7906 | 8620 | 0.01069 |
| science | deepseek/deepseek-v4.1-flash | 1 | 4564 | 3282 | 0.00531 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 22247 | 9319 | 0.13768 |
| market | z-ai/glm-5.3 | 1 | 2219 | 1305 | 0.00977 |
| investment | anthropic/claude-sonnet-5-5 | 1 | 14458 | 9721 | 0.12613 |
| x (data) | X API pay-per-use | 7 | 0 | 0 | 0.09000 |

Total estimated cost: $0.38440 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
