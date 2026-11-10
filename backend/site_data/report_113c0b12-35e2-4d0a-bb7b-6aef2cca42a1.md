# FUTURESCOUT AI research report: chiplet

Generated: 2026-11-09 10:56 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, x, patent, timing, scout, investment

## Verdict (forecast, computed from the report)
**Building: real activity, not yet proven commercially** — score 66.0, confidence medium.

Chiplets are small chips that are combined into one package instead of building a single large chip. Research, patents and company reports all show they are being taken up, especially for AI. The main thing that could slow this is that many claimed benefits are still only proven in simulations, and that packaging,…

Why:
- Research Momentum rated 4/5: Code-computed OpenAlex counts show strong growth (495 to 743 in 2024-2025, +50.1%; 2026 year-to-date +53.9%, rising).
- Commercial Readiness rated 4/5: Intel, AMD and Marvell describe chiplet offerings, Marvell has shipped a Photonic Fabric chiplet, and a supplier ecosystem of IP, EDA and SerDes chiplets exists.
- Papers 2024→2025: 495→743 (+50%)
- So far in 2026 (to 10-10): 805 papers vs 523 by the same date in 2025 (+54%, rising)

Watch out for:
- Packaging and interposer choices are unsettled, adding integration risk.
- Hybrid bonding and other alternatives could shift volume away from legacy products such as wire bonding.
- Several research results come from simulation or a single preprint, so transfer to production tools is unproven.
- Smaller names are thinly covered.

