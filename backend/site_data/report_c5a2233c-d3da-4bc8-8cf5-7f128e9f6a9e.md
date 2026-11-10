# FUTURESCOUT AI research report: silicon photonics

Generated: 2026-11-10 03:44 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, x, timing, scout, investment
- Agents NOT run in this version: patent. Conclusions therefore have no patent evidence.

## Verdict (forecast, computed from the report)
**Early and mixed: watch, do not assume** — score 53.8, confidence low.
Qualifiers: low confidence 35%, below the 70% that counts as confident; research is running well ahead of commercial reality.

Silicon photonics uses light instead of electricity to move data on and between chips, which matters more as AI data centres grow. Scientific interest is clearly rising, but most evidence so far is laboratory demonstrations, and the clearest business activity found is among companies selling testing and…

Why:
- Research Momentum rated 4/5: The phrase count grew from 1,157 to 1,304 (+12.7%) in 2025, and the year-to-date 2026 count is +27.7% versus 2025, so momentum is still building.
- Technical Feasibility rated 3/5: Device-level demonstrations are strong (100-GHz modulators and 56-GHz photodetectors on one chip, a foundry-compatible MEMS switch, a 32-channel link) [S2, S3, S4].
- Papers 2024→2025: 1157→1304 (+13%)
- So far in 2026 (to 10-11): 1299 papers vs 1017 by the same date in 2025 (+28%, rising)

Watch out for:
- System-level thermal sensitivity, noise and active stabilisation add complexity and power overhead.
- One optical supplier's outlook was reportedly cut by power and factory delays, and another's factory spending is consuming cash (unverified social signal).
- The result base is mostly single preprints, and the laser 'hardest component' claim leans heavily on one review.
- The quantum-dot detector is far slower (1.1 MHz) than the multi-GHz components elsewhere, targeting sensing rather than communications, and has no foundry-context assessment of lead content.

What would change this view:
- Stronger if: Verified volume-shipment or customer-contract disclosures by transceiver or co-packaged-optics makers, which are currently absent from the retrieved evidence.
- Weaker if: Scaling to large unit volumes stalls because the integration, fabrication or packaging bottlenecks are not resolved.
- Stronger if: Peer-reviewed, foundry-scale yield and contamination data for lithium niobate or tantalate integration.
- Weaker if: Contamination or yield problems prevent thin-film electro-optic or III-V integration from being run in standard foundry processes.

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
Research on silicon photonics is growing: 1,304 works in 2025 (+12.7% year on year) and 1,299 so far in 2026 against 1,017 at the same point in 2025 (+27.7%). These are raw phrase counts, not adjusted for overall publishing growth, and research volume is not commercial success. The Science findings show many device-level demonstrations (heterogeneous modulators, MEMS switches, multi-wavelength links, alternative detectors) [S2, S3, S4, S7]. The Risk and challenge findings show that most of these are single preprints or design-stage claims, and that the on-chip laser, packaging and system-level control remain open problems [S1, R1, R2, R3, C10]. Retrieved commercial evidence sits mainly in the test and equipment layer (Teradyne, FormFactor, Veeco, Aehr), not in silicon-photonics chip or transceiver makers [M7]. Co-packaged optics and optical-supplier earnings appear only as unverified social signals [X1, X4]. The main uncertainty is whether device-level progress converts into volume manufacturing and paying customers. The related stocks have also fallen sharply and are highly volatile [T13]. No patent evidence was available.

## Technology Opportunity Score
**Opportunity score: 53.8 / 100** · **Confidence: 35%** (low; evidence 50% x risk multiplier 0.7) · evidence coverage 80%

Risk: rating 3/5 does not change the score; it multiplies confidence by 0.7.

Commercialization Gap (research momentum rating minus commercial readiness rating): +2


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 4 | S1, S12 | The phrase count grew from 1,157 to 1,304 (+12.7%) in 2025, and the year-to-date 2026 count is +27.7% versus 2025, so momentum is still building. The counts are not normalised for overall publishing growth and exact-phrase matching misses synonyms. Research activity is not commercial success. |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 3 | S2, S3, S4, R1, R2, C4, C5, C6 | Device-level demonstrations are strong (100-GHz modulators and 56-GHz photodetectors on one chip, a foundry-compatible MEMS switch, a 32-channel link) [S2, S3, S4]. Key limits remain: the on-chip laser is the hardest unsolved element, system-level thermal and control issues persist, and many results are single preprints with overstated scope [R1, R2, C1, C4, C5, C6]. |
| Commercial Readiness | 15% | 2 | M1, M2, M7, R3 | Filings show commercial activity in test and equipment (an acquisition, product lines for silicon photonics testing) [M1, M2, M7], but no verified evidence of silicon photonics chip or transceiver volume production. Scaling to billions of units is posed as an open question [R3]. |
| Customer Adoption | 10% | missing | none | no valid 0-5 rating given |
| Industry Investment | 10% | 3 | M1, M2, M5, X2 | Teradyne's $127.2 million acquisition of Quantifi Photonics and Veeco's and Aehr's stated exposure show real corporate spending in the equipment layer [M1, M2, M5]. A reported Marvell-Lumentum deal is an unverified claim and gets little weight [X2]. Investment in chip and transceiver makers is not evidenced. |
| Competitive Position | 10% | 2 | S12, R6, R8 | Silicon provides a mature foundry base [S12], but faces possible displacement or partitioning by indium phosphide, silicon nitride and silicon carbide [R6], and hybrid III-V lasers weaken the 'pure CMOS, low-cost' framing [R8]. No market-share evidence is available. |
| Supply-Chain Readiness | 15% | 2 | S2, S3, S8, M1, M2, X4, C5 | Foundry compatibility is a stated strength for several results [S2, S3, S8], and equipment suppliers address laser-facet coating and test [M2, M1]. Reported power and factory delays at an optical supplier are an unverified social signal [X4], and heterogeneous materials lack shown volume yield [C5]. |

Formula: score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a validated prediction of stock performance; confidence is not a probability of profit.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### AI data-centre optical interconnect and co-packaged optics

Technologies: silicon photonic transceivers, wavelength-division multiplexing, Kerr-comb links, co-packaged optics, MEMS optical switches

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Research cites AI and data-centre traffic as the driver of 1.6 Tb/s-plus optics [S4, S5]. Press and social signals show attention to co-packaged optics and optical-supplier demand [X1, X3, X4], but these are unverified. Test and equipment companies cite silicon photonics as a demand driver [M2, M5]. There is no verified evidence here of transceiver volumes or customer contracts. *(forecast)* [S4, S5, X1, X3, X4, M2, M5] | low |
| medium_1_3y | Whether lab results turn into products depends on the packaging, integration and fabrication bottlenecks that the roadmap review treats as unsolved. Scaling to billions of units is posed as an open question [S1, R3]. Thermal sensitivity and control overhead may limit deployment even if device results hold [R2, C10]. The Kerr-comb scalability claim is an extrapolation [R5, C4]. The evidence supports plausible but unproven adoption. *(forecast)* [S1, R2, R3, R5, C4, C10] | low |
| long_3_5y | The findings say nothing direct about 3-5 year outcomes. The roadmap says sensing and computing products are 'around the corner' but gives no dated path [R3]. Competing platforms (indium phosphide, silicon nitride, silicon carbide) could take or share roles [R6]. *(forecast)* [R3, R6] | low |

**Bull case:** AI traffic growth pushes optical links to higher wavelength counts. Foundry-compatible silicon photonics, with improved coupling and multi-wavelength sources, becomes the standard for co-packaged optics, and the press-reported supplier demand turns into sustained orders. *(forecast)* [S4, S5, X1, X4]

**Base case:** Silicon photonics is used where it fits, supported by a test and equipment ecosystem, while heterogeneous materials and packaging constrain the pace. Progress is steady but uneven, and some platform share goes to alternatives. *(forecast)* [S1, S12, M7, R6]

**Bear case:** Packaging, thermal control and laser integration costs hold back volume. Headline results prove narrower than described (S5 merges two results, and the Kerr-comb scaling is an extrapolation) [C1, C4]. Competing platforms or copper and other optics approaches take share. *(forecast)* [C1, C4, R2, R3, R6]

**Catalysts:**
- Verified volume-shipment or customer-contract disclosures by transceiver or co-packaged-optics makers, which are currently absent from the retrieved evidence. *(forecast)* [M7, X1]
- Measured demonstrations beyond 32 wavelength channels with quantified power and thermal-control overhead. *(forecast)* [R5, C4]

**Risks:**
- System-level thermal sensitivity, noise and active stabilisation add complexity and power overhead. *(ai_interpretation)* [R2, C10]
- One optical supplier's outlook was reportedly cut by power and factory delays, and another's factory spending is consuming cash (unverified social signal). *(unverified_claim)* [X4]
- Related stocks have pulled back 21-59% over three months with 90-164% annualised volatility, so timing risk is substantial. This is risk context only. *(ai_interpretation)* [T13]

**What would invalidate this thesis:**
- Scaling to large unit volumes stalls because the integration, fabrication or packaging bottlenecks are not resolved. *(forecast)* [S1, R3]
- Competing platforms (indium phosphide, silicon nitride, silicon carbide) displace or partition the silicon platform in interconnect. *(forecast)* [R6]

**Conflicting evidence:**
- Sub-1 dB coupling and 1-dB bandwidth over 100 nm come from different designs, and the bandwidth is stated as something the design 'can' achieve, so S5 overstates one device. *(ai_interpretation)* [S5, C1]
- The Kerr-comb link measured 512 Gb/s over 32 channels. Scalability to hundreds of channels is the authors' claim, not a measurement. *(ai_interpretation)* [S4, C4, R5]
- The MEMS switch result is a single element with no switching speed, dynamic power or reliability data, and large switch matrices are not shown. *(ai_interpretation)* [S3, C6]

**Companies named by cited evidence:**
- Broadcom: Named in an EE Times post as saying co-packaged optics cut power and latency. This is an unverified social signal, not evidence of adoption. [X1]
- Celestica: Named in the same unverified EE Times partner-interview post on co-packaged optics. [X1]
- Marvell: Counterpoint is reported to describe a Marvell purchase of Lumentum with an implied $115 billion value. This is an unverified claim that should be confirmed before any weight is given. [X2]
- Lumentum: Named as the target in the unverified Counterpoint post on the optics value chain. [X2]
- Coherent: Reported by a third-party account to have raised its sales plan on AI optical growth while factory spending consumes cash. Unverified. [X4]
- Applied Optoelectronics: Reported to have more than doubled sales but cut its outlook on power and factory delays. Unverified. [X4]
- Viavi: Reported data-centre testing sales up 57% year on year to $469 million. Unverified. [X4]

### Heterogeneous integration and on-chip light sources

Technologies: thin-film lithium niobate/tantalate on silicon, III-V and quantum-dot lasers, colloidal quantum-dot detectors, silicon nitride platforms, micro-transfer printing

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Evidence is lab-stage: first-of-kind preprints for lithium tantalate and thin-film lithium niobate integration, quantum-dot detectors and GaSb printing [S2, S6, S7]. None is shown to be manufacturable in volume, and the lithium contamination issue is acknowledged [C5, C7]. Little near-term commercial evidence exists apart from small companies positioning materials (Lightwave Logic, Aeluma) [M4, M6]. *(forecast)* [S2, S6, S7, C5, C7, M4, M6] | low |
| medium_1_3y | The abstracts frame the architecture as silicon plus added materials for modulation, gain and detection [S12], but that pattern is retrieval-driven and other constraints (laser, detectors, coupling, system control) are also named [C9, R1]. Whether these routes reach foundry-scale yield is not shown [C5]. Alternative light sources are early-stage or bring non-CMOS materials [R8]. *(forecast)* [S12, C9, R1, C5, R8] | low |
| long_3_5y | The evidence does not address 3-5 year outcomes for these materials. The on-chip laser is still described as the hardest unsolved element [R1], and platform competition could change which material stack prevails [R6]. *(forecast)* [R1, R6] | low |

