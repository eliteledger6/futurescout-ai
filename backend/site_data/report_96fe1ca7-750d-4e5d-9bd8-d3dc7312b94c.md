# FUTURESCOUT AI research report: backside power delivery

Generated: 2026-11-10 04:16 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, patent, timing, scout, investment
- Agents NOT run in this version: x. Conclusions therefore have no social-media evidence.

## Verdict (forecast, computed from the report)
**Building: real activity, not yet proven commercially** — score 63.3, confidence low.
Qualifiers: low confidence 40%, below the 70% that counts as confident.

Backside power delivery moves a chip's power wiring to the underside of the silicon so the top side has more room for signals. Intel says it has started using this in its newest manufacturing process, and research interest keeps growing. The main thing that could hold it back is heat and the difficulty of building…

Why:
- Research Momentum rated 4/5: Code-computed OpenAlex counts rose from 48 (2024) to 77 (2025), +60.4%.
- Technical Feasibility rated 4/5: Intel reports measured silicon gains on Intel 4 (>30% droop improvement, 6% frequency) and states 18A uses PowerVia in volume manufacturing [S1, M1].
- Papers 2024→2025: 48→77 (+60%)
- So far in 2026 (to 10-11): 85 papers vs 60 by the same date in 2025 (+42%, rising)

Watch out for:
- Thermal resistance and non-uniform workload hotspots may offset power-delivery gains, though the supporting evidence is simulation-based [S2, S3, C1, C2].
- Signal-integrity degradation from removing frontside shielding and limited backside routing resources [S6, S5, C4].
- Several enabling results are single-group demonstrations, preprints or title-only sources with thin evidence [R2, R3, C5].
- Failure analysis and debug are flagged bottlenecks, and a dual-sided future would stretch them further [R1, R6, S10].

What would change this view:
- Stronger if: Independent or additional measured-silicon results on 18A, including gate-all-around devices, that confirm the droop and frequency gains [S1, C7].
- Weaker if: Measured silicon showing that thermal or signal-integrity penalties outweigh power-delivery benefits in production designs [S3, S6, S2].
- Stronger if: Peer-reviewed or silicon-validated demonstrations of nTSV/BPR co-integration, low-distortion bonding or embedded cooling [R2, C5, C6].
- Weaker if: Evidence that wafer thinning, bonding distortion or nTSV/BPR integration cannot reach acceptable yield [R2, R3, S7].

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
Research on backside power delivery is still growing: OpenAlex works rose from 48 in 2024 to 77 in 2025, and 85 so far in 2026 against 60 at the same date in 2025 (+41.7%). The strongest commercial evidence is Intel's own 10-K, which says Intel 18A introduces backside power (PowerVia) in high-volume manufacturing and will be used across multiple generations of its CPUs [M1, M2, M4]. The only measured-silicon result is a single-vendor, self-reported Intel 4 test showing a >30% voltage droop improvement and a 6% frequency gain [S1, C7]. Most of the evidence on thermal, clocking and signal-integrity penalties is simulation or preprint work, and several earlier findings were challenged as overstated [S2, S3, S4, C1, C2, C4, C6]. Open manufacturing and failure-analysis issues remain [S7, S10, R1, R2, R3, R4]. Patent filings are broad across logic, memory and equipment players [P1, P3, P4], but year-to-date filings are down 17.7% (partly publication lag). Intel's share price has fallen sharply and is highly volatile [T1, T2]. Evidence of external customers, yields, cost and competitor timing is missing, and the X agent did not run.

## Technology Opportunity Score
**Opportunity score: 63.3 / 100** · **Confidence: 40%** (low; evidence 58% x risk multiplier 0.7) · evidence coverage 90%

Risk: rating 3/5 does not change the score; it multiplies confidence by 0.7.

Commercialization Gap (research momentum rating minus commercial readiness rating): +1


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 4 | S2, S4, S7, S11, C4 | Code-computed OpenAlex counts rose from 48 (2024) to 77 (2025), +60.4%. Year to date 2026 is 85 versus 60 (+41.7%, rising), so momentum is still building. The count is not normalised for overall publishing growth, and research activity does not equal commercial success. Cited findings show the research agenda is broad (thermal, clocking, manufacturing, failure analysis), though many are simulation or preprint results. |
| Patent Momentum | 10% | 3 | P1, P2, P3, P4, P5 | Code-computed counts are 237 (2024) and 233 (2025), -1.7%, and 153 versus 186 year to date (-17.7%, cooling), though recent years are undercounted by publication delay. Filings are broad across 3D stacks, standard cells, equipment, substrates and application-specific designs, so the level is high but growth has flattened. |
| Technical Feasibility | 15% | 4 | S1, M1, C7, S7, R2, C1, C2, C4 | Intel reports measured silicon gains on Intel 4 (>30% droop improvement, 6% frequency) and states 18A uses PowerVia in volume manufacturing [S1, M1]. Caveats: a single-vendor self-reported result [C7], and thermal, signal-integrity, failure-analysis and process-integration issues remain open, largely evidenced by simulation [S2, S3, S6, S10, R2, C1, C2, C4]. |
| Commercial Readiness | 15% | 3 | M1, M2, M5 | Intel's 10-K states 18A includes backside power as an industry first in high-volume manufacturing and will underpin multiple CPU generations [M1, M2]. The findings contain no yield, shipment, revenue or cost data attributable to backside power, and no other manufacturer is shown in production [M5]. |
| Customer Adoption | 10% | missing | none | no valid 0-5 rating given |
| Industry Investment | 10% | 3 | M1, M4, K1, P1, P3, M5, T1 | Intel is investing across 18A and plans for 14A, with R&D at 26.1% of revenue [M1, M4, K1]. Patent filings come from logic, memory and equipment firms [P1, P3, K4, K5, K6]. Of the companies whose filings were checked, only Intel's mention the topic [M5], and Intel's financial stress shown in its share price is a caveat [T1]. |
| Competitive Position | 10% | 3 | M1, M4, M5, K4, K5 | Intel claims an industry first in high-volume backside power [M1] and is extending it to later nodes [M4]. TSMC, Micron and others hold related patents [K4, K5], but their filings do not mention it [M5], so competitor timing is unknown. The lead is claimed by Intel itself and not independently verified. |
| Supply-Chain Readiness | 15% | 2 | P3, K6, K3, R2, R3, R4, C5 | Equipment and materials suppliers are patenting enabling processes [P3, K6, K3], but integration issues remain: nTSV/BPR co-integration, slow thinning, no consensus on Ru versus Mo, and bonding distortion with only partial mitigation [R2, R3, R4, C5]. No supplier revenue or capacity evidence is present. |

Formula: score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a validated prediction of stock performance; confidence is not a probability of profit.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Backside power as a leading-edge logic feature (Intel 18A first)

Technologies: backside power delivery network (BSPDN), Intel PowerVia, gate-all-around / RibbonFET logic nodes

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Intel's 10-K (filed 2026-01-23) states 18A with PowerVia is its high-volume process and will serve multiple generations of client and server CPUs [M1, M2]. Measured benefits come from one Intel 4 test [S1, C7]. The findings contain no yield, shipment volume or external customer data, so the pace of the ramp is unverified. Intel's share price is down 43.3% over one month with very high volatility, which adds timing risk [T1, T2]. *(forecast)* [M1, M2, S1, C7, T1, T2] | medium |
| medium_1_3y | Intel says it is extending backside power into future nodes, pairing it with high-NA EUV for 14A development [M4]. Patent activity from several firms suggests others are pursuing the approach [P1, K4, K5]. The retrieved filings of TSMC, Micron and other companies do not mention the topic, so competitor deployment timing is not shown [M5]. Whether others adopt backside power on a comparable schedule is therefore unsupported by the findings. *(forecast)* [M4, M5, P1, K4, K5] | low |
| long_3_5y | Dual-sided ('Flip 3D') integration and backside clock/signal allocation are explored, but only through a non-peer-reviewed test vehicle and two simulation-only preprints [R6, S4, C4]. The evidence says little about this horizon beyond Intel's multi-generation intent [M2]. Research activity is not proof of commercial success. *(forecast)* [R6, S4, C4, M2] | low |

**Bull case:** Intel's 18A ramp delivers the reported power-integrity and frequency gains in volume [M1, S1]. Backside power becomes a standard feature that other manufacturers also adopt, as patent activity from logic and memory firms hints [P1, K4, K5]. *(forecast)* [M1, S1, P1, K4, K5]

**Base case:** Intel uses PowerVia across several CPU generations [M2, M4] while thermal, signal-integrity and test costs limit the net benefit to some designs [S2, S6, C1, C2]. Wider adoption stays uncertain and depends on evidence not yet in the findings [M5]. *(forecast)* [M2, M4, S2, S6, C1, C2, M5]

**Bear case:** Thermal penalties in realistic workloads, failure-analysis cost or process-integration problems erode the benefit [S3, S10, R1, R2]. Intel's weak share price shows financial stress that could affect its ability to fund the roadmap [T1, T2]. Benefit claims rest on one self-reported measurement [C7] and some loosely sourced claims [R7]. *(forecast)* [S3, S10, R1, R2, T1, T2, C7, R7]

**Catalysts:**
- Independent or additional measured-silicon results on 18A, including gate-all-around devices, that confirm the droop and frequency gains [S1, C7]. *(forecast)* [S1, C7]
- Evidence of external customers or competitors committing to backside power, which the findings do not yet show [M5, M2]. *(forecast)* [M5, M2]
- Progress on Intel 14A with high-NA EUV and backside power [M4]. *(forecast)* [M4]

**Risks:**
- Thermal resistance and non-uniform workload hotspots may offset power-delivery gains, though the supporting evidence is simulation-based [S2, S3, C1, C2]. *(ai_interpretation)* [S2, S3, C1, C2]
- Signal-integrity degradation from removing frontside shielding and limited backside routing resources [S6, S5, C4]. *(ai_interpretation)* [S6, S5, C4]
- Related stock timing risk: Intel is 39.0% below its 50-day average with 140.4% annualised 20-day volatility. The 'subdued' timing label reflects no run-up, not low risk [T1, T2]. *(ai_interpretation)* [T1, T2]
- Concentration: only Intel's filing evidence mentions the technology in production, so the case leans on one company's statements [M5, M1]. *(ai_interpretation)* [M5, M1]

**What would invalidate this thesis:**
- Measured silicon showing that thermal or signal-integrity penalties outweigh power-delivery benefits in production designs [S3, S6, S2]. *(assumption)* [S3, S6, S2]
- Evidence of poor yield, delay or retreat from backside power on 18A or later Intel nodes [M1, M2, M4]. *(assumption)* [M1, M2, M4]