What would change this view:
- Stronger if: Further capital commitments such as Applied Materials' expanded Besi investment and co-innovation beyond hybrid bonding.
- Weaker if: Evidence that hybrid bonding or chiplet packaging yield and cost do not improve versus monolithic at volume.
- Stronger if: Demonstrations of die-to-die link speeds in silicon (Cadence's 64GT/s claim, if confirmed).
- Weaker if: Evidence that chiplet design remains too bespoke for commercial tooling or IP to scale, or that standards fail to converge.

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
Research on chiplets is growing quickly: OpenAlex works rose from 495 to 743 in 2024-2025 (+50.1%), and the 2026 year-to-date count is up 53.9%. These counts are not adjusted for overall growth in publishing. Company filings show chiplet integration and advanced packaging already being offered commercially by Intel, AMD, Marvell and equipment suppliers [M1][M2][M3][M4][M5], and patent filings centre on hybrid bonding, die-to-die protocols and system management [P1][P2][P3]. Much of the academic evidence for cost and yield benefits rests on simulation, models or toy comparisons rather than silicon [R3][R4][C2], and Risk challenges weaken several Science claims, including the 'design automation is the main obstacle', 'learned optimisers are displacing heuristics' and 'open standards are a recurring framing' claims [C1][C5][C9]. Performance, security and packaging-choice risks are real [R1][R2][R6], and Marvell itself flags chiplet advances as a possible source of obsolescence [M10]. The three chiplet-linked large-cap stocks are down sharply with very high volatility [T7]. The main uncertainty is whether chiplet economics hold up at scale across workloads, and which suppliers capture the value.

## Technology Opportunity Score
**Opportunity score: 66.0 / 100** · **Confidence: 47%** (medium; evidence 58% x risk multiplier 0.8) · evidence coverage 100%

Risk: rating 2/5 does not change the score; it multiplies confidence by 0.8.

Commercialization Gap (research momentum rating minus commercial readiness rating): +0


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 4 | S12, S5, S1 | Code-computed OpenAlex counts show strong growth (495 to 743 in 2024-2025, +50.1%; 2026 year-to-date +53.9%, rising). The work spans design automation, thermal and interconnect topics, but the counts are not normalised for publishing growth, and research activity is not commercial success. |
| Patent Momentum | 10% | 3 | P1, P2, P3, P4, P5 | Patent findings show broad filings across hybrid bonding, die-to-die protocols, system management and specialised chiplets, with Bosch as the most active filer in the sample. No code-computed patent counts or growth trend are provided and applications are claims, so a strong rating is not supported. |
| Technical Feasibility | 15% | 3 | M3, M1, R3, R2, R1, R6, C2 | Shipped chiplet products and platforms exist at large vendors, but many academic benefits rest on simulation or toy comparisons. Thermal, latency, security and packaging-choice issues remain open. |
| Commercial Readiness | 15% | 4 | M1, M2, M3, M7 | Intel, AMD and Marvell describe chiplet offerings, Marvell has shipped a Photonic Fabric chiplet, and a supplier ecosystem of IP, EDA and SerDes chiplets exists. Revenue attributable to chiplets is not shown. |
| Customer Adoption | 10% | 2 | M3, M2, M8, X4 | Filings describe platforms and initiatives (custom ASIC platforms, a DoD initiative) but do not name customers or volumes. Social posts on next-generation consoles are unverified rumours, and describing a technology in a report is not proof of adoption. |
| Industry Investment | 10% | 4 | M4, M5, M6, M1, M9 | Applied Materials is expanding its Besi investment, Lam and Kulicke & Soffa position packaging tools for chiplets, and Intel's foundry includes chiplet integration as a core offering. Suppliers are rebuilding platforms for chiplet-driven complexity. |
| Competitive Position | 10% | 3 | M10, M7, M6, M1 | The field has many competing players (foundries, fabless, IP and equipment suppliers) with no clearly dominant position. Marvell warns that chiplet advances could obsolete existing lines, Ceva cites chiplets as competition, and Kulicke & Soffa warns of shifting packaging volume. |
| Supply-Chain Readiness | 15% | 3 | M4, M5, M9, R6, C8 | Equipment for hybrid bonding, panel-level packaging and HBM stacking is offered, and EDA and IP are available. Packaging substrate options remain unsettled, and process complexity and metrology demand are rising. Supply-chain resilience claims for automotive are asserted, not shown. |

Formula: score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a validated prediction of stock performance; confidence is not a probability of profit.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Advanced packaging and equipment for chiplet integration

Technologies: 2.5D/3D integration, hybrid bonding, fan-out panel-level packaging, HBM stacking

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Filings show suppliers already positioning for chiplet packaging: Intel foundry, Applied Materials' Besi co-innovation, Lam's panel-level and HBM stacking tools, and Kulicke & Soffa's assembly systems [M1][M4][M5][M6]. Process complexity and metrology demand are rising [M9]. Patents focus on hybrid bonding yield [P1]. The listed stocks are down sharply with very high volatility [T5][T7]. Filings describe positioning, not confirmed order volumes. *(forecast)* [M1, M4, M5, M6, M9, P1, T7] | medium |
| medium_1_3y | Demand for hybrid bonding and die-on-wafer integration could grow with AI-driven 3D IC scaling [M4], but packaging options (organic, interposer, glass) remain unsettled [R6]. Kulicke & Soffa itself warns that alternative packaging could shift volume away from its wire-bond products [M6]. Winners are therefore not yet clear. *(forecast)* [M4, R6, M6] | low |
| long_3_5y | The evidence says little directly about this horizon. Intel frames the industry as moving from monolithic to chiplet-based architectures [M1], which is a company view, not a demonstrated outcome. Thermal and reliability limits could constrain dense stacks [S3][S8][C3]. *(forecast)* [M1, S3, S8, C3] | low |

**Bull case:** AI-driven demand for 3D and multi-die integration keeps rising and packaging yield and bonding processes mature. Equipment, metrology and foundry packaging suppliers see sustained demand [M4][M5][M9][P1]. *(forecast)* [M4, M5, M9, P1]

**Base case:** Chiplet packaging grows as an important but contested segment. Several packaging approaches coexist, and process complexity creates demand for equipment and metrology while the technology mix shifts between suppliers [M6][M9][R6]. *(forecast)* [M6, M9, R6]

**Bear case:** Yield, thermal and cost benefits prove workload-dependent or smaller than modelled, and alternative packaging routes redirect spend away from specific suppliers. Volatile equity prices amplify the downside [R2][R3][R4][C2][M6][T7]. *(forecast)* [R2, R3, R4, C2, M6, T7]

**Catalysts:**
- Further capital commitments such as Applied Materials' expanded Besi investment and co-innovation beyond hybrid bonding. *(forecast)* [M4]
- Hybrid bonding yield improvements reflected in patent activity moving into production. *(forecast)* [P1]

**Risks:**
- Packaging and interposer choices are unsettled, adding integration risk. *(ai_interpretation)* [R6]
- Hybrid bonding and other alternatives could shift volume away from legacy products such as wire bonding. *(ai_interpretation)* [M6]
- Chiplet-linked large-cap stocks show 106-137% annualised short-term volatility and steep declines, so price swings are a material risk. *(ai_interpretation)* [T7]

**What would invalidate this thesis:**
- Evidence that hybrid bonding or chiplet packaging yield and cost do not improve versus monolithic at volume. *(assumption)* [R4, C2, P1]
- A packaging approach that bypasses the tools and processes these suppliers sell. *(assumption)* [M6, R6]

**Conflicting evidence:**
- Cost and yield benefits are asserted as motivation, but the only quantified yield comparison is a toy example with about a 10% difference in functional dies; the Risk challenge says the Science finding overstates the evidence. *(ai_interpretation)* [S2, R4, C2]
- Thermal management is called the key limiter, but the placement-order paper reports only a 1.01% peak-temperature improvement, and the micro-fluidic cooling claim rests on one simulation-only review. *(ai_interpretation)* [S3, C3]

**Companies named by cited evidence:**
- Intel: Its 10-K lists chiplet integration and advanced packaging among four core foundry offerings. The stock is down 47.4% over one month with very high volatility. [M1, T5]
- Applied Materials: Press release on expanding its investment in Besi and co-innovation on 3D IC integration. [M4]
- Lam Research: Offers advanced packaging equipment supporting fan-out panel-level packaging of chiplets and 3D HBM stacking. [M5]
- Kulicke & Soffa Industries: Positions assembly systems for chiplet packages but warns alternatives could shift volume from wire-bond products. Small company by revenue (about 0.65B USD, growth -7.4%), so higher risk and thinner disclosure; the score is a heuristic, not a recommendation. [M6, K5]
- Nova Ltd.: Says TSV and hybrid bonding raise process steps and tighten tolerances. Small company (about 0.88B USD revenue, growth +31.0%); smaller companies carry more risk and less disclosure. [M9, K2]

### Chiplet design tooling, IP and die-to-die interconnect

Technologies: EDA for 2.5D/3D, network-on-chip IP, UCIe-style die-to-die links, SerDes chiplets

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | A commercial ecosystem exists: Cadence's Integrity 3D-IC platform, Arteris NoC IP, Credo SerDes chiplets [M7]. Cadence claims 64GT/s operation on UCIe-related silicon [X1], a company social post and unverified. A social post reports Arteris revenue up 48% [X5], also unverified. Research frames design automation as an active focus [S1][C1]. *(forecast)* [M7, X1, X5, S1, C1] | low |
| medium_1_3y | Protocol and bandwidth-aggregation patent filings [P2] and research on automated partitioning and placement [S5][S12] suggest continued tooling demand. The claim that learned methods are replacing classical ones is not established [C5], and the claim that open standards are central is only partly supported [C9]. *(forecast)* [P2, S5, S12, C5, C9] | low |
| long_3_5y | The evidence does not address this horizon directly. Ceva cites chiplet-based AI architectures as competition [M7], so some IP suppliers may be disadvantaged as well as helped. *(forecast)* [M7] | low |

**Bull case:** Chiplet design complexity grows, and design, IP and connectivity suppliers become standard parts of multi-die flows, with rising revenue, as Arteris' reported growth hints [M7][M9][X5]. *(forecast)* [M7, M9, X5]

**Base case:** Tooling and IP suppliers gain incremental demand as chiplet products spread, while research progress on automation and standards stays uneven [S1][C1][C9]. *(forecast)* [M7, S1, C1, C9]

**Bear case:** Chiplet design flows consolidate into a few large vendors, or standards stay fragmented, limiting smaller suppliers. Benefits claimed in research stay unproven in silicon [R3][R6][C9]. *(forecast)* [R3, R6, C9]

**Catalysts:**
- Demonstrations of die-to-die link speeds in silicon (Cadence's 64GT/s claim, if confirmed). *(forecast)* [X1]
- Adoption of automated partitioning and floorplanning in commercial flows. *(forecast)* [M7, S5]

**Risks:**
- Several research results come from simulation or a single preprint, so transfer to production tools is unproven. *(ai_interpretation)* [R3, C4, C5]
- Smaller names are thinly covered; Arteris is micro-sized by revenue with R&D at 70.7% of revenue. *(ai_interpretation)* [K1]

**What would invalidate this thesis:**
- Evidence that chiplet design remains too bespoke for commercial tooling or IP to scale, or that standards fail to converge. *(assumption)* [C1, C9, R6]

**Conflicting evidence:**
- Science claims a shift to learned optimisers and a recurring open-standards theme, but Risk challenges find the cited papers do not show this. *(ai_interpretation)* [S5, C5, S11, C9]

**Companies named by cited evidence:**
- Cadence Design Systems: Offers the Integrity 3D-IC platform for multi-chiplet designs; a social post claims 64GT/s UCIe-related silicon (unverified). [M7, X1]
- Arteris, Inc.: NoC interconnect IP for chiplets; micro company by revenue (about 0.07B USD, growth +22.3%), with higher risk and less disclosure; heuristic score only, not a recommendation. [M7, K1, X5]
- Credo Technology Group Holding Ltd: Sells SerDes chiplets as products; mid-sized by revenue (about 1.34B USD, growth +205.7%), with only one SEC report mentioning the topic. [M7, K4]
- Ceva Inc: Cites chiplet-based AI architectures as competition. Micro company; the financials shown are from fiscal 2017, so the data may be stale. [M7, K3]

### Custom AI silicon and vertical chiplet markets (data centre, automotive, defense)

Technologies: custom ASIC with chiplets, co-packaged optics, automotive chiplet systems, defense heterogeneous integration

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Marvell's custom ASIC platform includes chiplets and it shipped a first-generation Photonic Fabric chiplet [M3]. AMD describes a custom-ready chiplet platform [M2]. Bosch leads patent filings on vehicle chiplet systems [P5], and Mercury describes a DoD initiative toward chiplet architectures [M8]. Customer adoption is not directly evidenced. All three large-cap stocks are down sharply [T7]. *(forecast)* [M3, M2, P5, M8, T7] | low |
| medium_1_3y | Specialised chiplets such as analog in-memory compute, co-packaged optics and memory arbiters are appearing in patents [P4], and HBM base dies may be co-designed with accelerators (an unverified social claim) [X2]. The automotive market statistic concerns automotive chips in general, not chiplets [S10][C8]. Marvell warns that chiplet advances could make existing products obsolete [M10]. *(forecast)* [P4, X2, S10, C8, M10] | low |
| long_3_5y | Little direct evidence. Operator-level chiplet composition is a research proposal with large claimed gains from a single preprint [S9][C7]. Quantum photonic chiplets are conceptual [R7]. *(forecast)* [S9, C7, R7] | low |

**Bull case:** Custom AI accelerators and vertical markets adopt chiplets widely, supported by shipping products such as Marvell's Photonic Fabric chiplet and growing patent activity in specialised chiplets [M3][P4][P5]. *(forecast)* [M3, P4, P5]

**Base case:** Chiplets become a standard part of custom silicon strategies at large vendors, while automotive and defense remain early and workload-dependent [M2][M8][R2]. *(forecast)* [M2, M8, R2]

**Bear case:** Memory bandwidth, network and cost bottlenecks persist regardless of chiplets [R5], performance is workload-dependent [R2], security exposure grows [R1], and chiplet advances may obsolete existing product lines [M10]. Automotive and defense stay at the pilot stage [S10][C8][M8]. *(forecast)* [R5, R2, R1, M10, S10, C8, M8]

**Catalysts:**
- Confirmed customer deployments of chiplet-based custom accelerators or vehicle chiplet systems. *(forecast)* [M3, P5]
- Maturing of co-packaged optics and custom HBM within chiplet platforms. *(forecast)* [M3, P4]

**Risks:**
- Physical-security exposure: interposer wires can be probed by laser, and delay-based sensors were shown to be insufficient. *(ai_interpretation)* [R1]
- Non-uniform memory-access latency degrades synchronisation, so the performance case is workload-dependent. *(ai_interpretation)* [R2]
- Extreme share-price volatility and steep declines in Marvell, AMD and Intel. *(ai_interpretation)* [T1, T3, T5, T7]

**What would invalidate this thesis:**
- Evidence that chiplet-based accelerators fail to deliver the modelled cost and energy advantages in fabricated systems. *(assumption)* [R3, C7]
- Unresolved security weaknesses or latency penalties that rule chiplets out for key workloads. *(assumption)* [R1, R2]

**Conflicting evidence:**
- The automotive 'lead application' claim rests on a market figure for automotive compute chips in general, not chiplets. *(ai_interpretation)* [S10, C8]
- Fengshui's large efficiency gains come from one preprint with the authors' own models and unclear cost assumptions. *(ai_interpretation)* [S9, C7]

**Companies named by cited evidence:**
- Marvell Technology: Custom ASIC platform with chiplets and a shipped Photonic Fabric chiplet; also flags chiplet advances as an obsolescence risk. The stock is far below its 50-day average with very high volatility. [M3, M10, T1]
- Advanced Micro Devices: Describes a custom-ready chiplet platform. The stock is down 27.7% over one month with 106.4% annualised volatility. [M2, T3]
- Robert Bosch GmbH: Most active filer in the patent sample, with six applications on vehicle chiplet systems and protocol stacks. Applications are claims, not proof of products. [P5]
- Mercury Systems: Describes a DoD initiative moving from monolithic ASICs to heterogeneous chiplet architectures. Small company (about 0.98B USD revenue); higher risk and thinner disclosure. [M8, K6]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 101, 2021: 143, 2022: 166, 2023: 349, 2024: 495, 2025: 743, 2026: 852}
Research Acceleration 2024->2025: 495 -> 743 (50.1% YoY). OpenAlex works whose title or abstract contains any of the exact phrases "chiplet", "chiplet architecture", per publication year (singular and plural forms match; each work counted once). The synonyms and abbreviations were kept only after an AI check of sampled papers. The number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-10): 2025 523 -> 2026 805 (53.9%, trend: rising). OpenAlex works with any of the exact phrases "chiplet", "chiplet architecture" in title or abstract published 1 Jan–10 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence high)* Chiplet design remains largely a manual process, and the abstracts repeatedly frame design automation (partitioning, floorplanning, placement, packaging co-design) as the main obstacle to realising the promised cost, reusability and performance benefits of 2.5D integration.
  - source: [Automated Design of Chiplets](https://doi.org/10.1145/3569052.3578917) (OpenAlex, 2023-03-22, abstract_only)
  - source: [The Survey of Chiplet-based Integrated Architecture: An EDA perspective](https://arxiv.org/abs/2411.04410v1) (arXiv, 2024-11-07, abstract_only)
  - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
  - excerpt: "the design of chiplets remains largely reliant on manual processes"
  - reasoning: Two conference/preprint sources state the manual nature of chiplet design and the reliance on EDA processes; a third describes floorplan design in chiplet architectures as having received limited attention. One source is an arXiv preprint (not peer reviewed).
- **[S2]** *(verified_fact, confidence medium)* Chiplet-based 2.5D/3D integration is motivated primarily by cost and yield: multiple abstracts state that heterogeneous integration of smaller dies reduces manufacturing cost and improves yield relative to monolithic 2D ICs at advanced nodes.
  - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
  - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
  - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
  - source: [The Survey of Chiplet-based Integrated Architecture: An EDA perspective](https://arxiv.org/abs/2411.04410v1) (arXiv, 2024-11-07, abstract_only)
  - excerpt: "These approaches offer a significant cost reduction and higher manufacturing yield than monolithic 2D integrated circuits."
  - reasoning: Four abstracts independently give cost/yield/reusability as the driver; no quantitative cost data is present in the abstracts, so the magnitude cannot be judged from this evidence.
- **[S3]** *(ai_interpretation, confidence medium)* Thermal management is repeatedly flagged as the key physical limiter of dense multi-chiplet packages, and the reviewed work attacks it from at least three angles: multi-fidelity thermal modelling, thermally-aware placement, and micro-fluidic cooling.
  - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
  - source: [Chiplet Placement Order Exploration Based on Learning to Rank with Graph Representation](https://arxiv.org/abs/2404.04943v1) (arXiv, 2024-04-07, abstract_only)
  - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
  - excerpt: "the compact arrangement and high compute density exacerbate the thermal management challenges, potentially compromising performance"
  - reasoning: MFIT states that compact arrangement and high compute density exacerbate thermal challenges; the placement-order paper reports a peak-temperature improvement; the automotive review describes a micro-fluids-based cooling design. Three independent sources, two of them arXiv preprints.
- **[S4]** *(verified_fact, confidence low)* Multi-fidelity thermal models are reported to cut thermal simulation time from days to seconds or milliseconds for 16, 36 and 64-chiplet 2.5D and 16x3 3D systems with negligible accuracy loss.
  - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
  - excerpt: "reduce execution times from days to mere seconds and milliseconds with negligible loss in accuracy"
  - reasoning: Single arXiv preprint (not peer reviewed); the abstract reports the speedups but gives no independent reproduction.
- **[S5]** *(ai_interpretation, confidence medium)* Machine learning, and reinforcement learning in particular, is being applied across chiplet design tasks including accelerator architecture selection, chiplet placement order, and floorplan trade-offs — a shift from hand-tuned heuristics to learned optimisers.
  - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
  - source: [Chiplet Placement Order Exploration Based on Learning to Rank with Graph Representation](https://arxiv.org/abs/2404.04943v1) (arXiv, 2024-04-07, abstract_only)
  - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
  - excerpt: "the absence of system and package-level co-design methodology make it difficult for the designer to find the optimum design point regarding Power, Performance, Area, and manufacturing Cost (PPAC)"
  - reasoning: Chiplet-Gym uses RL for PPAC design-space exploration; the placement-order paper uses learning-to-rank on top of an RL placement framework (arXiv preprint); Floorplet couples Gem5 simulation with cost/reliability models. The reported gains come from different setups and are not directly comparable.
- **[S6]** *(verified_fact, confidence medium)* Chiplet arrangement geometry itself is treated as a first-class design variable: a hexagonally arranged mesh is reported to outperform a grid arrangement in both theoretical network metrics and measured latency/throughput.
  - source: [HexaMesh: Scaling to Hundreds of Chiplets with an Optimized Chiplet Arrangement](https://doi.org/10.1109/dac56929.2023.10248006) (OpenAlex, 2023-07-09, abstract_only)
  - excerpt: "network diameter reduced by 42%; bisection bandwidth improved by 130%"
  - reasoning: Peer-reviewed conference paper (DAC) reporting both analytical and practical results; only one source in this set, so the finding rests on a single abstract.
- **[S7]** *(verified_fact, confidence low)* Getting enough individually regulated voltage rails to many chiplets is being addressed with single-input multiple-output, scalable on-package voltage regulator modules, with at least one prototype built and measured.
  - source: [Chiplet-LEGO: Delivering Multiple Voltage Rails to Chiplets with Chiplet VRMs](https://doi.org/10.1109/compel57166.2025.11121243) (OpenAlex, 2025-06-22, abstract_only)
  - excerpt: "delivers multiple individually regulated output voltages, making it well-suited for VRMs in system-on-chip (SoC) applications with multiple voltage rails"
  - reasoning: Single conference paper on power electronics; the abstract reports a 24 V-to-1 V 120 W dual-output prototype but gives no efficiency figures, so the practical merit is unclear.
- **[S8]** *(ai_interpretation, confidence low)* Reliability in chiplet systems is presented as a manageable but non-trivial engineering problem rather than as a solved property, with reliability optimisation appearing alongside cost and performance in chiplet floorplanning frameworks.
  - source: [Reliability and Chiplets](https://doi.org/10.1109/mrl.2024.3386643) (OpenAlex, 2024-04-19, abstract_only)
  - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
  - excerpt: "There are reliability challenges, but they can be overcome with good reliability engineering and practice."
  - reasoning: The reliability column is a magazine piece with an abstract that asserts challenges can be overcome by good practice; Floorplet mentions reliability optimisation in its cost/reliability models. Neither abstract gives failure-rate or lifetime data.
- **[S9]** *(verified_fact, confidence low)* Chiplet co-design is extending to operator-level disaggregation: a framework proposes selecting a small pool of heterogeneous chiplets (network switches, processing-in-memory units, diverse microarchitectures) and composing them into bespoke accelerators, claiming large energy and energy-cost reductions versus homogeneous accelerators.
  - source: [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](https://arxiv.org/abs/2609.10970v1) (arXiv, 2026-09-10, abstract_only)
  - excerpt: "With just 8 strategically selected chiplets, encompassing network switches, processing-in-memory units, and accelerators with diverse microarchitectures"
  - reasoning: Single very recent arXiv preprint (not peer reviewed) from 2026; the reported percentage reductions come from the authors' own simulation framework.
- **[S10]** *(verified_fact, confidence low)* Automotive electronics is being positioned as a lead application domain for chiplets, with an open chiplet ecosystem argued to be important for supply-chain resilience and a market projection of 20-22 billion automotive compute chips by 2030.
  - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
  - excerpt: "fueled by the surging demand for automotive compute chips, expected to reach 20-22 billion by 2030"
  - reasoning: Single arXiv preprint (not peer reviewed); the market figure and the 2030 date are the authors' projection, not an independent measurement. The horizon follows the abstract's own 2030 timing statement.
- **[S11]** *(ai_interpretation, confidence medium)* A recurring framing across the abstracts is that the value of a chiplet ecosystem depends on open interoperability and shared composition standards, because chiplet pool composition and the accelerators built from it are circularly dependent.
  - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
  - source: [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](https://arxiv.org/abs/2609.10970v1) (arXiv, 2026-09-10, abstract_only)
  - source: [Automated Design of Chiplets](https://doi.org/10.1145/3569052.3578917) (OpenAlex, 2023-03-22, abstract_only)
  - excerpt: "The research accentuates the crucial open Chiplet ecosystem, fostering collaboration and enhancing supply chain resilience."
  - reasoning: The automotive review explicitly argues for an open chiplet ecosystem; Fengshui describes the circular dependency between chiplet pool value and accelerator quality; the automated-design paper frames ecosystem-level opportunities and challenges. Two of the three are arXiv preprints.
- **[S12]** *(ai_interpretation, confidence medium)* Chiplet design-space work is converging on quantified trade-offs across power, performance, area, cost, temperature and wirelength rather than optimising performance alone, as shown by frameworks that report combined cost/performance and thermal/wirelength metrics.
  - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
  - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
  - source: [Chiplet Placement Order Exploration Based on Learning to Rank with Graph Representation](https://arxiv.org/abs/2404.04943v1) (arXiv, 2024-04-07, abstract_only)
  - excerpt: "The experimental results show that our framework decreases inter-chiplet communication costs by 24.81%."
  - reasoning: Floorplet reports a 24.81% reduction in inter-chiplet communication cost with cost/reliability models; Chiplet-Gym optimises PPAC; the learning-to-rank paper reports simultaneous wirelength and peak-temperature changes. Metrics are self-reported and non-comparable across the three.

**Emerging directions:**
- Reinforcement learning and learning-to-rank for chiplet placement, floorplanning and PPAC design-space exploration
- Multi-fidelity thermal modelling spanning design-time exploration and runtime thermal management
- Operator-level disaggregation and co-design of chiplet pools with bespoke ML accelerators
- On-package, per-chiplet voltage regulator modules delivering multiple regulated rails
- Alternative interconnect topologies (hexagonal mesh) for hundreds-of-chiplets scale-out
- Domain-specific chiplet solutions for automotive ADAS and infotainment, including micro-fluidic cooling
- Open chiplet ecosystem and interoperability standards for heterogeneous multi-vendor integration
- 3D stacking alongside 2.5D interposer integration for compute-density scaling

**Open problems:**
- Absence of a system- and package-level co-design methodology linking architecture, placement and packaging choices
- Manual, non-automated chiplet design flows
- Thermal management under compact, high-compute-density multi-chiplet arrangements
- Trade-off between thermal/electrical model accuracy and simulation speed across design stages
- Sensitivity of placement results to chiplet placement order
- Circular dependency between chiplet pool composition and the quality of accelerators built from it
- Reliability challenges in flexibly interconnected chiplet assemblies
- Scaling high-performance inter-chiplet interconnects to tens or hundreds of dies

**Limitations:**
- All evidence here is titles and abstracts only; no full texts, methods sections or datasets were read.
- One item (Chiplet Design and Heterogeneous Integration Packaging) is metadata-only with no abstract and contributed no findings.
- Several items are arXiv preprints and are not peer reviewed; conclusions depending on them are marked low confidence.
- Most quantitative results come from single papers with self-reported metrics under different setups, so cross-paper comparison is not possible.
- No paper counts, growth rates or citation statistics are reported here as findings; the system computes those separately.
- The 12 items are a narrow slice of the chiplet literature and do not cover foundry roadmaps, standards bodies, or commercial product data.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['chiplet yield penalty', 'die-to-die interconnect latency', 'chiplet thermal management', 'chiplet standardization fragmentation', 'chiplet reliability degradation', 'chiplet cost model']

- **[R1]** *(verified_fact, confidence medium)* Splitting a design into chiplets creates new physical-security exposure. Interposer wire drivers can be mapped and probed with laser contactless techniques, and delay-based protective sensors were shown to be insufficient against laser probing.
  - source: [Evaluating Vulnerability of Chiplet-Based Systems to Contactless Probing Techniques](https://doi.org/10.1109/itc51657.2024.00022) (OpenAlex, 2024-11-03, abstract_only)
  - excerpt: "Disaggregating a design into multiple separate dies introduces new security threats, including the possibility of tampering with and probing exposed data lines."
  - reasoning: This is one conference paper that tests a single commercial device, a chiplet-based VU9P FPGA. It shows a real attack surface but does not show how general the exposure is across other chiplet products or what mitigations cost. Whether the exposure is exploitable in deployed systems is a gap.
- **[R2]** *(verified_fact, confidence medium)* Chiplets add non-uniform memory-access latency relative to monolithic dies. This degrades synchronization primitives such as atomic memory operations and needs new microarchitectural workarounds, so the performance case for chiplets is workload-dependent.
  - source: [Delegato: Locality-Aware Atomic Memory Operations on Chiplets](https://doi.org/10.1145/3725843.3756030) (OpenAlex, 2025-10-17, abstract_only)
  - excerpt: "chiplets impose higher and non-uniform memory access (NUMA) latencies than monolithic integration."
  - reasoning: The abstract states the penalty directly and proposes a mitigation (Delegato). The paper is a MICRO architecture study, so the harm is likely simulation-based. Its magnitude on commercial parts is not in the abstract.
- **[R3]** *(ai_interpretation, confidence medium)* Many headline chiplet benefits rest on analytical models, simulation or small testcases rather than fabricated silicon. Examples are the 1.52x throughput, 0.27x energy and 0.89x cost versus monolithic in Chiplet-Gym, and the cost reductions in ChipletPart. Real-world transfer is unproven in these abstracts.
  - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
  - source: [ChipletPart: Cost-Aware Partitioning for 2.5D Systems](https://arxiv.org/abs/2507.19819v3) (arXiv, 2025-07-26, abstract_only)
  - source: [FAPlace: Joint Optimization of Chiplet Placement and Interposer Footprint for 2.5D Systems](https://doi.org/10.1145/3787109.3815298) (OpenAlex, 2026-06-18, abstract_only)
  - source: [CarbonPATH: Carbon-aware pathfinding and architecture optimization for chiplet-based AI systems](https://doi.org/10.48550/arxiv.2603.03878) (OpenAlex, 2026-03-04, abstract_only)
  - reasoning: Chiplet-Gym says it 'analytically model[s]' PPAC. ChipletPart reports gains only 'for the testcases we study', and its geometric-mean gains (6% to 30% versus prior tools, 15% for heterogeneous versus homogeneous) are far below the maxima quoted. CarbonPATH calls itself 'early-stage'. ChipletPart and CarbonPATH are arXiv preprints and not peer reviewed. The results are model outputs that depend on the cost-model assumptions, and the abstracts give no silicon validation.
- **[R4]** *(ai_interpretation, confidence low)* The yield advantage of chiplets is shown with a toy comparison, and the study's own numbers are modest. A dual-core RV32I design on an FPGA toolflow with a Poisson yield model gave up to about a 10% difference in functional dies. The paper's phrase 'clear advantages' therefore overreaches for realistic large SoCs.
  - source: [A Comparative Study of Monolithic and Chiplet CPU Architectures: Performance and Yield Perspectives](https://doi.org/10.12792/iciae2026.005) (OpenAlex, 2026-01-01, abstract_only)
  - reasoning: The design is tiny. Die area is estimated from LUT utilization, performance comes from Vivado simulation on simple instruction sequences, and the chiplet performance gain appears 'under certain clock settings'. The abstract does not include packaging, known-good-die test or assembly yield loss, which is the usual counterweight to die-yield gains. Those omissions are a gap and not evidence of failure.
- **[R5]** *(verified_fact, confidence low)* Chiplets do not remove the memory-bandwidth, network and cost bottlenecks of large AI systems. A modeling paper states that LLM growth has outpaced compute, memory bandwidth, network performance and cost efficiency, and it treats chiplet cost as one input to system trade-offs.
  - source: [System-performance and cost modeling of Large Language Model training and inference](https://arxiv.org/abs/2507.02456v1) (arXiv, 2025-07-03, abstract_only)
  - excerpt: "the exponential growth in LLM size and complexity has outpaced advancements in compute capacity, memory bandwidth, network performance, and cost efficiency"
  - reasoning: This is an arXiv preprint with a truncated abstract, so it does not say how much chiplets help or hurt these bottlenecks. It is context showing that disaggregation addresses die yield and cost but not necessarily the other limits.
- **[R6]** *(ai_interpretation, confidence low)* Packaging and inter-chiplet interconnect choices remain unsettled and add integration risk. Options span organic substrates, organic or TSV interposers, thin-film layers and emerging glass substrates. Each has its own advantages and disadvantages, and new topologies are still being proposed for them.
  - source: [Recent Advances and Trends in Chiplet Design and Heterogeneous Integration Packaging](https://doi.org/10.1115/1.4062529) (OpenAlex, 2023-05-15, abstract_only)
  - source: [FoldedHexaTorus: An Inter-Chiplet Interconnect Topology for Chiplet-based Systems using Organic and Glass Substrates](https://doi.org/10.48550/arxiv.2504.19878) (OpenAlex, 2025-04-28, abstract_only)
  - source: [FAPlace: Joint Optimization of Chiplet Placement and Interposer Footprint for 2.5D Systems](https://doi.org/10.1145/3787109.3815298) (OpenAlex, 2026-06-18, abstract_only)
  - reasoning: The packaging review lists several integration routes and says it will examine their 'advantages and disadvantages'. FoldedHexaTorus (an arXiv preprint) treats glass substrates as 'emerging', and FAPlace shows interposer footprint and placement still being optimized. Together these suggest no converged packaging or interconnect solution. The abstracts give no manufacturing-maturity, cost or reliability data for glass, so the timing is only suggestive.
- **[R7]** *(ai_interpretation, confidence low)* Photonic-interconnected quantum chiplets are presented as a possible architectural transition, but the evidence is a conceptual engineering analysis using secondary data. The benefit is conditional on jointly optimizing interconnect loss, feed-forward latency and module yield, which the abstract does not show being achieved.
  - source: [Photonic-Interconnected Quantum Chiplets for Modular and Networked Quantum Computing](https://doi.org/10.62311/nesx/rp9-30052026) (OpenAlex, 2026-05-24, abstract_only)
  - reasoning: The paper appears in a low-visibility journal and relies on 'secondary real-data anchors' and 'transparent engineering analysis' rather than new experiments. Its own problem statement lists yield, cryogenic routing, interconnect loss and calibration complexity as compounding constraints. The long horizon is my judgement and is not stated in the abstract.
- **[R8]** *(ai_interpretation, confidence low)* Sustainability and thermal costs of heterogeneous integration are not yet well quantified in these sources. Carbon-aware design is described as early-stage, and the placement work reports only that thermal performance is not compromised, with no numbers in the abstract.
  - source: [CarbonPATH: Carbon-aware pathfinding and architecture optimization for chiplet-based AI systems](https://doi.org/10.48550/arxiv.2603.03878) (OpenAlex, 2026-03-04, abstract_only)
  - source: [FAPlace: Joint Optimization of Chiplet Placement and Interposer Footprint for 2.5D Systems](https://doi.org/10.1145/3787109.3815298) (OpenAlex, 2026-06-18, abstract_only)
  - reasoning: CarbonPATH (an arXiv preprint) treats embodied and operational carbon as a design constraint but the abstract is cut off before any result. FAPlace asserts thermal parity without quantification. This is a gap in the evidence, not proof of a problem. Stacked and multi-die thermal limits remain a plausible risk that the abstracts do not test.

**Possible hype:**
- 'Fundamentally transforming semiconductor system design' (src_5414723b87): promotional framing from a low-visibility venue, and the abstract does not quantify its claimed advantages.
- 'Not a minor packaging improvement but a possible architectural transition' for quantum chiplets (src_641a33128a): based on a conceptual analysis with secondary data, and conditional on several unsolved optimization targets.
- 'Clear advantages in manufacturability' (src_e66f051609): drawn from a toy dual-core design, simulation and a model-based yield estimate of roughly 10%.
- 'Chiplets are a cost-effective option' (src_eec1d1a032): cost gains come from the authors' own cost model and selected testcases, and the average gains are much smaller than the maxima.
- The 'game changer' framing of chiplets (src_20f2377341): the same paper documents higher NUMA latency that harms atomic operations.

**Challenges to the Science findings:**
- Targets ['S1'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S1 overstates its evidence. The 'largely manual' claim comes from a single 2023 position paper. The abstracts do not call design automation 'the main obstacle'; they say it is needed to realise the benefits, or that it is an active research focus. The survey describes automation as a 'popular focus', which suggests the field is moving beyond fully manual design. Labelling this 'verified_fact' with high confidence is too strong.
    - source: [Automated Design of Chiplets](https://doi.org/10.1145/3569052.3578917) (OpenAlex, 2023-03-22, abstract_only)
    - source: [The Survey of Chiplet-based Integrated Architecture: An EDA perspective](https://arxiv.org/abs/2411.04410v1) (arXiv, 2024-11-07, abstract_only)
    - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
    - excerpt: "Despite progress made in various related domains, the design of chiplets remains largely reliant on manual processes."
    - reasoning: Only one cited abstract makes the manual-process statement, and it is from 2023. The survey says 'Currently, optimizing the automation methodologies for chiplet architecture is a popular focus', and Floorplet says only that floorplanning has 'received limited attention'. 'Main obstacle' is the Science agent's inference, not a quoted finding, and the high confidence is not justified.
- Targets ['S2'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S2 treats the cost and yield benefit as an established finding, but the cited abstracts only assert it as background motivation. The only quantitative evidence available is weak: a toy FPGA/Poisson comparison with about a 10% difference in functional dies, and model-based cost numbers. The cost and yield advantage of 3D stacking is not shown at all. Describing this as 'verified_fact' conflates an author claim with a demonstrated result.
    - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
    - source: [A Comparative Study of Monolithic and Chiplet CPU Architectures: Performance and Yield Perspectives](https://doi.org/10.12792/iciae2026.005) (OpenAlex, 2026-01-01, abstract_only)
    - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
    - excerpt: "These approaches offer a significant cost reduction and higher manufacturing yield than monolithic 2D integrated circuits."
    - reasoning: This MFIT sentence is introductory framing with no data behind it in the abstract. The one abstract that tests yield (src_e66f051609) reports only 'up to approximately a 10% difference' on a dual-core RV32I design. The Chiplet-Gym cost advantage comes from an analytical model. So 'motivated by' is supportable, but 'verified' relative to monolithic ICs is not.
- Targets ['S3'], severity medium:
  - **[C3]** *(ai_interpretation, confidence medium)* S3 says thermal management is 'repeatedly flagged as the key physical limiter', but only MFIT states a thermal challenge explicitly. The placement-order paper uses temperature as one optimisation metric and reports only a 1.01% peak-temperature improvement. That figure undercuts the idea that thermal is the dominant limiter and does not show thermal is being 'attacked'. The micro-fluidic cooling claim rests on one automotive review preprint with simulation-only evaluation.
    - source: [Chiplet Placement Order Exploration Based on Learning to Rank with Graph Representation](https://arxiv.org/abs/2404.04943v1) (arXiv, 2024-04-07, abstract_only)
    - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
    - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
    - excerpt: "applying the top-ranked placement order obtained from the learning to rank network results in a 10.05% reduction in total inter-chiplet wirelength and a 1.01% improvement in peak system temperature"
    - reasoning: The cited abstracts do not rank thermal against other limiters such as interconnect latency, NUMA effects or packaging. 'Key' is an unsupported ranking. The thermal gain in the placement paper is marginal compared with its wirelength gain.
- Targets ['S4'], severity low:
  - **[C4]** *(ai_interpretation, confidence medium)* S4 repeats the MFIT authors' claim of 'negligible accuracy loss' without noting that the abstract gives no accuracy figure, no reference simulator and no validation against measured hardware. It is a single arXiv preprint with no citation record. The 'days to seconds' speedup is also not a like-for-like comparison against a named baseline.
    - source: [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) (arXiv, 2024-10-11, abstract_only)
    - excerpt: "these models can reduce execution times from days to mere seconds and milliseconds with negligible loss in accuracy."
    - reasoning: 'Negligible' is an author characterisation with no error bound in the abstract. The claim is based on one non-peer-reviewed source, and the abstract does not show whether the models were checked against silicon or only against other simulators.
- Targets ['S5'], severity medium:
  - **[C5]** *(ai_interpretation, confidence medium)* S5 claims a shift 'from hand-tuned heuristics to learned optimisers', but the cited and available papers do not show learned methods displacing classical ones. Chiplet-Gym explicitly combines RL with non-RL optimisers 'to ensure robustness'. ChipletPart reaches its cost gains with a genetic algorithm and simulated annealing, and FAPlace uses a deterministic single pass. The placement-order paper only refines an existing RL placer, with small gains. Three or four papers do not establish a trend.
    - source: [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) (OpenAlex, 2024-09-11, abstract_only)
    - source: [ChipletPart: Cost-Aware Partitioning for 2.5D Systems](https://arxiv.org/abs/2507.19819v3) (arXiv, 2025-07-26, abstract_only)
    - source: [FAPlace: Joint Optimization of Chiplet Placement and Interposer Footprint for 2.5D Systems](https://doi.org/10.1145/3787109.3815298) (OpenAlex, 2026-06-18, abstract_only)
    - excerpt: "We also explore non-RL-based optimization approaches and combine these two approaches to ensure the robustness of the optimizer."
    - reasoning: The Chiplet-Gym quote shows that RL alone was not relied upon. ChipletPart uses GA and SA, and FAPlace is a deterministic single-pass framework, both from other abstracts. The 'shift' is the Science agent's extrapolation, and RL is not shown to beat non-learned baselines.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S6'], severity medium:
  - **[C6]** *(ai_interpretation, confidence medium)* S6 says the hexagonal arrangement was 'measured' to beat a grid in latency and throughput. The abstract says only 'in practice' and does not say whether this is hardware measurement or simulation. Chiplet counts of tens to hundreds are very unlikely to have been fabricated. A single conference paper also does not show that geometry is treated as a 'first-class design variable'. FoldedHexaTorus shows interconnect topology is still being actively revised.
    - source: [HexaMesh: Scaling to Hundreds of Chiplets with an Optimized Chiplet Arrangement](https://doi.org/10.1109/dac56929.2023.10248006) (OpenAlex, 2023-07-09, abstract_only)
    - source: [FoldedHexaTorus: An Inter-Chiplet Interconnect Topology for Chiplet-based Systems using Organic and Glass Substrates](https://doi.org/10.48550/arxiv.2504.19878) (OpenAlex, 2025-04-28, abstract_only)
    - excerpt: "in practice (latency reduced by 19%; throughput improved by 34%)"
    - reasoning: The abstract does not state the evaluation method, so 'measured' is an unsupported upgrade, and simulation is the likelier reading. FoldedHexaTorus proposes a new topology claiming 'significantly higher throughput than state-of-the-art topologies', which implies HexaMesh is not settled as the preferred arrangement.
- Targets ['S9'], severity medium:
  - **[C7]** *(ai_interpretation, confidence medium)* S9 presents large efficiency reductions (48.5% to 97.8%) for Fengshui as a verified result. They come from one arXiv preprint, with a baseline of 'homogeneous accelerators', and the reported figures are from the authors' own framework and models. The cost metrics (EC, EDPC) depend on assumed NRE and cost models that the abstract does not detail. The preprint's listed date (2026-09-10) is also unusual, which suggests metadata issues.
    - source: [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](https://arxiv.org/abs/2609.10970v1) (arXiv, 2026-09-10, abstract_only)
    - excerpt: "Fengshui-generated BASICs achieve 48.5%, 88.1%, 93.0%, and 97.8% reductions in energy, energy-cost product (EC), energy-delay product (EDP), and energy-delay-cost product (EDPC)"
    - reasoning: These are author-reported results from a co-design framework, not independent or silicon-measured ones, and the comparison baseline is chosen by the authors. The abstract is truncated in the evidence, so the exact baselines are not visible. The 'verified_fact' label should mean 'reported by the authors', not 'demonstrated'.
- Targets ['S10'], severity medium:
  - **[C8]** *(ai_interpretation, confidence medium)* S10 attaches a market statistic to chiplets that does not support the 'lead application domain' claim. The 20-22 billion figure is a forecast for automotive compute chips in general, not for chiplets. It is stated without a source in a review preprint whose own evidence is gem5 simulation and design studies. Supply-chain resilience is asserted, not shown.
    - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
    - excerpt: "surging demand for automotive compute chips, expected to reach 20-22 billion by 2030."
    - reasoning: The quote shows the number describes demand for automotive compute chips overall, not chiplet adoption. Nothing in the abstract shows automotive is leading chiplet adoption, or that a design has been qualified for automotive use. It is a single preprint, and automotive-grade reliability is not addressed.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S11'], severity medium:
  - **[C9]** *(ai_interpretation, confidence high)* S11 says the dependence on open interoperability and shared composition standards is a 'recurring framing across the abstracts'. The 'circular dependency' wording appears only in Fengshui, and Fengshui does not mention standards. The Automated Design of Chiplets abstract mentions neither interoperability nor standards. Only the automotive review mentions an 'open Chiplet ecosystem'. Two of the three cited papers do not support the claim, which is the Science agent's own synthesis.
    - source: [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](https://arxiv.org/abs/2609.10970v1) (arXiv, 2026-09-10, abstract_only)
    - source: [Automated Design of Chiplets](https://doi.org/10.1145/3569052.3578917) (OpenAlex, 2023-03-22, abstract_only)
    - source: [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) (arXiv, 2024-05-31, abstract_only)
    - excerpt: "choosing which chiplets to build and how to compose them into accelerators is circularly dependent"
    - reasoning: The circular dependency is about choosing a chiplet pool and designing accelerators, not about interoperability standards. 'Shared composition standards' does not appear in any cited abstract. The finding links a design-methodology problem to a standards argument that the sources do not make.
- Targets general, severity medium:
  - **[C10]** *(ai_interpretation, confidence high)* The findings omit the performance and security downsides of disaggregation. S1 to S12 present chiplets as cost-effective and promising, with thermal and EDA as the main open issues. Several available abstracts show other costs: packaging adds latency, memory access becomes non-uniform and hurts synchronisation, and exposed interposer wires create probing exposure that delay-based sensors do not stop. The performance benefit is therefore workload-dependent and the integration risk is understated.
    - source: [Delegato: Locality-Aware Atomic Memory Operations on Chiplets](https://doi.org/10.1145/3725843.3756030) (OpenAlex, 2025-10-17, abstract_only)
    - source: [Evaluating Vulnerability of Chiplet-Based Systems to Contactless Probing Techniques](https://doi.org/10.1109/itc51657.2024.00022) (OpenAlex, 2024-11-03, abstract_only)
    - source: [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) (arXiv, 2023-08-03, abstract_only)
    - excerpt: "chiplets impose higher and non-uniform memory access (NUMA) latencies than monolithic integration."
    - reasoning: Floorplet itself says 'additional latency introduced by advanced packaging can decrease performance', and the probing paper says disaggregation 'introduces new security threats'. Neither downside appears in the Science findings, even though S8 touches on reliability.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source

**Limitations:**
- Only titles and abstracts were available, and several abstracts are truncated, so results, caveats and methods in the full papers are unseen.
- The set has 12 papers, skewed toward EDA and design-space optimization, with little on manufacturing yield data, known-good-die test, UCIe or other standards, supply-chain concentration, or advanced-packaging capacity constraints.
- Several sources are arXiv preprints or low-citation papers (0 to 6 citations), and some come from low-visibility venues, so they are not reliable evidence.
- No paper compares chiplets against alternatives such as wafer-scale integration or monolithic designs on newer nodes, so displacement risk could not be assessed.
- Absence of data on thermal, reliability, cost and supplier dependence in these abstracts is a coverage gap, not evidence that those problems exist.
- Only titles, metadata and abstracts were available, and several abstracts are truncated, so I could not check methods, baselines or whether results come from simulation or hardware.
- I did not challenge S7, S8 or S12. They are modest and match their abstracts, though S12's 'converging' rests on only three papers.
- The evidence set is small (23 papers) and weighted towards arXiv preprints and EDA or placement work. Contradicting industry or silicon data may exist but was not retrieved.
- Some metadata (for example the 2026-09-10 date on Fengshui) looks anomalous. I flagged it but could not verify it.
- I did not assess whether specific numbers (for example 1.52x throughput) are reproducible or what baselines they use.

## Evidence: company filings and news
Status: ok. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: chiplet, 2.5D packaging, die-to-die interconnect, hybrid bonding, multi-die

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Micron Technology (MU) | 2 | 0 | large: 133.2B USD | +256.3% | 4.2% of revenue | 2 press release(s) read |
| NVIDIA (NVDA) | 2 | 0 | large: 26.9B USD | +61.4% | n/a |  |
| Advanced Micro Devices (AMD) | 2 | 1 | large: 34.6B USD | +34.3% | 23.4% of revenue |  |
| Intel (INTC) | 2 | 1 | large: 52.9B USD | -0.5% | 26.1% of revenue | 2 press release(s) read |
| Broadcom (AVGO) | 2 | 0 | large: 63.9B USD | +23.9% | 17.2% of revenue | 1 press release(s) read |
| Marvell Technology (MRVL) | 2 | 2 | mid: 8.2B USD | +42.1% | 25.3% of revenue | 2 press release(s) read |
| Qualcomm (QCOM) | 2 | 0 | large: 43.1B USD | -2.6% | 23.7% of revenue | 2 press release(s) read |
| Taiwan Semiconductor Manufacturing (TSM) | 1 | 0 | None: 2894.3B TWD | +33.9% | 7.1% of revenue |  |
| ASML Holding (ASML) | 1 | 0 | None: 32.7B EUR | +15.6% | 14.4% of revenue |  |
| Applied Materials (AMAT) | 2 | 1 | large: 28.4B USD | +4.4% | 12.6% of revenue | 2 press release(s) read |
| Lam Research (LRCX) | 2 | 1 | large: 23.2B USD | +26.0% | 10.2% of revenue |  |
| KLA (KLAC) | 2 | 0 | large: 13.6B USD | +11.7% | 11.3% of revenue | 2 press release(s) read |
| Arteris, Inc. (AIP) | 1 | 1 | micro: 0.1B USD | +22.3% | 70.7% of revenue | discovered by full-text search |
| Ceva Inc (CEVA) | 1 | 1 | micro: 0.1B USD | +20.4% | n/a | discovered by full-text search |
| Cadence Design Systems Inc (CDNS) | 1 | 1 | mid: 5.3B USD | +14.1% | n/a | discovered by full-text search |
| Credo Technology Group Holding Ltd (CRDO) | 1 | 1 | mid: 1.3B USD | +205.7% | 20.9% of revenue | discovered by full-text search |
| Kulicke & Soffa Industries Inc (KLIC) | 1 | 1 | small: 0.7B USD | -7.4% | 22.9% of revenue | discovered by full-text search |
| Mercury Systems Inc (MRCY) | 1 | 1 | small: 1.0B USD | +7.9% | 6.1% of revenue | discovered by full-text search |
| Nova Ltd. (NVMI) | 1 | 1 | small: 0.9B USD | +31.0% | 16.3% of revenue | discovered by full-text search |
| Pdf Solutions Inc (PDFS) | 1 | 1 | small: 0.1B USD | -5.2% | n/a | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Intel's foundry business explicitly includes chiplet integration and advanced packaging among its four core offerings, and Intel frames the industry as shifting from monolithic chips to chiplet-based disaggregated architectures.
  - source: [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) (SEC EDGAR, 2026-01-23, excerpt_only)
  - excerpt: "Our foundry offerings include four components: wafer fabrication, advanced packaging, chiplet integration and design enablement services."
  - reasoning: Direct filing statement; Intel also cites EMIB multi-die Xeon processors and describes the industry shift to chiplets in the same 10-K.
- **[M2]** *(verified_fact, confidence medium)* AMD describes a custom-ready chiplet platform as part of its strategy to remain a leading custom-design silicon provider.
  - source: [Advanced Micro Devices Inc Form 10-K, filed 2026-02-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm) (SEC EDGAR, 2026-02-04, excerpt_only)
  - excerpt: "Our investments in technologies such as our custom-ready chiplet platform and AMD Infinity Fabric™ switch position us to maintain our leadership as a custom-design silicon provider"
  - reasoning: Direct quote from AMD 10-K; only one excerpt, so confidence medium.
- **[M3]** *(verified_fact, confidence high)* Marvell's custom ASIC platform incorporates die-to-die interconnects, chiplets, co-packaged optics and custom HBM, and it has shipped a first-generation Photonic Fabric chiplet integrating electrical and optical components.
  - source: [Marvell Technology, Inc. Form 10-K (FORM 10-K), filed 2026-03-11](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm) (SEC EDGAR, 2026-03-11, excerpt_only)
  - excerpt: "advanced packaging, including die to die interconnects, chiplets, co-packaged optics (“CPO”) and custom high-bandwidth memory (“HBM”)."
  - reasoning: Two excerpts from Marvell's 10-K describe both the platform capabilities and a specific shipping chiplet product.
- **[M4]** *(verified_fact, confidence high)* Applied Materials is expanding its investment in Besi and its co-innovation beyond hybrid bonding into new interconnect architectures, citing AI-driven demand for 3D IC scaling and die-on-wafer/die-on-die/die-on-panel integration.
  - source: [Applied Materials Inc /De 8-K press release (exhibit ex991prforprojectbasil.htm), filed 2026-10-26](https://www.sec.gov/Archives/edgar/data/6951/000162828026067303/ex991prforprojectbasil.htm) (SEC EDGAR, 2026-10-26, excerpt_only)
  - excerpt: "Applied Materials is adding to its investment in Besi as hybrid bonding technology and next-generation interconnect architectures become increasingly critical enablers"
  - reasoning: Press-release excerpt filed as 8-K exhibit; indicates equipment-maker investment in packaging technology tied to AI compute.
- **[M5]** *(verified_fact, confidence medium)* Lam Research offers advanced packaging equipment supporting fan-out panel-level packaging of chips or chiplets and 3D stacking of HBM.
  - source: [Lam Research Corp Form 10-K, filed 2026-08-07](https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm) (SEC EDGAR, 2026-08-07, excerpt_only)
  - excerpt: "We offer advanced packaging solutions that support fan-out panel-level packaging, a process in which chips or chiplets are cut from a large format substrate sheet"
  - reasoning: Direct filing statement showing equipment-side commercial readiness for chiplet packaging.
- **[M6]** *(verified_fact, confidence medium)* Kulicke & Soffa positions its assembly systems to enable growth of chiplet-based advanced packages, while flagging that hybrid bonding and other alternative packaging technologies could shift volume away from its wire-bond products.
  - source: [Kulicke & Soffa Industries Inc Form 10-K, filed 2025-11-20](https://www.sec.gov/Archives/edgar/data/56978/000005697825000081/klic-20251004.htm) (SEC EDGAR, 2025-11-20, excerpt_only)
  - excerpt: "With this system, we are well positioned to enable growth of chiplet-based advanced packages."
  - reasoning: Filing shows both opportunity and competitive risk framing around chiplet packaging.
- **[M7]** *(ai_interpretation, confidence medium)* A commercial ecosystem of IP, EDA and connectivity suppliers has formed around chiplet design: Arteris (NoC interconnect IP for chiplets), Cadence (Integrity 3D-IC platform for multi-chiplet 2.5D/3D designs), Credo (SerDes chiplets as products), and Ceva (citing chiplet-based AI architectures as competition).
  - source: [Arteris, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1667011/000162828026071154/aip-20260930.htm) (SEC EDGAR, 2026-11-05, excerpt_only)
  - source: [Cadence Design Systems Inc Form 10-K, filed 2026-02-19](https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) (SEC EDGAR, 2026-02-19, excerpt_only)
  - source: [Credo Technology Group Holding Ltd Form 10-K, filed 2026-06-15](https://www.sec.gov/Archives/edgar/data/1807794/000162828026043303/crdo-20260502.htm) (SEC EDGAR, 2026-06-15, excerpt_only)
  - source: [Ceva Inc Form 10-K, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1173489/000143774926006091/ceva20251231_10k.htm) (SEC EDGAR, 2026-02-27, excerpt_only)
  - reasoning: Each filing independently names chiplets in a distinct commercial role (IP licensing, EDA tooling, shipping connectivity products, competitive threat), suggesting an emerging multi-layer supplier ecosystem; this synthesis is my own across four sources.
- **[M8]** *(verified_fact, confidence low)* Defense applications are an emerging chiplet market: Mercury Systems describes a DoD initiative to bridge from monolithic ASICs to heterogeneous chiplet architectures packaging commercial silicon for defense-specific uses.
  - source: [Mercury Systems Inc Form 10-K, filed 2025-08-11](https://www.sec.gov/Archives/edgar/data/1049521/000104952125000024/mrcy-20250627.htm) (SEC EDGAR, 2025-08-11, excerpt_only)
  - excerpt: "to heterogeneous “chiplet” architectures, which leverage best-of-breed silicon from commercial providers and packages the silicon for defense-specific applications"
  - reasoning: Single filing excerpt; shows a government/defense adoption channel but no scale evidence.
- **[M9]** *(ai_interpretation, confidence medium)* Chiplet adoption is increasing process complexity and metrology demand: Nova notes that TSV and hybrid bonding dramatically increase process steps and tighten tolerances, and PDF Solutions says chiplet products routinely generate millions of parameters, prompting a rebuild of its analytics platform.
  - source: [Nova Ltd. Form 20-F, filed 2026-02-17](https://www.sec.gov/Archives/edgar/data/1109345/000117891326000504/zk2634307.htm) (SEC EDGAR, 2026-02-17, excerpt_only)
  - source: [Pdf Solutions Inc Form 10-K, filed 2026-02-24](https://www.sec.gov/Archives/edgar/data/1120914/000143774926005366/pdfs20251231d_10k.htm) (SEC EDGAR, 2026-02-24, excerpt_only)
  - reasoning: Both filings independently frame chiplets/3D integration as a driver of complexity that their offerings address; the synthesis across the two is my own.
- **[M10]** *(verified_fact, confidence medium)* Marvell identifies AI-driven advances in chiplet-based architectures as a risk that could render certain existing product lines, manufacturing processes or IP less valuable or obsolete.
  - source: [Marvell Technology, Inc. Form 10-K (FORM 10-K), filed 2026-03-11](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm) (SEC EDGAR, 2026-03-11, excerpt_only)
  - source: [Marvell Technology, Inc. Form 10-Q (FORM 10-Q), filed 2026-08-28](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000025/mrvl-20260801.htm) (SEC EDGAR, 2026-08-28, excerpt_only)
  - excerpt: "AI-driven advances in chiplet-based architectures, advanced packaging, or novel materials science could render certain of our existing product lines"
  - reasoning: Risk language repeated in both Marvell's 10-K and 10-Q, indicating the company sees chiplets as both opportunity and disruption risk.

**Limitations:**
- Only excerpt passages from filings were available, not full reports; companies whose filings did not mention the keywords (Micron, NVIDIA, Broadcom, Qualcomm, TSMC, ASML, KLA) cannot be concluded to be absent from the chiplet market.
- No news headlines were retrieved for this topic, so all findings rest on filing excerpts; no market-share, capacity, customer or revenue figures specific to chiplets were present in the excerpts.
- TSMC, a likely central player in advanced packaging, had zero keyword mentions in the one report read, leaving the foundry/packaging supply side under-covered.
- Discovered companies (Arteris, Ceva, Cadence, Credo, Kulicke & Soffa, Mercury, Nova, PDF Solutions) were each represented by a single filing with only a few excerpts, so their full chiplet-related activities are unknown.
- No evidence on hybrid bonding volume, die-to-die interconnect standards (e.g., UCIe), customer adoption counts, or pricing was present in the sources.

## Social signals from X
Status: ok. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 50 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (130): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie, @SemiconductorsX, @KirkDBorne, @kyleichan, @thePandaily, @HPCwire, @WarGuy_, @PIBKohima, @robvank, @LifeboatHQ, @zhaoweiasu, @BlackEngineer, @ShapesXR, @engadget, @Gadgets360, @eeNewsEurope, @machinelearnflx, @dez_blanchfield, @0xRicker, @Lance_Edelman, @Techmeme, @chr1sa, @Romka2x, @OWW, @CyberRobooo, @Decoded08, @techniahqrobot, @liuziwei7, @johnkoetsier, @preskill, @gp_pulipaka, @QuantumStateX, @Scholarshipps, @QuantumDaily, @scitechgirl, @Amandasatiro07, @thatoptometrist, @QuantumPapers, @the_hindu, @IndiaToday, @EconomicTimes, @ETNOWlive, @GreaterKashmir, @DDIndialive, @c_aashish, @TheQuietSensei, @CBCRajouri, @india_plus_, @alphaaffairsf2f, @dayalugurubjp, @Prabinmen, @PsuWatch, @aseemmanchanda, @bhagwantkhuba, @SUDHIRb9661, @governancenow, @PIB_India, @marinaj4q, @Finsee_main, @skathire, @singularityhub, @ahier, @MolecularCell, @RevvityLifeSci, @idtdna, @NaturePlants, @SimbokeSarah, @ChEnected, @RZubiranS, @BioinfoAdv, @srqstockpicker, @ShorterLab, @nabil125125125, @ThalesDigiSec, @ThejesterVerse, @WOCTechnology, @QuantSecXYZ, @Ronald_vanLoon, @PrameyaEnglish, @craigapplecom, @BLU_Products, @PragativadiNews, @HimanshiTech, @NyongesaSande, @gadgetbytenepal, @bobbymorris280, @TechieUltimatum, @PaidFreeDroid, @nitin_gadkari, @MIB_India, @kishanreddybjp, @IndiaInGuate, @PIBDehradun, @CISACyber
Posts read: 6 (estimated X cost $0.030)

- **[X1]** *(unverified_claim, confidence low)* Cadence says its UCIe-related silicon has demonstrated 64GT/s operation, which it presents as a milestone for scaling die-to-die bandwidth and enabling flexible multi-die architectures for AI and HPC.
  - source: [@Cadence: 64GT/s is the milestone. What it enables is the bigger story. In Part 2 of our UCIe series…](https://x.com/Cadence/status/2118418144607842733) (X API, 2026-11-05, full_text)
  - excerpt: "64GT/s is the milestone... why 64GT/s operation in silicon matters for scaling die-to-die bandwidth and enabling flexible multi-die architectures for AI and HPC."
  - reasoning: Single company post, promotional in nature (part of a UCIe blog/video series); the underlying silicon demonstration cannot be verified from the post alone. Very low engagement.
- **[X2]** *(unverified_claim, confidence low)* @SemiconductorsX claims that from HBM4 onward the base logic die is co-designed with the customer's accelerator, carrying custom interfaces, controllers and logic blocks on leading-edge nodes, citing NVIDIA's NVHBM built with multiple memory suppliers as an example.
  - source: [@SemiconductorsX: HBM is no longer a drop-in commodity. From HBM4 on, the base logic die is co-designed with…](https://x.com/SemiconductorsX/status/2119275506436866336) (X API, 2026-11-08, full_text)
  - reasoning: Analyst/agent account asserting an industry trend; NVIDIA and memory suppliers are named but did not post here. The claim is plausible but unverifiable from this post; moderate engagement (109) indicates attention, not accuracy.
- **[X3]** *(unverified_claim, confidence low)* eeNews Europe reports that Fraunhofer IPMS is researching chiplet integration and low-power memory as key areas for more efficient, flexible electronic systems.
  - source: [@eeNewsEurope: Could chiplets and more efficient memory help shape the next generation of semiconductor t…](https://x.com/eeNewsEurope/status/2117708581143278020) (X API, 2026-11-03, full_text)
  - reasoning: Press account summarising an article not read here; describes research activity rather than a product or roadmap claim.
- **[X4]** *(unverified_claim, confidence low)* @TechieUltimatum reports that Sony and Microsoft are reportedly taking different approaches to their next-generation AMD processors for PS6 and Xbox, with Microsoft allegedly pursuing a more powerful but costlier design.
  - source: [@TechieUltimatum: PS6 vs Xbox Project Helix: Microsoft could be building a MUCH more powerful next-gen conso…](https://x.com/TechieUltimatum/status/2119007757269659727) (X API, 2026-11-07, full_text)
  - reasoning: Rumour-based aggregator post ('reportedly', 'could be'); highest engagement in the set (147) but weakest evidentiary value. Included only because it touches next-gen AMD multi-die processor design.
- **[X5]** *(unverified_claim, confidence low)* Finsee reports Arteris, a supplier of chip-design/network-on-chip software, grew Q3 FY2026 revenue 48% year-over-year to $25.8 million and is nearing its first quarterly operating profit, though backlog additions stalled.
  - source: [@Finsee_main: $AIP Q3 2026 earnings: Arteris nears its first profit, but backlog additions stall Arteris…](https://x.com/Finsee_main/status/2118457114355994661) (X API, 2026-11-05, full_text)
  - reasoning: Earnings summary from a low-engagement owner-added account; figures are as reported in the post and the linked article was not read. Signals demand for die-to-die connectivity IP indirectly.

**Limitations:**
- Only 6 posts in a 7-day window matched the chiplet-related keywords; several are tangential (console rumours, licensing/EDA earnings), so evidence on chiplets specifically is thin.
- All findings are unverified claims: company marketing (Cadence), analyst assertion (@SemiconductorsX), press summaries of unread articles, or rumour aggregation.
- No posts from the major chiplet/advanced-packaging players themselves (Intel, AMD, TSMC-adjacent OSATs like Amkor, standards bodies like JEDEC/UCIe consortium) appeared in this window; their silence is not evidence of inactivity.
- Engagement counts are low overall except two posts, limiting any signal about market attention.
- Linked articles and videos (Cadence UCIe series, eeNews Fraunhofer piece) were not read, so details behind the summaries are unknown.
- The fixed account list includes many owner-added accounts unrelated to semiconductors, which dilutes topical coverage.

## Evidence: patents
Status: partial. Worldwide patent publications from EPO OPS matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.

Most frequent first applicants among retrieved publications: BOSCH GMBH ROBERT (6), MICRON TECHNOLOGY INC (2), OPTOML PTE LTD (2), APPLIED MAT INC (1), HON HAI PREC INDUSTRY CO LTD (1), JCET STATS CHIPPAC KOREA LTD (1), OPENCHIP & SOFTWARE TECH S L (1), IBM (1)

- **[P1]** *(ai_interpretation, confidence medium)* Hybrid bonding interfaces and packaging yield are a primary focus, with applicants addressing signal integrity, barrier materials, and manufacturing defects.
  - source: [ELECTRIC-FIELD SHUNT FOR HYBRID BONDING INTERFACES [US20260354205A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354205A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [SEMICONDUCTOR STRUCTURE AND MANUFACTURING METHOD THEREOF [US20260353862A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260353862A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [SEMICONDUCTOR PACKAGE AND METHOD FOR FORMING THE SAME [US20260354284A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354284A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [HYBRID BONDING TECHNIQUES THAT UTILIZE MULTI-FUNCTIONAL BARRIER MATERIALS [US20260344498A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260344498A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [MEMORY CHIP HAVING HYBRID BONDING PADS AND SEMICONDUCTOR DEVICE INCLUDING THE SAME [US20260351293A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260351293A1) (EPO OPS, 2026-11-05, abstract_only)
  - source: [CHIP STACK STRUCTURE, MANUFACTURING METHOD THEREFOR, CHIP PACKAGE STRUCTURE, AND ELECTRONIC DEVICE [WO2026200137A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026200137A1) (EPO OPS, 2026-10-01, abstract_only)
  - reasoning: Multiple recent applications describe methods to improve hybrid bonding quality and electrical performance. Applied Materials addresses parasitic capacitance and TSV grounding, while Micron and Huawei focus on barrier layers and cleaning molten slag debris to improve yield. Hon Hai and JCET describe bonding LED and semiconductor wafers directly.
- **[P2]** *(ai_interpretation, confidence medium)* Die-to-die interconnect protocols and bandwidth aggregation are being standardized and optimized for high-bandwidth memory and vehicle applications.
  - source: [TRANSACTION LAYER PROTOCOL FOR COMMUNICATING HBM TRAFFIC OVER DIE-TO-DIE PHYSICAL LAYER INTERFACES [US20260339856A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339856A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [METHOD FOR ADJUSTING A COMMUNICATION BANDWIDTH WITHIN A PROTOCOL STACK OF A CHIPLET [WO2026219733A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026219733A1) (EPO OPS, 2026-10-22, abstract_only)
  - source: [FLEXIBLE CHIPLET ARCHITECTURE WITH BANDWIDTH AGGREGATION [US20260300208A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300208A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [Chiplet, Chiplet-System und Verfahren zur Datenübertragung innerhalb eines Chiplet-Systems [DE102025115112A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115112A1) (EPO OPS, 2026-10-22, metadata_only)
  - source: [Chiplet, Chiplet-System und Verfahren zur Kommunikation innerhalb eines Chiplet-Systems [DE102025115115A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115115A1) (EPO OPS, 2026-10-22, metadata_only)
  - reasoning: Filings describe transaction layer protocols for HBM traffic over die-to-die interfaces, bandwidth adjustment based on signal priority, and UCIe module aggregation. Bosch and FortaeGis also cover protocol stacks and trusted authentication between chiplets, indicating a push toward interoperable and secure interconnect standards.
- **[P3]** *(ai_interpretation, confidence medium)* Chiplet system management, telemetry, and thermal/power delivery are critical for reliability in 3D stacked architectures.
  - source: [CERTIFIED TELEMETRY DATA COLLECTION IN CHIPLET PROCESSOR ARCHITECTURE [US20260339808A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339808A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [POWER DELIVERY AND COOLING OF 3D STACKED MULTI-CHIPLET MODULES [US20260344508A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260344508A1) (EPO OPS, 2026-10-29, abstract_only)
  - source: [GLOBAL RAS DECISION AND DVFS ALLOCATOR WITH PER DIE MONITORS AND CONTROLLERS IN CHIPLET ARCHITECTURES [US20260329452A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260329452A1) (EPO OPS, 2026-10-22, abstract_only)
  - source: [OPTICAL INTERCONNECT MONITORING AND FAULT DETECTION IN DISTRIBUTED COMPUTING COMPONENTS [US20260322683A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260322683A1) (EPO OPS, 2026-10-15, abstract_only)
  - reasoning: Applications describe certified telemetry collection across multiple chiplets, global DVFS and RAS controllers for aging uniformity, and heat-conducting layers for power delivery. Citibank's filing uses AI models to predict faults in optical interconnects, highlighting growing attention to system-level monitoring and predictive maintenance.
- **[P4]** *(ai_interpretation, confidence medium)* Specialized chiplets for analog in-memory compute, co-packaged optics, and memory arbiters are emerging to address AI and storage bottlenecks.
  - source: [INTEGRATED CIRCUIT WITH ANALOG IN-MEMORY COMPUTE AND OPTICAL INTERCONNECT [US20260310621A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260310621A1) (EPO OPS, 2026-10-08, abstract_only)
  - source: [INTEGRATED CIRCUIT WITH ANALOG IN-MEMORY COMPUTE [US20260310620A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260310620A1) (EPO OPS, 2026-10-08, abstract_only)
  - source: [SEMICONDUCTOR PACKAGE AND PRINTED CIRCUIT BOARD ASSEMBLY [US20260324513A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260324513A1) (EPO OPS, 2026-10-15, abstract_only)
  - source: [MEMORY CHIPLET ARCHITECTURE AND SEMICONDUCTOR PACKAGE STRUCTURE USING THE SAME [US20260300190A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300190A1) (EPO OPS, 2026-10-01, abstract_only)
  - source: [Processor system [GB2705588A]](https://worldwide.espacenet.com/patent/search?q=pn%3DGB2705588A) (EPO OPS, 2026-10-21, abstract_only)
  - reasoning: Optoml describes vertically stacked cluster chiplets with analog in-memory compute and optical interconnects. MediaTek files for optical chiplets mounted on interposers, while Walechip and Red Semiconductor address memory bank arbitration and separate interface units, respectively, pointing to modular designs for AI acceleration and high-bandwidth storage.
- **[P5]** *(verified_fact, confidence medium)* Robert Bosch GmbH is the most active filer in this sample, with six applications focused on vehicle chiplet systems and communication protocol stacks.
  - source: [Chiplet, Chiplet-System und Verfahren zur Datenübertragung innerhalb eines Chiplet-Systems [DE102025115112A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115112A1) (EPO OPS, 2026-10-22, metadata_only)
  - source: [Chiplet, Chiplet-System und Verfahren zur Kommunikation innerhalb eines Chiplet-Systems [DE102025115115A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115115A1) (EPO OPS, 2026-10-22, metadata_only)
  - source: [Protokollschicht, Protokollstapel, Chiplet, Chiplet-System und Verfahren zur Fehlererkennung und Isolation eines Chiplets innerhalb eines Chiplet-Systems [DE102025115110A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115110A1) (EPO OPS, 2026-10-22, metadata_only)
  - source: [Protokoll Stack, Verfahren zum Konfigurieren eines Protokoll Stacks und Chiplet [DE102025115117A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115117A1) (EPO OPS, 2026-10-22, metadata_only)
  - source: [METHOD FOR ADJUSTING A COMMUNICATION BANDWIDTH WITHIN A PROTOCOL STACK OF A CHIPLET [WO2026219733A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026219733A1) (EPO OPS, 2026-10-22, abstract_only)
  - source: [CHIPLET SYSTEM AND METHOD FOR A CHIPLET SYSTEM [WO2026209144A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026209144A1) (EPO OPS, 2026-10-08, abstract_only)
  - excerpt: "A chiplet system comprising a first chiplet configured to perform first functions for a vehicle and a second chiplet configured to perform second functions for a vehicle"
  - reasoning: The applicant list shows Bosch filing six times, significantly more than other entities. The titles and abstracts confirm a focus on chiplet communication, protocol stack configuration, bandwidth adjustment, and distinct functions for vehicle applications.

**Limitations:**
- Analysis relies solely on titles and abstracts, which may omit critical claim details or broader technical scope.
- The sample covers only the 25 most recent publications out of 1,495 since 2023, which may not represent the full landscape.
- Patent publication delays of approximately 18 months mean recent filing activity is likely undercounted.
- Keyword matching may miss relevant patents that describe chiplet technologies using alternative terminology.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: partial. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.

| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |
|---|---|---|---|---|---|---|---|
| Marvell Technology (MRVL) | 141.2 (2026-11-06) | -48.6% | -32.3% | -39.7% | 112.6% | -57.2% | **subdued**: 39.7% below its 50-day average and -32.3% over 3 months; high volatility (112.6% annualised, 20-day) |
| Advanced Micro Devices (AMD) | 449.04 (2026-11-06) | -27.7% | -4.4% | -17.9% | 106.4% | -31.8% | **subdued**: 17.9% below its 50-day average and -4.4% over 3 months; high volatility (106.4% annualised, 20-day) |
| Intel (INTC) | 56.28 (2026-11-06) | -47.4% | -42.3% | -42.5% | 137.2% | -60.5% | **subdued**: 42.5% below its 50-day average and -42.3% over 3 months; high volatility (137.2% annualised, 20-day) |

- **[T1]** *(verified_fact, confidence medium)* Marvell Technology has fallen sharply over the past month and trades far below its 50-day average, with very high short-term volatility.
  - source: [Marvell Technology (MRVL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MRVL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -48.6%. 3-month return -32.3%. Price vs 50-day average -39.7%. 20-day annualised volatility 112.6%."
- **[T2]** *(ai_interpretation, confidence medium)* For Marvell, the rule-based timing risk is subdued in the sense of no recent run-up: the stock sits 39.7% below its 50-day average and 57.2% below its 100-day high. This means the timing risk here is not one of an overextended price, but of a steep, volatile decline continuing; a subdued level does not imply the price will recover.
  - source: [Marvell Technology (MRVL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MRVL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T3]** *(verified_fact, confidence medium)* AMD has pulled back over the past month (-27.7%) and trades 17.9% below its 50-day average, with 20-day annualised volatility of 106.4%.
  - source: [Advanced Micro Devices (AMD) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMD&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -27.7%. 3-month return -4.4%. Price vs 50-day average -17.9%. 20-day annualised volatility 106.4%."
- **[T4]** *(ai_interpretation, confidence medium)* AMD shows the mildest drawdown of the three chiplet-linked names (-31.8% from its 100-day high, 3-month return -4.4%), so timing risk from prior run-up is low, but volatility above 100% annualised means large day-to-day price swings remain a material risk either way.
  - source: [Advanced Micro Devices (AMD) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMD&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T5]** *(verified_fact, confidence medium)* Intel has declined steeply, down 47.4% in one month and 42.3% over three months, trading 42.5% below its 50-day average with the highest volatility of the group (137.2% annualised).
  - source: [Intel (INTC) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -47.4%. 3-month return -42.3%. Price vs 50-day average -42.5%. 20-day annualised volatility 137.2%."
- **[T6]** *(ai_interpretation, confidence medium)* Intel's timing-risk profile is dominated by extreme volatility and a 60.5% fall from its 100-day high rather than by prior run-up. For a researcher of the chiplet theme, this indicates prices in the theme are moving violently; subdued run-up metrics here reflect heavy selling pressure, not stability.
  - source: [Intel (INTC) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T7]** *(ai_interpretation, confidence medium)* Cross-company observation: none of the three chiplet-linked stocks shows run-up risk; all are well below their 50-day averages and 100-day highs, but all carry very high short-term volatility (106%-137% annualised), so the dominant timing risk across the theme is sharp ongoing price swings rather than overextension.
  - source: [Marvell Technology (MRVL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MRVL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Advanced Micro Devices (AMD) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMD&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Intel (INTC) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)

**Limitations:**
- The metrics cover only about 100 trading days, a short window that may not capture longer-term price context or structural trends.
- Analysis is based solely on computed price metrics; no fundamentals, valuation, earnings, or news are considered.
- Prices move for many reasons unrelated to the chiplet topic (macro conditions, sector-wide moves, company-specific events), so these readings cannot be attributed to the theme alone.
- Past price behaviour does not predict future prices; 'subdued' timing risk means no recent run-up, not that prices will rise or have bottomed.
- Volatility figures are annualised from only 20 days and can change quickly.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 30 distinct company names from 25 patent publications, 1 company-affiliated papers and 13 SEC filers; 16 matched to the SEC ticker file (8 outside the configured list), 10 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Arteris, Inc. (AIP) · Semiconductors & Related Devices | 0 | 0 | 6 | micro: 0.07B USD | +22.3% | 70.7% | **55** |
| Nova Ltd. (NVMI) · Optical Instruments & Lenses | 0 | 0 | 1 | small: 0.88B USD | +31.0% | 16.3% | **50** |
| Ceva Inc (CEVA) · Services-Computer Programming, Data Processing, Etc. | 0 | 0 | 2 | micro: 0.09B USD | +20.4% | n/a | **45** |
| Credo Technology Group Holding Ltd (CRDO) · Semiconductors & Related Devices | 0 | 0 | 1 | mid: 1.34B USD | +205.7% | 20.9% | **45** |
| Kulicke & Soffa Industries Inc (KLIC) · Semiconductors & Related Devices | 0 | 0 | 1 | small: 0.65B USD | -7.4% | 22.9% | **40** |
| Mercury Systems Inc (MRCY) · Electronic Components & Accessories | 0 | 0 | 1 | small: 0.98B USD | +7.9% | 6.1% | **35** |
| Cadence Design Systems Inc (CDNS) · Services-Prepackaged Software | 0 | 0 | 1 | mid: 5.30B USD | +14.1% | n/a | **30** |
| Pdf Solutions Inc (PDFS) · Services-Prepackaged Software | 0 | 0 | 1 | small: 0.10B USD | -5.2% | n/a | **30** |

- Arteris, Inc.: 6 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth +22% (+10); R&D 71% of revenue (+10)
- Nova Ltd.: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +31% (+10); R&D 16% of revenue (+10)
- Ceva Inc: 2 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth +20% (+10)
- Credo Technology Group Holding Ltd: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +206% (+10); R&D 21% of revenue (+10)
- Kulicke & Soffa Industries Inc: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth -7% (+0); R&D 23% of revenue (+10)
- Mercury Systems Inc: 1 SEC report(s) mentioning the topic (+15); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +8% (+5)

**Configured incumbents that also showed up:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Marvell Technology (MRVL) | 0 | 0 | 2 | mid: 8.19B USD | +42.1% | 25.3% | **50** |
| Applied Materials Inc /De (AMAT) | 1 | 0 | 1 | large: 28.37B USD | +4.4% | 12.6% | **35** |
| INTEL CORP (INTC) | 1 | 0 | 1 | large: 52.85B USD | -0.5% | 26.1% | **35** |
| Advanced Micro Devices (AMD) | 0 | 0 | 1 | large: 34.64B USD | +34.3% | 23.4% | **35** |
| Lam Research (LRCX) | 0 | 0 | 1 | large: 23.23B USD | +26.0% | 10.2% | **30** |
| Micron Technology Inc (MU) | 2 | 0 | 0 | large: 133.19B USD | +256.3% | 4.2% | **28** |
| Qualcomm Inc/De (QCOM) | 1 | 0 | 0 | large: 43.12B USD | -2.6% | 23.7% | **20** |
| Nvidia Corp (NVDA) | 0 | 1 | 0 | large: 26.91B USD | +61.4% | n/a | **18** |

**Found but not in the SEC ticker file (private, foreign, or name not matched):** BOSCH GMBH ROBERT (6P/0A/0F), OPTOML PTE LTD (2P/0A/0F), HON HAI PREC INDUSTRY CO LTD (1P/0A/0F), JCET STATS CHIPPAC KOREA LTD (1P/0A/0F), OPENCHIP & SOFTWARE TECH S L (1P/0A/0F), IBM (1P/0A/0F), AP MEMORY TECH CORPORATION (1P/0A/0F), SAMSUNG ELECTRONICS CO LTD (1P/0A/0F), MEDIATEK INC (1P/0A/0F), CITIBANK NA (1P/0A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* Arteris, Inc. (AIP) is active on chiplet: 6 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.07B USD (micro by revenue), growth +22.3%, R&D 70.7% of revenue. Next-runner score 55/100 (heuristic).
  - source: [Arteris, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1667011/000162828026071154/aip-20260930.htm) (SEC EDGAR, 2026-11-05, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Nova Ltd. (NVMI) is active on chiplet: 1 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.88B USD (small by revenue), growth +31.0%, R&D 16.3% of revenue. Next-runner score 50/100 (heuristic).
  - source: [Nova Ltd. Form 20-F, filed 2026-02-17](https://www.sec.gov/Archives/edgar/data/1109345/000117891326000504/zk2634307.htm) (SEC EDGAR, 2026-02-17, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Ceva Inc (CEVA) is active on chiplet: 2 of its SEC report(s) mention the topic; fiscal 2017 revenue 0.09B USD (micro by revenue), growth +20.4%. Next-runner score 45/100 (heuristic).
  - source: [Ceva Inc Form 10-K, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1173489/000143774926006091/ceva20251231_10k.htm) (SEC EDGAR, 2026-02-27, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Credo Technology Group Holding Ltd (CRDO) is active on chiplet: 1 of its SEC report(s) mention the topic; fiscal 2025 revenue 1.34B USD (mid by revenue), growth +205.7%, R&D 20.9% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Credo Technology Group Holding Ltd Form 10-K, filed 2026-06-15](https://www.sec.gov/Archives/edgar/data/1807794/000162828026043303/crdo-20260502.htm) (SEC EDGAR, 2026-06-15, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K5]** *(ai_interpretation, confidence low)* Kulicke & Soffa Industries Inc (KLIC) is active on chiplet: 1 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.65B USD (small by revenue), growth -7.4%, R&D 22.9% of revenue. Next-runner score 40/100 (heuristic).
  - source: [Kulicke & Soffa Industries Inc Form 10-K, filed 2025-11-20](https://www.sec.gov/Archives/edgar/data/56978/000005697825000081/klic-20251004.htm) (SEC EDGAR, 2025-11-20, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K6]** *(ai_interpretation, confidence low)* Mercury Systems Inc (MRCY) is active on chiplet: 1 of its SEC report(s) mention the topic; fiscal 2026 revenue 0.98B USD (small by revenue), growth +7.9%, R&D 6.1% of revenue. Next-runner score 35/100 (heuristic).
  - source: [Mercury Systems Inc Form 10-K, filed 2025-08-11](https://www.sec.gov/Archives/edgar/data/1049521/000104952125000024/mrcy-20250627.htm) (SEC EDGAR, 2025-08-11, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [@SemiconductorsX: HBM is no longer a drop-in commodity. From HBM4 on, the base logic die is co-designed with…](https://x.com/SemiconductorsX/status/2119275506436866336) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_e1a886c435
- [@TechieUltimatum: PS6 vs Xbox Project Helix: Microsoft could be building a MUCH more powerful next-gen conso…](https://x.com/TechieUltimatum/status/2119007757269659727) | X API | 2026-11-07 | retrieved 2026-11-09 | full_text | id src_c1ef0343db
- [Marvell Technology (MRVL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MRVL&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_f4e6995472
- [Advanced Micro Devices (AMD) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMD&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_1d09c72ae3
- [Intel (INTC) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INTC&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_5ab961d478
- [Arteris, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1667011/000162828026071154/aip-20260930.htm) | SEC EDGAR | 2026-11-05 | retrieved 2026-11-09 | excerpt_only | id src_1b5f942613
- [@Cadence: 64GT/s is the milestone. What it enables is the bigger story. In Part 2 of our UCIe series…](https://x.com/Cadence/status/2118418144607842733) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_c5ea20e6c0
- [@Finsee_main: $AIP Q3 2026 earnings: Arteris nears its first profit, but backlog additions stall Arteris…](https://x.com/Finsee_main/status/2118457114355994661) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_9e767db716
- [ELECTRIC-FIELD SHUNT FOR HYBRID BONDING INTERFACES [US20260354205A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354205A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-09 | abstract_only | id src_27f40f48fc
- [SEMICONDUCTOR STRUCTURE AND MANUFACTURING METHOD THEREOF [US20260353862A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260353862A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-09 | abstract_only | id src_1c2c22c63b
- [SEMICONDUCTOR PACKAGE AND METHOD FOR FORMING THE SAME [US20260354284A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260354284A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-09 | abstract_only | id src_80bae34665
- [MEMORY CHIP HAVING HYBRID BONDING PADS AND SEMICONDUCTOR DEVICE INCLUDING THE SAME [US20260351293A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260351293A1) | EPO OPS | 2026-11-05 | retrieved 2026-11-09 | abstract_only | id src_b6015d320f
- [@eeNewsEurope: Could chiplets and more efficient memory help shape the next generation of semiconductor t…](https://x.com/eeNewsEurope/status/2117708581143278020) | X API | 2026-11-03 | retrieved 2026-11-09 | full_text | id src_8ecbf97f9f
- [@Finsee_main: $ADEA Q3 2026 earnings: Adeia cuts its annual sales plan while legal costs rise Adeia's qu…](https://x.com/Finsee_main/status/2117364680914022506) | X API | 2026-11-02 | retrieved 2026-11-09 | full_text | id src_d2ad14244c
- [HYBRID BONDING TECHNIQUES THAT UTILIZE MULTI-FUNCTIONAL BARRIER MATERIALS [US20260344498A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260344498A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-09 | abstract_only | id src_194011e327
- [CERTIFIED TELEMETRY DATA COLLECTION IN CHIPLET PROCESSOR ARCHITECTURE [US20260339808A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339808A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-09 | abstract_only | id src_95d74ca37f
- [TRANSACTION LAYER PROTOCOL FOR COMMUNICATING HBM TRAFFIC OVER DIE-TO-DIE PHYSICAL LAYER INTERFACES [US20260339856A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260339856A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-09 | abstract_only | id src_04290c22b0
- [POWER DELIVERY AND COOLING OF 3D STACKED MULTI-CHIPLET MODULES [US20260344508A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260344508A1) | EPO OPS | 2026-10-29 | retrieved 2026-11-09 | abstract_only | id src_81bcedf46e
- [Applied Materials Inc /De 8-K press release (exhibit ex991prforprojectbasil.htm), filed 2026-10-26](https://www.sec.gov/Archives/edgar/data/6951/000162828026067303/ex991prforprojectbasil.htm) | SEC EDGAR | 2026-10-26 | retrieved 2026-11-09 | excerpt_only | id src_ab03a143c8
- [Chiplet, Chiplet-System und Verfahren zur Datenübertragung innerhalb eines Chiplet-Systems [DE102025115112A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115112A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | metadata_only | id src_bdd625620f
- [Chiplet, Chiplet-System und Verfahren zur Kommunikation innerhalb eines Chiplet-Systems [DE102025115115A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115115A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | metadata_only | id src_acba4a1635
- [Protokollschicht, Protokollstapel, Chiplet, Chiplet-System und Verfahren zur Fehlererkennung und Isolation eines Chiplets innerhalb eines Chiplet-Systems [DE102025115110A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115110A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | metadata_only | id src_72b4373153
- [Protokoll Stack, Verfahren zum Konfigurieren eines Protokoll Stacks und Chiplet [DE102025115117A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DDE102025115117A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | metadata_only | id src_18ab0b2ad8
- [METHOD FOR ADJUSTING A COMMUNICATION BANDWIDTH WITHIN A PROTOCOL STACK OF A CHIPLET [WO2026219733A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026219733A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | abstract_only | id src_0e47238f6d
- [GLOBAL RAS DECISION AND DVFS ALLOCATOR WITH PER DIE MONITORS AND CONTROLLERS IN CHIPLET ARCHITECTURES [US20260329452A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260329452A1) | EPO OPS | 2026-10-22 | retrieved 2026-11-09 | abstract_only | id src_8ce5547772
- [Processor system [GB2705588A]](https://worldwide.espacenet.com/patent/search?q=pn%3DGB2705588A) | EPO OPS | 2026-10-21 | retrieved 2026-11-09 | abstract_only | id src_169744dd3d
- [SEMICONDUCTOR PACKAGE AND PRINTED CIRCUIT BOARD ASSEMBLY [US20260324513A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260324513A1) | EPO OPS | 2026-10-15 | retrieved 2026-11-09 | abstract_only | id src_b40e0bdd54
- [OPTICAL INTERCONNECT MONITORING AND FAULT DETECTION IN DISTRIBUTED COMPUTING COMPONENTS [US20260322683A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260322683A1) | EPO OPS | 2026-10-15 | retrieved 2026-11-09 | abstract_only | id src_a2f5f597f6
- [CHIPLET SYSTEM AND METHOD FOR A CHIPLET SYSTEM [WO2026209144A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026209144A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-09 | abstract_only | id src_526845ac55
- [TRUSTED COMMUNICATION FOR CHIPLET ASSEMBLIES [WO2026209922A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026209922A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-09 | abstract_only | id src_d94f81df5a
- [INTEGRATED CIRCUIT WITH ANALOG IN-MEMORY COMPUTE AND OPTICAL INTERCONNECT [US20260310621A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260310621A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-09 | abstract_only | id src_4f25d3664f
- [INTEGRATED CIRCUIT WITH ANALOG IN-MEMORY COMPUTE [US20260310620A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260310620A1) | EPO OPS | 2026-10-08 | retrieved 2026-11-09 | abstract_only | id src_c833f035e9
- [FLEXIBLE CHIPLET ARCHITECTURE WITH BANDWIDTH AGGREGATION [US20260300208A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300208A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-09 | abstract_only | id src_c47eb2375c
- [CHIP STACK STRUCTURE, MANUFACTURING METHOD THEREFOR, CHIP PACKAGE STRUCTURE, AND ELECTRONIC DEVICE [WO2026200137A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026200137A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-09 | abstract_only | id src_0d18ec3860
- [MEMORY CHIPLET ARCHITECTURE AND SEMICONDUCTOR PACKAGE STRUCTURE USING THE SAME [US20260300190A1]](https://worldwide.espacenet.com/patent/search?q=pn%3DUS20260300190A1) | EPO OPS | 2026-10-01 | retrieved 2026-11-09 | abstract_only | id src_189fbc3548
- [METHODS OF FORMING BRIDGE CHIPLET SHIELD STRUCTURES [EP4815713A2]](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4815713A2) | EPO OPS | 2026-09-30 | retrieved 2026-11-09 | abstract_only | id src_8c6e00d40b
- [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](https://arxiv.org/abs/2609.10970v1) | arXiv | 2026-09-10 | retrieved 2026-11-09 | abstract_only | id src_4d93cbadd2
- [Marvell Technology, Inc. Form 10-Q (FORM 10-Q), filed 2026-08-28](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000025/mrvl-20260801.htm) | SEC EDGAR | 2026-08-28 | retrieved 2026-11-09 | excerpt_only | id src_6217df255e
- [Lam Research Corp Form 10-K, filed 2026-08-07](https://www.sec.gov/Archives/edgar/data/707549/000070754926000037/lrcx-20260628.htm) | SEC EDGAR | 2026-08-07 | retrieved 2026-11-09 | excerpt_only | id src_10f8a976da
- [FAPlace: Joint Optimization of Chiplet Placement and Interposer Footprint for 2.5D Systems](https://doi.org/10.1145/3787109.3815298) | OpenAlex | 2026-06-18 | retrieved 2026-11-09 | abstract_only | id src_602e5f7ea3
- [Credo Technology Group Holding Ltd Form 10-K, filed 2026-06-15](https://www.sec.gov/Archives/edgar/data/1807794/000162828026043303/crdo-20260502.htm) | SEC EDGAR | 2026-06-15 | retrieved 2026-11-09 | excerpt_only | id src_442a04871e
- [Photonic-Interconnected Quantum Chiplets for Modular and Networked Quantum Computing](https://doi.org/10.62311/nesx/rp9-30052026) | OpenAlex | 2026-05-24 | retrieved 2026-11-09 | abstract_only | id src_641a33128a
- [Marvell Technology, Inc. Form 10-K (FORM 10-K), filed 2026-03-11](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm) | SEC EDGAR | 2026-03-11 | retrieved 2026-11-09 | excerpt_only | id src_ce00447bcf
- [CarbonPATH: Carbon-aware pathfinding and architecture optimization for chiplet-based AI systems](https://doi.org/10.48550/arxiv.2603.03878) | OpenAlex | 2026-03-04 | retrieved 2026-11-09 | abstract_only | id src_dc3aff89e3
- [Ceva Inc Form 10-K, filed 2026-02-27](https://www.sec.gov/Archives/edgar/data/1173489/000143774926006091/ceva20251231_10k.htm) | SEC EDGAR | 2026-02-27 | retrieved 2026-11-09 | excerpt_only | id src_45a16a8a0a
- [Pdf Solutions Inc Form 10-K, filed 2026-02-24](https://www.sec.gov/Archives/edgar/data/1120914/000143774926005366/pdfs20251231d_10k.htm) | SEC EDGAR | 2026-02-24 | retrieved 2026-11-09 | excerpt_only | id src_f71c367de3
- [Cadence Design Systems Inc Form 10-K, filed 2026-02-19](https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm) | SEC EDGAR | 2026-02-19 | retrieved 2026-11-09 | excerpt_only | id src_ff6d69bb47
- [Nova Ltd. Form 20-F, filed 2026-02-17](https://www.sec.gov/Archives/edgar/data/1109345/000117891326000504/zk2634307.htm) | SEC EDGAR | 2026-02-17 | retrieved 2026-11-09 | excerpt_only | id src_1cc820d689
- [Advanced Micro Devices Inc Form 10-K, filed 2026-02-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm) | SEC EDGAR | 2026-02-04 | retrieved 2026-11-09 | excerpt_only | id src_ba0fa71be5
- [Intel Corp Form 10-K, filed 2026-01-23](https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm) | SEC EDGAR | 2026-01-23 | retrieved 2026-11-09 | excerpt_only | id src_3374efcb45
- [A Comparative Study of Monolithic and Chiplet CPU Architectures: Performance and Yield Perspectives](https://doi.org/10.12792/iciae2026.005) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | abstract_only | id src_e66f051609
- [Kulicke & Soffa Industries Inc Form 10-K, filed 2025-11-20](https://www.sec.gov/Archives/edgar/data/56978/000005697825000081/klic-20251004.htm) | SEC EDGAR | 2025-11-20 | retrieved 2026-11-09 | excerpt_only | id src_ecb0d60feb
- [Delegato: Locality-Aware Atomic Memory Operations on Chiplets](https://doi.org/10.1145/3725843.3756030) | OpenAlex | 2025-10-17 | retrieved 2026-11-09 | abstract_only | id src_20f2377341
- [Mercury Systems Inc Form 10-K, filed 2025-08-11](https://www.sec.gov/Archives/edgar/data/1049521/000104952125000024/mrcy-20250627.htm) | SEC EDGAR | 2025-08-11 | retrieved 2026-11-09 | excerpt_only | id src_1742438bb6
- [ChipletPart: Cost-Aware Partitioning for 2.5D Systems](https://arxiv.org/abs/2507.19819v3) | arXiv | 2025-07-26 | retrieved 2026-11-09 | abstract_only | id src_eec1d1a032
- [System-performance and cost modeling of Large Language Model training and inference](https://arxiv.org/abs/2507.02456v1) | arXiv | 2025-07-03 | retrieved 2026-11-09 | abstract_only | id src_8e7d85a20a
- [Chiplet-LEGO: Delivering Multiple Voltage Rails to Chiplets with Chiplet VRMs](https://doi.org/10.1109/compel57166.2025.11121243) | OpenAlex | 2025-06-22 | retrieved 2026-11-09 | abstract_only | id src_e2f9d27d90
- [FoldedHexaTorus: An Inter-Chiplet Interconnect Topology for Chiplet-based Systems using Organic and Glass Substrates](https://doi.org/10.48550/arxiv.2504.19878) | OpenAlex | 2025-04-28 | retrieved 2026-11-09 | abstract_only | id src_f45eb0dd41
- [Emerging Chiplet-Based Architectures for Heterogeneous Integration](https://doi.org/10.32628/cseit25112439) | OpenAlex | 2025-03-12 | retrieved 2026-11-09 | abstract_only | id src_5414723b87
- [The Survey of Chiplet-based Integrated Architecture: An EDA perspective](https://arxiv.org/abs/2411.04410v1) | arXiv | 2024-11-07 | retrieved 2026-11-09 | abstract_only | id src_c79ea9c7a2
- [Evaluating Vulnerability of Chiplet-Based Systems to Contactless Probing Techniques](https://doi.org/10.1109/itc51657.2024.00022) | OpenAlex | 2024-11-03 | retrieved 2026-11-09 | abstract_only | id src_5a6ffd9bd5
- [MFIT: Multi-Fidelity Thermal Modeling for 2.5D and 3D Multi-Chiplet Architectures](https://arxiv.org/abs/2410.09188v4) | arXiv | 2024-10-11 | retrieved 2026-11-09 | abstract_only | id src_c12eaac7f0
- [Chiplet-Gym: Optimizing Chiplet-Based AI Accelerator Design With Reinforcement Learning](https://doi.org/10.1109/tc.2024.3457740) | OpenAlex | 2024-09-11 | retrieved 2026-11-09 | abstract_only | id src_b01918dba5
- [Chiplets on Wheels: Review Paper on Holistic Chiplet Solutions for Autonomous Vehicles](https://arxiv.org/abs/2406.00182v1) | arXiv | 2024-05-31 | retrieved 2026-11-09 | abstract_only | id src_0430d2dc0a
- [Reliability and Chiplets](https://doi.org/10.1109/mrl.2024.3386643) | OpenAlex | 2024-04-19 | retrieved 2026-11-09 | abstract_only | id src_56397432e6
- [Chiplet Placement Order Exploration Based on Learning to Rank with Graph Representation](https://arxiv.org/abs/2404.04943v1) | arXiv | 2024-04-07 | retrieved 2026-11-09 | abstract_only | id src_68434f3428
- [Floorplet: Performance-aware Floorplan Framework for Chiplet Integration](https://arxiv.org/abs/2308.01672v2) | arXiv | 2023-08-03 | retrieved 2026-11-09 | abstract_only | id src_ba79490075
- [HexaMesh: Scaling to Hundreds of Chiplets with an Optimized Chiplet Arrangement](https://doi.org/10.1109/dac56929.2023.10248006) | OpenAlex | 2023-07-09 | retrieved 2026-11-09 | abstract_only | id src_77bc8b2776
- [Recent Advances and Trends in Chiplet Design and Heterogeneous Integration Packaging](https://doi.org/10.1115/1.4062529) | OpenAlex | 2023-05-15 | retrieved 2026-11-09 | abstract_only | id src_3d4fdc51d7
- [Automated Design of Chiplets](https://doi.org/10.1145/3569052.3578917) | OpenAlex | 2023-03-22 | retrieved 2026-11-09 | abstract_only | id src_c2273b57ae
- [Chiplet Design and Heterogeneous Integration Packaging](https://doi.org/10.1007/978-981-19-9917-8) | OpenAlex | 2023-01-01 | retrieved 2026-11-09 | metadata_only | id src_b6dd836db9

## Gaps, limitations and errors
- Missing data: Revenue or order volumes attributable to chiplet products, and named customers.
- Missing data: Fabricated-silicon validation of cost, yield and thermal benefits, since most academic evidence is simulation or models [R3].
- Missing data: Code-computed patent counts and growth trends; the patent sample is small.
- Missing data: Evidence on standards adoption (e.g. UCIe) beyond a company social post [X1] and the Risk challenge [C9].
- Missing data: Verified post-announcement evidence for social-media claims (HBM4 base-die co-design, console chips, Arteris results).
- Missing data: Information on private or foreign players seen only in patents (Bosch, OptoML, Hon Hai, JCET, OpenChip, IBM).
- Limitation: Research counts come from exact-phrase matching in OpenAlex and are not normalised for overall publishing growth; research activity is not commercial success.
- Limitation: Science findings were challenged by the Risk agent on several points (C1-C9), so those findings carry lower weight.
- Limitation: Market evidence mostly shows company positioning in annual and quarterly reports, not demonstrated adoption.
- Limitation: X findings are unverified social signals and were used only as context.
- Limitation: Price findings are code-computed risk context over about 100 trading days, not timing guidance.
- Limitation: Scout scores are heuristics, and smaller companies listed carry higher risk and thinner disclosure.
- Limitation: This is a research assessment, not a recommendation or forecast of returns.
- Chief review gap: Die-to-die interconnect performance (measured bandwidth and latency from published silicon) is thin; evidence is limited to a latency-impact paper (R2) and protocol patents (P2), with no dedicated finding on UCIe standard versions or measured interconnect throughput.
- Chief review gap: Hybrid bonding manufacturing maturity (defect rates, throughput, wafer-level yield) is covered by patents (P1) and a market filing (M4) but has no dedicated research-paper finding quantifying process readiness.
- Chief review gap: The yield advantage of chiplets over monolithic dies rests on a toy FPGA model with a Poisson yield assumption (R4); no foundry-level or large-SoC yield data is present.
- Chief review gap: Several science findings (S4, S6, S7, S8, S9, S10) and most risk findings (R4–R8) carry low confidence, meaning the report must hedge heavily on specific technical claims.
- Chief review gap: X findings are all unverified social signals and cannot be used as factual support; the UCIe 64GT/s claim (X1) and HBM4 co-design claim (X2) remain unconfirmed by any verified source.
- ERROR [patent/EPO OPS]: counts: EPO refused the request (fair use / quota or bad token)
- ERROR [timing/Alpha Vantage]: AMAT: Alpha Vantage limit or notice: We have detected your API key as *** and our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https:
- ERROR [timing/Alpha Vantage]: LRCX: Alpha Vantage limit or notice: We have detected your API key as *** and our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https:
- ERROR [timing/Alpha Vantage]: AIP: Alpha Vantage limit or notice: We have detected your API key as *** and our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https:

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 2 | 6749 | 3457 | 0.00494 |
| x | z-ai/glm-5.3-flash | 1 | 2965 | 1100 | 0.00079 |
| relevance | z-ai/glm-5.3-flash | 3 | 8447 | 456 | 0.00090 |
| market | z-ai/glm-5.3 | 1 | 6212 | 1913 | 0.02054 |
| patent | Qwen/Qwen3.6-35B-A3B-FP8 | 1 | 6763 | 7198 | 0.00907 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 24266 | 11042 | 0.15895 |
| science | deepseek/deepseek-v4.1-flash | 1 | 4345 | 4096 | 0.00622 |
| timing | z-ai/glm-5.3-flash | 1 | 1393 | 1073 | 0.00065 |
| investment | anthropic/claude-sonnet-5-5 | 1 | 18145 | 9726 | 0.13355 |
| x (data) | X API pay-per-use | 7 | 0 | 0 | 0.03000 |

Total estimated cost: $0.36560 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