**Bull case:** One or more integration routes (thin-film electro-optic layers, bonded or printed III-V gain, quantum-dot sources) proves manufacturable in foundry flows without process redesign, letting silicon photonics add faster modulation and integrated light sources. *(forecast)* [S2, S6, S12]

**Base case:** Several heterogeneous routes continue as lab and pilot demonstrations, with slow progress toward manufacturability. The laser source stays the main constraint, and commercial activity by small materials companies remains early. *(forecast)* [R1, C5, C7, M4, M6]

**Bear case:** Contamination, yield and cost problems keep heterogeneous materials out of volume production. Defect-based or hybrid laser routes fail to deliver, and other platforms take the roles silicon cannot fill. *(forecast)* [C5, C7, R6, R8]

**Catalysts:**
- Peer-reviewed, foundry-scale yield and contamination data for lithium niobate or tantalate integration. *(forecast)* [C5, S2]
- Reported laser performance figures for micro-transfer-printed or quantum-dot sources. *(forecast)* [C7, S6]

**Risks:**
- The result base is mostly single preprints, and the laser 'hardest component' claim leans heavily on one review. *(ai_interpretation)* [C5, C7, R1]
- The quantum-dot detector is far slower (1.1 MHz) than the multi-GHz components elsewhere, targeting sensing rather than communications, and has no foundry-context assessment of lead content. *(ai_interpretation)* [S7, C8]
- Lightwave Logic and Aeluma stocks have fallen sharply (35% and 59% over three months) with very high volatility. This is risk context only. *(ai_interpretation)* [T1, T11, T13]

**What would invalidate this thesis:**
- Contamination or yield problems prevent thin-film electro-optic or III-V integration from being run in standard foundry processes. *(forecast)* [C5, C7]
- The on-chip laser problem is solved without added materials or by another platform, removing the case for silicon-plus-additive stacks. *(forecast)* [R1, R6]

**Conflicting evidence:**
- Both integration preprints are first-of-kind lab demonstrations, and the lithium tantalate abstract itself says lithium contamination complicates CMOS integration, which weakens any claim that integration is close to solved. *(ai_interpretation)* [S2, C5]
- The claim that co-integration and packaging are the binding constraint is not supported by most of the cited abstracts, which name the light source, materials, waveguide loss and detectors. *(ai_interpretation)* [S12, C9]

**Companies named by cited evidence:**
- Lightwave Logic, Inc.: Polymer materials for silicon photonics modulators, with an MOA executed in January 2026. A micro-revenue company, which means higher risk and less disclosure. Scout heuristic only, not a recommendation. [M4, K1, T1]
- Aeluma, Inc.: Quantum dot laser and photodetector technologies positioned for silicon photonics. A micro-revenue company with R&D above revenue, which means higher risk and less disclosure. Scout heuristic only. [M6, K5, T11]
- Axt Inc: Scout finding lists it as a micro-revenue SEC filer mentioning silicon photonics in 5 reports. The finding cites no source, so treat it with caution. Higher risk, less disclosure. [K6]

### Test, measurement and equipment layer for silicon photonics

Technologies: photonic integrated circuit test, optical probing, burn-in test, ion-beam deposition for laser facet coating

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Filings show equipment and test companies tying products to silicon photonics: Teradyne bought Quantifi Photonics for $127.2 million for PIC test, Veeco cites silicon photonics and InP laser exposure, and Aehr cites silicon photonics as a demand driver [M1, M2, M5]. The retrieved evidence is concentrated here rather than in chip makers [M7]. Filings do not quantify revenue from silicon photonics. *(forecast)* [M1, M2, M5, M7] | medium |
| medium_1_3y | Test demand depends on device volumes rising, which the roadmap treats as an open question [R3]. The Teradyne and FormFactor collaboration for device validation suggests a developing ecosystem [M8], but no evidence shows how much silicon photonics volume it will serve. *(forecast)* [R3, M8] | low |
| long_3_5y | The findings do not address the long-term position of these equipment suppliers. Test needs for silicon photonics could change if packaging approaches or competing platforms shift [R6]. *(forecast)* [R6] | low |

**Bull case:** Rising photonic integrated circuit volumes require more wafer-level and package-level test, probing, burn-in and deposition steps, and these suppliers capture growing silicon-photonics-related demand. *(forecast)* [M1, M2, M5, M8]

**Base case:** Equipment makers see growing but modest silicon-photonics exposure alongside other end markets (e.g. generative AI and power semiconductors for Aehr), with results driven mainly by wider semiconductor cycles. *(forecast)* [M5, M7]

**Bear case:** Device volumes grow more slowly than hoped because of packaging and scaling bottlenecks, so test demand disappoints. The recent sharp share price falls suggest the market is already cautious. *(forecast)* [R3, S1, T13]

**Catalysts:**
- Filings that quantify silicon-photonics-related revenue or orders. *(forecast)* [M7, M2]
- Integration of Quantifi Photonics into Teradyne's product test offering for photonic integrated circuits. *(forecast)* [M1]

**Risks:**
- Silicon photonics is only one of several named demand drivers, so its contribution is hard to isolate. *(ai_interpretation)* [M5, M2]
- Stocks in this group have fallen 21-49% over three months with 90-164% annualised volatility. This is risk context only, not a timing signal. *(ai_interpretation)* [T3, T5, T7, T9, T13]
- The FormFactor Keystone Photonics statement is rated an unverified claim. *(unverified_claim)* [M3]

**What would invalidate this thesis:**
- Silicon photonics unit volumes fail to scale because integration, fabrication and packaging bottlenecks remain unsolved. *(forecast)* [S1, R3]

**Conflicting evidence:**
- Filings show silicon photonics activity among equipment makers, yet the retrieved evidence shows little from silicon photonics chip or transceiver makers, so the demand chain is not confirmed end to end. *(ai_interpretation)* [M7]
- Equipment stocks have fallen sharply despite the AI-infrastructure framing in filings and social posts. *(ai_interpretation)* [T13, M2, X4]