**Conflicting evidence:**
- S1 is the only measured-silicon result: a single-vendor, self-reported figure on one E-core on a finFET node and compared with 'a similar design'. Most risk evidence is simulated, so measured benefits are not weighed against modeled penalties [C7]. *(ai_interpretation)* [S1, C7]
- The thermal-penalty claim is thinner and more mixed than 'recurring' implies: a device-level paper finds parasitics dominate over self-heating and backside contacts suppress self-heating [S2, S9, C2]. The non-uniform-workload penalty comes from one non-peer-reviewed simulation preprint [S3, C1]. *(ai_interpretation)* [S2, S9, S3, C1, C2]
- The backside clock-mesh and signal-integrity findings come from two simulation-only 2026 preprints, not silicon [S4, S5, S6, C4]. *(ai_interpretation)* [S4, S5, S6, C4]
- Patent publications cooled year to date (-17.7%) while research output rose, which sends mixed momentum signals [P1, P4]. *(ai_interpretation)* [P1, P4]

**Companies named by cited evidence:**
- Intel Corp (INTC): States in its 10-K that 18A introduces backside power in high-volume manufacturing. Also an assignee on 2 retrieved patents and affiliated with 2 retrieved papers; fiscal 2025 revenue 52.85B USD with R&D 26.1% of revenue; the share price has fallen sharply with extreme volatility. This is not a recommendation. [M1, M2, K1, T1, T2]
- Taiwan Semiconductor Manufacturing Co Ltd (TSM): Named as assignee on 3 retrieved patent publications on backside power; its retrieved filings do not mention the topic, so deployment timing is unknown. [K4, M5]
- Micron Technology Inc (MU): Assignee on 3 retrieved patent publications, including a memory-related refresh patent and a hybrid device with backside power delivery networks; its filings retrieved do not mention the topic. [K5, M5]

### Enablers and mitigation: wafer thinning, bonding, materials, thermal design and failure analysis

Technologies: wafer thinning, wafer-to-wafer bonding, nano-TSVs and buried power rails, backside thermal/microfluidic cooling, failure analysis tools

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Equipment and materials suppliers are filing patents on fabrication processes and substrates [P3, K3, K6]. Integration is still described as difficult: buried-power-rail/nTSV co-integration has unresolved interface and alignment issues, and thinning is slow and wears consumables [R2, R3]. Failure analysis is degraded and costly rather than blocked [S10, C3, R1]. *(forecast)* [P3, K3, K6, R2, R3, S10, C3, R1] | medium |
| medium_1_3y | Partial progress exists, such as sub-10 nm residual grid distortion in a low-distortion bonding approach [C5]. No consensus on backside metal (Ru versus Mo) is visible, and each has hard-metal processing problems [R4]. Backside cooling proposals are modeled, not shown in hardware [S8, C6]. The evidence does not show whether these will be solved on a useful timescale. *(forecast)* [C5, R4, S8, C6] | low |
| long_3_5y | Thermal modeling of 3D stacks with backside power remains immature (accurate transient simulation including BEOL is open), and dual-sided integration would add complexity [S11, R6]. The cited evidence is silent on commercial outcomes this far out. *(forecast)* [S11, R6] | low |

**Bull case:** Bonding, thinning and contact processes mature, with partial results already reported [C5], and suppliers' patenting [P3] turns into tooling and materials demand as backside power spreads. Co-designed cooling reaches hardware [S8]. *(forecast)* [C5, P3, S8]

**Base case:** Process steps improve incrementally while thermal, thinning and metal-choice questions stay open [R2, R3, R4, S11]. Failure-analysis methods adapt at higher cost [S10, C3]. *(forecast)* [R2, R3, R4, S11, S10, C3]

**Bear case:** Manufacturing integration, thermal management or test costs prove too high and limit adoption outside a few products [R1, R2, R3, S3]. Supplier patents do not become revenue [P3]. *(forecast)* [R1, R2, R3, S3, P3]

**Catalysts:**
- Peer-reviewed or silicon-validated demonstrations of nTSV/BPR co-integration, low-distortion bonding or embedded cooling [R2, C5, C6]. *(forecast)* [R2, C5, C6]
- Convergence on a backside metal choice [R4]. *(forecast)* [R4]

**Risks:**
- Several enabling results are single-group demonstrations, preprints or title-only sources with thin evidence [R2, R3, C5]. *(ai_interpretation)* [R2, R3, C5]
- Failure analysis and debug are flagged bottlenecks, and a dual-sided future would stretch them further [R1, R6, S10]. *(ai_interpretation)* [R1, R6, S10]
- No BPDN-specific quantification of thermal or reliability penalties exists in the retrieved abstracts [R5]. *(ai_interpretation)* [R5]

**What would invalidate this thesis:**
- Evidence that wafer thinning, bonding distortion or nTSV/BPR integration cannot reach acceptable yield [R2, R3, S7]. *(assumption)* [R2, R3, S7]
- Evidence that backside power is being abandoned for the designs these suppliers target [M2, M4]. *(assumption)* [M2, M4]

**Conflicting evidence:**
- S7 lists manufacturing constraints as open problems but cites a title-only source. The bonding paper also reports partial progress (sub-10 nm residual distortion) [S7, C5]. *(ai_interpretation)* [S7, C5]
- Failure analysis is described as made obsolete or degraded [S10], but the same source reviews methods that still apply, and OBIRCH has been demonstrated on a BSPDN structure [C3]. *(ai_interpretation)* [S10, C3]
- Cooling 'co-design' rests on modeling proposals, not fabricated hardware [S8, C6]. *(ai_interpretation)* [S8, C6]

**Companies named by cited evidence:**
- Applied Materials Inc (AMAT): Assignee on 2 retrieved patent publications, including semi self-aligned contact fabrication for backside power delivery; large company (fiscal 2025 revenue 28.37B USD, growth +4.4%). Patents are claims, not proof of revenue. [K6, P3]
- Microchip Technology Inc (MCHP): Assignee on 2 retrieved patents on a polySiC wafer base with power and ground rails; mid-sized (fiscal 2025 revenue 4.71B USD, growth +7.1%). Link to commercial backside power products is not shown. [K3, P3]
- Adeia Inc. (ADEA): Small company (fiscal 2025 revenue 0.44B USD, growth +17.9%) with 2 retrieved patent publications titled 'Backside Power Delivery'. Smaller companies carry more risk and less disclosure; the heuristic score is not a prediction of returns. [K2]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 2, 2021: 4, 2022: 13, 2023: 23, 2024: 48, 2025: 77, 2026: 87}
Research Acceleration 2024->2025: 48 -> 77 (60.4% YoY). OpenAlex works whose title or abstract contains any of the exact phrases "backside power delivery", "backside power", "BSPDN", "backside power distribution network", per publication year (singular and plural forms match; each work counted once). The synonyms and abbreviations were kept only after an AI check of sampled papers. The number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-11): 2025 60 -> 2026 85 (41.7%, trend: rising). OpenAlex works with any of the exact phrases "backside power delivery", "backside power", "BSPDN", "backside power distribution network" in title or abstract published 1 Jan–11 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence medium)* Intel's PowerVia backside power delivery, implemented on the Intel 4 finFET process, is reported to deliver a >30% platform voltage droop improvement and a 6% frequency benefit versus a comparable design without it.
  - source: [Intel PowerVia Technology: Backside Power Delivery for High Density and High-Performance Computing](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208) (OpenAlex, 2023-06-11, abstract_only)
  - excerpt: "A fabricated E-core with $\gt 90$% cell utilization showed $\gt 30$% platform voltage droop improvement and 6% frequency benefit compared to a similar design without PowerVia."
  - reasoning: Single conference paper abstract reporting silicon-level measurements; the result is specific and quantitative but comes from one group and one process node.