**Companies named by cited evidence:**
- Teradyne: Acquired Quantifi Photonics for $127.2 million for PIC test and includes silicon photonics testing in its Product Test segment; has a collaboration with FormFactor. [M1, M8]
- Formfactor Inc: Keystone Photonics optical probing for silicon photonics and co-packaged optics testing (unverified claim). Small by revenue (about $0.78B), scout score 45/100 (heuristic, not a recommendation). [M3, K2]
- Veeco Instruments Inc: Cites exposure to silicon photonics and InP lasers, with ion-beam deposition for laser-facet coating. Small by revenue, scout score 45/100 (heuristic). [M2, K4]
- Aehr Test Systems: Cites silicon photonics as one end-market demand driver. Micro by revenue, with fiscal 2025 revenue growth of -15.2%, so higher risk and less disclosure. Scout score 45/100 (heuristic). [M5, K3]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 1040, 2021: 981, 2022: 977, 2023: 1076, 2024: 1157, 2025: 1304, 2026: 1397}
Research Acceleration 2024->2025: 1157 -> 1304 (12.7% YoY). OpenAlex works whose title or abstract contains the exact phrase "silicon photonics", per publication year (singular and plural forms match; each work counted once). Synonyms and abbreviations are not counted. The number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-11): 2025 1017 -> 2026 1299 (27.7%, trend: rising). OpenAlex works with the exact phrase "silicon photonics" in title or abstract published 1 Jan–11 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence medium)* A 2024 perspective review charts generational trends in silicon photonics by analogy to CMOS generations, and identifies integration, fabrication, circuit and packaging bottlenecks as the critical challenges for scaling the technology to much larger unit volumes.
  - source: [Roadmapping the next generation of silicon photonics](https://doi.org/10.1038/s41467-024-44750-0) (OpenAlex, 2024-01-25, abstract_only)
  - excerpt: "We chart the generational trends in silicon photonics technology, drawing parallels from the generational definitions of CMOS technology."
  - reasoning: Single review abstract; the framing is authorial and directional rather than a measured result.
- **[S2]** *(verified_fact, confidence medium)* Heterogeneous integration of electro-optic thin films onto silicon photonics is being pursued to overcome the modulation limits of silicon: one preprint reports the first integration of lithium tantalate onto a silicon photonics chip without modifying the standard process design kit, and another reports back-end-of-line die-to-wafer bonding of thin-film lithium niobate onto an active silicon photonics platform with 100-GHz modulators and 56-GHz Ge photodetectors on one chip.
  - source: [A high-speed heterogeneous lithium tantalate silicon photonics platform](https://arxiv.org/abs/2503.10557v2) (arXiv, 2025-03-13, abstract_only)
  - source: [Heterogeneous back-end-of-line integration of thin-film lithium niobate on active silicon photonics for single-chip optical transceivers](https://arxiv.org/abs/2512.07196v1) (arXiv, 2025-12-08, abstract_only)
  - excerpt: "Here, we present for the first time the integration of lithium tantalate onto a silicon photonics chip. This integration is achieved without modifying the standard silicon photonics process design kit."
  - reasoning: Two independent preprints point the same way, but both are arXiv preprints and not peer reviewed, and the quoted excerpt covers only the lithium tantalate work.
- **[S3]** *(verified_fact, confidence medium)* Silicon's weak electro-optic effects are described as forcing large modulator footprints and power-hungry thermo-optic tuning, which motivates MEMS-based building blocks; a 2026 preprint demonstrates a zero-change foundry-compatible silicon photonic MEMS switch with more than 30 dB extinction ratio, under 1.5 dB insertion loss and roughly 20 nW static power at maximum actuation.
  - source: [Integrated silicon photonic MEMS](https://doi.org/10.1038/s41378-023-00498-z) (OpenAlex, 2023-03-19, abstract_only)
  - source: [Zero-change foundry compatible silicon photonics MEMS optical switch](https://arxiv.org/abs/2608.03146v1) (arXiv, 2026-08-04, abstract_only)
  - excerpt: "The optical switch element exhibits an insertion loss of less than 1.5 dB with a low static power consumption of approx 20 nW at maximum actuation voltage."
  - reasoning: One review-style article states the motivation and one preprint reports the device result; the device numbers come from a single non-peer-reviewed preprint.
- **[S4]** *(verified_fact, confidence medium)* AI and machine-learning workloads are named as the driver for next-generation optical interconnect, with a chip-based Kerr-comb silicon photonic link demonstrating 512 Gb/s aggregate over 32 wavelength channels on a single fibre and described as fundamentally scalable to hundreds of channels.
  - source: [Massively scalable Kerr comb-driven silicon photonic link](https://doi.org/10.1038/s41566-023-01244-7) (OpenAlex, 2023-06-29, abstract_only)
  - excerpt: "aggregate single-fibre data transmission of 512 Gb s−1 across 32 independent wavelength channels. The demonstrated architecture is fundamentally scalable to hundreds of wavelength channels"
  - reasoning: Single peer-reviewed journal article; the scalability claim is the authors' projection, not a demonstrated result at that scale.
- **[S5]** *(verified_fact, confidence medium)* Wavelength-division-multiplexed transceiver demand beyond 1.6 Tb/s, linked to growth in generative AI and data-centre traffic, is driving work on waveguide grating couplers that achieve sub-1 dB fibre-to-chip coupling loss and 1-dB bandwidths over 100 nm in foundry-manufactured chips.
  - source: [Silicon photonics for high-speed communications and photonic signal processing](https://doi.org/10.1038/s44310-024-00024-7) (OpenAlex, 2024-07-17, abstract_only)
  - excerpt: "foundry manufactured chips to have fiber-chip coupling losses of under 1 dB. The use of mirror symmetry and resonant cavity enhancement in the design of gratings can increase the 1-dB optical bandwidths of grating couplers to over 100 nm."
  - reasoning: Single review article abstract; coupling-loss and bandwidth figures are reported as the authors' results but cannot be independently checked from the abstract alone.
- **[S6]** *(verified_fact, confidence medium)* The on-chip laser source is repeatedly identified as the hardest remaining component because silicon has an indirect bandgap, and integration routes under exploration include III-V semiconductors, two-dimensional materials and colloidal quantum dots, as well as micro-transfer printing of GaSb gain chips for the 2-3 micrometre range.
  - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
  - source: [Micro-transfer printing of GaSb optoelectronics chips for mid-infrared silicon photonics integrated circuits](https://arxiv.org/abs/2409.13413v1) (arXiv, 2024-09-20, abstract_only)
  - excerpt: "The most challenging aspect remains to be the on-chip laser source, whose performance is constrained by the indirect bandgap of silicon."
  - reasoning: One review and one preprint agree on the problem statement; the GaSb transfer-printing demonstration is a non-peer-reviewed preprint and its excerpt was not quoted.
- **[S7]** *(verified_fact, confidence medium)* Extending silicon photonic photodetection beyond 1.6 micrometres is described as a persistent materials problem; one preprint integrates lead sulphide colloidal quantum dot photodiodes onto silicon waveguides, reporting 1.3 A/W responsivity and 74.8% external quantum efficiency at 2.1 micrometres, with a 1.1 MHz bandwidth at -3 V bias.
  - source: [A silicon photonics waveguide-coupled colloidal quantum dot photodiode sensitive beyond 1.6 um](https://arxiv.org/abs/2405.12376v2) (arXiv, 2024-05-20, abstract_only)
  - excerpt: "The integrated photodiodes exhibit a remarkable responsivity of 1.3 A/W (with an external quantum efficiency of 74.8%) at a wavelength of 2.1 um, a low dark current of only 106 nA and a bandwidth of 1.1 MHz under a -3 V bias."
  - reasoning: Single arXiv preprint; the reported bandwidth is low relative to communication-grade detectors, which the abstract itself implies by positioning the work for sensing applications.
- **[S8]** *(verified_fact, confidence medium)* Short-wavelength silicon photonics for the 380-1100 nm range is being adapted from telecommunication-optimised foundry platforms, with silicon nitride and aluminium oxide waveguide platforms becoming CMOS-foundry compatible, while low-loss waveguides, input/output coupling, sensitive detectors and heterogeneous laser/modulator integration are still named as the key challenges below 1100 nm.
  - source: [Silicon photonics for the visible and near-infrared spectrum](https://doi.org/10.1364/aop.501846) (OpenAlex, 2023-11-27, abstract_only)
  - excerpt: "The key challenges are low-loss waveguides, efficient input/output coupling, sensitive detectors, and heterogeneous integration of lasers and modulators, particularly those using lithium niobate and other electro-optic materials."
  - reasoning: Single review article; application drivers such as quantum information, biosensing and AR are stated as motivation rather than demonstrated market outcomes.
- **[S9]** *(verified_fact, confidence medium)* Inverse design and machine learning are being applied to silicon photonic device design to handle structures with hundreds or thousands of degrees of freedom, and open-source tooling is emerging: one package exposes waveguide parameters with automatic differentiation via JAX for gradient-based optimisation.
  - source: [The Intelligent Design of Silicon Photonic Devices](https://doi.org/10.1002/adom.202301337) (OpenAlex, 2024-02-07, abstract_only)
  - source: [Silicon Photonics Toolkit](https://doi.org/10.1364/opticaopen.23098334.v1) (OpenAlex, 2023-07-19, abstract_only)
  - excerpt: "Extremely complex silicon photonic devices with hundreds or even thousands of degrees of freedom (DOF) are successfully designed and manufactured based on recent advances in data science and nanofabrication technology."
  - reasoning: One review article plus one preprint describing a software package; the software item is not peer reviewed and its adoption cannot be judged from the abstract.
- **[S10]** *(verified_fact, confidence medium)* Silicon photonics is also being used as a platform for quantum information functions: one preprint reports the first on-chip deterministic entanglement purification, improving state fidelity from 0.71 to 0.82 under 20% bit-flip error, and another reports a pairwise-scan calibration method for cascaded phase shifters achieving 99.97% fidelity in a packaged chip.
  - source: [Entanglement Purification by Integrated Silicon Photonics](https://arxiv.org/abs/2507.03604v1) (arXiv, 2025-07-04, abstract_only)
  - source: [Calibration of cascaded phase shifters using pairwise scan method in silicon photonics integrated chip](https://arxiv.org/abs/2412.03951v1) (arXiv, 2024-12-05, abstract_only)
  - excerpt: "We demonstrate the first on-chip deterministic entanglement purification based on silicon photonics. ... The state fidelity improves from 0.71 to 0.82 under a 20% bit-flip error."
  - reasoning: Both are preprints (one explicitly arXiv quant-ph, the other an arXiv preprint later published in a journal); the fidelity numbers come from separate experiments and are not directly comparable.
- **[S11]** *(verified_fact, confidence low)* Scaling silicon photonic quantum circuits is presented as a calibration problem as well as a fabrication problem: the time required to calibrate cascaded phase shifters grows with chip scale, and thermal crosstalk between thermal-optical phase shifters is named as a design concern addressed by simulation and optimisation.
  - source: [Calibration of cascaded phase shifters using pairwise scan method in silicon photonics integrated chip](https://arxiv.org/abs/2412.03951v1) (arXiv, 2024-12-05, abstract_only)
  - excerpt: "Owing to an increase in the scale of silicon photonics chips, the time required to calibrate various CPSs has increased."
  - reasoning: Single preprint abstract; the calibration-time claim is stated qualitatively with no measurement of the reduction achieved.
- **[S12]** *(ai_interpretation, confidence medium)* Across these abstracts the recurring architectural bet is that no single material system suffices: silicon provides the mature foundry base while lithium niobate/tantalate, III-V, quantum dots, MEMS and silicon nitride layers are added for modulation, gain, detection and short-wavelength operation, with co-integration and packaging rather than the waveguide itself framed as the binding constraint.
  - source: [Roadmapping the next generation of silicon photonics](https://doi.org/10.1038/s41467-024-44750-0) (OpenAlex, 2024-01-25, abstract_only)
  - source: [Integrated silicon photonic MEMS](https://doi.org/10.1038/s41378-023-00498-z) (OpenAlex, 2023-03-19, abstract_only)
  - source: [A high-speed heterogeneous lithium tantalate silicon photonics platform](https://arxiv.org/abs/2503.10557v2) (arXiv, 2025-03-13, abstract_only)
  - source: [Heterogeneous back-end-of-line integration of thin-film lithium niobate on active silicon photonics for single-chip optical transceivers](https://arxiv.org/abs/2512.07196v1) (arXiv, 2025-12-08, abstract_only)
  - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
  - source: [Silicon photonics for the visible and near-infrared spectrum](https://doi.org/10.1364/aop.501846) (OpenAlex, 2023-11-27, abstract_only)
  - source: [Micro-transfer printing of GaSb optoelectronics chips for mid-infrared silicon photonics integrated circuits](https://arxiv.org/abs/2409.13413v1) (arXiv, 2024-09-20, abstract_only)
  - source: [A silicon photonics waveguide-coupled colloidal quantum dot photodiode sensitive beyond 1.6 um](https://arxiv.org/abs/2405.12376v2) (arXiv, 2024-05-20, abstract_only)
  - reasoning: This is my synthesis across review articles and preprints; each individual abstract supports only part of it, several key sources are non-peer-reviewed preprints, and no abstract gives a comparative benchmark across material platforms.

**Emerging directions:**
- Back-end-of-line heterogeneous integration of thin-film lithium niobate and lithium tantalate on active silicon photonics
- Silicon photonic MEMS for low-power switching and reconfigurability
- Kerr-comb-driven wavelength-division-multiplexed data-centre links
- Mid-infrared silicon photonics via micro-transfer-printed GaSb gain chips
- Colloidal quantum dot detectors and emitters integrated on silicon waveguides
- Short-wavelength (visible/NIR) foundry platforms based on silicon nitride and aluminium oxide
- Inverse design and deep-learning-assisted device engineering with differentiable tooling
- On-chip quantum photonic functions such as entanglement purification and scalable phase-shifter calibration

**Open problems:**
- Silicon's weak electro-optic effect forces large modulator footprints and high-power thermo-optic tuning, limiting very large-scale integration
- No native on-chip laser source because of silicon's indirect bandgap; gain must come from heterogeneous materials
- Lithium contamination from lithium niobate/tantalate complicates compatibility with CMOS fabrication
- Photodetection beyond about 1.6 micrometres lacks suitable epitaxial materials on silicon
- Low-loss waveguides, efficient input/output coupling and sensitive detectors remain unresolved below 1100 nm
- Calibration time of cascaded phase shifters grows with chip scale, and thermal crosstalk between phase shifters must be managed
- Heterogeneous integration and packaging, rather than individual device performance, are described as the blocking bottlenecks for next-generation systems

**Limitations:**
- All evidence comes from titles and abstracts only; no full texts, figures, methods or datasets were read.
- Five of the sixteen items are arXiv preprints and are not peer reviewed, including most of the concrete device-performance claims.
- Several performance numbers cited here come from a single abstract each and were not independently replicated within this set.
- The set mixes review articles, a book, a software preprint and primary research, so findings are heterogeneous in evidence strength.
- No abstract provides a cross-platform benchmark, so claims about which material system is superior cannot be settled from this evidence.
- Search coverage is limited to the 16 retrieved items; relevant work may be missing, and no bibliometric or citation analysis is included here.
- None of the abstracts constitute evidence of commercial deployment, manufacturing yield at volume, or market adoption, and none support investment conclusions.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['silicon photonics thermal limitations', 'silicon photonics yield variability', 'silicon photonics coupling loss', 'silicon photonics laser reliability', 'silicon photonics cost per channel', 'silicon photonics fabrication tolerance']

- **[R1]** *(verified_fact, confidence medium)* The on-chip light source is still described as the hardest unsolved element of silicon photonics. Silicon's indirect bandgap limits efficient light emission, so most platforms depend on non-silicon gain material or unproven defect-based approaches.
  - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
  - source: [Photoluminescent Color Centers in Foundry Silicon Photonics](https://hdl.handle.net/1974/34590) (OpenAlex, 2025-05-27, abstract_only)
  - excerpt: "The most challenging aspect remains to be the on-chip laser source, whose performance is constrained by the indirect bandgap of silicon."
  - reasoning: Two independent abstracts, a review and a thesis, state the same limitation. The thesis is not a peer-reviewed article. The abstracts do not quantify how much this limitation costs in yield or cost.
- **[R2]** *(verified_fact, confidence medium)* System-level deployment at scale is limited by the thermal sensitivity of resonant devices, analog noise and variability, and a mismatch between photonic hardware and digital/ML frameworks. Active stabilization and control are needed to compensate, which adds complexity and likely power overhead.
  - source: [Addressing Hardware Limitations in Silicon Photonics for Scalable Optical Interconnects and Neural Networks](https://doi.org/10.26262/heal.auth.ir.375565) (OpenAlex, 2026-01-01, abstract_only)
  - excerpt: "the deployment of photonic systems at scale remains constrained by a range of system-level challenges, including thermal sensitivity of resonant devices, susceptibility to analog noise and variability"
  - reasoning: This rests on one thesis abstract, which also proposes its own fix, so the framing may favour that approach. The abstract is truncated and gives no figures on stabilization power overhead. That overhead is an inference, not a reported result.
- **[R3]** *(verified_fact, confidence medium)* Scaling from millions to billions of units is posed as an open question, not an established trajectory. The roadmap perspective names integration, fabrication and packaging bottlenecks that must be solved first, and says sensing and computing products are only 'around the corner'.
  - source: [Roadmapping the next generation of silicon photonics](https://doi.org/10.1038/s41467-024-44750-0) (OpenAlex, 2024-01-25, abstract_only)
  - excerpt: "We identify the crucial challenges that must be solved to make giant strides in CMOS-foundry-compatible devices, circuits, integration, and packaging."
  - reasoning: This is a single perspective article that frames the bottlenecks as questions to answer. It is a roadmap and contains no experimental or cost data. The abstract does not rank the bottlenecks or give timing.
- **[R4]** *(ai_interpretation, confidence low)* Evidence for phase-change-material (PCM) reconfigurable photonics is thin and mostly design-stage. One paper reports simulation results with a limit of about 4 bits per cell and insertion-loss trade-offs. Another is a conference talk saying PCMs 'can potentially' transform devices. The abstracts report nothing on endurance, yield or large-scale fabrication.
  - source: [Programmable phase change materials and silicon photonics co-integration for photonic memory applications: a systematic study](https://doi.org/10.1117/1.jom.4.3.031208) (OpenAlex, 2024-08-14, abstract_only)
  - source: [Phase change material integrated silicon photonics](https://doi.org/10.1117/12.3023946) (OpenAlex, 2024-10-02, abstract_only)
  - reasoning: The memory-cell paper cites 'multi-physics simulation results' and states 'fundamental limitations' on bits per cell and optical insertion loss. The second item is a talk abstract with zero citations. Endurance, switching cycles and foundry compatibility are not in the abstracts, so this is a gap, not a demonstrated failure. Neither source shows PCM devices at scale.
- **[R5]** *(ai_interpretation, confidence low)* The Kerr-comb silicon photonic link was demonstrated at 512 Gb/s across 32 wavelength channels. The statement that it is 'fundamentally scalable to hundreds of channels' is an extrapolation, not a measured result.
  - source: [Massively scalable Kerr comb-driven silicon photonic link](https://doi.org/10.1038/s41566-023-01244-7) (OpenAlex, 2023-06-29, abstract_only)
  - reasoning: The abstract reports 32 channels as the experiment and projects hundreds. It does not address comb source power, the filtering/modulator thermal control needed at higher channel counts, or system integration. The link is a laboratory demonstration, and it depends on a comb source that is a separate technology from the silicon chip.
- **[R6]** *(verified_fact, confidence low)* Silicon photonics faces competition and possible displacement or partitioning by other platforms (indium phosphide, silicon nitride, silicon carbide). Silicon carbide papers present it as overcoming other platforms' limitations, although that source is an advocacy-leaning review.
  - source: [Silicon integrated photonics](https://doi.org/10.3367/ufne.2024.09.039762) (OpenAlex, 2024-09-01, abstract_only)
  - source: [Pioneering the future with silicon carbide integrated photonics](https://doi.org/10.1016/j.optlastec.2024.111910) (OpenAlex, 2024-10-04, abstract_only)
  - excerpt: "In many respects, silicon integrated photonics competes with alternative platforms based on indium phosphide, silicon nitride and dioxide, and other platforms."
  - reasoning: One review confirms the competition. The SiC abstract uses promotional language ('paradigm shift', 'poised to deliver') and gives no cost or performance comparison with silicon. Whether any platform actually displaces silicon in a given application is not shown by these abstracts.
- **[R7]** *(verified_fact, confidence low)* Polarization control and non-reciprocal functions such as isolation are still open integration challenges, and monolithic integration of these functions is described as difficult.
  - source: [Polarization management in silicon photonics](https://doi.org/10.1038/s44310-024-00033-6) (OpenAlex, 2024-09-02, abstract_only)
  - excerpt: "we discuss strategies for developing non-reciprocal photonic devices and the challenges associated with monolithic integration in photonics circuits."
  - reasoning: This is a single review abstract with few details. It names the challenge but gives no quantitative penalty or timeline.
- **[R8]** *(ai_interpretation, confidence low)* Alternative light-source routes are early-stage or bring non-CMOS materials. The W-center approach is shown only as formation of defect centers in a foundry process, with no performance result in the visible abstract text. The hybrid III-V/Si laser route brings in a second material system, which weakens the 'pure CMOS, low-cost' framing.
  - source: [Photoluminescent Color Centers in Foundry Silicon Photonics](https://hdl.handle.net/1974/34590) (OpenAlex, 2025-05-27, abstract_only)
  - source: [Active silicon photonics for cutting edge applications](https://doi.org/10.32657/10356/204422) (OpenAlex, 2025-01-01, abstract_only)
  - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
  - reasoning: Both items are theses and not peer reviewed, and the abstracts are truncated. Absence of efficiency numbers in the abstract text is a gap, not proof of poor performance. The cost implication of hybrid integration is my inference, because no cost data appear in the abstracts.

**Possible hype:**
- 'From millions to billions of units': an aspirational framing in a roadmap perspective with no demand or cost evidence in the abstract.
- 'Allows for high-volume production at a low cost' (overview chapter): a generic CMOS claim with no cost data, and it sits uneasily with the unsolved on-chip laser and packaging issues.
- 'Fundamentally scalable to hundreds of wavelength channels': demonstrated only at 32 channels.
- 'Zero static power' and 'order of magnitude reduction in size' for PCM devices: based on simulation and a talk, with no reliability or endurance data in the abstracts.
- 'Paradigm shift' and 'poised to deliver' for silicon carbide photonics: promotional language without comparative data.
- Sensing and computing products 'around the corner': unsupported timing claim in a perspective article.

**Challenges to the Science findings:**
- Targets ['S5'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S5 merges two separate results into one achievement. The abstract credits sub-1 dB fibre-chip coupling to shifted-polysilicon overlay gratings on foundry-manufactured chips. The 1-dB bandwidth beyond 100 nm is attributed to a different design approach (mirror symmetry and resonant cavity enhancement) and is phrased as something the design 'can' achieve. S5 says couplers 'achieve sub-1 dB ... and 1-dB bandwidths over 100 nm in foundry-manufactured chips'. That implies one device delivers both in a foundry chip, which the abstract does not state.
    - source: [Silicon photonics for high-speed communications and photonic signal processing](https://doi.org/10.1038/s44310-024-00024-7) (OpenAlex, 2024-07-17, abstract_only)
    - excerpt: "The use of mirror symmetry and resonant cavity enhancement in the design of gratings can increase the 1-dB optical bandwidths of grating couplers to over 100 nm."
    - reasoning: The abstract separates the foundry-measured sub-1 dB result from the bandwidth claim, which is worded as a design capability. It does not show that both are met together in a manufactured device. The 1.6 Tb/s demand framing is the authors' motivation, not a measured system result.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S10'], severity medium:
  - **[C2]** *(ai_interpretation, confidence high)* S10 reports fidelity rising from 0.71 to 0.82 'under 20% bit-flip error' without saying the errors are emulated. The abstract states the bit-flip and phase-flip errors are simulated by reconfigurable on-chip circuits, so this is not purification of naturally occurring channel noise. The result is a single preprint. 'First' is the authors' own priority claim, and the abstract gives no scalability or success-probability information.
    - source: [Entanglement Purification by Integrated Silicon Photonics](https://arxiv.org/abs/2507.03604v1) (arXiv, 2025-07-04, abstract_only)
    - excerpt: "To evaluate the purification performance, we simulate the bit-flip and phase-flip errors by reconfigurable circuits on chip."
    - reasoning: The omission makes the demonstration look closer to a practical quantum-communication function than the abstract supports. It is a proof-of-principle with engineered noise.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S10', 'S11'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S11 and S10 treat the 99.97% calibration fidelity as evidence for scaling quantum circuits, but it was verified on only a 6-element cascaded phase-shifter structure. The thermal crosstalk 'addressed by simulation and optimisation' is a design-stage fix, not a measured result at larger scale. The abstract shows no data on calibration time or fidelity as chip size grows. It is also one preprint.
    - source: [Calibration of cascaded phase shifters using pairwise scan method in silicon photonics integrated chip](https://arxiv.org/abs/2412.03951v1) (arXiv, 2024-12-05, abstract_only)
    - reasoning: The abstract says calibration time 'has increased' with chip scale and validates the method on a '6-CPSs structure'. Whether the method removes the scaling problem is an extrapolation that the cited text does not test.
- Targets ['S4'], severity medium:
  - **[C4]** *(ai_interpretation, confidence high)* S4 presents the Kerr-comb link as 'fundamentally scalable to hundreds of channels' under a verified_fact label. The measured result is 512 Gb/s over 32 channels, about 16 Gb/s per channel. Scalability beyond 32 channels is the authors' architectural claim, not a demonstration. Practical limits such as comb power, per-channel modulator and filter control, and thermal stabilisation are not quantified in the abstract.
    - source: [Massively scalable Kerr comb-driven silicon photonic link](https://doi.org/10.1038/s41566-023-01244-7) (OpenAlex, 2023-06-29, abstract_only)
    - excerpt: "experimentally show aggregate single-fibre data transmission of 512 Gb s−1 across 32 independent wavelength channels. The demonstrated architecture is fundamentally scalable to hundreds of wavelength channels"
    - reasoning: The abstract separates the experimental result (32 channels) from the scalability statement. The finding repeats the claim as fact without flagging it as a projection. It is also a 2023 demonstration set against 1.6 Tb/s+ transceiver demand.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S2'], severity medium:
  - **[C5]** *(ai_interpretation, confidence medium)* S2 relies on two preprints, each making a 'first' claim, and implies that CMOS-compatible integration is close to solved. The lithium tantalate abstract itself says lithium contamination 'complicates integration with CMOS fabrication processes'. Showing the integration works on a chip without modifying the PDK does not show foundry-scale yield or contamination control. The TFLN abstract is also a lab demonstration of die-to-wafer bonding. Neither is peer reviewed, and neither is shown to be manufacturable in volume.
    - source: [A high-speed heterogeneous lithium tantalate silicon photonics platform](https://arxiv.org/abs/2503.10557v2) (arXiv, 2025-03-13, abstract_only)
    - source: [Heterogeneous back-end-of-line integration of thin-film lithium niobate on active silicon photonics for single-chip optical transceivers](https://arxiv.org/abs/2512.07196v1) (arXiv, 2025-12-08, abstract_only)
    - excerpt: "However, a persistent drawback of such platforms is the lithium contamination, which complicates integration with CMOS fabrication processes."
    - reasoning: The finding's wording ('being pursued to overcome the modulation limits') is reasonable. The weakness is that it does not caveat the single-preprint, self-declared-first, lab-scale nature of the evidence.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S3'], severity low:
  - **[C6]** *(ai_interpretation, confidence medium)* S3 reports the MEMS switch's extinction ratio, insertion loss and ~20 nW static power as if they establish suitability for large-scale switching, but the result is a single-element preprint. The abstract gives only static power at maximum actuation. It reports no switching speed, dynamic or drive-electronics power, long-term reliability, or results for a large switch matrix. The motivating claim that large-scale photonic switches are needed for AI/ML clusters is the authors' framing. Wafer-level sealing and reliability appear only in the separate MEMS-platform paper, not for the zero-change device.
    - source: [Zero-change foundry compatible silicon photonics MEMS optical switch](https://arxiv.org/abs/2608.03146v1) (arXiv, 2026-08-04, abstract_only)
    - source: [Integrated silicon photonic MEMS](https://doi.org/10.1038/s41378-023-00498-z) (OpenAlex, 2023-03-19, abstract_only)
    - reasoning: The abstract states 'The optical switch element exhibits an insertion loss of less than 1.5 dB with a low static power consumption of approx 20 nW'. It stops at element level. Scaling to large optical circuit switches is the authors' stated aim, not an evidenced result.
- Targets ['S6'], severity low:
  - **[C7]** *(ai_interpretation, confidence medium)* S6 says the laser is 'repeatedly identified' as the hardest component. That repetition comes mainly from one review (plus a thesis in the wider evidence), not from independent convergence. The GaSb micro-transfer-printing preprint is cited as an integration route, yet its abstract reports no laser performance figures. It says fabrication factors are limiting the gain coupons' performance. It is a process demonstration for the 2-3 µm range, not a mature route.
    - source: [Micro-transfer printing of GaSb optoelectronics chips for mid-infrared silicon photonics integrated circuits](https://arxiv.org/abs/2409.13413v1) (arXiv, 2024-09-20, abstract_only)
    - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
    - excerpt: "The characterization provides insight into the fabrication factors limiting the performance of the gain coupons."
    - reasoning: The finding lists routes (2D materials, quantum dots, micro-transfer printing) without distinguishing a review's taxonomy from demonstrated device performance. The abstracts give no power, efficiency or yield data.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S7'], severity low:
  - **[C8]** *(ai_interpretation, confidence medium)* S7 omits that the 1.1 MHz bandwidth of the PbS quantum-dot photodiode is orders of magnitude below the multi-GHz components in S2 and S4. The result therefore addresses sensing and spectroscopy around 2 µm, not high-speed communication. The abstract does not address lead-containing material in a CMOS or foundry context. The result is a single preprint.
    - source: [A silicon photonics waveguide-coupled colloidal quantum dot photodiode sensitive beyond 1.6 um](https://arxiv.org/abs/2405.12376v2) (arXiv, 2024-05-20, abstract_only)
    - reasoning: The abstract itself positions the work as 'tailored for a wide range of sensing applications around the 2 um wavelength range' with a 1.1 MHz bandwidth. A reader could wrongly take it as evidence that silicon photonic detection is extending to the data-communication context of the other findings. Toxicity and regulatory concerns are my inference, not stated in the abstract.
- Targets ['S12'], severity medium:
  - **[C9]** *(ai_interpretation, confidence medium)* S12 claims the abstracts frame 'co-integration and packaging rather than the waveguide itself' as the binding constraint. Most cited abstracts name other constraints. The laser review and the quantum-dot paper name the light source and materials limits, and the visible-spectrum review names waveguide loss, detectors and coupling. Only the roadmap abstract explicitly names packaging. The synthesis also omits system-level constraints on scaling, such as thermal sensitivity and control overhead of resonant devices, and competition from other platforms (R2, R6). It rests on a selected set of papers about additive material layers, so it is a retrieval-driven pattern, not an independent test.
    - source: [Roadmapping the next generation of silicon photonics](https://doi.org/10.1038/s41467-024-44750-0) (OpenAlex, 2024-01-25, abstract_only)
    - source: [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) (OpenAlex, 2024-02-27, abstract_only)
    - source: [Silicon photonics for the visible and near-infrared spectrum](https://doi.org/10.1364/aop.501846) (OpenAlex, 2023-11-27, abstract_only)
    - source: [Addressing Hardware Limitations in Silicon Photonics for Scalable Optical Interconnects and Neural Networks](https://doi.org/10.26262/heal.auth.ir.375565) (OpenAlex, 2026-01-01, abstract_only)
    - reasoning: The 'no single material suffices' pattern is a fair reading. The 'packaging as binding constraint' conclusion is not supported across the abstracts. Low-loss waveguides are themselves named as a key challenge in S8 (visible/NIR), which contradicts 'rather than the waveguide itself'.
- Targets general, severity medium:
  - **[C10]** *(ai_interpretation, confidence medium)* The findings contain no system-level reliability or control risks. Thermal sensitivity of resonant devices, analog noise and variability, and the need for active stabilisation (which adds complexity and likely power overhead) are not mentioned. They limit scaled deployment even where the device-level results in S2–S7 hold. The findings are device-heavy and list mostly positive demonstrations.
    - source: [Addressing Hardware Limitations in Silicon Photonics for Scalable Optical Interconnects and Neural Networks](https://doi.org/10.26262/heal.auth.ir.375565) (OpenAlex, 2026-01-01, abstract_only)
    - excerpt: "thermal sensitivity of resonant devices, susceptibility to analog noise and variability"
    - reasoning: The source is a 2026 thesis abstract, a single and lower-tier source. It nevertheless names risks directly relevant to the interconnect and tunable-device claims in S3–S5. The omission means the overall picture is more optimistic than the evidence set supports.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source

**Limitations:**
- Only 12 papers and abstracts (some truncated) were available. Nothing was checked against full texts.
- Several sources are theses, a talk abstract or a book chapter with 0-1 citations. Their quality and peer-review status are uncertain.
- No arXiv preprints were in the set, and no sources cover co-packaged optics economics, yield or packaging cost, supply-chain concentration, or competing electrical/copper interconnect progress. Those are coverage gaps, not evidence that the risks are absent.
- No quantitative cost, yield, reliability or power-overhead figures appear in these abstracts, so the size of each risk cannot be judged.
- The search was risk-oriented but returned mostly general or optimistic reviews, so the list of risks is probably incomplete.
- Only titles, metadata and abstracts were reviewed, and several abstracts are truncated, so results or caveats later in the text may be missed.
- Many cited sources are arXiv preprints, theses or single-lab demonstrations, and I could not check peer review status, replication or follow-up work.
- I did not challenge S1, S8 or S9. They match their abstracts closely and are modestly worded.
- The evidence set is small (25 papers) and weighted towards recent work, so contradicting literature may exist that was not retrieved.
- The MEMS preprint (src_e2d4f96a6f) carries a publication date of 2026-08-04, which I could not verify against the actual release date, so no challenge was built on it.
- Severity ratings are judgements about how much each problem weakens the finding, not measured quantities.

## Evidence: company filings and news
Status: ok. Companies are chosen from the evidence: SEC-listed patent assignees and employers of paper authors found by the Patent and Science agents (1 company name(s) in the patents and papers; 0 matched to the SEC ticker file; the top 0 by patents + papers are read), plus filers whose reports mention the topic. Company evidence is limited to short verbatim passages from their latest SEC annual/quarterly reports that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase only; no patent or paper of theirs was found, they are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: silicon photonics, SiPh, photonic integrated circuit, co-packaged optics, optical interconnect, optical transceiver

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Lightwave Logic, Inc. (LWLG) | 1 | 1 | micro: 0.0B USD | +147.7% | 4850.9% of revenue | discovered by full-text search |
| Teradyne, Inc (TER) | 1 | 1 | mid: 2.1B USD | -1.7% | n/a | discovered by full-text search |
| Axt Inc (AXTI) | 1 | 0 | micro: 0.1B USD | -11.1% | 10.2% of revenue | discovered by full-text search |
| Formfactor Inc (FORM) | 1 | 1 | small: 0.8B USD | +2.8% | 14.7% of revenue | discovered by full-text search |
| Photronics Inc (PLAB) | 1 | 0 | small: 0.8B USD | -2.0% | 1.9% of revenue | discovered by full-text search |
| Aehr Test Systems (AEHR) | 1 | 1 | micro: 0.1B USD | -15.2% | 25.3% of revenue | discovered by full-text search |
| Veeco Instruments Inc (VECO) | 1 | 1 | small: 0.5B USD | +45.8% | n/a | discovered by full-text search |
| Aeluma, Inc. (ALMU) | 1 | 1 | micro: 0.0B USD | -4.4% | 104.6% of revenue | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Teradyne acquired Quantifi Photonics for $127.2 million to deliver scalable photonic integrated circuit (PIC) test solutions, and its Product Test segment includes silicon photonics testing.
  - source: [Teradyne, Inc Form 10-Q, filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/97210/000119312526441091/ter-20260927.htm) (SEC EDGAR, 2026-10-30, excerpt_only)
  - excerpt: "acquired all of the issued and outstanding shares of Quantifi Photonics (“Quantifi”), a privately held company in New Zealand and a leader in photonic integrated circuit (“PIC”) test solutions for a total purchase price of $127.2 million."
  - reasoning: Directly stated in Teradyne's 10-Q excerpt; the acquisition price and purpose are explicit.
- **[M2]** *(verified_fact, confidence medium)* Veeco states it benefits from AI-infrastructure demand through exposure to silicon photonics and InP lasers, and that its Spector ion-beam deposition systems address the laser-facet coating process in silicon photonics.
  - source: [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - excerpt: "We are a market leader with our ion beam deposition technology, and within the Silicon Photonics space our Spector systems address the critical laser-facet coating process."
  - reasoning: Filing excerpt directly states Veeco's equipment role in silicon photonics manufacturing; the market-leadership claim is the company's own characterization.
- **[M3]** *(unverified_claim, confidence low)* FormFactor's Keystone Photonics provides optical probing technology for testing silicon photonics, co-packaged optics (CPO), and near-packaged optics (NPO) devices.
  - source: [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - excerpt: "Keystone Photonics provides optical probing technology used in the testing of silicon photonics (“SiPh”), co‑packaged optics (“CPO”), and near‑packaged optics (“NPO”) devices."
  - reasoning: Directly stated in FormFactor's 10-Q excerpt.
  - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- **[M4]** *(verified_fact, confidence medium)* Lightwave Logic's polymer materials are engineered for integration into silicon photonics and PIC platforms, and in January 2026 it executed an MOA related to modulators on silicon photonics; its strategy is to enable customers making optical transceivers rather than manufacturing them itself.
  - source: [Lightwave Logic, Inc. Form 10-Q, filed 2026-08-14](https://www.sec.gov/Archives/edgar/data/1325964/000107997326001097/lwlg_10q-063026.htm) (SEC EDGAR, 2026-08-14, excerpt_only)
  - excerpt: "is engineered for integration into silicon photonics (“SiPh”) and other photonic integrated circuit (“PIC”) platforms."
  - reasoning: Multiple excerpts from Lightwave Logic's 10-Q describe a materials-supplier strategy (licensing polymer materials, enabling customers' transceiver manufacturing) and a January 2026 MOA on SiPh modulators.
- **[M5]** *(verified_fact, confidence medium)* Aehr Test Systems cites silicon photonics (alongside generative AI and power semiconductors) as an end-market demand driver for its test/burn-in products.
  - source: [Aehr Test Systems Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1040470/000165495426009601/aehr_10q.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - excerpt: "demand related to generative AI, silicon photonics and power semiconductors such as silicon carbide and gallium nitride."
  - reasoning: Directly stated in Aehr's 10-Q; silicon photonics is listed as a demand driver, though no SiPh-specific revenue or customers are disclosed.
- **[M6]** *(verified_fact, confidence low)* Aeluma positions its quantum dot laser, nonlinear materials and photodetector technologies for silicon photonics and quantum photonics markets, and cites growing demand for optical transceivers and silicon photonics.
  - source: [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) (SEC EDGAR, 2026-09-16, excerpt_only)
  - excerpt: "This increases demand for optical transceivers, silicon photonics, lasers, and"
  - reasoning: Excerpts show Aeluma views silicon photonics as a demand driver and competitive arena, but the excerpts are fragmentary and the company is micro-sized with no named SiPh customers or products shipping.
- **[M7]** *(ai_interpretation, confidence medium)* The retrieved evidence shows silicon photonics commercial activity concentrated in the test-and-measurement and equipment layer (Teradyne, FormFactor, Veeco, Aehr) rather than in SiPh chip or transceiver makers themselves.
  - source: [Teradyne, Inc Form 10-Q, filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/97210/000119312526441091/ter-20260927.htm) (SEC EDGAR, 2026-10-30, excerpt_only)
  - source: [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - source: [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - source: [Aehr Test Systems Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1040470/000165495426009601/aehr_10q.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - source: [Lightwave Logic, Inc. Form 10-Q, filed 2026-08-14](https://www.sec.gov/Archives/edgar/data/1325964/000107997326001097/lwlg_10q-063026.htm) (SEC EDGAR, 2026-08-14, excerpt_only)
  - reasoning: Across five filings, the named companies supply test systems, probing, deposition equipment, or materials for silicon photonics; none of the excerpts describe a company shipping SiPh transceivers or CPO modules itself. This is a pattern in the retrieved sample, not a statement about the whole market.
- **[M8]** *(verified_fact, confidence medium)* Teradyne and FormFactor have a commercial collaboration combining Teradyne test platforms with FormFactor probe, contactor and interface technologies, including for silicon photonics device validation.
  - source: [Teradyne, Inc Form 10-Q, filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/97210/000119312526441091/ter-20260927.htm) (SEC EDGAR, 2026-10-30, excerpt_only)
  - excerpt: "Teradyne’s test platforms with FormFactor’s probe, contactor, and interface technologies to help semiconductor customers accelerate device validation and bring advanced devices to production, including in silicon photonics"
  - reasoning: Stated in Teradyne's 10-Q excerpt; corroborated by FormFactor's own filing describing Keystone Photonics SiPh/CPO probing technology.

**Limitations:**
- Only 6 sources were retrieved, all SEC filing excerpts; no news headlines, patents, or papers were provided, so media coverage and IP activity on silicon photonics are not covered.
- AXT and Photronics were flagged as mentioning the topic in filings, but the retrieved excerpts for them contain no keyword mentions, so their role in silicon photonics cannot be assessed from this evidence.
- All sources are excerpt_only passages from single filings per company; absence of a keyword in an excerpt does not mean the company is absent from the silicon photonics market.
- Major silicon photonics players (e.g., large transceiver, foundry, and hyperscaler co-packaged-optics developers) are not represented in the retrieved evidence, so the picture is skewed toward test/equipment suppliers.
- No customer names, revenue figures, capacity, or shipment data specific to silicon photonics appear in the excerpts, limiting assessment of commercial readiness and adoption.
- Lightwave Logic's and Aeluma's excerpts are fragmentary (some sentences cut off), so their exact commercial arrangements cannot be fully characterized.

## Social signals from X
Status: ok. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 50 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (130): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie, @SemiconductorsX, @KirkDBorne, @kyleichan, @thePandaily, @HPCwire, @WarGuy_, @PIBKohima, @robvank, @LifeboatHQ, @zhaoweiasu, @BlackEngineer, @ShapesXR, @engadget, @Gadgets360, @eeNewsEurope, @machinelearnflx, @dez_blanchfield, @0xRicker, @Lance_Edelman, @Techmeme, @chr1sa, @Romka2x, @OWW, @CyberRobooo, @Decoded08, @techniahqrobot, @liuziwei7, @johnkoetsier, @preskill, @gp_pulipaka, @QuantumStateX, @Scholarshipps, @QuantumDaily, @scitechgirl, @Amandasatiro07, @thatoptometrist, @QuantumPapers, @the_hindu, @IndiaToday, @EconomicTimes, @ETNOWlive, @GreaterKashmir, @DDIndialive, @c_aashish, @TheQuietSensei, @CBCRajouri, @india_plus_, @alphaaffairsf2f, @dayalugurubjp, @Prabinmen, @PsuWatch, @aseemmanchanda, @bhagwantkhuba, @SUDHIRb9661, @governancenow, @PIB_India, @marinaj4q, @Finsee_main, @skathire, @singularityhub, @ahier, @MolecularCell, @RevvityLifeSci, @idtdna, @NaturePlants, @SimbokeSarah, @ChEnected, @RZubiranS, @BioinfoAdv, @srqstockpicker, @ShorterLab, @nabil125125125, @ThalesDigiSec, @ThejesterVerse, @WOCTechnology, @QuantSecXYZ, @Ronald_vanLoon, @PrameyaEnglish, @craigapplecom, @BLU_Products, @PragativadiNews, @HimanshiTech, @NyongesaSande, @gadgetbytenepal, @bobbymorris280, @TechieUltimatum, @PaidFreeDroid, @nitin_gadkari, @MIB_India, @kishanreddybjp, @IndiaInGuate, @PIBDehradun, @CISACyber
Posts read: 7 (estimated X cost $0.035)

- **[X1]** *(unverified_claim, confidence low)* EE Times reports that Celestica and Broadcom say co-packaged optics cut power and latency to scale AI data center networks beyond copper limits.
  - source: [@eetimes: In this partner interview, #Celestica and #Broadcom explain how co-packaged #optics cut po…](https://x.com/eetimes/status/2119797353896964464) (X API, 2026-11-09, full_text)
  - excerpt: "Celestica and Broadcom explain how co-packaged optics cut power and latency to scale AI data center networks beyond copper limits."
  - reasoning: Press post summarising a partner interview; underlying article not read, and the claims originate from the companies themselves.
- **[X2]** *(unverified_claim, confidence low)* Counterpoint Research says Marvell is buying Lumentum in a deal with an implied value of $115 billion, framed as climbing the 'AI laser wall' in the optics value chain.
  - source: [@CounterPointTR: 𝗠𝗮𝗿𝘃𝗲𝗹𝗹 𝗕𝘂𝘆𝘀 𝗟𝘂𝗺𝗲𝗻𝘁𝘂𝗺 𝘁𝗼 𝗖𝗹𝗶𝗺𝗯 𝘁𝗵𝗲 𝗔𝗜 𝗟𝗮𝘀𝗲𝗿 𝗪𝗮𝗹𝗹: 𝗪𝗵𝗮𝘁 𝘁𝗵𝗲 $𝟭𝟭𝟱 𝗕𝗶𝗹𝗹𝗶𝗼𝗻 𝗗𝗲𝗮𝗹 𝗠𝗲𝗮𝗻𝘀 𝗳𝗼𝗿 𝗢𝗽𝘁…](https://x.com/CounterPointTR/status/2117499775654482067) (X API, 2026-11-03, full_text)
  - excerpt: "Marvell is buying Lumentum for an implied... $115 Billion Deal Means for Optics Value Chain"
  - reasoning: Analyst-firm post asserting a large acquisition; the post text is truncated and the full analysis was not read, so details cannot be verified.
  - citation check: company name(s) not found in the cited posts removed: Marvell, Lumentum
- **[X3]** *(ai_interpretation, confidence low)* EE Times published an explainer, 'Five Things You Didn't Know About Co-Packaged Optics', indicating continued press attention to co-packaged optics as a topic.
  - source: [@eetimes: Five Things You Didn’t Know About Co-Packaged Optics https://t.co/9b7vcYeVlp https://t.co/…](https://x.com/eetimes/status/2117617868787384756) (X API, 2026-11-03, full_text)
  - source: [@eetimes: In this partner interview, #Celestica and #Broadcom explain how co-packaged #optics cut po…](https://x.com/eetimes/status/2119797353896964464) (X API, 2026-11-09, full_text)
  - excerpt: "Five Things You Didn't Know About Co-Packaged Optics"
  - reasoning: Two EE Times posts in one week covering co-packaged optics (an explainer and a vendor interview) suggest the topic is an active editorial focus, though volume is small.
- **[X4]** *(unverified_claim, confidence low)* Owner-added account Finsee reports earnings signals from optical-component suppliers tied to AI datacenter demand: Applied Optoelectronics sales more than doubled but power/factory delays cut its outlook; Coherent raised its sales plan on AI optical growth while factory spending consumes cash; Viavi's data-center testing sales rose 57% year over year to $469 million.
  - source: [@Finsee_main: $AAOI Q3 2026 earnings: Applied Optoelectronics sales more than double, but power delays c…](https://x.com/Finsee_main/status/2118454807388106826) (X API, 2026-11-05, full_text)
  - source: [@Finsee_main: $COHR Q1 2027 earnings: Coherent raises its sales plan, but factory spending burns cash Co…](https://x.com/Finsee_main/status/2118093426994372647) (X API, 2026-11-04, full_text)
  - source: [@Finsee_main: $VIAV Q1 2027 earnings: Viavi's sales outlook tops $500 million, but share dilution grows …](https://x.com/Finsee_main/status/2118095750089310308) (X API, 2026-11-04, full_text)
  - excerpt: "Coherent's artificial intelligence optical business is growing even faster as new laser capacity comes online"
  - reasoning: Three posts from a single owner-added account summarising earnings; figures are as reported in truncated post text and not independently verified.

**Limitations:**
- Only 7 posts in the 7-day window matched the topic, from a small fixed account list; several are tangential (e.g., Himax display chips).
- Posts are promotional or truncated summaries; linked articles were not read, so claims cannot be verified.
- No posts from major silicon photonics players in the list (Intel, Nvidia, AMD, imec, etc.) appeared in this window.
- Engagement counts are low overall, indicating limited attention rather than confirmation.
- Earnings figures come from one owner-added account and may be paraphrased or incomplete.

## Evidence: patents
Status: partial. Worldwide patent publications from EPO OPS matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: ok. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.

| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |
|---|---|---|---|---|---|---|---|
| Lightwave Logic, Inc. (LWLG) | 4.91 (2026-11-09) | -1.2% | -35.1% | +1.1% | 110.3% | -53.6% | **moderate**: no stretch or pull-back rule triggered; high volatility (110.3% annualised, 20-day) |
| Teradyne, Inc (TER) | 246.0 (2026-11-09) | -38.9% | -35.2% | -29.6% | 100.3% | -49.6% | **subdued**: 29.6% below its 50-day average and -35.2% over 3 months; high volatility (100.3% annualised, 20-day) |
| Formfactor Inc (FORM) | 85.2 (2026-11-09) | -39.0% | -29.6% | -24.9% | 137.9% | -46.8% | **subdued**: 24.9% below its 50-day average and -29.6% over 3 months; high volatility (137.9% annualised, 20-day) |
| Aehr Test Systems (AEHR) | 59.81 (2026-11-09) | -29.3% | -49.0% | -24.6% | 164.2% | -59.4% | **subdued**: 24.6% below its 50-day average and -49.0% over 3 months; high volatility (164.2% annualised, 20-day) |
| Veeco Instruments Inc (VECO) | 39.6 (2026-11-09) | -24.3% | -21.0% | -11.9% | 90.0% | -51.6% | **subdued**: 11.9% below its 50-day average and -21.0% over 3 months; high volatility (90.0% annualised, 20-day) |
| Aeluma, Inc. (ALMU) | 7.47 (2026-11-09) | -34.5% | -58.9% | -30.6% | 126.3% | -71.6% | **subdued**: 30.6% below its 50-day average and -58.9% over 3 months; high volatility (126.3% annualised, 20-day) |

- **[T1]** *(verified_fact, confidence medium)* Lightwave Logic closed at 4.91 on 2026-11-09, down 35.1% over 3 months, roughly at its 50-day average (+1.1%), with 20-day annualised volatility of 110.3% and a rule-based timing risk of moderate.
  - source: [Lightwave Logic, Inc. (LWLG) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LWLG&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "3-month return -35.1%. Price vs 50-day average 1.1%. 20-day annualised volatility 110.3%"
- **[T2]** *(ai_interpretation, confidence medium)* For Lightwave Logic, the price is neither stretched above nor far below its recent average, so the main timing risk flagged by the data is volatility itself (110.3% annualised) rather than an extended run-up; a -35.1% three-month decline shows the theme's price action has been sharply negative.
  - source: [Lightwave Logic, Inc. (LWLG) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LWLG&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T3]** *(verified_fact, confidence medium)* Teradyne closed at 246.0 on 2026-11-09, down 38.9% over 1 month and 35.2% over 3 months, 29.6% below its 50-day average, with 20-day annualised volatility of 100.3% and a rule-based timing risk of subdued.
  - source: [Teradyne, Inc (TER) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TER&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "1-month return -38.9%. 3-month return -35.2%. Price vs 50-day average -29.6%"
- **[T4]** *(ai_interpretation, confidence medium)* Teradyne has pulled back sharply rather than run up: it sits far below its 50-day average after steep recent declines. A subdued reading means less recent run-up, not that the price will recover; volatility near 100% annualised remains a substantial timing risk.
  - source: [Teradyne, Inc (TER) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TER&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T5]** *(verified_fact, confidence medium)* Formfactor closed at 85.2 on 2026-11-09, down 39.0% over 1 month and 29.6% over 3 months, 24.9% below its 50-day average, with the highest volatility in this group at 137.9% annualised (20-day) and a rule-based timing risk of subdued.
  - source: [Formfactor Inc (FORM) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FORM&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "1-month return -39.0%. 3-month return -29.6%. Price vs 50-day average -24.9%. 20-day annualised volatility 137.9%"
- **[T6]** *(ai_interpretation, confidence medium)* Formfactor shows a deep pull-back combined with very high volatility: prices have fallen far below the recent average, but swings of this magnitude mean any positioning around this theme carries elevated uncertainty in both directions.
  - source: [Formfactor Inc (FORM) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FORM&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T7]** *(verified_fact, confidence medium)* Aehr Test Systems closed at 59.81 on 2026-11-09, down 29.3% over 1 month and 49.0% over 3 months, 24.6% below its 50-day average, 59.4% below its 100-day high, with 20-day annualised volatility of 164.2% and a rule-based timing risk of subdued.
  - source: [Aehr Test Systems (AEHR) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AEHR&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "3-month return -49.0%. Price vs 50-day average -24.6%. 20-day annualised volatility 164.2%"
- **[T8]** *(ai_interpretation, confidence medium)* Aehr Test Systems has the most severe drawdown and highest volatility in the group: a -49.0% three-month decline and 164.2% annualised volatility indicate extreme price instability, which is itself the dominant timing risk even though no stretch rule was triggered.
  - source: [Aehr Test Systems (AEHR) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AEHR&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T9]** *(verified_fact, confidence medium)* Veeco Instruments closed at 39.6 on 2026-11-09, down 24.3% over 1 month and 21.0% over 3 months, 11.9% below its 50-day average, with 20-day annualised volatility of 90.0% and a rule-based timing risk of subdued.
  - source: [Veeco Instruments Inc (VECO) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VECO&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "Price vs 50-day average -11.9%. 20-day annualised volatility 90.0%"
- **[T10]** *(ai_interpretation, confidence medium)* Veeco Instruments shows the mildest pull-back in this group (-21.0% over 3 months, 11.9% below its 50-day average) and the lowest volatility (90.0% annualised), but volatility near 90% is still high in absolute terms, so timing risk remains material.
  - source: [Veeco Instruments Inc (VECO) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VECO&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T11]** *(verified_fact, confidence medium)* Aeluma closed at 7.47 on 2026-11-09, down 34.5% over 1 month and 58.9% over 3 months, 30.6% below its 50-day average and 71.6% below its 100-day high, with 20-day annualised volatility of 126.3% and a rule-based timing risk of subdued.
  - source: [Aeluma, Inc. (ALMU) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ALMU&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - excerpt: "3-month return -58.9%. Price vs 50-day average -30.6%. 20-day annualised volatility 126.3%"
- **[T12]** *(ai_interpretation, confidence medium)* Aeluma has experienced the deepest decline in the group (-58.9% over 3 months, -71.6% from its 100-day high). The subdued label reflects the absence of run-up, not stability: volatility of 126.3% annualised signals a highly unstable price environment.
  - source: [Aeluma, Inc. (ALMU) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ALMU&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
- **[T13]** *(ai_interpretation, confidence medium)* Cross-company observation: five of the six silicon-photonics-linked stocks (Teradyne, Formfactor, Aehr Test Systems, Veeco Instruments, Aeluma) are flagged subdued, each trading well below its 50-day average after steep 1-3 month declines, while all six carry 20-day annualised volatility of 90% or more.
  - source: [Teradyne, Inc (TER) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TER&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - source: [Formfactor Inc (FORM) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FORM&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - source: [Aehr Test Systems (AEHR) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AEHR&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - source: [Veeco Instruments Inc (VECO) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VECO&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - source: [Aeluma, Inc. (ALMU) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ALMU&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - source: [Lightwave Logic, Inc. (LWLG) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LWLG&outputsize=compact) (Alpha Vantage, 2026-11-09, full_text)
  - reasoning: The theme's price action over this window is broadly a sell-off, not a run-up; the dominant timing risk across the group is extreme volatility rather than stretched prices.

**Limitations:**
- The metrics cover only about 100 trading days, a short window that may not capture longer-term price behaviour or cycles.
- This analysis uses price data only: no fundamentals, valuation, earnings or balance-sheet information is considered.
- Prices can move for reasons unrelated to silicon photonics (market-wide moves, sector rotation, company-specific news), so drawdowns or volatility cannot be attributed to the theme itself.
- Past price behaviour does not predict future prices; a subdued level means less recent run-up, not that prices will rise, and declines can continue or reverse.
- Volatility figures are annualised from a 20-day window and can change quickly.
- Rule-based timing-risk labels are heuristic and do not constitute trading advice or forecasts.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 9 distinct company names from 0 patent publications, 1 company-affiliated papers and 8 SEC filers; 8 matched to the SEC ticker file (8 outside the configured list), 1 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Lightwave Logic, Inc. (LWLG) · Miscellaneous Plastics Products | 0 | 0 | 6 | micro: 0.00B USD | +147.7% | 4850.9% | **55** |
| Formfactor Inc (FORM) · Semiconductors & Related Devices | 0 | 0 | 4 | small: 0.78B USD | +2.8% | 14.7% | **45** |
| Aehr Test Systems (AEHR) · Instruments For Meas & Testing of  Electricity & Elec Signals | 0 | 0 | 3 | micro: 0.05B USD | -15.2% | 25.3% | **45** |
| Veeco Instruments Inc (VECO) · Special Industry Machinery, NEC | 0 | 0 | 3 | small: 0.48B USD | +45.8% | n/a | **45** |
| Aeluma, Inc. (ALMU) · Semiconductors & Related Devices | 0 | 0 | 2 | micro: 0.00B USD | -4.4% | 104.6% | **45** |
| Axt Inc (AXTI) · Semiconductors & Related Devices | 0 | 0 | 5 | micro: 0.09B USD | -11.1% | 10.2% | **40** |
| Photronics Inc (PLAB) · Semiconductors & Related Devices | 0 | 0 | 4 | small: 0.85B USD | -2.0% | 1.9% | **35** |
| Teradyne, Inc (TER) · Instruments For Meas & Testing of  Electricity & Elec Signals | 0 | 0 | 6 | mid: 2.10B USD | -1.7% | n/a | **30** |

- Lightwave Logic, Inc.: 6 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth +148% (+10); R&D 4851% of revenue (+10)
- Formfactor Inc: 4 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +3% (+5); R&D 15% of revenue (+5)
- Aehr Test Systems: 3 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth -15% (+0); R&D 25% of revenue (+10)
- Veeco Instruments Inc: 3 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +46% (+10)
- Aeluma, Inc.: 2 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth -4% (+0); R&D 105% of revenue (+10)
- Axt Inc: 5 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); micro company by revenue (+15): more room to grow, more risk; revenue growth -11% (+0); R&D 10% of revenue (+5)

**Found but not in the SEC ticker file (private, foreign, or name not matched):** Swiss Center for Electronics and Microtechnology (Switzerland) (0P/1A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* Lightwave Logic, Inc. (LWLG) is active on silicon photonics: 6 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.00B USD (micro by revenue), growth +147.7%, R&D 4850.9% of revenue. Next-runner score 55/100 (heuristic).
  - source: [Lightwave Logic, Inc. Form 10-Q, filed 2026-08-14](https://www.sec.gov/Archives/edgar/data/1325964/000107997326001097/lwlg_10q-063026.htm) (SEC EDGAR, 2026-08-14, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Formfactor Inc (FORM) is active on silicon photonics: 4 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.78B USD (small by revenue), growth +2.8%, R&D 14.7% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Aehr Test Systems (AEHR) is active on silicon photonics: 3 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.05B USD (micro by revenue), growth -15.2%, R&D 25.3% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Aehr Test Systems Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1040470/000165495426009601/aehr_10q.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Veeco Instruments Inc (VECO) is active on silicon photonics: 3 of its SEC report(s) mention the topic; fiscal 2017 revenue 0.48B USD (small by revenue), growth +45.8%. Next-runner score 45/100 (heuristic).
  - source: [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K5]** *(ai_interpretation, confidence low)* Aeluma, Inc. (ALMU) is active on silicon photonics: 2 of its SEC report(s) mention the topic; fiscal 2026 revenue 0.00B USD (micro by revenue), growth -4.4%, R&D 104.6% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) (SEC EDGAR, 2026-09-16, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K6]** *(ai_interpretation, confidence low)* Axt Inc (AXTI) is active on silicon photonics: 5 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.09B USD (micro by revenue), growth -11.1%, R&D 10.2% of revenue. Next-runner score 40/100 (heuristic).
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [@eetimes: In this partner interview, #Celestica and #Broadcom explain how co-packaged #optics cut po…](https://x.com/eetimes/status/2119797353896964464) | X API | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_29d22f200a
- [Lightwave Logic, Inc. (LWLG) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LWLG&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_33cb5748f3
- [Teradyne, Inc (TER) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TER&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_3cdce48bee
- [Formfactor Inc (FORM) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=FORM&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_0262a739d5
- [Aehr Test Systems (AEHR) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AEHR&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_1c46c1c442
- [Veeco Instruments Inc (VECO) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=VECO&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_d0aa03b428
- [Aeluma, Inc. (ALMU) daily prices 2026-06-18 to 2026-11-09](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ALMU&outputsize=compact) | Alpha Vantage | 2026-11-09 | retrieved 2026-11-10 | full_text | id src_ec772c3e76
- [Aehr Test Systems Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1040470/000165495426009601/aehr_10q.htm) | SEC EDGAR | 2026-11-06 | retrieved 2026-11-10 | excerpt_only | id src_c14bb8c6a4
- [@Finsee_main: $AAOI Q3 2026 earnings: Applied Optoelectronics sales more than double, but power delays c…](https://x.com/Finsee_main/status/2118454807388106826) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_7311390364
- [@Finsee_main: $HIMX Q3 2026 earnings: Himax third-quarter profit beats plan, but Chinese car orders drop…](https://x.com/Finsee_main/status/2118313834431529032) | X API | 2026-11-05 | retrieved 2026-11-10 | full_text | id src_35e30e6dc9
- [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) | SEC EDGAR | 2026-11-04 | retrieved 2026-11-10 | excerpt_only | id src_10ad34c466
- [@Finsee_main: $VIAV Q1 2027 earnings: Viavi's sales outlook tops $500 million, but share dilution grows …](https://x.com/Finsee_main/status/2118095750089310308) | X API | 2026-11-04 | retrieved 2026-11-10 | full_text | id src_0c3648a1d9
- [@Finsee_main: $COHR Q1 2027 earnings: Coherent raises its sales plan, but factory spending burns cash Co…](https://x.com/Finsee_main/status/2118093426994372647) | X API | 2026-11-04 | retrieved 2026-11-10 | full_text | id src_dd82e82d50
- [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) | SEC EDGAR | 2026-11-03 | retrieved 2026-11-10 | excerpt_only | id src_635ef44763
- [@eetimes: Five Things You Didn’t Know About Co-Packaged Optics https://t.co/9b7vcYeVlp https://t.co/…](https://x.com/eetimes/status/2117617868787384756) | X API | 2026-11-03 | retrieved 2026-11-10 | full_text | id src_3b0c8869a4
- [@CounterPointTR: 𝗠𝗮𝗿𝘃𝗲𝗹𝗹 𝗕𝘂𝘆𝘀 𝗟𝘂𝗺𝗲𝗻𝘁𝘂𝗺 𝘁𝗼 𝗖𝗹𝗶𝗺𝗯 𝘁𝗵𝗲 𝗔𝗜 𝗟𝗮𝘀𝗲𝗿 𝗪𝗮𝗹𝗹: 𝗪𝗵𝗮𝘁 𝘁𝗵𝗲 $𝟭𝟭𝟱 𝗕𝗶𝗹𝗹𝗶𝗼𝗻 𝗗𝗲𝗮𝗹 𝗠𝗲𝗮𝗻𝘀 𝗳𝗼𝗿 𝗢𝗽𝘁…](https://x.com/CounterPointTR/status/2117499775654482067) | X API | 2026-11-03 | retrieved 2026-11-10 | full_text | id src_5ebae369cf
- [Teradyne, Inc Form 10-Q, filed 2026-10-30](https://www.sec.gov/Archives/edgar/data/97210/000119312526441091/ter-20260927.htm) | SEC EDGAR | 2026-10-30 | retrieved 2026-11-10 | excerpt_only | id src_4aa95b65ab
- [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) | SEC EDGAR | 2026-09-16 | retrieved 2026-11-10 | excerpt_only | id src_f574b69c51
- [Lightwave Logic, Inc. Form 10-Q, filed 2026-08-14](https://www.sec.gov/Archives/edgar/data/1325964/000107997326001097/lwlg_10q-063026.htm) | SEC EDGAR | 2026-08-14 | retrieved 2026-11-10 | excerpt_only | id src_86b7fab896
- [Zero-change foundry compatible silicon photonics MEMS optical switch](https://arxiv.org/abs/2608.03146v1) | arXiv | 2026-08-04 | retrieved 2026-11-10 | abstract_only | id src_e2d4f96a6f
- [Silicon Photonics](https://doi.org/10.1002/9781119601289) | OpenAlex | 2026-06-26 | retrieved 2026-11-10 | abstract_only | id src_31c6309ca5
- [Silicon Photonics: An Overview](https://doi.org/10.5772/intechopen.1010619) | OpenAlex | 2026-04-13 | retrieved 2026-11-10 | abstract_only | id src_051665312a
- [Addressing Hardware Limitations in Silicon Photonics for Scalable Optical Interconnects and Neural Networks](https://doi.org/10.26262/heal.auth.ir.375565) | OpenAlex | 2026-01-01 | retrieved 2026-11-10 | abstract_only | id src_3916d9accd
- [Heterogeneous back-end-of-line integration of thin-film lithium niobate on active silicon photonics for single-chip optical transceivers](https://arxiv.org/abs/2512.07196v1) | arXiv | 2025-12-08 | retrieved 2026-11-10 | abstract_only | id src_c8f379c16b
- [Entanglement Purification by Integrated Silicon Photonics](https://arxiv.org/abs/2507.03604v1) | arXiv | 2025-07-04 | retrieved 2026-11-10 | abstract_only | id src_b8d6efcfa2
- [Photoluminescent Color Centers in Foundry Silicon Photonics](https://hdl.handle.net/1974/34590) | OpenAlex | 2025-05-27 | retrieved 2026-11-10 | abstract_only | id src_14a9d4e483
- [A high-speed heterogeneous lithium tantalate silicon photonics platform](https://arxiv.org/abs/2503.10557v2) | arXiv | 2025-03-13 | retrieved 2026-11-10 | abstract_only | id src_f9200bb17d
- [Active silicon photonics for cutting edge applications](https://doi.org/10.32657/10356/204422) | OpenAlex | 2025-01-01 | retrieved 2026-11-10 | abstract_only | id src_2e1115dca5
- [Calibration of cascaded phase shifters using pairwise scan method in silicon photonics integrated chip](https://arxiv.org/abs/2412.03951v1) | arXiv | 2024-12-05 | retrieved 2026-11-10 | abstract_only | id src_f2af7d0724
- [Pioneering the future with silicon carbide integrated photonics](https://doi.org/10.1016/j.optlastec.2024.111910) | OpenAlex | 2024-10-04 | retrieved 2026-11-10 | abstract_only | id src_15fa219b57
- [Phase change material integrated silicon photonics](https://doi.org/10.1117/12.3023946) | OpenAlex | 2024-10-02 | retrieved 2026-11-10 | abstract_only | id src_22db6d71bf
- [Micro-transfer printing of GaSb optoelectronics chips for mid-infrared silicon photonics integrated circuits](https://arxiv.org/abs/2409.13413v1) | arXiv | 2024-09-20 | retrieved 2026-11-10 | abstract_only | id src_5656b97eed
- [Polarization management in silicon photonics](https://doi.org/10.1038/s44310-024-00033-6) | OpenAlex | 2024-09-02 | retrieved 2026-11-10 | abstract_only | id src_f2cd625a33
- [Silicon integrated photonics](https://doi.org/10.3367/ufne.2024.09.039762) | OpenAlex | 2024-09-01 | retrieved 2026-11-10 | abstract_only | id src_b1ca6c716a
- [Programmable phase change materials and silicon photonics co-integration for photonic memory applications: a systematic study](https://doi.org/10.1117/1.jom.4.3.031208) | OpenAlex | 2024-08-14 | retrieved 2026-11-10 | abstract_only | id src_93c5afdeac
- [Silicon photonics for high-speed communications and photonic signal processing](https://doi.org/10.1038/s44310-024-00024-7) | OpenAlex | 2024-07-17 | retrieved 2026-11-10 | abstract_only | id src_1918618d2d
- [A silicon photonics waveguide-coupled colloidal quantum dot photodiode sensitive beyond 1.6 um](https://arxiv.org/abs/2405.12376v2) | arXiv | 2024-05-20 | retrieved 2026-11-10 | abstract_only | id src_bcc7aee342
- [On-Chip Lasers for Silicon Photonics](https://doi.org/10.3390/photonics11030212) | OpenAlex | 2024-02-27 | retrieved 2026-11-10 | abstract_only | id src_1818143641
- [The Intelligent Design of Silicon Photonic Devices](https://doi.org/10.1002/adom.202301337) | OpenAlex | 2024-02-07 | retrieved 2026-11-10 | abstract_only | id src_ea922564fd
- [Roadmapping the next generation of silicon photonics](https://doi.org/10.1038/s41467-024-44750-0) | OpenAlex | 2024-01-25 | retrieved 2026-11-10 | abstract_only | id src_efdb9d7519
- [Silicon photonics for the visible and near-infrared spectrum](https://doi.org/10.1364/aop.501846) | OpenAlex | 2023-11-27 | retrieved 2026-11-10 | abstract_only | id src_179de5267e
- [Silicon Photonics Toolkit](https://doi.org/10.1364/opticaopen.23098334.v1) | OpenAlex | 2023-07-19 | retrieved 2026-11-10 | abstract_only | id src_8337f8f143
- [Massively scalable Kerr comb-driven silicon photonic link](https://doi.org/10.1038/s41566-023-01244-7) | OpenAlex | 2023-06-29 | retrieved 2026-11-10 | abstract_only | id src_49a501b932
- [Integrated silicon photonic MEMS](https://doi.org/10.1038/s41378-023-00498-z) | OpenAlex | 2023-03-19 | retrieved 2026-11-10 | abstract_only | id src_4737284b4a

## Gaps, limitations and errors
- Missing data: Patent agent did not run: no patent evidence or patent counts, so patent_momentum cannot be rated
- Missing data: No company evidence yet from silicon photonics chip or transceiver makers; retrieved market evidence is concentrated in test and equipment suppliers
- Missing data: No verified customer, volume-shipment or contract evidence
- Missing data: No revenue figures attributing sales to silicon photonics in the retrieved filings
- Missing data: No peer-reviewed foundry-scale yield, reliability or cost data for heterogeneous integration
- Missing data: No measured data beyond 32 wavelength channels, nor power and thermal-control overhead for multi-wavelength links
- Missing data: Social and news signals (co-packaged optics, Marvell-Lumentum, optical supplier earnings) are unverified and not confirmed from primary sources
- Missing data: Source citations missing for the Axt scout finding (K6)
- Limitation: Research counts are raw exact-phrase counts, not normalised for overall publishing growth, and synonyms are excluded
- Limitation: Science and Risk findings are largely based on abstracts and preprints, which are not peer reviewed
- Limitation: Many device results are single demonstrations and some were challenged as overstated
- Limitation: Market evidence is limited to short filing excerpts and headlines, and the FormFactor statement is an unverified claim
- Limitation: Price and timing findings cover about 100 trading days and are risk context only, not signals
- Limitation: Company scout scores are heuristics, not predictions, and smaller companies carry more risk and less disclosure
- Limitation: This is a research assessment, not investment advice, and contains no price targets or recommendations
- Chief review gap: No dedicated science finding on co-packaged optics (CPO) architecture or packaging challenges, despite CPO being a major commercial driver for AI data-centre silicon photonics; the planned packaging query does not appear to have yielded a specific finding.
- Chief review gap: III-V/Si heteroepitaxy progress (e.g., InP-on-Si laser integration maturity) is only addressed from a risk angle (R1, R8) with no positive technical progress finding; this is a key enabler for on-chip light sources.
- Chief review gap: No finding on current transceiver performance benchmarks (e.g., 800G/1.6T modulator bandwidth, insertion loss) to anchor the technology's commercial readiness.
- Chief review gap: Patent agent was not run, so the IP landscape (key patents, freedom-to-operate, patent thickets) is entirely unassessed; this cannot be filled by paper search.
- Chief review gap: Cost-per-channel or cost-trajectory evidence is absent; market findings cover the test/equipment layer but not the SiPh transceiver BOM or pricing vs. alternatives.
- Chief review gap: Patent agent was not run, so there is no IP landscape, freedom-to-operate, or competitive patent positioning analysis
- Chief review gap: Market evidence is concentrated in the test-and-equipment layer (Teradyne, FormFactor, Veeco, Aehr); no direct filings from major silicon photonics chip or transceiver makers (e.g., Intel, Broadcom, Marvell, Coherent) were retrieved
- Chief review gap: Co-packaged optics (CPO) appears only in unverified social signals and press mentions, with no paper-level or verified market-filing evidence on CPO architecture, yield, or deployment timelines
- Chief review gap: No quantitative manufacturing yield, cost-per-channel, or wafer-level test data from the retrieved papers; scaling to volume production remains qualitatively described as an open question
- Chief review gap: Advanced packaging (3D integration, fiber-array coupling, thermal management at the package level) is named as a bottleneck but lacks dedicated technical coverage beyond a single coupling-loss data point
- Reference checks changed 1 statement(s) in the assessment (see notes in italics above).
- ERROR [patent/EPO OPS]: counts: EPO refused the request (fair use / quota or bad token)
- ERROR [patent/EPO OPS]: year-to-date count: EPO refused the request (fair use / quota or bad token)
- ERROR [patent/EPO OPS]: EPO refused the request (fair use / quota or bad token)

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 3 | 10373 | 4655 | 0.00670 |
| x | z-ai/glm-5.3-flash | 1 | 3338 | 738 | 0.00064 |
| science | deepseek/deepseek-v4.1-flash | 2 | 10714 | 7959 | 0.01276 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 24503 | 10980 | 0.15881 |
| market | z-ai/glm-5.3 | 1 | 3407 | 1844 | 0.01501 |
| timing | z-ai/glm-5.3-flash | 1 | 1835 | 1777 | 0.00104 |
| investment | anthropic/claude-sonnet-5-5 | 2 | 38136 | 15089 | 0.22716 |
| x (data) | X API pay-per-use | 8 | 0 | 0 | 0.03500 |

Total estimated cost: $0.45711 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