- **[S2]** *(verified_fact, confidence medium)* A recurring counterweight in the literature is that BSPDN increases thermal resistance between the on-chip power grid and cooling, so power-delivery gains come with a cooling problem.
  - source: [Thermal Mitigation Strategy for Backside Power Delivery Network](https://doi.org/10.1109/ectc51529.2024.00241) (OpenAlex, 2024-05-28, abstract_only)
  - source: [Modeling of Backside Power Delivery and Thermal Management in Semiconductor Die Packages](https://doi.org/10.1109/itherm55375.2024.10709612) (OpenAlex, 2024-05-28, abstract_only)
  - source: [Thermal Impacts of Backside Power Delivery Networks on GAAFET Technology](https://doi.org/10.1109/ted.2025.3569614) (OpenAlex, 2025-05-22, abstract_only)
  - excerpt: "it also brings thermal challenges due to a significantly larger thermal resistance between the CPU power grid and on-chip forced cooling."
  - reasoning: Three abstracts independently frame thermal dissipation as the principal trade-off of moving the power network to the wafer backside.
- **[S3]** *(verified_fact, confidence medium)* Under realistic non-uniform workloads in 3D/2.5D chiplet packages, backside power delivery can show pronounced thermal penalties relative to frontside delivery because of limited lateral heat spreading, an effect that uniform-power simulations hide.
  - source: [Thermal Implications of Non-Uniform Power in BSPDN-Enabled 2.5D/3D Chiplet-based Systems-in-Package using Nanosheet Technology](https://arxiv.org/abs/2508.02284v1) (arXiv, 2025-08-04, abstract_only)
  - excerpt: "BSPDN configurations in 3D, although beneficial in simplified uniform scenarios, exhibit pronounced thermal penalties under realistic, localized workloads due to limited lateral heat spreading."
  - reasoning: Preprint (not peer reviewed) with high-resolution thermal simulation results; single source, so confidence is capped at medium.
- **[S4]** *(ai_interpretation, confidence medium)* Research has moved beyond power-only BSPDN to jointly allocating scarce backside metal between clock and signal nets, because backside routing resources are limited and must be partitioned.
  - source: [Design Space Exploration of Backside Clock Meshes for 2 nm GAAFET BSPDN Technology](https://arxiv.org/abs/2610.02401v1) (arXiv, 2026-10-01, abstract_only)
  - source: [CSCO: A Backside-PDN-Aware Clock-Signal Co-Optimization Framework for Improved PPA](https://arxiv.org/abs/2607.13700v1) (arXiv, 2026-07-15, abstract_only)
  - excerpt: "Backside power delivery networks (BSPDN) have emerged as a promising technology for advanced logic nodes to address IR-drop and PPA challenges."
  - reasoning: Two independent arXiv preprints (cs.AR and cs.CE) both treat backside wiring as a contested resource rather than a free bonus. Both are preprints and neither reports foundry silicon, so this is a design-methodology trend, not a manufacturing claim.
- **[S5]** *(verified_fact, confidence medium)* Backside clock meshes are reported to outperform identical frontside meshes in 2 nm GAAFET exploration, but they cannot drive frontside flip-flops directly and every connection must pass through a through-silicon via.
  - source: [Design Space Exploration of Backside Clock Meshes for 2 nm GAAFET BSPDN Technology](https://arxiv.org/abs/2610.02401v1) (arXiv, 2026-10-01, abstract_only)
  - excerpt: "Across all four designs, the backside mesh consistently outperforms an identical frontside mesh, with on average 45% lower skew, 25% lower sink slew, 4.5% lower power, and 28% less frontside clock wiring"
  - reasoning: Single arXiv preprint using multi-objective Bayesian optimization on four benchmarks with SPICE verification; results are simulation, not silicon, and the abstract notes the cyclic mesh cannot be evaluated by static timing analysis.
- **[S6]** *(verified_fact, confidence low)* Removing frontside power-ground shielding in a BSPDN introduces signal-integrity degradation, including coupling noise and crosstalk, which designers are attempting to mitigate using backside routing itself.
  - source: [CSCO: A Backside-PDN-Aware Clock-Signal Co-Optimization Framework for Improved PPA](https://arxiv.org/abs/2607.13700v1) (arXiv, 2026-07-15, abstract_only)
  - excerpt: "lacking frontside power-ground shielding, BSPDN introduces severe signal integrity (SI) degradation."
  - reasoning: One preprint asserts the problem and proposes co-optimization as the fix; no independent confirmation in this set.
- **[S7]** *(verified_fact, confidence medium)* Backside power delivery imposes manufacturing constraints that are themselves research topics: extreme wafer thinning, wafer-to-wafer bonding without residual stress or high-order shape change, and backside lithography correction for bonding-induced wafer distortion.
  - source: [Nano-Through Silicon Vias (nTSV) for Backside Power Delivery Networks (BSPDN)](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185227) (OpenAlex, 2023-06-11, abstract_only)
  - source: [Low Distortion Fusion Bonding using Pneumatically Warped Wafers](https://arxiv.org/abs/2606.04625v1) (arXiv, 2026-06-03, abstract_only)
  - source: [Backside Power Delivery Process Integration Challenges](https://doi.org/10.7567/ssdm.2024.c-4-01) (OpenAlex, 2024-09-03, metadata_only)
  - excerpt: "Key technology challenges are the extreme wafer thinning required and back-side lithography correction to correct for wafer distortions caused by wafer processing and W2W bonding."
  - reasoning: A VLSI conference paper plus an ECTC preprint both describe bonding and distortion as gating process issues. The third source (src_b1bae9c128) is titled on process integration challenges but has no abstract, so it is cited only as corroborating the topic's existence, not for any specific claim.
- **[S8]** *(verified_fact, confidence medium)* Cooling is being co-designed with the power network itself, for example embedded microchannel or microfluidic channels placed on the die backside alongside the backside power delivery network.
  - source: [Thermal Mitigation Strategy for Backside Power Delivery Network](https://doi.org/10.1109/ectc51529.2024.00241) (OpenAlex, 2024-05-28, abstract_only)
  - source: [Modeling of Backside Power Delivery and Thermal Management in Semiconductor Die Packages](https://doi.org/10.1109/itherm55375.2024.10709612) (OpenAlex, 2024-05-28, abstract_only)
  - excerpt: "We propose a synergistic integration of microfluidic channels with power delivery on the backside of semiconductor dies"
  - reasoning: Two independent conference papers (ECTC and I-THERM) in the same year propose backside fluidic cooling for BSPDN, suggesting a converging direction rather than an isolated idea. Both report modeling/FEA, not measured packaged parts.
- **[S9]** *(verified_fact, confidence low)* The choice of backside connection architecture matters thermally: backside contacts are reported to suppress self-heating and parasitic effects better than through-silicon vias placed in the middle-of-line.
  - source: [Thermal Impacts of Backside Power Delivery Networks on GAAFET Technology](https://doi.org/10.1109/ted.2025.3569614) (OpenAlex, 2025-05-22, abstract_only)
  - excerpt: "Evaluation results indicate that backside contacts (BSCs) are more capable of suppressing SHEs and parasitic effects, while through silicon via in middle-of-line (MOL) (TSVM)-based circuits experience pronounced performance degradation"
  - reasoning: One journal paper using SPICE-compatible models; a design guideline derived from modeling rather than measured silicon.
- **[S10]** *(verified_fact, confidence medium)* Backside power delivery disrupts established failure analysis: many electrical fault isolation techniques are made obsolete and others severely degraded by the presence of the backside network.
  - source: [Leading Edge Technologies: Backside Power Delivery](https://doi.org/10.31399/asm.tb.edfastr.t56090091) (OpenAlex, 2023-11-01, abstract_only)
  - excerpt: "The obstruction created by the presence of BPD networks obsoletes many of the electrical fault isolation (EFI) techniques that have been used for the past few decades and severely degrades the performance of others."
  - reasoning: A book chapter reviewing EFI methods; the claim is qualitative but clearly stated and not contradicted by other papers here.
- **[S11]** *(verified_fact, confidence medium)* Thermal modeling of backside power delivery in 3D stacks is immature: homogenization works for steady state, but accurate 3D transient simulation that includes BEOL structures remains an open challenge.
  - source: [Transient Multiscale Workflow for Thermal Analysis of 3DHI Chip Stack](https://arxiv.org/abs/2605.00399v1) (arXiv, 2026-05-01, abstract_only)
  - source: [Modeling of Backside Power Delivery and Thermal Management in Semiconductor Die Packages](https://doi.org/10.1109/itherm55375.2024.10709612) (OpenAlex, 2024-05-28, abstract_only)
  - source: [Thermal Implications of Non-Uniform Power in BSPDN-Enabled 2.5D/3D Chiplet-based Systems-in-Package using Nanosheet Technology](https://arxiv.org/abs/2508.02284v1) (arXiv, 2025-08-04, abstract_only)
  - excerpt: "Multiscale homogenization strategies have been demonstrated to be effective for steady-state simulations, however accurate 3D transient simulations that include BEOL structures remain an open challenge."
  - reasoning: An arXiv preprint states the gap explicitly; the other two sources describe homogenization-based workflows that implicitly confirm the computational-complexity barrier. Preprints are not peer reviewed.

**Emerging directions:**
- Backside clock meshes using spare thick backside metal on 2 nm GAAFET nodes
- Joint clock/signal allocation and shielding-aware co-optimization frameworks for limited backside routing
- Embedded microchannel or microfluidic cooling co-integrated with the backside power network
- nano-TSV 'last' and 'first' integration flows at standard-cell granularity
- Transient, multi-scale BEOL thermal homogenization from GDSII/OASIS layouts
- Low-distortion, force-free wafer-to-wafer fusion bonding for backside lithography

**Open problems:**
- Trade-off space between backside resources allocated to clock versus signal nets under IR-drop and congestion constraints
- Elevated thermal resistance and limited lateral heat spreading with backside delivery under realistic non-uniform workloads
- Accurate 3D transient thermal simulation including heterogeneous BEOL structures
- Electrical fault isolation and failure analysis on wafers with backside networks
- Wafer distortion and residual stress from bonding and extreme thinning that backside lithography must correct
- Signal-integrity and crosstalk degradation in the absence of frontside power-ground shielding
- Relative merits of backside contacts versus middle-of-line through-silicon vias for self-heating

**Limitations:**
- All conclusions rest on titles and abstracts only; no full text was read.
- One included item (src_b1bae9c128, 'Backside Power Delivery Process Integration Challenges') has no abstract and could not be used for any substantive claim.
- The sample is small (12 items) and heterogeneous: conference papers, a book chapter, a journal article and several arXiv preprints covering design, process, thermal and failure-analysis angles rather than one controlled comparison.
- Four items are arXiv preprints and are not peer reviewed; several of the most specific quantitative results (backside clock mesh, non-uniform-power thermal penalties, transient thermal workflow) come from those preprints.
- Reported quantitative benefits (droop, frequency, skew) come from different designs, nodes and simulation setups and are not directly comparable.
- Papers describe research and simulation results; nothing here establishes commercial deployment, manufacturing yield at scale or market adoption.
- Citation-based filtering may over-represent well-established work (for example Intel PowerVia) relative to newer process-integration work.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['BSPDN yield defect', 'backside power thermal', 'BSPDN cost overhead', 'power delivery network reliability', 'backside power alternative', 'BSPDN process complexity']

- **[R1]** *(ai_interpretation, confidence medium)* Failure analysis and debug are a flagged bottleneck for backside and hybrid-bonded architectures. Backside power delivery networks (BPDNs) add buried structures and block conventional probing access, which complicates fault isolation.
  - source: [Failure Analysis in Transition: An Industry Survey of Challenges, Priorities, and Standardization Needs in Advanced Packaging and Heterogeneous Integration](https://doi.org/10.48550/arxiv.2606.22149) (OpenAlex, 2026-06-20, abstract_only)
  - source: [Inkjet-printed electrical interconnects for high resolution integrated circuit diagnostics](https://doi.org/10.1038/s44172-023-00073-4) (OpenAlex, 2023-05-02, abstract_only)
  - excerpt: "Hybrid bonding emerged as the most difficult new architecture to analyze at 54%"
  - reasoning: The survey (arXiv preprint, not peer reviewed, about 100 self-selected respondents) lists backside technologies among the architectures reshaping failure analysis. Its most specific difficulty finding is about hybrid bonding, not BSPDN. The inkjet paper says FA resolution is limited by probe needles and wire bonds, and it needed a custom printed redistribution layer to analyse a BSPDN structure with OBIRCH. Together they suggest FA workflows for BSPDN are still being invented, but neither abstract quantifies a BSPDN-specific yield or time-to-diagnosis penalty.
- **[R2]** *(verified_fact, confidence medium)* Co-integrating buried power rails (BPRs) and nano-TSVs (nTSVs) is described as difficult, with interfacial instability and tight alignment cited as unresolved challenges. The proposed Ru-based fix is a single-group demonstration.
  - source: [In-situ Co-Integration of Ru-based Buried Power Rails and nTSVs for Advanced Backside Power Delivery](https://doi.org/10.1016/j.chip.2026.100222) (OpenAlex, 2026-09-01, abstract_only)
  - excerpt: "However, the integration of key components like buried power rails (BPRs) and nano-through-silicon vias (nTSVs) faces significant challenges, including interfacial instability and stringent alignment requirements."
  - reasoning: The abstract itself states the challenges. It reports line resistance of 11.4-11.8 Ω/μm and a multiphysics electromigration model that matches experimental failure times. It reports no yield, no statistical spread across wafers and no scale-up data, and the ion-beam thinning-back step replaces polishing, so its manufacturability at volume is not shown. This is one abstract.
- **[R3]** *(ai_interpretation, confidence low)* Wafer thinning for BPDN is an extra process-risk step. The abstracts show hard-material thinning is slow and wears consumables, and one thinning paper is available only as a title.
  - source: [Pre-weakened anodization-assisted rapid thinning of silicon carbide wafers](https://doi.org/10.1016/j.matdes.2026.116697) (OpenAlex, 2026-07-28, abstract_only)
  - source: [Extreme silicon thinning for back side power delivery network: Si thinning stopping on scaled SiGe etch stop layer](https://doi.org/10.1016/j.mee.2024.112246) (OpenAlex, 2024-07-24, metadata_only)
  - excerpt: "directly grinding the SiC substrate was not only time-consuming but also consumed four diamond rough-grinding wheels through severe abrasive wear."
  - reasoning: The SiC paper reports that the baseline direct grinding was slow and consumed four diamond wheels, so a new hybrid anodization process was needed. SiC is mentioned as a thermal-management substrate for sub-3 nm, and BPDN is named only as a possible application. Ultra-thin (75 µm) SiC is not the same as the silicon thinning used in BPDN. The Si-thinning/SiGe etch-stop paper (src_8744718e19) has no abstract, so only its title shows that stopping on a scaled etch-stop layer is a focus of work. Neither abstract gives thickness-uniformity or yield data for BPDN flows.
- **[R4]** *(ai_interpretation, confidence low)* No consensus on the backside and buried power metal is visible. Ru and Mo are both pursued, and each has hard-metal processing problems (polishing for Ru, controlled etching for Mo). This leaves supply-chain and process-maturity risk.
  - source: [In-situ Co-Integration of Ru-based Buried Power Rails and nTSVs for Advanced Backside Power Delivery](https://doi.org/10.1016/j.chip.2026.100222) (OpenAlex, 2026-09-01, abstract_only)
  - source: [Controllable and Nanoscale Linear Etching of Atomic Layer Deposited Molybdenum Using Cyclic Stepwise CHF 3 /O 2 Plasma](https://doi.org/10.1002/smll.76133) (OpenAlex, 2026-10-07, abstract_only)
  - reasoning: The Ru paper says polishing a hard metal is a challenge and works around it with ion-beam thinning-back. The Mo paper presents a cyclic CHF3/O2 etch for Mo films that lists BPDN among several target applications, alongside interconnects and 3D NAND. It reports blanket-film etch linearity and roughness, not patterned-structure or integration results. Both are early-stage lab results (the Mo paper has 0 citations), so this is an inference about fragmentation, not evidence of failure. The timing is a judgement.
- **[R5]** *(ai_interpretation, confidence low)* Reliability, thermal and security concerns are described as increasingly shaping architecture and packaging choices. The abstracts provide no BPDN-specific quantification of thermal or reliability penalties, which is an evidence gap.
  - source: [Focus Session: Advanced CMOS and 5.5D Packaging: Perspectives and Challenges for Design, Reliability and Security](https://doi.org/10.23919/date69613.2026.11539746) (OpenAlex, 2026-04-20, abstract_only)
  - source: [Pre-weakened anodization-assisted rapid thinning of silicon carbide wafers](https://doi.org/10.1016/j.matdes.2026.116697) (OpenAlex, 2026-07-28, abstract_only)
  - reasoning: The DATE focus session (conference abstract) states the need for electrical, thermal, mechanical and reliability analysis in advanced CMOS and 5.5D packaging, and does not mention BPDN in its abstract. The SiC paper notes demand for thermal management in sub-3 nm architectures. Neither shows a measured BPDN heat-removal or electromigration problem. This should be read as an unquantified risk area, not a demonstrated failure.
- **[R6]** *(ai_interpretation, confidence low)* Dual-sided ('Flip 3D') integration is a possible next step beyond power-only backside use, but it rests on a non-peer-reviewed FinFET test vehicle. It would add complexity and further stretch failure-analysis and process readiness.
  - source: [Unifying Heterogeneous and Monolithic Integration via Dual-sided 3D Technology](https://doi.org/10.21203/rs.3.rs-8891286/v1) (OpenAlex, 2026-03-02, abstract_only)
  - source: [Failure Analysis in Transition: An Industry Survey of Challenges, Priorities, and Standardization Needs in Advanced Packaging and Heterogeneous Integration](https://doi.org/10.48550/arxiv.2606.22149) (OpenAlex, 2026-06-20, abstract_only)
  - reasoning: The Research Square preprint is not peer reviewed. It claims the scheme solves the 'computing', 'memory' and 'connectivity' walls on the basis of a FinFET test vehicle, and its abstract is truncated. It reports no yield, cost or thermal data. Whether this would displace or merely extend BPDN is unknown. The link to survey-reported FA difficulty is my inference.
- **[R7]** *(unverified_claim, confidence low)* Some retrieved papers overstate or loosely report BPDN-adjacent benefits and schedules: a '12% energy efficiency' figure and a 2025 production date are cited without sourcing in the abstract, and a 2D-material CFET roadmap is framed as an expected enabler.
  - source: [Breaking Physics Limits: How 2nm Chip Technology Powers Next-Gen 3D ICs](https://doi.org/10.63995/brit1756) (OpenAlex, 2025-02-16, abstract_only)
  - source: [Enabling the Angstrom Era: 2D material-based multi-bridge-channel complementary field effect transistors](https://doi.org/10.1038/s41699-025-00591-z) (OpenAlex, 2025-08-02, abstract_only)
  - reasoning: src_0a3405b8e0 is a general overview with promotional wording ('breakthrough', 'revolutionary'). It does not isolate the contribution of backside power from the 2nm node as a whole, and its 12% figure and TSMC timing are not backed by data in the abstract. src_27b9f0d6ea is a review whose benefits are 'expected', and BPDN is not mentioned in its abstract. Neither is primary evidence for BPDN performance or schedule.

**Possible hype:**
- 'Breaking Physics Limits' / 'revolutionary' 2nm framing: promotional wording, a single efficiency figure (12%) not attributed to backside power, and no data in the abstract.
- 'Provides effective solution to the computing, memory and connectivity walls' (Flip 3D): a broad claim from a FinFET test vehicle in a non-peer-reviewed preprint.
- 'Expected to enable ultra-small, energy-efficient... devices' (2D-material CFET review): a forward-looking roadmap, not demonstrated BPDN-relevant performance.
- 'Promising pathway' / 'robust integration strategy' language in the Mo etch and Ru BPR papers: results are lab-scale and report no yield or volume-manufacturing data.

**Challenges to the Science findings:**
- Targets ['S3'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S3 is stated more broadly than its single source supports. The source is one non-peer-reviewed arXiv preprint based only on thermal simulation. S3 extends the finding to "3D/2.5D chiplet packages", but the abstract reports BSPDN penalties for 3D configurations and says only that benefits hold in simplified uniform scenarios. No measured silicon data back it. The finding also gives no magnitude of the penalty.
    - source: [Thermal Implications of Non-Uniform Power in BSPDN-Enabled 2.5D/3D Chiplet-based Systems-in-Package using Nanosheet Technology](https://arxiv.org/abs/2508.02284v1) (arXiv, 2025-08-04, abstract_only)
    - excerpt: "BSPDN configurations in 3D, although beneficial in simplified uniform scenarios, exhibit pronounced thermal penalties under realistic, localized workloads due to limited lateral heat spreading."
    - reasoning: The abstract scopes the penalty to 3D configurations and to nanosheet technology. S3's "2.5D" wording and its verified_fact label overstate what a single simulation preprint shows. The result should be read as a model-based warning, not an established effect.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S2', 'S9'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S2 says a "recurring" literature finding is that BSPDN increases thermal resistance. Only src_a91300a32b states this, and it is a cooling-proposal paper. The device-level paper src_7762759087 reports that parasitic effects dominate circuit dynamic performance over self-heating. It also finds backside contacts better at suppressing self-heating. src_26b3f5b1fe, as far as its abstract shows, frames backside power as reducing resistance loss and does not claim higher thermal resistance. The evidence is thinner and more mixed than "recurring" implies.
    - source: [Thermal Mitigation Strategy for Backside Power Delivery Network](https://doi.org/10.1109/ectc51529.2024.00241) (OpenAlex, 2024-05-28, abstract_only)
    - source: [Thermal Impacts of Backside Power Delivery Networks on GAAFET Technology](https://doi.org/10.1109/ted.2025.3569614) (OpenAlex, 2025-05-22, abstract_only)
    - excerpt: "parasitic effects dominate circuit dynamic performance compared to self-heating effects (SHEs)"
    - reasoning: Citing src_7762759087 and src_26b3f5b1fe in support of S2 overstates agreement. One abstract states the thermal-resistance claim directly. Another ranks self-heating as secondary to parasitics for circuit speed. Self-heating still worsens HCI and BTI, so the thermal risk is real, but its magnitude is not quantified.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S10'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S10 reports only the negative side of failure analysis. The same chapter reviews EFI methods that remain applicable to BPD ICs: e-beam and atomic force probing, x-ray and magnetic field imaging, and lock-in thermography. The Intel PowerVia abstract also says fault isolation capability is detailed. src_5148be71d2 demonstrates OBIRCH on a BSPDN structure. The finding should be framed as degraded and costly rather than blocked.
    - source: [Leading Edge Technologies: Backside Power Delivery](https://doi.org/10.31399/asm.tb.edfastr.t56090091) (OpenAlex, 2023-11-01, abstract_only)
    - source: [Intel PowerVia Technology: Backside Power Delivery for High Density and High-Performance Computing](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208) (OpenAlex, 2023-06-11, abstract_only)
    - source: [Inkjet-printed electrical interconnects for high resolution integrated circuit diagnostics](https://doi.org/10.1038/s44172-023-00073-4) (OpenAlex, 2023-05-02, abstract_only)
    - excerpt: "This chapter provides an overview of EFI methods that are still applicable to ICs with BPD networks, including e-beam and atomic force probing, x-ray and magnetic field imaging, and lock-in thermography."
    - reasoning: The omission of workable methods inflates the severity of the risk. The chapter itself says it assesses each method's potential for improvement, which S10 does not mention.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S4', 'S5', 'S6'], severity medium:
  - **[C4]** *(ai_interpretation, confidence medium)* S4, S5 and S6 rest on two 2026 arXiv preprints that use EDA and simulation only. The backside clock-mesh result comes from OpenROAD with SPICE on GT2N, a 2 nm nanosheet technology the abstract does not describe as production silicon. The CSCO signal-integrity claims come from the framework's own experiments. None of this is silicon-validated or peer-reviewed. "Research has moved beyond power-only BSPDN" is a trend claim drawn from just two papers. The S5 and S6 "verified_fact" labels do not convey that these are simulated, self-reported gains.
    - source: [Design Space Exploration of Backside Clock Meshes for 2 nm GAAFET BSPDN Technology](https://arxiv.org/abs/2610.02401v1) (arXiv, 2026-10-01, abstract_only)
    - source: [CSCO: A Backside-PDN-Aware Clock-Signal Co-Optimization Framework for Improved PPA](https://arxiv.org/abs/2607.13700v1) (arXiv, 2026-07-15, abstract_only)
    - reasoning: The abstracts report improvements, such as 45% lower skew, on four benchmarks in a research flow. These cannot be generalized to commercial BSPDN nodes. The CSCO abstract asserts "severe" SI degradation as motivation, not as a measured finding. S6 should be treated as a hypothesis and not as an established fact.
- Targets ['S7'], severity low:
  - **[C5]** *(ai_interpretation, confidence high)* S7 cites src_b1bae9c128, which has no abstract and is available as title and metadata only, as support for specific manufacturing constraints. It cannot support them. The thinning and lithography-correction claims are actually backed by src_dbfbe09f9a. The bonding claim is backed by src_f00c9d96cf, which also reports a mitigation: sub-10 nm residual grid distortion with a low-distortion bonding approach. S7 presents the constraints as open problems and leaves out this partial progress.
    - source: [Backside Power Delivery Process Integration Challenges](https://doi.org/10.7567/ssdm.2024.c-4-01) (OpenAlex, 2024-09-03, metadata_only)
    - source: [Low Distortion Fusion Bonding using Pneumatically Warped Wafers](https://arxiv.org/abs/2606.04625v1) (arXiv, 2026-06-03, abstract_only)
    - source: [Nano-Through Silicon Vias (nTSV) for Backside Power Delivery Networks (BSPDN)](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185227) (OpenAlex, 2023-06-11, abstract_only)
    - reasoning: The metadata-only citation inflates the apparent evidence base. The balance of the finding is also skewed towards unsolved problems, even though the bonding abstract describes an evaluated fix.
- Targets ['S8'], severity low:
  - **[C6]** *(ai_interpretation, confidence medium)* S8 says cooling "is being co-designed" with the BSPDN, but both cited sources are proposals backed by finite-element or homogenized numerical modeling. Neither abstract shows fabricated embedded-microchannel BSPDN hardware or measured thermal benefit. Phrased as current practice, this overstates maturity.
    - source: [Thermal Mitigation Strategy for Backside Power Delivery Network](https://doi.org/10.1109/ectc51529.2024.00241) (OpenAlex, 2024-05-28, abstract_only)
    - source: [Modeling of Backside Power Delivery and Thermal Management in Semiconductor Die Packages](https://doi.org/10.1109/itherm55375.2024.10709612) (OpenAlex, 2024-05-28, abstract_only)
    - reasoning: One abstract says "we propose" and describes FEA. The other describes developing a model that "can potentially offer" balanced performance. Both are conceptual and simulation-stage.
- Targets ['S1'], severity low:
  - **[C7]** *(ai_interpretation, confidence medium)* S1 is the only measured-silicon performance result in the findings, and it is a single-vendor, self-reported figure. It comes from one E-core on Intel 4 finFET, compared against "a similar design", not a controlled equivalent. It is not GAA technology. S1 does not caveat that the droop and frequency gains are not independently reproduced. Meanwhile most of the cited risk evidence (thermal, clocking, SI) is simulated, so the findings do not weigh measured benefits against modeled penalties.
    - source: [Intel PowerVia Technology: Backside Power Delivery for High Density and High-Performance Computing](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208) (OpenAlex, 2023-06-11, abstract_only)
    - excerpt: "A fabricated E-core with $\gt 90$% cell utilization showed $\gt 30$% platform voltage droop improvement and 6% frequency benefit compared to a similar design without PowerVia."
    - reasoning: The number is accurately quoted, but "platform voltage droop" and "similar design" are not defined in the abstract. Applying the gain to other nodes, designs or vendors would be unsupported.

**Limitations:**
- The analysis rests on titles, metadata and abstracts only. Two papers (src_93d0a26339, src_8744718e19) had no abstract, and src_6d3f3e6337 is front matter with no content.
- Only 12 papers were retrieved, and most are tangential to BPDN (BPDN is named as an application or example). The corpus contains no direct evidence on BPDN cost, yield, IR-drop benefit, thermal penalty or supplier concentration. These are gaps, not evidence that the problems do not exist.
- src_93d0a26339 (TSV electrodeposition) does not mention backside power in its metadata, so its relevance is unclear and it was not used for a finding.
- Several sources are preprints or not peer reviewed (src_bf3b12f944 on arXiv, src_45682c8d2d on Research Square). Many papers have 0 citations and are recent.
- Search coverage is narrow and risk-oriented. Industry roadmaps, foundry disclosures and conference papers (for example IEDM, VLSI) that would quantify BPDN risks may be missing.
- Only titles, metadata and abstracts were reviewed. Several abstracts are truncated, and three sources have no abstract.
- The evidence set has no TSMC or Samsung BSPDN sources and no independent replication of the Intel PowerVia result, so cross-vendor comparison could not be checked.
- Several sources are 2026 preprints or very recent papers with few or no citations. Their reliability could not be assessed beyond what the abstract states.
- S11 and the manufacturing-constraint parts of S7 look adequately supported by their abstracts, so they were not challenged beyond the citation issue noted.

## Evidence: company filings and news
Status: partial. Companies are chosen from the evidence: SEC-listed patent assignees and employers of paper authors found by the Patent and Science agents (14 company name(s) in the patents and papers; 8 matched to the SEC ticker file; the top 8 by patents + papers are read), plus filers whose reports mention the topic. Company evidence is limited to short verbatim passages from their latest SEC annual/quarterly reports that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase only; no patent or paper of theirs was found, they are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: backside power delivery, BSPDN, power delivery network, backside power

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Intel Corp (INTC) | 2 | 1 | large: 52.9B USD | -0.5% | 26.1% of revenue | 2 press release(s) read |
| Micron Technology Inc (MU) | 2 | 0 | large: 133.2B USD | +256.3% | 4.2% of revenue | 2 press release(s) read |
| Taiwan Semiconductor Manufacturing Co Ltd (TSM) | 1 | 0 | None: 2894.3B TWD | +33.9% | 7.1% of revenue |  |
| Adeia Inc. (ADEA) | 2 | 0 | small: 0.4B USD | +17.9% | 15.2% of revenue | 2 press release(s) read |
| Applied Materials Inc /De (AMAT) | 2 | 0 | large: 28.4B USD | +4.4% | 12.6% of revenue | 2 press release(s) read |
| Microchip Technology Inc (MCHP) | 2 | 0 | mid: 4.7B USD | +7.1% | 23.0% of revenue |  |
| Infineon Technologies Ag (IFNNY) | 0 | 0 | n/a | n/a | n/a |  |
| Nvidia Corp (NVDA) | 2 | 0 | large: 26.9B USD | +61.4% | n/a |  |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Intel states that its Intel 18A node introduces backside power delivery (PowerVia) as an industry first in high-volume semiconductor manufacturing, alongside RibbonFET gate-all-around transistors.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - excerpt: "Intel 18A introduces two industry firsts in high-volume semiconductor manufacturing: gate-all-around transistors (RibbonFET) and backside power delivery (PowerVia)."
  - reasoning: Direct restatement of the filing excerpt; Intel itself frames it as high-volume manufacturing, indicating commercial readiness of the process.
- **[M2]** *(verified_fact, confidence high)* Intel expects Intel 18A, which includes backside power delivery, to be the manufacturing process for multiple generations of its future client and server CPU products.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - excerpt: "We expect Intel 18A to serve as the manufacturing process for multiple generations of our future client and server CPU products."
  - reasoning: Exact quote of Intel's own expectation; this is the company's forward-looking statement, not an independent forecast.
- **[M3]** *(verified_fact, confidence high)* Intel describes PowerVia as routing power connections to the back side of the chip through dedicated vias, separating power delivery from signal routing to reduce congestion and improve power efficiency and performance.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - excerpt: "PowerVia is our unique industry-first implementation of backside power delivery that is designed to optimize signal transmission by eliminating the need for power routing on the front side of the wafer."
  - reasoning: Restates the filing's definition of PowerVia and its claimed technical benefits.
- **[M4]** *(ai_interpretation, confidence medium)* Intel is extending backside power and related advanced technologies into future nodes, pairing backside power in Intel 18A with high-NA EUV lithography planned for Intel 14A development.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - reasoning: Combining two excerpts: the filing lists backside power in 18A and high-NA EUV for 14A development, suggesting a multi-node advanced-technology roadmap. This is my synthesis, not a single filing statement.
- **[M5]** *(ai_interpretation, confidence medium)* Among the companies checked, only Intel's filing evidence mentions backside power delivery; Micron, TSMC, Adeia, Applied Materials, Microchip, Infineon and Nvidia filings retrieved do not mention the keywords.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - reasoning: Per the retrieval summary, only Intel's report mentions the keywords. However, absence from excerpts does not prove absence from the market; TSMC, Micron, Adeia, AMAT, Microchip and Infineon hold patents on the topic per the evidence-selection step, so their commercial activity cannot be assessed from these filings.
  - citation check: company name(s) not found in the cited sources removed: Micron Technology Inc, Taiwan Semiconductor Manufacturing Co Ltd, Adeia Inc., Applied Materials Inc /De, Microchip Technology Inc, Infineon Technologies Ag, Nvidia Corp

**Limitations:**
- Only one SEC filing source (Intel 10-K, excerpt-only) was retrieved; no news headlines, press releases, or filings from other companies are in the source list.
- The Intel 10-K was read as excerpts only, not in full; other backside-power content in the filing may exist.
- TSMC, Micron, Adeia, Applied Materials, Microchip, Infineon and Nvidia were selected because patents or papers name them, but no filing or news evidence about their backside-power commercial activity was retrieved, so their market roles cannot be characterized.
- No evidence on customers, capacity investment, supply chain, or competition for backside power delivery beyond Intel's own statements.
- Intel's statements about future products and node plans are company expectations, not verified outcomes.

## Social signals from X
Status: no_data. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 50 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (130): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie, @SemiconductorsX, @KirkDBorne, @kyleichan, @thePandaily, @HPCwire, @WarGuy_, @PIBKohima, @robvank, @LifeboatHQ, @zhaoweiasu, @BlackEngineer, @ShapesXR, @engadget, @Gadgets360, @eeNewsEurope, @machinelearnflx, @dez_blanchfield, @0xRicker, @Lance_Edelman, @Techmeme, @chr1sa, @Romka2x, @OWW, @CyberRobooo, @Decoded08, @techniahqrobot, @liuziwei7, @johnkoetsier, @preskill, @gp_pulipaka, @QuantumStateX, @Scholarshipps, @QuantumDaily, @scitechgirl, @Amandasatiro07, @thatoptometrist, @QuantumPapers, @the_hindu, @IndiaToday, @EconomicTimes, @ETNOWlive, @GreaterKashmir, @DDIndialive, @c_aashish, @TheQuietSensei, @CBCRajouri, @india_plus_, @alphaaffairsf2f, @dayalugurubjp, @Prabinmen, @PsuWatch, @aseemmanchanda, @bhagwantkhuba, @SUDHIRb9661, @governancenow, @PIB_India, @marinaj4q, @Finsee_main, @skathire, @singularityhub, @ahier, @MolecularCell, @RevvityLifeSci, @idtdna, @NaturePlants, @SimbokeSarah, @ChEnected, @RZubiranS, @BioinfoAdv, @srqstockpicker, @ShorterLab, @nabil125125125, @ThalesDigiSec, @ThejesterVerse, @WOCTechnology, @QuantSecXYZ, @Ronald_vanLoon, @PrameyaEnglish, @craigapplecom, @BLU_Products, @PragativadiNews, @HimanshiTech, @NyongesaSande, @gadgetbytenepal, @bobbymorris280, @TechieUltimatum, @PaidFreeDroid, @nitin_gadkari, @MIB_India, @kishanreddybjp, @IndiaInGuate, @PIBDehradun, @CISACyber
Posts read: 0 (estimated X cost $0.000)


**Limitations:**
- No post from the approved accounts mentioned the keywords in the last 7 days.

## Evidence: patents
Status: ok. Worldwide patent publications from EPO OPS matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.

Patent publications per year (EPO, terms ['backside power delivery', 'BSPDN', 'power delivery network', 'backside power']): {2022: 82, 2023: 106, 2024: 237, 2025: 233, 2026: 160}
Patent Acceleration 2024->2025: 237 -> 233 (-1.7% YoY). EPO OPS publications per publication year matching any of ['backside power delivery', 'BSPDN', 'power delivery network', 'backside power'] (worldwide, applications and grants, one family can count several times). Recent years are undercounted because of the ~18-month publication delay. The current partial year is excluded.
Most frequent first applicants among retrieved publications: SAMSUNG ELECTRONICS CO LTD (4), IBM (3), MICRON TECHNOLOGY INC (3), INTEL CORP (2), TAIWAN SEMICONDUCTOR MFG (2), ADEIA SEMICONDUCTOR BONDING TECHNOLOGIES INC (2), APPLIED MATERIALS INC (2), MICROCHIP TECH INC (1)

- **[P1]** *(ai_interpretation, confidence medium)* Logic and memory manufacturers are actively applying for BSPDN integration into 3D stacked and standard cell architectures.
  - source: [THREE-DIMENSIONAL CHIP STACK WITH BACKSIDE POWER DISTRIBUTION NETWORK [US20260314486A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260314486A1) (EPO OPS, 2026-10-08, abstract_only)
  - source: [BONDED DIE STRUCTURES WITH BACKSIDE POWER DISTRIBUTION NETWORK AND INTEGRATED FUNCTONAL DIES AND METHODS OF FORMING THE SAME [US20260293628A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293628A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [STANDARD CELL ARCHITECTURE WITH FRONTSIDE AND BACKSIDE POWER VIA CONNECTIONS [EP4815707A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4815707A1) (EPO OPS, 2026-09-30, abstract_only)
  - source: [INTEGRATED CIRCUIT DEVICES INCLUDING CONTACT POWER RAIL STRUCTURES FOR THREE-DIMENSIONAL STACKED FIELD-EFFECT TRANSISTOR STRUCTURES AND METHODS OF FORMING THE SAME [US20260223453A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260223453A1) (EPO OPS, 2026-07-30, abstract_only)
  - excerpt: "A semiconductor structure is provided which includes a 3D chip stack including a bottom chip and a top chip having a backside power distribution network (BSPDN)"
  - reasoning: Multiple recent filings describe BSPDN structures within 3D chip stacks, bonded dies, and standard cell layouts, indicating a shift toward backside power routing in advanced node designs.
- **[P2]** *(ai_interpretation, confidence medium)* Reducing electrical resistance and managing power integrity are primary engineering challenges addressed in these filings.
  - source: [LOW RESISTANCE STRUCTURES IN SYSTEMS [US20260314467A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260314467A1) (EPO OPS, 2026-10-08, abstract_only)
  - source: [BACKSIDE POWER DELIVERY NETWORK WITH REDUCED RESISTANCE CONNECTION [US20260305329A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260305329A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [DECOUPLING OF CRAM FROM FPGA FABRIC USING BACKSIDE POWER RAIL [US20260293719A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293719A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [INTEGRATED CIRCUIT STRUCTURE WITH DECOUPLING CAPACITOR CELL FOR POWER DELIVERY NETWORK [US20260293238A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293238A1) (EPO OPS, 2026-09-24, abstract_only)
  - excerpt: "Methods, systems, and devices for low resistance structures in systems are described. The described techniques provide for various structures of a power delivery network (PDN), each associated with a reduced resistance"
  - reasoning: Filings describe low-resistance TSV structures, decoupling capacitors, and backside power rails to mitigate voltage droops and current spikes in high-density designs.
- **[P3]** *(verified_fact, confidence medium)* Equipment and materials suppliers are applying for fabrication processes and novel substrates to enable BSPDN manufacturing.
  - source: [SEMI SELF-ALIGNED CONTACT FABRICATION FOR BACKSIDE POWER DELIVERY [WO2026164857A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026164857A1) (EPO OPS, 2026-08-06, abstract_only)
  - source: [POLYSiC WAFER BASE WITH MANDREL DEFINED POWER AND GROUND RAILS [US20260354291A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354291A1) (EPO OPS, 2026-11-05, abstract_only)
  - excerpt: "A method of forming a contact to a source/drain (S/D) region of a semiconductor structure includes forming a sidewall nitride layer on inner surfaces of an S/D recess"
  - reasoning: Recent applications cover self-aligned contact fabrication, polysilicon carbide wafer bases, and hybrid bonding methods, suggesting supply chain preparation for backside power routing.
- **[P4]** *(ai_interpretation, confidence medium)* Power delivery architectures are being customized for specific high-demand applications like AI, FPGA, and memory systems.
  - source: [POWER DELIVERY FOR AI COMPUTING WITH ORTHOGONAL EMBEDDING AND EDGE ACCESS [US20260231757A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260231757A1) (EPO OPS, 2026-08-06, abstract_only)
  - source: [DECOUPLING OF CRAM FROM FPGA FABRIC USING BACKSIDE POWER RAIL [US20260293719A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293719A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [Refresh Latency Indication for Refresh Operations [US20260237417A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260237417A1) (EPO OPS, 2026-08-13, abstract_only)
  - source: [PROCESSING CHIP, POWER CONSUMPTION CONTROL METHOD, SEMICONDUCTOR PACKAGING STRUCTURE, AND ELECTRONIC DEVICE [WO2026170859A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026170859A1) (EPO OPS, 2026-08-20, abstract_only)
  - source: [CURRENT MANAGEMENT CIRCUIT, SYSTEM AND METHOD WITH CURRENT CLAMPING FOR IMPROVING PERFORMANCE, REDUCING POWER DELIVERY NETWORK INVESTMENT AND PROVIDING PROTECTION [US20260221876A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260221876A1) (EPO OPS, 2026-07-30, abstract_only)
  - excerpt: "A semiconductor device with a vertically mounted IPD may include a substrate may include a cavity... The device may include a backside power delivery network in electrical contact with a second edge"
  - reasoning: Filings describe orthogonal embedding for AI computing, decoupling FPGA fabrics from memory, staggered refresh latency to prevent current spikes, and current clamping for system stability.
- **[P5]** *(ai_interpretation, confidence low)* Independent power domains and fault management are being integrated into BSPDN designs to improve reliability.
  - source: [RESOLVING A HARDWARE FAULT OCCURRENCE IN A MULTI-DOMAIN DEVICE [US20260244524A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260244524A1) (EPO OPS, 2026-08-20, abstract_only)
  - excerpt: "The PDN of each domain is operable independently of the PDN of the other domains. The CDN of each domain is operable independently of the CDN of the other domains."
  - reasoning: One filing describes independent PDNs and CDNs per domain with fault-structure circuits to detect and escalate hardware faults, highlighting reliability concerns in complex power routing.

**Limitations:**
- Analysis is based on abstracts only, not full claims or specifications.
- Publication delay of approximately 18 months means recent filings may be undercounted.
- Keyword matching may miss patents using alternative terminology for backside power delivery.
- Patent applications represent claims of invention, not proof of commercial viability or granted rights.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: ok. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.

| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |
|---|---|---|---|---|---|---|---|
| Intel Corp (INTC) | 59.37 (2026-11-09) | -43.3% | -39.2% | -39.0% | 140.4% | -58.3% | **subdued**: 39.0% below its 50-day average and -39.2% over 3 months; high volatility (140.4% annualised, 20-day) |

- **[T1]** *(verified_fact, confidence medium)* Intel Corp closed at 59.37 on 2026-11-09, down 43.3% over one month and 39.2% over three months.
  - source: [Intel Corp (INTC) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "closed at 59.37 on 2026-11-09. 1-month return -43.3%. 3-month return -39.2%."
- **[T2]** *(ai_interpretation, confidence medium)* Intel's price sits 39.0% below its 50-day average and 58.3% below its 100-day high, with very high volatility (140.4% annualised, 20-day). The rule-based timing-risk level is 'subdued' in the sense of no recent run-up, but the extreme volatility and steep decline mean timing risk is far from low: prices this unstable can move sharply in either direction, and a 'subdued' level reflects the absence of run-up, not any expectation of recovery.
  - source: [Intel Corp (INTC) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - reasoning: Subdued run-up combined with extreme volatility signals unstable, not favourable, conditions.

**Limitations:**
- The window is only about 100 trading days, so these metrics capture a short, possibly unrepresentative period.
- No fundamentals, valuation or earnings data are considered; price moves may reflect factors unrelated to backside power delivery.
- Past prices do not predict future prices; a subdued level means less recent run-up, not that the price will rise.
- Only one price series is available for this topic, so no cross-company comparison is possible.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 13 distinct company names from 25 patent publications, 3 company-affiliated papers and 1 SEC filers; 8 matched to the SEC ticker file (8 outside the configured list), 5 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| INTEL CORP (INTC) · Semiconductors & Related Devices | 2 | 2 | 1 | large: 52.85B USD | -0.5% | 26.1% | **58** |
| Adeia Inc. (ADEA) · Cable & Other Pay Television Services | 2 | 0 | 0 | small: 0.44B USD | +17.9% | 15.2% | **48** |
| Microchip Technology Inc (MCHP) · Semiconductors & Related Devices | 2 | 0 | 0 | mid: 4.71B USD | +7.1% | 23.0% | **43** |
| Taiwan Semiconductor Manufacturing Co Ltd (TSM) · Semiconductors & Related Devices | 3 | 0 | 0 | n/a: 2894.31B TWD | +33.9% | 7.1% | **33** |
| Micron Technology Inc (MU) · Semiconductors & Related Devices | 3 | 0 | 0 | large: 133.19B USD | +256.3% | 4.2% | **28** |
| Applied Materials Inc /De (AMAT) · Semiconductors & Related Devices | 2 | 0 | 0 | large: 28.37B USD | +4.4% | 12.6% | **28** |
| Nvidia Corp (NVDA) · Semiconductors & Related Devices | 0 | 1 | 0 | large: 26.91B USD | +61.4% | n/a | **18** |
| Infineon Technologies Ag (IFNNY) · Semiconductors & Related Devices | 1 | 0 | 0 | no XBRL facts for this company | n/a | n/a | **15** |

- INTEL CORP: 2 patent publication(s) as assignee (+18); 2 paper(s) with its researchers as authors (+15); 1 SEC report(s) mentioning the topic (+15); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth -0% (+0); R&D 26% of revenue (+10)
- Adeia Inc.: 2 patent publication(s) as assignee (+18); small company by revenue (+15): more room to grow, more risk; revenue growth +18% (+5); R&D 15% of revenue (+10)
- Microchip Technology Inc: 2 patent publication(s) as assignee (+18); mid-size company by revenue (+10); revenue growth +7% (+5); R&D 23% of revenue (+10)
- Taiwan Semiconductor Manufacturing Co Ltd: 3 patent publication(s) as assignee (+18); size unknown from SEC XBRL (+5, neutral); revenue growth +34% (+10)
- Micron Technology Inc: 3 patent publication(s) as assignee (+18); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth +256% (+10)
- Applied Materials Inc /De: 2 patent publication(s) as assignee (+18); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth +4% (+5); R&D 13% of revenue (+5)

**Found but not in the SEC ticker file (private, foreign, or name not matched):** SAMSUNG ELECTRONICS CO LTD (4P/0A/0F), IBM (3P/1A/0F), XILINX INC (1P/0A/0F), HUAWEI TECH CO LTD (1P/0A/0F), MEDIATEK SINGAPORE PTE LTD (1P/0A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence medium)* INTEL CORP (INTC) is active on backside power delivery: 2 retrieved patent publication(s) name it as assignee; 2 retrieved paper(s) have authors affiliated to it; 1 of its SEC report(s) mention the topic; fiscal 2025 revenue 52.85B USD (large by revenue), growth -0.5%, R&D 26.1% of revenue. Next-runner score 58/100 (heuristic).
  - source: [STANDARD CELL ARCHITECTURE WITH FRONTSIDE AND BACKSIDE POWER VIA CONNECTIONS [EP4815707A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4815707A1) (EPO OPS, 2026-09-30, abstract_only)
  - source: [INTEGRATED CIRCUIT STRUCTURE WITH DECOUPLING CAPACITOR CELL FOR POWER DELIVERY NETWORK [US20260293238A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293238A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [Intel PowerVia Technology: Backside Power Delivery for High Density and High-Performance Computing](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208) (OpenAlex, 2023-06-11, abstract_only)
  - source: [Leading Edge Technologies: Backside Power Delivery](https://doi.org/10.31399/asm.tb.edfastr.t56090091) (OpenAlex, 2023-11-01, abstract_only)
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Adeia Inc. (ADEA) is active on backside power delivery: 2 retrieved patent publication(s) name it as assignee; fiscal 2025 revenue 0.44B USD (small by revenue), growth +17.9%, R&D 15.2% of revenue. Next-runner score 48/100 (heuristic).
  - source: [BACKSIDE POWER DELIVERY [US20260247967A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260247967A1) (EPO OPS, 2026-08-20, abstract_only)
  - source: [BACKSIDE POWER DELIVERY [US20260247966A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260247966A1) (EPO OPS, 2026-08-20, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Microchip Technology Inc (MCHP) is active on backside power delivery: 2 retrieved patent publication(s) name it as assignee; fiscal 2025 revenue 4.71B USD (mid by revenue), growth +7.1%, R&D 23.0% of revenue. Next-runner score 43/100 (heuristic).
  - source: [POLYSiC WAFER BASE WITH MANDREL DEFINED POWER AND GROUND RAILS [US20260354291A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354291A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [POLYSiC WAFER BASE WITH MANDREL DEFINED POWER AND GROUND RAILS [WO2026231182A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026231182A1) (EPO OPS, 2026-11-05, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Taiwan Semiconductor Manufacturing Co Ltd (TSM) is active on backside power delivery: 3 retrieved patent publication(s) name it as assignee; fiscal 2024 revenue 2894.31B TWD, growth +33.9%, R&D 7.1% of revenue. Next-runner score 33/100 (heuristic).
  - source: [BONDED DIE STRUCTURES WITH BACKSIDE POWER DISTRIBUTION NETWORK AND INTEGRATED FUNCTONAL DIES AND METHODS OF FORMING THE SAME [US20260293628A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293628A1) (EPO OPS, 2026-09-24, abstract_only)
  - source: [SEMICONDUCTOR DEVICE [US20260271258A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260271258A1) (EPO OPS, 2026-09-10, abstract_only)
  - source: [SEMICONDUCTOR DEVICE AND MANUFACTURING METHOD THEREOF [US20260239669A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260239669A1) (EPO OPS, 2026-08-13, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K5]** *(ai_interpretation, confidence low)* Micron Technology Inc (MU) is active on backside power delivery: 3 retrieved patent publication(s) name it as assignee; fiscal 2026 revenue 133.19B USD (large by revenue), growth +256.3%, R&D 4.2% of revenue. Next-runner score 28/100 (heuristic).
  - source: [LOW RESISTANCE STRUCTURES IN SYSTEMS [US20260314467A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260314467A1) (EPO OPS, 2026-10-08, abstract_only)
  - source: [Refresh Latency Indication for Refresh Operations [US20260237417A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260237417A1) (EPO OPS, 2026-08-13, abstract_only)
  - source: [HYBRID DEVICE WITH BACKSIDE POWER DELIVERY NETWORKS AND ASSOCIATED SYSTEMS AND METHODS [WO2026165472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026165472A1) (EPO OPS, 2026-08-06, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K6]** *(ai_interpretation, confidence low)* Applied Materials Inc /De (AMAT) is active on backside power delivery: 2 retrieved patent publication(s) name it as assignee; fiscal 2025 revenue 28.37B USD (large by revenue), growth +4.4%, R&D 12.6% of revenue. Next-runner score 28/100 (heuristic).
  - source: [POWER DELIVERY FOR AI COMPUTING WITH ORTHOGONAL EMBEDDING AND EDGE ACCESS [US20260231757A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260231757A1) (EPO OPS, 2026-08-06, abstract_only)
  - source: [SEMI SELF-ALIGNED CONTACT FABRICATION FOR BACKSIDE POWER DELIVERY [WO2026164857A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026164857A1) (EPO OPS, 2026-08-06, abstract_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [Intel Corp (INTC) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_5ab961d478
- [POLYSiC WAFER BASE WITH MANDREL DEFINED POWER AND GROUND RAILS [US20260354291A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354291A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-10 | abstract_only | id src_4b3e9a778a
- [POLYSiC WAFER BASE WITH MANDREL DEFINED POWER AND GROUND RAILS [WO2026231182A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026231182A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-10 | abstract_only | id src_05357fef5d
- [INTEGRATED CIRCUIT AND METHOD OF DESIGNING THE INTEGRATED CIRCUIT [US20260334214A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260334214A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-10 | abstract_only | id src_3d740ed437
- [THREE-DIMENSIONAL CHIP STACK WITH BACKSIDE POWER DISTRIBUTION NETWORK [US20260314486A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260314486A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-10 | abstract_only | id src_18327d1b73
- [LOW RESISTANCE STRUCTURES IN SYSTEMS [US20260314467A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260314467A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-10 | abstract_only | id src_b831196943
- [Controllable and Nanoscale Linear Etching of Atomic Layer Deposited Molybdenum Using Cyclic Stepwise CHF 3 /O 2 Plasma](https://doi.org/10.1002/smll.76133) | OpenAlex | 2026-10-07 | retrieved 2026-11-10 | abstract_only | id src_a58352ac31
- [Design Space Exploration of Backside Clock Meshes for 2 nm GAAFET BSPDN Technology](https://arxiv.org/abs/2610.02401v1) | arXiv | 2026-10-01 | retrieved 2026-11-10 | abstract_only | id src_29c72af767
- [BACKSIDE POWER DELIVERY NETWORK WITH REDUCED RESISTANCE CONNECTION [US20260305329A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260305329A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-10 | abstract_only | id src_78aabf496e
- [STANDARD CELL ARCHITECTURE WITH FRONTSIDE AND BACKSIDE POWER VIA CONNECTIONS [EP4815707A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4815707A1) | EPO OPS | 2026-09-30 | retrieved 2026-11-10 | abstract_only | id src_2c6159860f
- [DECOUPLING OF CRAM FROM FPGA FABRIC USING BACKSIDE POWER RAIL [US20260293719A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293719A1) | EPO OPS | 2026-09-24 | retrieved 2026-11-10 | abstract_only | id src_ea90fc4ce5
- [INTEGRATED CIRCUIT STRUCTURE WITH DECOUPLING CAPACITOR CELL FOR POWER DELIVERY NETWORK [US20260293238A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293238A1) | EPO OPS | 2026-09-24 | retrieved 2026-11-10 | abstract_only | id src_7b2a7a2166
- [BONDED DIE STRUCTURES WITH BACKSIDE POWER DISTRIBUTION NETWORK AND INTEGRATED FUNCTONAL DIES AND METHODS OF FORMING THE SAME [US20260293628A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260293628A1) | EPO OPS | 2026-09-24 | retrieved 2026-11-10 | abstract_only | id src_af4dd65f9e
- [SEMICONDUCTOR DEVICE [US20260271258A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260271258A1) | EPO OPS | 2026-09-10 | retrieved 2026-11-10 | abstract_only | id src_f5a91afa16
- [ENGINEERING CHANGE ORDER CELL USING DUAL POWER RAILS [EP4804763A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4804763A2) | EPO OPS | 2026-09-09 | retrieved 2026-11-10 | abstract_only | id src_e215aa0c75
- [In-situ Co-Integration of Ru-based Buried Power Rails and nTSVs for Advanced Backside Power Delivery](https://doi.org/10.1016/j.chip.2026.100222) | OpenAlex | 2026-09-01 | retrieved 2026-11-10 | abstract_only | id src_a5cfab6d14
- [Front Matter](https://doi.org/10.1002/9781394406517.fmatter) | OpenAlex | 2026-08-31 | retrieved 2026-11-10 | abstract_only | id src_6d3f3e6337
- [DIODE-TRIGGERED SILICON CONTROLLED-RECTIFIER IN FRONT VIA BACKSIDE POWER TECHNOLOGY [US20260255688A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260255688A1) | EPO OPS | 2026-08-27 | retrieved 2026-11-10 | abstract_only | id src_a9b9620f2d
- [SYSTEMS, METHODS, AND APPARATUS FOR SEMICONDUCTOR PACKAGING WITH SUBSTRATE HAVING THERMALLY CONDUCTIVE LAYER [US20260255999A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260255999A1) | EPO OPS | 2026-08-27 | retrieved 2026-11-10 | abstract_only | id src_59159d530c
- [BACKSIDE POWER DELIVERY [US20260247967A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260247967A1) | EPO OPS | 2026-08-20 | retrieved 2026-11-10 | abstract_only | id src_10543d77d3
- [BACKSIDE POWER DELIVERY [US20260247966A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260247966A1) | EPO OPS | 2026-08-20 | retrieved 2026-11-10 | abstract_only | id src_0c00f9c3bf
- [RESOLVING A HARDWARE FAULT OCCURRENCE IN A MULTI-DOMAIN DEVICE [US20260244524A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260244524A1) | EPO OPS | 2026-08-20 | retrieved 2026-11-10 | abstract_only | id src_4071c50bfe
- [PROCESSING CHIP, POWER CONSUMPTION CONTROL METHOD, SEMICONDUCTOR PACKAGING STRUCTURE, AND ELECTRONIC DEVICE [WO2026170859A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026170859A1) | EPO OPS | 2026-08-20 | retrieved 2026-11-10 | abstract_only | id src_abac85f5e2
- [SEMICONDUCTOR DEVICE AND MANUFACTURING METHOD THEREOF [US20260239669A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260239669A1) | EPO OPS | 2026-08-13 | retrieved 2026-11-10 | abstract_only | id src_693a69c7bb
- [Refresh Latency Indication for Refresh Operations [US20260237417A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260237417A1) | EPO OPS | 2026-08-13 | retrieved 2026-11-10 | abstract_only | id src_db574fbda5
- [HYBRID DEVICE WITH BACKSIDE POWER DELIVERY NETWORKS AND ASSOCIATED SYSTEMS AND METHODS [WO2026165472A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026165472A1) | EPO OPS | 2026-08-06 | retrieved 2026-11-10 | abstract_only | id src_dfee13a527
- [POWER DELIVERY FOR AI COMPUTING WITH ORTHOGONAL EMBEDDING AND EDGE ACCESS [US20260231757A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260231757A1) | EPO OPS | 2026-08-06 | retrieved 2026-11-10 | abstract_only | id src_ae14fb82a4
- [SEMI SELF-ALIGNED CONTACT FABRICATION FOR BACKSIDE POWER DELIVERY [WO2026164857A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026164857A1) | EPO OPS | 2026-08-06 | retrieved 2026-11-10 | abstract_only | id src_01ae7e705d
- [INTEGRATED CIRCUIT DEVICES INCLUDING CONTACT POWER RAIL STRUCTURES FOR THREE-DIMENSIONAL STACKED FIELD-EFFECT TRANSISTOR STRUCTURES AND METHODS OF FORMING THE SAME [US20260223453A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260223453A1) | EPO OPS | 2026-07-30 | retrieved 2026-11-10 | abstract_only | id src_6c98507a4d
- [CURRENT MANAGEMENT CIRCUIT, SYSTEM AND METHOD WITH CURRENT CLAMPING FOR IMPROVING PERFORMANCE, REDUCING POWER DELIVERY NETWORK INVESTMENT AND PROVIDING PROTECTION [US20260221876A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260221876A1) | EPO OPS | 2026-07-30 | retrieved 2026-11-10 | abstract_only | id src_cd29e84a8b
- [Pre-weakened anodization-assisted rapid thinning of silicon carbide wafers](https://doi.org/10.1016/j.matdes.2026.116697) | OpenAlex | 2026-07-28 | retrieved 2026-11-10 | abstract_only | id src_06bc1c6960
- [CSCO: A Backside-PDN-Aware Clock-Signal Co-Optimization Framework for Improved PPA](https://arxiv.org/abs/2607.13700v1) | arXiv | 2026-07-15 | retrieved 2026-11-10 | abstract_only | id src_8d80bb876d
- [Failure Analysis in Transition: An Industry Survey of Challenges, Priorities, and Standardization Needs in Advanced Packaging and Heterogeneous Integration](https://doi.org/10.48550/arxiv.2606.22149) | OpenAlex | 2026-06-20 | retrieved 2026-11-10 | abstract_only | id src_bf3b12f944
- [Low Distortion Fusion Bonding using Pneumatically Warped Wafers](https://arxiv.org/abs/2606.04625v1) | arXiv | 2026-06-03 | retrieved 2026-11-10 | abstract_only | id src_f00c9d96cf
- [Transient Multiscale Workflow for Thermal Analysis of 3DHI Chip Stack](https://arxiv.org/abs/2605.00399v1) | arXiv | 2026-05-01 | retrieved 2026-11-10 | abstract_only | id src_925a2367d1
- [Focus Session: Advanced CMOS and 5.5D Packaging: Perspectives and Challenges for Design, Reliability and Security](https://doi.org/10.23919/date69613.2026.11539746) | OpenAlex | 2026-04-20 | retrieved 2026-11-10 | abstract_only | id src_c6bf729742
- [Unifying Heterogeneous and Monolithic Integration via Dual-sided 3D Technology](https://doi.org/10.21203/rs.3.rs-8891286/v1) | OpenAlex | 2026-03-02 | retrieved 2026-11-10 | abstract_only | id src_45682c8d2d
- [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) | SEC EDGAR | 2026-01-23 | retrieved 2026-11-10 | excerpt_only | id src_3374efcb45
- [Thermal Implications of Non-Uniform Power in BSPDN-Enabled 2.5D/3D Chiplet-based Systems-in-Package using Nanosheet Technology](https://arxiv.org/abs/2508.02284v1) | arXiv | 2025-08-04 | retrieved 2026-11-10 | abstract_only | id src_9a2f532ed1
- [Enabling the Angstrom Era: 2D material-based multi-bridge-channel complementary field effect transistors](https://doi.org/10.1038/s41699-025-00591-z) | OpenAlex | 2025-08-02 | retrieved 2026-11-10 | abstract_only | id src_27b9f0d6ea
- [Investigation of bottom-up electrodeposition filling for nanoscale through-silicon vias (TSVs)](https://doi.org/10.1016/j.electacta.2025.146869) | OpenAlex | 2025-07-07 | retrieved 2026-11-10 | metadata_only | id src_93d0a26339
- [Thermal Impacts of Backside Power Delivery Networks on GAAFET Technology](https://doi.org/10.1109/ted.2025.3569614) | OpenAlex | 2025-05-22 | retrieved 2026-11-10 | abstract_only | id src_7762759087
- [Breaking Physics Limits: How 2nm Chip Technology Powers Next-Gen 3D ICs](https://doi.org/10.63995/brit1756) | OpenAlex | 2025-02-16 | retrieved 2026-11-10 | abstract_only | id src_0a3405b8e0
- [Backside Power Delivery Process Integration Challenges](https://doi.org/10.7567/ssdm.2024.c-4-01) | OpenAlex | 2024-09-03 | retrieved 2026-11-10 | metadata_only | id src_b1bae9c128
- [Extreme silicon thinning for back side power delivery network: Si thinning stopping on scaled SiGe etch stop layer](https://doi.org/10.1016/j.mee.2024.112246) | OpenAlex | 2024-07-24 | retrieved 2026-11-10 | metadata_only | id src_8744718e19
- [Thermal Mitigation Strategy for Backside Power Delivery Network](https://doi.org/10.1109/ectc51529.2024.00241) | OpenAlex | 2024-05-28 | retrieved 2026-11-10 | abstract_only | id src_a91300a32b
- [Modeling of Backside Power Delivery and Thermal Management in Semiconductor Die Packages](https://doi.org/10.1109/itherm55375.2024.10709612) | OpenAlex | 2024-05-28 | retrieved 2026-11-10 | abstract_only | id src_26b3f5b1fe
- [Leading Edge Technologies: Backside Power Delivery](https://doi.org/10.31399/asm.tb.edfastr.t56090091) | OpenAlex | 2023-11-01 | retrieved 2026-11-10 | abstract_only | id src_daf3c596a1
- [Intel PowerVia Technology: Backside Power Delivery for High Density and High-Performance Computing](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208) | OpenAlex | 2023-06-11 | retrieved 2026-11-10 | abstract_only | id src_72134be1b8
- [Nano-Through Silicon Vias (nTSV) for Backside Power Delivery Networks (BSPDN)](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185227) | OpenAlex | 2023-06-11 | retrieved 2026-11-10 | abstract_only | id src_dbfbe09f9a
- [Inkjet-printed electrical interconnects for high resolution integrated circuit diagnostics](https://doi.org/10.1038/s44172-023-00073-4) | OpenAlex | 2023-05-02 | retrieved 2026-11-10 | abstract_only | id src_5148be71d2

## Gaps, limitations and errors
- Missing data: X agent did not run: no social-signal or recent announcement evidence
- Missing data: No evidence of external customers, design wins or product shipments using backside power
- Missing data: No yield, volume, cost or margin data for Intel 18A or any other backside power process
- Missing data: No evidence on TSMC, Samsung or other foundries' backside power production timing; the retrieved filings of TSMC, Micron and others do not mention the topic
- Missing data: No independent or peer-reviewed silicon measurements of thermal and signal-integrity penalties; most evidence is simulation or preprints
- Missing data: No BPDN-specific quantification of reliability penalties
- Missing data: Supplier revenue or order evidence for equipment and materials companies; patent filings are claims only
- Missing data: Samsung, IBM, Huawei and MediaTek appear only in the scout's non-SEC note with no financials, so they were not assessed
- Limitation: Analysis uses only the supplied findings; many are abstract-level and several come from preprints
- Limitation: The only measured-silicon performance result is single-vendor and self-reported [S1, C7]
- Limitation: Market evidence is essentially one company's 10-K, so it may not represent the industry [M5]
- Limitation: Research and patent counts are keyword-based, not normalised for overall growth, and recent patent counts are undercounted by publication delay
- Limitation: Price and timing findings cover Intel only over about 100 trading days and are risk context, not a forecast
- Limitation: Company scout scores are heuristics, not predictions of returns, and nothing here is a buy, sell or hold recommendation
- Chief review gap: No quantitative yield or cost-overhead data for BSPDN in high-volume manufacturing; Intel 10-K confirms HVM but provides no yield figures, and R5 explicitly flags absence of BPDN-specific reliability quantification.
- Chief review gap: Competitive landscape is thin: only Intel's filing mentions BSPDN among checked companies (M5); TSMC's announced backside power plans for N2/N2P are not reflected in the market evidence, leaving the competitive picture one-sided.
- Chief review gap: X agent was not run, so no social or community signals are available; this does not limit the technical conclusions but reduces the breadth of market sentiment coverage.
- Chief review gap: Reliability and long-term degradation data (e.g., electromigration in nTSVs, bonding interface aging) are not covered by any finding; R5 notes this as an evidence gap.
- Chief review gap: Several risk findings (R3, R4, R5, R6) are rated low confidence and rest on abstracts or single-group demonstrations rather than multi-source verification.
- ERROR [market/SEC XBRL company facts]: IFNNY: no XBRL facts for this company
- ERROR [scout/SEC XBRL company facts]: IFNNY: no XBRL facts for this company

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 2 | 4916 | 2583 | 0.00368 |
| patent | Qwen/Qwen3.6-35B-A3B-FP8 | 1 | 7378 | 7600 | 0.00948 |
| science | deepseek/deepseek-v4.1-flash | 1 | 4633 | 3766 | 0.00591 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 21707 | 9732 | 0.14073 |
| market | z-ai/glm-5.3 | 1 | 2498 | 1041 | 0.00875 |
| timing | z-ai/glm-5.3-flash | 1 | 1098 | 361 | 0.00027 |
| investment | anthropic/claude-sonnet-5-5 | 1 | 14159 | 10080 | 0.12912 |
| x (data) | X API pay-per-use | 7 | 0 | 0 | 0.00000 |

Total estimated cost: $0.29795 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
