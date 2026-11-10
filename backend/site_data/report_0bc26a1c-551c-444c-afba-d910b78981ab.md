# FUTURESCOUT AI research report: co-packaged optics

Generated: 2026-11-09 04:42 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, x, scout, investment
- Agents NOT run in this version: patent. Conclusions therefore have no patent evidence.

## Summary
The evidence shows co-packaged optics (CPO) is an active and fast-growing research field [S1][S2], with code-computed research acceleration of 82->149 papers (YoY 81.7%) between 2024 and 2025, and a first vendor prototype reported at 51.2 Tb/s [S2]. Commercial activity is real but currently visible only as company self-descriptions in SEC filings: Marvell [M1], AMD [M2], Amkor [M3], ASE [M4], Coherent [M5], FormFactor [M6], Lumentum [M7] and Veeco [M8] all describe CPO-related products, services or acquisitions, but no filing excerpt in this set demonstrates a named customer adopting CPO. The main uncertainty is technical and system-level: thermal management [R1], manufacturing yield and alignment [R3], and standardization and serviceability [R4] are repeatedly identified as unresolved, and several Science findings are weakened by challenges [C1][C6][C7]. Patent evidence is absent (patent agent did not run), so no patent-momentum rating is possible, and there is no price or timing evidence. Research activity should not be read as commercial success.

## Technology Opportunity Score
**Score: 46.6 / 100** (confidence: low; evidence coverage 80%)

Risk adjustment: rating 4/5 lowered the score by 24.0% (base 61.3).

Commercialization Gap (research momentum rating minus commercial readiness rating): +3


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S2, S3, S4 | Code-computed exact-phrase OpenAlex works rose from 82 (2024) to 149 (2025), an 81.7% YoY increase, and the findings span reviews, prototypes, materials, lithography and cooling [S1][S2][S4][S12]. Note this counts only the exact phrase, is not normalised for overall publishing growth, and research volume is not commercial success. |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 3 | S2, S4, S6, R1, R3, C1 | Prototypes and component results exist (a 51.2 Tb/s CPO switch [S2], glass substrates [S4], an external laser source [S6]), but yield, alignment, thermal and reliability barriers are repeatedly flagged [R1][R3][R5] and the prototype lacks performance data [C1]. |
| Commercial Readiness | 15% | 2 | M1, M4, M5, M7, R4, R6 | Filings show companies offering CPO products or services [M1][M5][M7][M4], but cost and economic viability are named as goals rather than demonstrated [R6], and CPO is described as an architectural commitment rather than a component swap [R4]. No shipment or revenue data is given. |
| Customer Adoption | 10% | missing | none | no valid 0-5 rating given |
| Industry Investment | 10% | 3 | M2, M9, K1, K2, K3, K4 | AMD reported strategic acquisitions for photonics and CPO [M2], Marvell described optical engines, external lasers and optical I/O [M9], and Scout lists company R&D intensities and SEC mentions across several firms [K1][K2][K3][K4]. These are investment signals, not proof of demand. |
| Competitive Position | 10% | 2 | M1, M4, M5, M7 | Multiple companies describe overlapping CPO capabilities (Marvell [M1], Coherent [M5], Lumentum [M7], ASE [M4]), but the filings do not establish differentiated position, design wins or share, and no customer evidence exists. |
| Supply-Chain Readiness | 15% | 3 | M3, M4, M6, M7, M8, S4, S5, R3, R7 | Packaging, test and materials roles are described by Amkor [M3], ASE [M4], FormFactor [M6], Lumentum [M7] and Veeco [M8], and glass and polymer substrate work exists [S4][S5]. But yield and alignment are unresolved [R3] and the ecosystem depends on one platform and early-stage materials [R7]. |

Formula: base = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100; score = base x (1 - max_penalty x risk_rating/5). Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. The score is an explainable heuristic, not a validated prediction of stock performance.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.
- Confidence lowered to 'low': coverage is 80%, but the cited ratings themselves are mostly of lower confidence.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Co-packaged optics for AI datacenter interconnect

Technologies: silicon photonics, co-packaged optics, optical engines, external laser sources

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Evidence for the near term is company portfolio and roadmap statements rather than deployment outcomes: Marvell lists CPO in its custom silicon/interconnect portfolio [M1], Coherent says it sells CPO products into datacenter/communications [M5], Lumentum supplies lasers and packaging for CPO [M7], and Marvell investor materials describe pre-validated optical engines and optical I/O [M9]. A social post claims 2027 will focus on platform qualification and testing [X1] but is an unverified claim. No price/timing data was provided, so near-term timing risk cannot be assessed. *(ai_interpretation)* [M1, M5, M7, M9, X1] | low |
| medium_1_3y | A prototype 51.2 Tb/s all-optical switch co-packaging eight 6.4 Tb/s optical engines has been reported [S2], and component-level results exist for external lasers [S6] and glass substrates [S4]. However, standardization and serviceability remain open [R4], and the prototype abstract carries no power, yield, thermal or reliability data [C1]. Whether CPO displaces pluggable or near-packaged optics is not resolved in the evidence [R6]. *(ai_interpretation)* [S2, S4, S6, R4, R6, C1] | low |
| long_3_5y | The cited evidence does not support a long-horizon outcome. High research volume [S1] does not establish commercial success (see limitations), and cost and economic viability are described as goals rather than demonstrated [R6]. The abstracts give no field reliability or long-term serviceability data [R2][R5]. *(ai_interpretation)* [S1, R2, R5, R6] | low |

**Bull case:** CPO is proposed to raise interconnect bandwidth density and energy efficiency by shortening electrical links through advanced packaging [S1], and a prototype has been reported co-packaging eight 6.4 Tb/s optical engines into a 51.2 Tb/s switch [S2]. Multiple large public companies already describe CPO products or capabilities [M1][M5][M7], AMD made strategic acquisitions for photonics and CPO [M2], and Marvell's investor materials describe pre-validated optical engines and optical I/O for custom XPUs [M9]. *(forecast)* [S1, S2, M1, M2, M5, M7, M9]

**Base case:** CPO is developing with real component and packaging progress [S4][S6], commercial activity concentrated in company portfolios and roadmaps [M1][M5][M7], and continued technical work on platform qualification and testing [X1]. Adoption is likely gated by unresolved standardization, serviceability and system-level trade-offs, and CPO is characterised as an architectural commitment rather than a component swap [R4]. *(ai_interpretation)* [S4, S6, M1, M5, M7, R4, X1]

**Bear case:** The 51.2 Tb/s prototype is a single vendor demonstration with no power, efficiency, yield, thermal, reliability or serviceability data, and 'industry first' is the authors' own claim [C1]. The CPO benefits are described in qualitative advocacy terms with few comparative numbers, and cost and economic viability are goals rather than demonstrations [C6][R6]. Laser integration, device reliability and photonic thermal sensitivity are unsolved, and fixing the optical engine to the ASIC package makes a failed laser or fiber array harder to replace [R5]. *(ai_interpretation)* [C1, C6, R5, R6]

**Catalysts:**
- Reporting of platform qualification and faster testing/passive alignment would strengthen the near-term case, but this is currently only an unverified social claim [X1]. *(unverified_claim)* [X1]
- Further strategic acquisitions for photonics/CPO, as AMD reported [M2], or Marvell's described optical I/O and external-laser engine push [M9], indicate continued industry investment. *(ai_interpretation)* [M2, M9]

**Risks:**
- Thermal management is repeatedly named as a central constraint: co-integrating a high-power-density switch ASIC with temperature-sensitive photonics creates thermal crosstalk and a cooling burden pluggable optics avoid [R1]. *(ai_interpretation)* [R1]
- Manufacturing yield and alignment precision are acknowledged as unresolved barriers, and the VCSEL flip-chip validation is lab-scale [R3]. *(ai_interpretation)* [R3]
- Laser integration, device reliability and thermal sensitivity of photonics are listed as unsolved, with harder serviceability than pluggable modules [R5]. *(ai_interpretation)* [R5]
- Standardization and serviceability may decide whether CPO moves from early deployment to broad adoption [R4]. *(ai_interpretation)* [R4]

**What would invalidate this thesis:**
- Clear evidence that near-packaged optics or pluggable optics win on cost/performance and CPO displacement does not materialise would weaken the thesis; the evidence notes this comparison is unresolved [R6]. *(forecast)* [R6]
- Persistent failure to resolve thermal, yield and standardization barriers [R1][R3][R4] would undermine the case for broad adoption. *(forecast)* [R1, R3, R4]

**Conflicting evidence:**
- C1 weakens S2: no power, efficiency, yield, thermal, reliability or serviceability data, and 'industry first' is the authors' own claim [C1]. *(ai_interpretation)* [C1, S2]
- C6 weakens S1: benefit claims rest on qualitative advocacy abstracts with few comparative numbers, and displacement risk versus near-packaged optics is not assessed [C6]. *(ai_interpretation)* [C6, S1]
- C7 argues the findings set omits system-level barriers (thermal as a critical bottleneck, yield, alignment, serviceability, standardization) and gives an overly optimistic readiness picture [C7]. *(ai_interpretation)* [C7]

**Companies named by cited evidence:**
- Marvell Technology, Inc.: 10-K states Marvell offers co-packaged optics in its custom silicon and interconnect portfolio on silicon photonics [M1]; investor materials describe pre-validated optical engines, external lasers and optical I/O for custom XPUs [M9]. Large incumbent. [M1, M9]
- Advanced Micro Devices Inc: 10-K states AMD made strategic acquisitions during the year to support photonics and co-packaged optics for next-generation AI systems [M2]. Large incumbent; acquisition specifics not given in the excerpt. [M2]
- Coherent Corp.: 10-Q states Coherent sells co-packaged optics products into the datacenter and communications market within a reporting segment [M5]; Scout flags 3 SEC reports mentioning the topic, fiscal 2026 revenue 7.12B USD, growth +22.5%, R&D 10.2% of revenue, next-runner score 45/100 [K2]. Mid-size company; score is a heuristic, not a prediction. [M5, K2]
- Lumentum Holdings Inc.: 10-K states Lumentum delivers customised laser and packaging solutions enabling co-packaged optics and integrated photonics assemblies [M7]; Scout flags 2 SEC reports mentioning the topic, fiscal 2025 revenue 3.01B USD, growth +83.2%, R&D 11.8% of revenue, next-runner score 45/100 [K4]. Mid-size company; more risk and less disclosure than large incumbents. [M7, K4]
- Aeluma, Inc.: 10-K mentions silicon photonics companies and integrated light source providers as competitors or demand drivers, but the excerpts do not establish a concrete CPO role [M10]; Scout flags 1 SEC report mentioning the topic, fiscal 2026 revenue ~0.00B USD, R&D 104.6% of revenue, next-runner score 40/100 [K5]. Micro-cap, very thin disclosure; high risk. [M10, K5]

### Advanced packaging, materials and test supply chain for CPO

Technologies: glass substrates with embedded waveguides, fan-out wafer-level packaging, through-silicon/through-glass vias, wafer-level packaging, optical probing/test, InP epitaxy and laser-facet coating

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | Several companies describe packaging, test or equipment roles today: Amkor positions CPO and silicon photonics wafer-level packaging [M3], ASE lists CPO processing among advanced packaging services and makes optical engines [M4], FormFactor's Keystone Photonics supplies optical probing for CPO/NPO test [M6], and Veeco sees hyperscalers advancing toward near-package and co-packaged optics over the longer term, driving InP epitaxy and facet-coating equipment demand [M8]. These are filing descriptions, not order or revenue evidence. *(ai_interpretation)* [M3, M4, M6, M8] | low |
| medium_1_3y | Glass substrates with embedded waveguides and through-glass vias have been demonstrated with reported coupling loss of 0.5–0.65 dB and propagation loss below 0.1 dB/cm [S4], and a BCB polymer waveguide platform is reported with reflow and damp-heat survival [S5]. Manufacturing yield and alignment remain unresolved [R3], and the glass work is a laboratory process without yield or reliability data [C2]. *(ai_interpretation)* [S4, S5, R3, C2] | low |
| long_3_5y | No finding supports a long-horizon supply-chain conclusion. The ecosystem depends heavily on silicon photonics and on novel packaging materials and processes still early-stage [R7], and no field or qualification data appears. *(ai_interpretation)* [R7] | low |

**Bull case:** CPO requires advanced packaging, new substrate materials and dedicated test and equipment, and multiple companies already describe these capabilities: Amkor's CPO/silicon-photonics wafer-level packaging [M3], ASE's CPO processing and optical-engine manufacturing [M4], FormFactor's optical probing for CPO/NPO test [M6], and Veeco's InP epitaxy and laser-facet coating equipment [M8]. Scout highlights FormFactor (small by revenue, R&D 14.7% of revenue) and Veeco as comparatively active smaller names [K1][K3]. *(forecast)* [M3, M4, M6, M8, K1, K3]

**Base case:** Packaging and materials work is progressing across several integration routes including glass substrates [S4] and polymer waveguides [S5], with companies positioning packaging, test and equipment roles [M3][M4][M6][M8]. The glass result is a laboratory process and the coupling-loss figure is a best-case minimum from what appears to be one process stream [C2], so readiness is not yet established. *(ai_interpretation)* [S4, S5, M3, M4, M6, M8, C2]

**Bear case:** Manufacturing yield and alignment precision are acknowledged unresolved barriers and validation is lab-scale [R3]. The ecosystem depends heavily on a single integration platform (silicon photonics) and on novel packaging materials still early-stage, with the glass coupling loss from a single process stream in one proceedings paper [R7]. The reported coupling-loss numbers omit fibre-connector loss and yield/reliability data [C2]. *(ai_interpretation)* [R3, R7, C2]

**Catalysts:**
- Reporting of volume packaging yield, qualification or optical-engine production data (currently absent) would strengthen the supply-chain case; existing evidence is capability descriptions [M3][M4]. *(forecast)* [M3, M4]

**Risks:**
- Yield and alignment precision are unresolved and validation is lab-scale [R3]. *(ai_interpretation)* [R3]
- Dependence on one integration platform and early-stage novel materials concentrates supply-chain risk [R7]. *(ai_interpretation)* [R7]
- The glass-substrate performance numbers are best-case minimums, omit fibre-connector loss, and lack yield/reliability data [C2]. *(ai_interpretation)* [C2]

**What would invalidate this thesis:**
- Evidence that packaging yield and alignment cannot be brought to production scale [R3], or that glass/polymer substrates fail qualification [C2], would weaken the supply-chain thesis. *(forecast)* [R3, C2]

**Conflicting evidence:**
- C2 weakens S4: the coupling-loss figures are best-case minimums from what appears to be one process stream, fibre-connector loss is omitted, and there is no yield or reliability data [C2]. *(ai_interpretation)* [C2, S4]

**Companies named by cited evidence:**
- Amkor Technology, Inc.: 10-K positions CPO and silicon photonics wafer-level packaging as a way to participate in datacenter/AI scaling [M3]. Large packaging incumbent. [M3]
- ASE Technology Holding Co., Ltd.: 20-F lists Co-Packaged Optics processing among advanced packaging services and states it manufactures high-data-rate optoelectronic components and optical engines [M4]. Large packaging incumbent (foreign filer). [M4]
- Formfactor Inc: 10-Q states its Keystone Photonics unit provides optical probing for silicon photonics, CPO and near-packaged optics test [M6]; Scout flags 4 SEC reports mentioning the topic, fiscal 2025 revenue 0.78B USD (small), growth +2.8%, R&D 14.7% of revenue, next-runner score 45/100 [K1]. Smaller company: more risk and less disclosure; score is a heuristic. [M6, K1]
- Veeco Instruments Inc: 10-Q states Veeco sees hyperscalers advancing toward near-package and co-packaged optics over the longer term, driving InP epitaxy and laser-facet coating equipment demand [M8]; Scout flags 3 SEC reports mentioning the topic, revenue 0.48B USD (small, note the fiscal-year label shown as 2017 in the source), growth +45.8%, next-runner score 45/100 [K3]. Smaller company: more risk and less disclosure; score is a heuristic. [M8, K3]
- Jabil Inc: Scout flags 2 SEC reports mentioning co-packaged optics, fiscal 2026 revenue 35.95B USD (large), growth +20.6%, R&D 0.1% of revenue, next-runner score 30/100 [K6]. The specific CPO role is not established in the cited excerpt; score is a heuristic. [K6]

### Thermal management and reliability as the CPO gating factor

Technologies: liquid cooling and cold-plate design, thermal-crosstalk mitigation, phase-change-material non-volatile photonics

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The evidence identifies thermal management as a repeated central constraint but provides no field or reliability outcome [R1]. There is no near-term timing or price evidence provided. *(ai_interpretation)* [R1] | low |
| medium_1_3y | Liquid-cooling work exists but is narrow and mostly simulation-backed, testing different bandwidth classes with custom cold plates and reporting simulation within 4% of a bench platform; no long-term reliability, thermal-cycling, field or serviceability data is reported [R2]. Micro-ring thermal tuning is described as limited by high static power and severe thermal crosstalk, motivating phase-change-material non-volatile photonics [S8]. *(ai_interpretation)* [R2, S8] | low |
| long_3_5y | No finding supports a long-horizon conclusion on thermal solutions; the abstracts report no long-term reliability or field data [R2][R5]. *(ai_interpretation)* [R2, R5] | low |

**Bull case:** Thermal constraints are being actively researched and alternatives are proposed, such as phase-change-material non-volatile photonics to reduce the high static power and severe thermal crosstalk of conventional micro-ring thermal tuning [S8]. Solving cooling and reliability would unlock CPO's cited bandwidth-density and energy-efficiency benefits [S1]. *(forecast)* [S8, S1]

**Base case:** Thermal management is repeatedly named a central constraint on CPO reliability and performance because a high-power-density switch ASIC sits with temperature-sensitive photonics [R1]. The available cooling evidence is narrow and mostly simulation-backed, with custom cold plates and no long-term reliability, thermal-cycling, field or serviceability data [R2]. *(ai_interpretation)* [R1, R2]

**Bear case:** The findings focus on component and packaging demonstrations and understate system-level barriers that risk literature calls decisive, including thermal management as a critical bottleneck, yield, alignment, laser/fibre-array serviceability and standardization [C7]. Laser integration, device reliability and photonic thermal sensitivity are unsolved, and a failed laser or fibre array is harder to replace than a pluggable module [R5]. *(ai_interpretation)* [C7, R5]

**Catalysts:**
- Reporting of long-term reliability, thermal-cycling, field or serviceability data for liquid-cooled or otherwise cooled CPO, which the current abstracts do not provide [R2], would strengthen this theme. *(forecast)* [R2]

**Risks:**
- Thermal crosstalk between electrical and optical domains and the cooling burden are central constraints pluggable optics avoid [R1]. *(ai_interpretation)* [R1]
- Cooling evidence is simulation-heavy with different bandwidth classes and no field, reliability or serviceability data [R2]. *(ai_interpretation)* [R2]
- System-level barriers are underweighted in the component-focused findings set [C7]. *(ai_interpretation)* [C7]

**What would invalidate this thesis:**
- Demonstration of field-proven thermal reliability at production scale would weaken the 'gating factor' framing; no such evidence currently exists [R2]. *(forecast)* [R2]

**Conflicting evidence:**
- C7 argues the findings give an overly optimistic readiness picture by omitting system-level barriers such as thermal management as a critical bottleneck [C7]. *(ai_interpretation)* [C7]

**Companies named by cited evidence:**
- none (no company evidence in the cited findings)

## Evidence: academic research
Status: partial. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 15, 2021: 27, 2022: 56, 2023: 61, 2024: 82, 2025: 149, 2026: 192}
Research Acceleration 2024->2025: 82 -> 149 (81.7% YoY). OpenAlex works whose title or abstract contains the exact phrase "co-packaged optics", per publication year. Synonyms and abbreviations are not counted, and the number is not normalised for overall growth in publishing. The current (partial) year is excluded.

- **[S1]** *(verified_fact, confidence medium)* CPO is proposed as a way to raise interconnect bandwidth density and energy efficiency by greatly shortening the electrical link length through advanced packaging and joint optimisation of electronics and photonics, motivated by datacenter traffic growth that conventional pluggable optics cannot match.
  - source: [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) (OpenAlex, 2023-03-20, abstract_only)
  - source: [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) (OpenAlex, 2024-09-29, abstract_only)
  - source: [Heterogeneous Integration Technology Drives the Evolution of Co-Packaged Optics](https://doi.org/10.3390/mi16091037) (OpenAlex, 2025-09-10, abstract_only)
  - excerpt: "Co-packaged optics (CPO) is a disruptive approach to increasing the interconnecting bandwidth density and energy efficiency by dramatically shortening the electrical link length through advanced packaging and co-optimization of electronics and photonics."
  - reasoning: The quoted statement comes from one review (src_8bc0d86153); two further reviews (src_e674fc828f, src_711ed43b25) describe the same bandwidth/power motivation, so the framing is consistent across independent overviews, though all are review articles rather than new measurements.
- **[S2]** *(verified_fact, confidence medium)* A prototype CPO switch solution has been reported that co-packages eight silicon-photonic optical engines, each with 6.4 Tb/s bandwidth, into an all-optical 51.2 Tb/s switch.
  - source: [High Density Integration of Silicon Photonic Chiplets for 51.2T Co-packaged Optics](https://doi.org/10.1109/ectc51529.2024.00022) (OpenAlex, 2024-05-28, abstract_only)
  - excerpt: "This paper shows the high-density integration of CMOS based silicon photonic chiplets to achieve an optical engine bandwidth of 6.4Tb/s and deliver an all-optical 51.2Tb/s co-packaged optics (CPO) switch solution."
  - reasoning: Single conference-paper abstract reporting an industry-first prototype system; the figure is stated by the authors and is not independently corroborated by other papers in this set.
- **[S3]** *(ai_interpretation, confidence medium)* CPO packaging research spans several distinct integration routes, including 2D, 2.5D and 3D packaging, fan-out wafer-level packaging, through-silicon vias and through-glass vias, rather than converging on a single architecture.
  - source: [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) (OpenAlex, 2024-09-29, abstract_only)
  - source: [Heterogeneous Integration Technology Drives the Evolution of Co-Packaged Optics](https://doi.org/10.3390/mi16091037) (OpenAlex, 2025-09-10, abstract_only)
  - source: [Heterogeneous Integration in Co-Packaged Optics](https://doi.org/10.1109/jetcas.2025.3590744) (OpenAlex, 2025-07-21, abstract_only)
  - reasoning: Two reviews itemise different packaging families (2D/2.5D/3D in src_e674fc828f; FOWLP, TSV, TGV in src_711ed43b25) and a third discusses interposer material trade-offs and multi-physics packaging (src_926601ff5d). The parallel listing suggests a technology landscape still in competition, but the abstracts do not compare the routes quantitatively.
- **[S4]** *(verified_fact, confidence medium)* Glass-based substrates with embedded optical waveguides, through-glass vias and electrical redistribution inside a cavity have been demonstrated for CPO, with reported optical coupling loss between silicon-nitride photonic chips and ion-exchange glass waveguides in the 0.5–0.65 dB range and waveguide propagation loss below 0.1 dB/cm.
  - source: [Glass Platform for Co-Packaged Optics](https://doi.org/10.1109/jstqe.2023.3247245) (OpenAlex, 2023-01-01, abstract_only)
  - source: [Glass Substrate for Co-Packaged Optics](https://doi.org/10.4071/001c.74749) (OpenAlex, 2023-05-01, abstract_only)
  - excerpt: "Photonic chips with silicon nitride waveguides were optically coupled to glass waveguides with a minimum loss of 0.5 dB, achieved by fiducial-aligned flip-chip photonic assembly."
  - reasoning: Two papers give broadly consistent numbers (0.5 dB and 0.65 dB coupling; <0.1 dB/cm propagation), which strengthens the claim, but they describe closely related glass-platform work and may not be fully independent.
- **[S5]** *(verified_fact, confidence low)* A photo-patternable benzocyclobutene (BCB) polymer waveguide platform has been reported with propagation loss below 0.1 dB/cm at 850 nm and below 0.3 dB/cm at 1310 nm, patterned on silicon and PCB substrates to sub-10 μm accuracy and surviving multiple reflows and 1000 h of 85 °C/85% humidity testing.
  - source: [Polymer Waveguides for Co-Packaged Optics](https://doi.org/10.1109/ectc51529.2024.00278) (OpenAlex, 2024-05-28, abstract_only)
  - excerpt: "achieving a propagation loss value of <0.1 dB/cm at 850 nm and <0.3 dB/cm at 1310 nm at the system level based on cutback measurements"
  - reasoning: Single conference-paper abstract reporting the authors' own material and reliability results; no independent replication appears in this set.
- **[S6]** *(verified_fact, confidence low)* An external laser source designed for CPO has been demonstrated as an uncooled pigtailed QSFP module with an 8-channel CWDM transmitter optical subassembly, reporting 100 mW per channel operation and 14.3% power conversion efficiency at 55 °C housing temperature.
  - source: [A record energy efficient QSFP ELS for co-packaged optics](https://doi.org/10.1049/icp.2023.2364) (OpenAlex, 2023-11-13, abstract_only)
  - excerpt: "When operating 100 mW for all 8 channels, the ELS achieves a record high power conversion efficiency of 14.3 % at a housing temperature of 55 °C."
  - reasoning: Self-reported 'record' from a single conference abstract; the efficiency figure cannot be compared against other papers in this set and the claim of a record is not independently verified here.
- **[S7]** *(verified_fact, confidence medium)* Thermal crosstalk (within the electrical domain and between electrical and optical domains), signal- and power-integrity issues across mixed channel types, and interposer material trade-offs are identified as the central heterogeneous-integration challenges for CPO.
  - source: [Heterogeneous Integration in Co-Packaged Optics](https://doi.org/10.1109/jetcas.2025.3590744) (OpenAlex, 2025-07-21, abstract_only)
  - excerpt: "Challenges in HI technologies are reviewed and corresponding mitigation methods are provided, including (1) thermal crosstalk within the electrical domain and between the electrical and the optical interaction"
  - reasoning: Direct statement from one 2025 journal article abstract; the co-optimisation framing is echoed by other reviews in the set but the specific challenge list is that paper's.
- **[S8]** *(verified_fact, confidence low)* Micro-ring resonators are presented as a compact, CMOS-compatible high-density integration option, but conventional thermal tuning is described as limited by high static power consumption and severe thermal crosstalk, motivating exploration of phase-change-material-based non-volatile photonics.
  - source: [Heterogeneous Integration Technology Drives the Evolution of Co-Packaged Optics](https://doi.org/10.3390/mi16091037) (OpenAlex, 2025-09-10, abstract_only)
  - excerpt: "traditional thermal tuning methods face limitations such as high static power consumption and severe thermal crosstalk"
  - reasoning: One review abstract states the limitation and the proposed PCM direction; the claimed breakthrough is described at a high level with no device metrics in the abstract, and the paper is a review, not an experimental demonstration.
- **[S9]** *(verified_fact, confidence medium)* CPO is being examined beyond datacenters for 6G radio-access networks, where authors argue it could deliver high capacity at low energy consumption, but they state that radio-specific development and standardization/industrialization paths are still required.
  - source: [Perspectives for Co-Packaged Optics in Radio Access Networks](https://doi.org/10.1109/icton59386.2023.10207522) (OpenAlex, 2023-07-02, abstract_only)
  - source: [Co-Packaged Optics Opportunities in Radio-Access Networks](https://doi.org/10.23919/etr.2023.10438941) (OpenAlex, 2023-11-01, abstract_only)
  - excerpt: "Co-packaged optics is an emerging technology with the potential to play a key role in 6G radio-access networks, due to its ability to enable high capacity at low energy consumption."
  - reasoning: Two papers make the same argument and both flag the need for dedicated radio-oriented development; they appear to come from the same industrial research group, so independent corroboration is limited. The 6G timing itself is not evidenced in the abstracts.
- **[S10]** *(verified_fact, confidence low)* Work on CPO assembly and interconnection components includes a reflow-compatible ceramic multifiber ferrule reported to avoid ferrule deformation, fiber pistoning and performance degradation after exposure to environments above 260 °C.
  - source: [Reflowable Ceramics Multifiber Ferrule for Co-Packaged Optics](https://doi.org/10.23919/icep-iaac64884.2025.11002876) (OpenAlex, 2025-04-15, abstract_only)
  - excerpt: "We are developing and evaluating reflow compatible Ceramics Multifiber Ferrule (CMF), which does not suffer any ferrule deformation, fiber pistoning, and performance deterioration even after exposure to more than 260°C environment."
  - reasoning: Single conference abstract describing work in progress ('developing and evaluating'); no quantitative data or independent confirmation is provided in the abstract.
- **[S11]** *(verified_fact, confidence low)* Two distinct photonic integration approaches for CPO are being pursued in parallel: VCSEL-based links and silicon-photonics-based integration.
  - source: [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) (OpenAlex, 2024-09-29, abstract_only)
  - source: [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) (OpenAlex, 2023-03-20, abstract_only)
  - excerpt: "Additionally, it examines the current research progress of two distinct approaches utilizing Vertical-Cavity Surface-Emitting Laser (VCSEL) and silicon photonics integration technology."
  - reasoning: One review explicitly frames the field this way; a second review argues the silicon platform is the most promising for large-scale integration, which is a stated preference rather than comparative evidence. The abstracts give no head-to-head performance data.
- **[S12]** *(verified_fact, confidence low)* For patterning silicon waveguides in CPO fabrication, a comparison of i-line steppers, KrF scanners and nanoimprint lithography reports notably higher pattern fidelity, particularly in line-edge roughness, for nanoimprint, with cost and power consumption considered alongside resolution.
  - source: [A study of lithography process comparison for Co-Package Optics](https://doi.org/10.1109/ectc51846.2026.00371) (OpenAlex, 2026-05-26, abstract_only)
  - excerpt: "the high pattern fidelity of nanoimprint lithography was shown to be remarkably superior"
  - reasoning: Single 2026 conference abstract; the quantitative comparison is not reproduced in the abstract and no other paper in this set addresses lithography tooling for CPO.

**Emerging directions:**
- Glass substrates with ion-exchange waveguides and through-glass vias as an electro-optical packaging platform
- Photo-patternable polymer/BCB waveguide layers integrated on silicon and PCB substrates
- Phase-change-material non-volatile photonic memory co-integrated with photonic interconnects
- External laser sources (uncooled, multi-channel CWDM) as a separate CPO building block
- Nanoimprint lithography for silicon waveguide patterning
- Optical through-silicon vias, 3D waveguides, microlenses and optical 3DIC
- CPO architectures adapted for 6G radio-access networks
- Reflow-compatible optical connector components (ceramic multifiber ferrules)

**Open problems:**
- Thermal crosstalk within electrical domains and between electrical and optical domains in a single package
- Static power consumption and thermal crosstalk limits of thermally tuned micro-ring resonators
- Signal- and power-integrity management across wide-and-slow and narrow-and-fast channel links
- Trade-offs in interposer material selection for heterogeneous CPO packages
- Multi-physics co-design complexity spanning electrical, optical, thermal, mechanical and material domains
- Reflow compatibility of optical interfaces (e.g., >260 °C exposure)
- Optical coupling loss and fiber-attach loss between photonic chips and packaged waveguides
- Absence of standardised, industrialised paths for CPO outside datacenters, notably for radio access

**Limitations:**
- Analysis relies on titles, venues and abstracts only; no full texts were read, so device-level results and experimental conditions cannot be checked.
- Three of the 16 items carry no usable content: src_6e1e90b306 and src_bff4d58588 have no abstract, and src_89eb116049 contains only a bulleted session outline with no results.
- Several sources are conference papers and proceedings (e.g., ECTC, ICEP-IAAC, ICTON, IET), which may not be peer reviewed in the same way as journal articles, and 'record' or 'industry first' claims are author self-reports.
- Evidence for most specific quantitative results rests on a single abstract, so confidence is generally low or medium.
- Some sources appear to originate from the same industrial research groups or are closely related reviews of the same glass platform, so they may not be fully independent corroboration.
- The set contains no cost, manufacturability yield, field-reliability or commercial-deployment data, so no conclusion about commercial viability can be drawn.
- Coverage is limited to what the search returned for the topic; relevant standards-body or supplier material may be absent.

## Evidence: risks and contrarian findings
Status: partial. Risk search queries: ['co-packaged optics thermal management', 'CPO yield reliability', 'optical engine serviceability', 'co-packaged optics power overhead', 'CPO cost per bit', 'optical interconnect failure rate']

- **[R1]** *(verified_fact, confidence medium)* Thermal management is repeatedly named as a central constraint on CPO reliability and performance. Co-integrating a high-power-density switch ASIC with temperature-sensitive photonics creates thermal crosstalk and a cooling burden that pluggable optics avoid.
  - source: [Simulation and experimental investigation of liquid-cooling thermal management for high-bandwidth co-packaged optics](https://doi.org/10.1007/s12200-025-00156-4) (OpenAlex, 2025-05-14, abstract_only)
  - source: [Thermal management in copackaged optics: from device assembly to system operation](https://doi.org/10.1117/1.apn.5.3.034001) (OpenAlex, 2026-03-19, abstract_only)
  - source: [3D Optoelectronics and Co-Packaged Optics: Innovations, Challenges, and Future Trends](https://doi.org/10.1109/jstqe.2025.3641790) (OpenAlex, 2025-12-08, abstract_only)
  - excerpt: "thermal management one of the key challenges that constrain the reliability of high-capacity co-packaged optics"
  - reasoning: Three independent abstracts, one a 2026 review, agree that thermal management is a bottleneck. They are abstracts only, so the severity cannot be quantified here.
- **[R2]** *(ai_interpretation, confidence medium)* The liquid-cooling evidence is narrow and mostly simulation-backed. The two cooling studies test different bandwidth classes (12.8 Tbps and 51.2 Tbps) with custom cold-plate designs. Agreement is reported as simulation within 4% of a bench platform. The abstracts report no long-term reliability, thermal-cycling, or field data, and no serviceability data for liquid-cooled CPO.
  - source: [Simulation and experimental investigation of liquid-cooling thermal management for high-bandwidth co-packaged optics](https://doi.org/10.1007/s12200-025-00156-4) (OpenAlex, 2025-05-14, abstract_only)
  - source: [Liquid-Cooled Heat Dissipation Technology for Co-Packaged Optics over 12.8 Tbps](https://doi.org/10.1109/icept63120.2024.10668507) (OpenAlex, 2024-08-07, abstract_only)
  - reasoning: Both papers are single-design studies in which simulation and a lab test rig mostly validate each other. The abstracts do not say whether the test vehicles used real operating optical engines or the actual heat loads of a production switch. The reported temperatures (for example an ASIC at 97.3 °C versus optics at 31.3 °C in one study, and 51 °C at 290 W in the other) come from different configurations and cannot be compared. Missing long-term data is a gap, not proof of failure.
- **[R3]** *(verified_fact, confidence medium)* Manufacturing yield and alignment precision are acknowledged as unresolved barriers. The VCSEL flip-chip study shows that bonding quality depends on tightly tuned Au-bump flattening and low misalignment, and its validation is lab-scale.
  - source: [3D Optoelectronics and Co-Packaged Optics: Innovations, Challenges, and Future Trends](https://doi.org/10.1109/jstqe.2025.3641790) (OpenAlex, 2025-12-08, abstract_only)
  - source: [3D Heterogeneous Integration of Back-Emitting VCSEL Arrays via Flip-Chip Bonding for Co-Packaged Optics Systems](https://doi.org/10.1109/jstqe.2025.3650463) (OpenAlex, 2026-01-05, abstract_only)
  - excerpt: "thermal management, manufacturing yields, and alignment precision remain key challenges"
  - reasoning: One review abstract names yield and alignment as open challenges. A device-level study shows that bonding results are sensitive to alignment and bump geometry. The abstracts give no yield percentages, so the scale of the problem is unknown.
- **[R4]** *(verified_fact, confidence low)* Standardization and serviceability are open questions that may decide whether CPO moves from early deployment to broad adoption. A 2026 preprint argues that device-centric analyses underweight system-level trade-offs and that CPO is an architectural commitment rather than a component swap.
  - source: [3D optoelectronics and co-packaged optics: when solving the wrong problems stalls deployment](https://doi.org/10.48550/arxiv.2603.21313) (OpenAlex, 2026-03-22, abstract_only)
  - source: [Unlocking the Potential of Co-Packaged Optics in AI and HPC: Opportunities and Challenges](https://doi.org/10.1109/mcom.001.2500504) (OpenAlex, 2025-12-17, abstract_only)
  - excerpt: "standardization, serviceability, and thermal-aware co-design will be decisive in determining whether co-packaged optics can transition from early deployment to widespread adoption"
  - reasoning: The main source is an arXiv preprint that is not peer reviewed, and it is a perspective piece rather than an empirical result. The IEEE Communications Magazine abstract only says standardization efforts are 'ongoing', which is consistent with incomplete standards. The horizon is an inference from the phrase 'early deployment'.
- **[R5]** *(ai_interpretation, confidence low)* Laser integration, device reliability and the thermal sensitivity of photonic components are listed as unsolved challenges. Fixing the optical engine to the ASIC package means a failed laser or fiber array is harder to replace than a pluggable module, but the abstracts do not quantify this.
  - source: [Silicon Photonics for Co‐Packaged Optics: A Review of Core PIC Components and Industry Strategies](https://doi.org/10.1002/admt.71266) (OpenAlex, 2026-08-20, abstract_only)
  - source: [Thermal management in copackaged optics: from device assembly to system operation](https://doi.org/10.1117/1.apn.5.3.034001) (OpenAlex, 2026-03-19, abstract_only)
  - source: [3D optoelectronics and co-packaged optics: when solving the wrong problems stalls deployment](https://doi.org/10.48550/arxiv.2603.21313) (OpenAlex, 2026-03-22, abstract_only)
  - reasoning: The reviews list laser integration, thermal management and device reliability as critical challenges. The replacement-difficulty inference is mine, drawing on the serviceability concern in the preprint. No abstract reports laser failure rates or field reliability data.
- **[R6]** *(ai_interpretation, confidence medium)* Power and bandwidth benefits are described in qualitative terms such as 'significantly reduces' and 'transformative', and the abstracts carry few comparative numbers. Cost and economic viability are named as goals rather than demonstrated. Comparison with near-packaged optics (NPO) is mentioned, but no outcome appears in the abstracts, so displacement risk cannot be assessed.
  - source: [Unlocking the Potential of Co-Packaged Optics in AI and HPC: Opportunities and Challenges](https://doi.org/10.1109/mcom.001.2500504) (OpenAlex, 2025-12-17, abstract_only)
  - source: [3D Optoelectronics and Co-Packaged Optics: Innovations, Challenges, and Future Trends](https://doi.org/10.1109/jstqe.2025.3641790) (OpenAlex, 2025-12-08, abstract_only)
  - source: [Silicon Photonics for Co‐Packaged Optics: A Review of Core PIC Components and Industry Strategies](https://doi.org/10.1002/admt.71266) (OpenAlex, 2026-08-20, abstract_only)
  - source: [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) (OpenAlex, 2024-09-29, abstract_only)
  - reasoning: Several review abstracts use promotional framing without quantified power-per-bit, cost or total-cost-of-ownership comparisons. The NPO comparison is only named, not reported. This describes the evidence available in abstracts, not a flaw in the full papers.
- **[R7]** *(ai_interpretation, confidence low)* The ecosystem depends heavily on a single integration platform (silicon photonics) and on novel packaging materials and processes that are still early-stage. The glass-substrate work reports a minimum 0.65 dB coupling loss from a single process stream in a 2023 proceedings paper.
  - source: [Silicon Photonics for Co‐Packaged Optics: A Review of Core PIC Components and Industry Strategies](https://doi.org/10.1002/admt.71266) (OpenAlex, 2026-08-20, abstract_only)
  - source: [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) (OpenAlex, 2023-03-20, abstract_only)
  - source: [Glass Substrate for Co-Packaged Optics](https://doi.org/10.4071/001c.74749) (OpenAlex, 2023-05-01, abstract_only)
  - reasoning: Reviews describe PICs as predominantly on SiPh and name a few leading companies, which suggests platform and supplier concentration. The abstracts do not analyze supply-chain concentration directly, so this is an inference. The glass substrate result is a small demonstration with no yield or cost data.

**Possible hype:**
- 'Transformative' / 'revolutionize' / 'disruptive' (reviews of CPO): promotional wording not backed by quantified comparisons in the abstracts.
- 'Significantly reduces power consumption': no power-per-bit figures or like-for-like pluggable baselines appear in the abstracts.
- 'Excellent performance' of liquid-cooled designs: based on simulation plus a single bench test, with no long-term reliability evidence.
- 'Economically viable' deployment roadmap: cost evidence is not shown in the abstracts.
- Widespread adoption framed as a technical inevitability: the preprint (not peer reviewed) argues that standardization, serviceability and system trade-offs could stall deployment.

**Challenges to the Science findings:**
- Targets ['S2'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S2 presents a single vendor prototype as evidence for the 51.2 Tb/s CPO switch. The abstract gives no power, efficiency, yield, thermal, reliability or serviceability data. 'Industry first' is the authors' own claim. A prototype demonstration says little about manufacturability or deployment readiness, and the 'verified_fact' label covers only that the prototype was reported.
    - source: [High Density Integration of Silicon Photonic Chiplets for 51.2T Co-packaged Optics](https://doi.org/10.1109/ectc51529.2024.00022) (OpenAlex, 2024-05-28, abstract_only)
    - excerpt: "An industry first prototype system by co-packaging eight engines with switch die that can deliver double the bandwidth of a 25.6Tb/s solution."
    - reasoning: The abstract reports only bandwidth and the prototype's existence. It contains no energy-per-bit, yield or reliability figure, and nothing independent supports the 'first' claim. The finding should be read as a capability demonstration, not evidence of maturity.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S4'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S4 reports the 0.5–0.65 dB coupling loss as the glass platform's performance. Both numbers are 'minimum' (best-case) values, and the two papers appear to describe the same glass-substrate process stream, so they are not independent confirmation. The finding omits the 0.83 dB average fibre-connector loss reported in the same IEEE JSTQE paper, which adds to the total optical path loss. It also omits that the demonstration is a laboratory process, with no yield or reliability data in the abstracts.
    - source: [Glass Platform for Co-Packaged Optics](https://doi.org/10.1109/jstqe.2023.3247245) (OpenAlex, 2023-01-01, abstract_only)
    - source: [Glass Substrate for Co-Packaged Optics](https://doi.org/10.4071/001c.74749) (OpenAlex, 2023-05-01, abstract_only)
    - excerpt: "Average connector loss of 0.83 dB was demonstrated with physical contact between fibers and IOX glass waveguides."
    - reasoning: The omitted connector loss is larger than the chip-to-glass coupling loss. Quoting only the best chip-to-waveguide figures overstates link-level performance. The 0.5 dB figure is also described as 'minimum loss', i.e. a best case rather than a distribution.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S11'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S11 cites src_8bc0d86153 for 'two integration approaches pursued in parallel' (VCSEL-based and silicon photonics). That abstract never mentions VCSELs and instead calls silicon the most promising platform. Only src_e674fc828f supports the dual-approach claim. Other retrieved reviews describe CPO PICs as 'predominantly' silicon photonics, so 'parallel' may overstate how much VCSEL-based CPO is being pursued.
    - source: [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) (OpenAlex, 2023-03-20, abstract_only)
    - source: [Silicon Photonics for Co‐Packaged Optics: A Review of Core PIC Components and Industry Strategies](https://doi.org/10.1002/admt.71266) (OpenAlex, 2026-08-20, abstract_only)
    - excerpt: "silicon platform is the most promising platform for large-scale integration."
    - reasoning: One of the two citations does not support the claim as written, and a second retrieved review points to silicon-photonics dominance. The finding needs a narrower citation and a note that the approaches are not equally weighted.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S12'], severity low:
  - **[C4]** *(ai_interpretation, confidence medium)* S12 treats the lithography comparison as showing nanoimprint to be superior for CPO silicon waveguides. The abstract's evidence is SEM images of line patterns with emphasis on line-edge roughness. It reports no measured numbers, and no yield, overlay, defectivity or throughput data. The claim of advantages in cost and power is asserted, not quantified. The paper is a single-group conference abstract, and its link to CPO-specific requirements is only asserted.
    - source: [A study of lithography process comparison for Co-Package Optics](https://doi.org/10.1109/ectc51846.2026.00371) (OpenAlex, 2026-05-26, abstract_only)
    - excerpt: "We presented SEM images of line patterns using not only conventional exposure tools such as i-line steppers and KrF scanners, but also a nanoimprint lithography tool"
    - reasoning: A qualitative SEM comparison of patterning fidelity is weak support for a tool-selection conclusion. Manufacturing readiness cannot be judged from line-edge roughness alone.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S6', 'S10'], severity low:
  - **[C5]** *(ai_interpretation, confidence medium)* S6 and S10 report component results that are self-characterised or still in progress. S6's 'record' efficiency is the authors' own claim, with no comparison table or reliability data in the abstract. S10's ferrule is described as under development ('We are developing and evaluating'), and its abstract gives no quantitative performance, so 'reported to avoid' deformation rests on an unquantified statement. Neither finding should carry the weight of a verified performance result.
    - source: [A record energy efficient QSFP ELS for co-packaged optics](https://doi.org/10.1049/icp.2023.2364) (OpenAlex, 2023-11-13, abstract_only)
    - source: [Reflowable Ceramics Multifiber Ferrule for Co-Packaged Optics](https://doi.org/10.23919/icep-iaac64884.2025.11002876) (OpenAlex, 2025-04-15, abstract_only)
    - excerpt: "We are developing and evaluating reflow compatible Ceramics Multifiber Ferrule (CMF)"
    - reasoning: Both are short conference abstracts from single groups. The S6 efficiency comes from one operating point (100 mW per channel at 55 °C housing temperature). The S10 ferrule is a work-in-progress with no numbers, so neither is independently corroborated.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S1'], severity medium:
  - **[C6]** *(ai_interpretation, confidence medium)* S1 states CPO's benefits (bandwidth density, energy efficiency) as established. Beyond the Science agent's own caution, the abstracts supplying these benefits are qualitative advocacy ('significantly reduces', 'transformative') with few comparative numbers. A cited abstract compares CPO with near-packaged optics but gives no outcome in the abstract, so displacement risk and the cost case are not assessed. The 'verified_fact' label on S1 covers only that CPO is proposed for this purpose.
    - source: [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) (OpenAlex, 2023-03-20, abstract_only)
    - source: [Unlocking the Potential of Co-Packaged Optics in AI and HPC: Opportunities and Challenges](https://doi.org/10.1109/mcom.001.2500504) (OpenAlex, 2025-12-17, abstract_only)
    - reasoning: src_8bc0d86153 states that pluggable-optics growth lags traffic as a motivating assertion. src_a072730865 only says it 'compares CPO with Near-Packaged Optics (NPO)', with no result in the abstract. Without quantified comparisons against pluggables or NPO, the efficiency claim is a goal, not an established result.
- Targets general, severity medium:
  - **[C7]** *(ai_interpretation, confidence medium)* The findings focus on component and packaging demonstrations and omit the system-level barriers that retrieved risk literature identifies as decisive: thermal management as a 'critical bottleneck' for reliability, manufacturing yield, alignment precision, laser and fibre-array serviceability, and standardization. S7 mentions thermal crosstalk but frames it as a heterogeneous-integration detail from one paper. The set therefore gives an overly optimistic picture of readiness.
    - source: [Thermal management in copackaged optics: from device assembly to system operation](https://doi.org/10.1117/1.apn.5.3.034001) (OpenAlex, 2026-03-19, abstract_only)
    - source: [3D Optoelectronics and Co-Packaged Optics: Innovations, Challenges, and Future Trends](https://doi.org/10.1109/jstqe.2025.3641790) (OpenAlex, 2025-12-08, abstract_only)
    - source: [3D optoelectronics and co-packaged optics: when solving the wrong problems stalls deployment](https://doi.org/10.48550/arxiv.2603.21313) (OpenAlex, 2026-03-22, abstract_only)
    - excerpt: "makes thermal management a critical bottleneck for CPO performance and reliability."
    - reasoning: Three independent reviews and one preprint name thermal management, yield, alignment and serviceability as open. The retrieved cooling studies are largely simulation-backed lab platforms. The 2026 preprint (src_57b1133fd7) argues that device-centric analyses underweight system trade-offs. It is a single, uncited preprint, so this is a caution, not a settled conclusion.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S3'], severity low:
  - **[C8]** *(ai_interpretation, confidence medium)* S3 concludes that CPO is 'not converging on a single architecture'. The cited abstracts list packaging techniques (2D/2.5D/3D, FOWLP, TSV/TGV) but do not say the field is divergent or that these routes compete rather than complement each other. The finding is also partly cited to src_926601ff5d, whose abstract does not list 2D/2.5D/3D or FOWLP.
    - source: [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) (OpenAlex, 2024-09-29, abstract_only)
    - source: [Heterogeneous Integration in Co-Packaged Optics](https://doi.org/10.1109/jetcas.2025.3590744) (OpenAlex, 2025-07-21, abstract_only)
    - reasoning: A list of covered topics in review abstracts does not show absence of convergence. The routes may serve different bandwidth tiers or product generations, and the abstracts give no market or standards evidence either way.

**Limitations:**
- Analysis uses titles and abstracts only. Full-text details such as test conditions, error bars and cost models were not seen.
- One paper (src_34b3ddf46b, Nature Electronics) has no abstract, so it contributes nothing to the findings.
- Most papers are reviews or perspectives that summarize other work, so findings are not fully independent.
- The retrieved set is small (12 papers) and skews toward thermal management, so other risk areas (security, supply chain, cost, laser reliability, competing architectures) are thinly covered.
- One key source (src_57b1133fd7) is an arXiv preprint and not peer reviewed.
- No papers directly compare CPO with NPO, pluggable or linear-drive optics on cost or power, so displacement risk is a gap in the evidence rather than a finding.
- Only titles, metadata and abstracts were reviewed. Full-paper methods, quantitative results and caveats were not read, so some of the problems flagged may be addressed in the full texts.
- Several retrieved items have no abstract (src_6e1e90b306, src_bff4d58588, src_34b3ddf46b) or only a slide-title list (src_89eb116049). They could not be used to test the findings.
- I did not challenge S8 and S9 because they are hedged and consistent with their abstracts, though both are advocacy or speculative in tone.
- No independent evidence on commercial deployment, cost, yield or field reliability was available, so I could not test those claims against external sources. Several challenges are therefore labelled ai_interpretation.

## Evidence: company filings and news
Status: ok. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: co-packaged optics, CPO, optical engine, silicon photonics, optical I/O
News headline search: "co-packaged optics" (GDELT)

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Micron Technology (MU) | 2 | 0 | large: 133.2B USD | +256.3% | 4.2% of revenue | 2 press release(s) read |
| NVIDIA (NVDA) | 2 | 0 | large: 26.9B USD | +61.4% | n/a |  |
| Advanced Micro Devices (AMD) | 2 | 1 | large: 34.6B USD | +34.3% | 23.4% of revenue |  |
| Intel (INTC) | 2 | 0 | large: 52.9B USD | -0.5% | 26.1% of revenue | 2 press release(s) read |
| Broadcom (AVGO) | 2 | 0 | large: 63.9B USD | +23.9% | 17.2% of revenue | 1 press release(s) read |
| Marvell Technology (MRVL) | 2 | 3 | mid: 8.2B USD | +42.1% | 25.3% of revenue | 2 press release(s) read |
| Qualcomm (QCOM) | 2 | 0 | large: 43.1B USD | -2.6% | 23.7% of revenue | 2 press release(s) read |
| Taiwan Semiconductor Manufacturing (TSM) | 1 | 0 | None: 2894.3B TWD | +33.9% | 7.1% of revenue |  |
| ASML Holding (ASML) | 1 | 0 | None: 32.7B EUR | +15.6% | 14.4% of revenue |  |
| Applied Materials (AMAT) | 2 | 0 | large: 28.4B USD | +4.4% | 12.6% of revenue | 2 press release(s) read |
| Lam Research (LRCX) | 2 | 0 | large: 23.2B USD | +26.0% | 10.2% of revenue |  |
| KLA (KLAC) | 2 | 0 | large: 13.6B USD | +11.7% | 11.3% of revenue | 2 press release(s) read |
| Formfactor Inc (FORM) | 1 | 1 | small: 0.8B USD | +2.8% | 14.7% of revenue | discovered by full-text search |
| Coherent Corp. (COHR) | 1 | 1 | mid: 7.1B USD | +22.5% | 10.2% of revenue | discovered by full-text search |
| Veeco Instruments Inc (VECO) | 1 | 1 | small: 0.5B USD | +45.8% | n/a | discovered by full-text search |
| Jabil Inc (JBL) | 1 | 0 | large: 36.0B USD | +20.6% | 0.1% of revenue | discovered by full-text search |
| Lumentum Holdings Inc. (LITE) | 1 | 1 | mid: 3.0B USD | +83.2% | 11.8% of revenue | discovered by full-text search |
| ASE Technology Holding Co., Ltd. (ASX) | 1 | 1 | None: 645.4B TWD | +8.4% | 5.1% of revenue | discovered by full-text search |
| Aeluma, Inc. (ALMU) | 1 | 1 | micro: 0.0B USD | -4.4% | 104.6% of revenue | discovered by full-text search |
| Amkor Technology, Inc. (AMKR) | 1 | 1 | mid: 6.7B USD | +6.2% | 2.5% of revenue | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Marvell offers co-packaged optics (CPO) as part of its custom silicon and interconnect product portfolio, built on silicon photonics technology that integrates hundreds of components into a single device.
  - source: [Marvell Technology, Inc. Form 10-K (FORM 10-K), filed 2026-03-11](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm) (SEC EDGAR, 2026-03-11, excerpt_only)
  - excerpt: "Our CPO solutions leverage advanced silicon photonics technology, integrating hundreds of components such as waveguides, modulators, photodetectors, modulator drivers, trans-impedance amplifiers, microcontrollers, and various passive components into a single, unified device."
  - reasoning: Marvell's 10-K directly describes CPO in both its custom ASIC platform and its interconnect product line, making it the most detailed filing evidence in this set.
- **[M2]** *(verified_fact, confidence high)* AMD made strategic acquisitions during the year to support and develop photonics and co-packaged optics solutions for next-generation AI systems.
  - source: [Advanced Micro Devices Inc Form 10-K, filed 2026-02-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm) (SEC EDGAR, 2026-02-04, excerpt_only)
  - excerpt: "to scale our ability to support and develop a variety of photonics and co-packaged optics solutions across next-gen AI systems"
  - reasoning: AMD's 10-K frames CPO as a capability gained via acquisitions for AI systems, but the excerpt does not name specific CPO products or customers.
  - citation check: company name(s) not found in the cited sources removed: AMD
- **[M3]** *(verified_fact, confidence high)* Amkor positions its CPO and silicon photonics wafer-level packaging as a way to participate in datacenter and AI scaling, reducing power consumption and improving performance.
  - source: [Amkor Technology, Inc. Form 10-K, filed 2026-02-20](https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm) (SEC EDGAR, 2026-02-20, excerpt_only)
  - excerpt: "SiPh and CPO allow for the integration of fiberoptic interconnects both within a package and within the server architecture to reduce power consumption, heat generation and improve performance."
  - reasoning: Amkor's 10-K describes CPO as an existing wafer-level package offering co-developed with semiconductor companies and OEMs, indicating packaging-side commercial activity.
- **[M4]** *(verified_fact, confidence high)* ASE Technology Holding lists Co-Packaged Optics processing capabilities among its advanced packaging services and manufactures high-data-rate optoelectronic components and optical engines.
  - source: [ASE Technology Holding Co., Ltd. Form 20-F, filed 2026-04-01](https://www.sec.gov/Archives/edgar/data/1122411/000119312526135585/d50802d20f.htm) (SEC EDGAR, 2026-04-01, excerpt_only)
  - excerpt: "Manufacture, sales as well as research and development of high-data rate optoelectronic components and optical engines."
  - reasoning: ASE's 20-F names CPO among its packaging technology suite (CoWoS/CoPoS/CoWoP/CPO/3D IC) and describes CPO/silicon photonics as leveraging the CMOS ecosystem for low-cost photonic ICs.
- **[M5]** *(verified_fact, confidence high)* Coherent sells co-packaged optics products into the datacenter and communications market within one of its reporting segments.
  - source: [Coherent Corp. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/820318/000082031826000023/iivi-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - excerpt: "This segment sells primarily into the datacenter and communications market, including transceivers, co-packaged optics, optical circuit switches, systems, subsystems, modules, components, optics, and semiconductor devices."
  - reasoning: Coherent's 10-Q lists CPO among products it sells, indicating commercial product activity, though the excerpt gives no revenue or customer detail.
- **[M6]** *(verified_fact, confidence medium)* FormFactor's Keystone Photonics unit provides optical probing technology used to test silicon photonics, co-packaged optics, and near-packaged optics devices, indicating test-equipment demand tied to CPO.
  - source: [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - excerpt: "Keystone Photonics provides optical probing technology used in the testing of silicon photonics (“SiPh”), co‑packaged optics (“CPO”), and near-packaged optics (“NPO”) devices."
  - reasoning: A single 10-Q excerpt; it shows FormFactor's role is test equipment for CPO devices, not CPO products themselves.
- **[M7]** *(verified_fact, confidence medium)* Lumentum delivers customized laser and packaging solutions enabling co-packaged optics and integrated photonics assemblies.
  - source: [Lumentum Holdings Inc. Form 10-K, filed 2026-08-17](https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm) (SEC EDGAR, 2026-08-17, excerpt_only)
  - excerpt: "we deliver customized solutions tailored to specific customer needs, such as high-power laser sources, compact laser arrays, and advanced packaging schemes enabling co-packaged optics and integrated photonics assemblies."
  - reasoning: Lumentum's 10-K positions it as a component/packaging enabler for CPO; no customers or volumes are named in the excerpt.
- **[M8]** *(verified_fact, confidence medium)* Veeco sees hyperscalers advancing toward near-package and co-packaged optics over the longer term, driving demand for InP epitaxy and laser-facet coating equipment.
  - source: [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - excerpt: "Hyperscalers and their suppliers are advancing higher-speed pluggable transceivers and, over the longer term, near-package and co-packaged optics."
  - reasoning: Veeco's 10-Q frames CPO as a longer-term equipment demand driver; its Spector systems address laser-facet coating in silicon photonics. Note Veeco's fundamentals shown are from fiscal 2017, so size context is stale.
- **[M9]** *(ai_interpretation, confidence medium)* Marvell's November 2026 investor materials describe pre-validated optical engines, external lasers (ELSFP), and optical I/O engines for custom XPUs, suggesting a push toward optical I/O for AI connectivity.
  - source: [Marvell Technology, Inc. 8-K press release (exhibit d81187dex992.htm), filed 2026-11-02](https://www.sec.gov/Archives/edgar/data/1835632/000119312526442714/d81187dex992.htm) (SEC EDGAR, 2026-11-02, excerpt_only)
  - source: [Marvell Technology, Inc. 8-K press release (exhibit d81187dex991.htm), filed 2026-11-02](https://www.sec.gov/Archives/edgar/data/1835632/000119312526442714/d81187dex991.htm) (SEC EDGAR, 2026-11-02, excerpt_only)
  - reasoning: The 8-K exhibit slides (fragmented text) mention 'Pre-validated optical engines + highly reliable lasers enable next-gen AI connectivity' and 'Extreme co-design accelerates Optical I/O engine', alongside a portfolio spanning silicon photonics, advanced packaging and compound semiconductors. The slide text is fragmentary, so the interpretation of a concrete product roadmap is inferred rather than fully stated.
- **[M10]** *(unverified_claim, confidence low)* Aeluma's 10-K mentions silicon photonics companies and integrated light source providers as competitors or demand drivers, but the excerpts do not establish a concrete co-packaged optics role.
  - source: [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) (SEC EDGAR, 2026-09-16, excerpt_only)
  - reasoning: The two short excerpts only reference silicon photonics in competitive and demand contexts; Aeluma's actual CPO-related role cannot be determined from this evidence.

**Limitations:**
- Only excerpt passages from filings were available, not full reports; companies whose filings did not mention the keywords (NVIDIA, Broadcom, Intel, TSMC, Micron, equipment makers) cannot be concluded to be absent from the co-packaged optics market.
- No news headlines were included in this source set, so no market-event or customer-adoption signals beyond filings could be assessed.
- No customer names, shipment volumes, revenue figures, or qualification milestones for CPO products appear in any excerpt, limiting assessment of commercial readiness.
- The Marvell 8-K exhibit text is fragmented slide content and may be misinterpreted; it is marked confidential investor material, not a product announcement.
- Veeco's fundamentals are from fiscal 2017, so size context for that company is outdated; Aeluma is a micro-cap and its mention may be peripheral.
- Jabil was discovered by full-text search but its retrieved filing showed no keyword-matching excerpt in the provided sources, so no finding could be made for it.

## Social signals from X
Status: ok. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 30 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (37): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie
Posts read: 3 (estimated X cost $0.015)

- **[X1]** *(unverified_claim, confidence low)* TrendForce says that heading into 2027, CPO development will focus on platform qualification, faster testing, and passive alignment.
  - source: [@trendforce: Heading into 2027, #TrendForce flags what to watch across key tech segments: Foundry: Reve…](https://x.com/trendforce/status/2118320138286157953) (X API, 2026-11-05, full_text)
  - excerpt: "CPO: Platform qualification, faster testing, and passive alignment in"
  - reasoning: Press account's outlook post; the linked article was not read, and the tweet is truncated, so details are unavailable.
- **[X2]** *(unverified_claim, confidence low)* Counterpoint Research reports that Marvell is buying Lumentum in a deal it frames as an implied $115 billion transaction, positioning it around the 'AI laser wall' and the optics value chain.
  - source: [@CounterPointTR: 𝗠𝗮𝗿𝘃𝗲𝗹𝗹 𝗕𝘂𝘆𝘀 𝗟𝘂𝗺𝗲𝗻𝘁𝘂𝗺 𝘁𝗼 𝗖𝗹𝗶𝗺𝗯 𝘁𝗵𝗲 𝗔𝗜 𝗟𝗮𝘀𝗲𝗿 𝗪𝗮𝗹𝗹: 𝗪𝗵𝗮𝘁 𝘁𝗵𝗲 $𝟭𝟭𝟱 𝗕𝗶𝗹𝗹𝗶𝗼𝗻 𝗗𝗲𝗮𝗹 𝗠𝗲𝗮𝗻𝘀 𝗳𝗼𝗿 𝗢𝗽𝘁…](https://x.com/CounterPointTR/status/2117499775654482067) (X API, 2026-11-03, full_text)
  - reasoning: Press summary of an M&A deal; the full article was not read and the tweet is truncated, so deal terms beyond the headline cannot be confirmed from this post.
  - citation check: company name(s) not found in the cited posts removed: Marvell, Lumentum
- **[X3]** *(unverified_claim, confidence low)* EE Times published an explainer titled 'Five Things You Didn't Know About Co-Packaged Optics', indicating continued specialist-press attention to CPO fundamentals.
  - source: [@eetimes: Five Things You Didn’t Know About Co-Packaged Optics https://t.co/9b7vcYeVlp https://t.co/…](https://x.com/eetimes/status/2117617868787384756) (X API, 2026-11-03, full_text)
  - reasoning: Headline only; the article content was not read, so no substantive claims can be drawn from it.

**Limitations:**
- Only 3 posts in the 7-day window from a fixed list of 37 accounts; no company accounts posted about CPO this week.
- All posts are press/analyst summaries; linked articles were not read, so underlying claims could not be verified.
- Tweet texts are truncated, cutting off key details (e.g., TrendForce's CPO outlook and Counterpoint's deal analysis).
- Low engagement counts indicate limited attention, not accuracy or inaccuracy.
- Quiet week on X is not evidence of absence of CPO activity by the companies tracked.

## Evidence: patents
Status: partial. Worldwide patent publications from Google Patents (SerpApi) matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 23 distinct company names from 0 patent publications, 10 company-affiliated papers and 10 SEC filers; 12 matched to the SEC ticker file (9 outside the configured list), 10 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Formfactor Inc (FORM) | 0 | 0 | 4 | small: 0.78B USD | +2.8% | 14.7% | **45** |
| Coherent Corp. (COHR) | 0 | 0 | 3 | mid: 7.12B USD | +22.5% | 10.2% | **45** |
| Veeco Instruments Inc (VECO) | 0 | 0 | 3 | small: 0.48B USD | +45.8% | n/a | **45** |
| Lumentum Holdings Inc. (LITE) | 0 | 0 | 2 | mid: 3.01B USD | +83.2% | 11.8% | **45** |
| Aeluma, Inc. (ALMU) | 0 | 0 | 1 | micro: 0.00B USD | -4.4% | 104.6% | **40** |
| Jabil Inc (JBL) | 0 | 0 | 2 | large: 35.95B USD | +20.6% | 0.1% | **30** |
| Amkor Technology, Inc. (AMKR) | 0 | 0 | 1 | mid: 6.71B USD | +6.2% | 2.5% | **30** |
| ASE Technology Holding Co., Ltd. (ASX) | 0 | 0 | 1 | n/a: 645.39B TWD | +8.4% | 5.1% | **25** |
| Canon Inc (CAJPY) | 0 | 1 | 0 | n/a: 4031.41B JPY | +14.7% | 7.6% | **18** |

- Formfactor Inc: 4 SEC report(s) mentioning the topic (+20); small company by revenue (+15): more room to grow, more risk; revenue growth +3% (+5); R&D 15% of revenue (+5)
- Coherent Corp.: 3 SEC report(s) mentioning the topic (+20); mid-size company by revenue (+10); revenue growth +22% (+10); R&D 10% of revenue (+5)
- Veeco Instruments Inc: 3 SEC report(s) mentioning the topic (+20); small company by revenue (+15): more room to grow, more risk; revenue growth +46% (+10)
- Lumentum Holdings Inc.: 2 SEC report(s) mentioning the topic (+20); mid-size company by revenue (+10); revenue growth +83% (+10); R&D 12% of revenue (+5)
- Aeluma, Inc.: 1 SEC report(s) mentioning the topic (+15); micro company by revenue (+15): more room to grow, more risk; revenue growth -4% (+0); R&D 105% of revenue (+10)
- Jabil Inc: 2 SEC report(s) mentioning the topic (+20); large company by revenue (+0): the topic is unlikely to move the whole business; revenue growth +21% (+10)

**Configured incumbents that also showed up:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Marvell Technology (MRVL) | 0 | 0 | 3 | mid: 8.19B USD | +42.1% | 25.3% | **50** |
| Advanced Micro Devices (AMD) | 0 | 0 | 1 | large: 34.64B USD | +34.3% | 23.4% | **35** |
| Broadcom Inc. (AVGO) | 0 | 1 | 0 | large: 63.89B USD | +23.9% | 17.2% | **28** |

**Found but not in the SEC ticker file (private, foreign, or name not matched):** Corning (United States) (0P/2A/0F), Hisense (China) (0P/1A/0F), Huawei Technologies (China) (0P/1A/0F), Corning (South Korea) (0P/1A/0F), MediaTek (Taiwan) (0P/1A/0F), Ericsson (Sweden) (0P/1A/0F), DuPont (United States) (0P/1A/0F), Lam Research (United States) (0P/1A/0F), Furukawa Electric (Japan) (0P/1A/0F), Furukawa Co., Ltd. (Japan) (0P/1A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* Formfactor Inc (FORM) is active on co-packaged optics: 4 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.78B USD (small by revenue), growth +2.8%, R&D 14.7% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Coherent Corp. (COHR) is active on co-packaged optics: 3 of its SEC report(s) mention the topic; fiscal 2026 revenue 7.12B USD (mid by revenue), growth +22.5%, R&D 10.2% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Coherent Corp. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/820318/000082031826000023/iivi-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Veeco Instruments Inc (VECO) is active on co-packaged optics: 3 of its SEC report(s) mention the topic; fiscal 2017 revenue 0.48B USD (small by revenue), growth +45.8%. Next-runner score 45/100 (heuristic).
  - source: [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Lumentum Holdings Inc. (LITE) is active on co-packaged optics: 2 of its SEC report(s) mention the topic; fiscal 2025 revenue 3.01B USD (mid by revenue), growth +83.2%, R&D 11.8% of revenue. Next-runner score 45/100 (heuristic).
  - source: [Lumentum Holdings Inc. Form 10-K, filed 2026-08-17](https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm) (SEC EDGAR, 2026-08-17, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K5]** *(ai_interpretation, confidence low)* Aeluma, Inc. (ALMU) is active on co-packaged optics: 1 of its SEC report(s) mention the topic; fiscal 2026 revenue 0.00B USD (micro by revenue), growth -4.4%, R&D 104.6% of revenue. Next-runner score 40/100 (heuristic).
  - source: [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) (SEC EDGAR, 2026-09-16, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K6]** *(ai_interpretation, confidence low)* Jabil Inc (JBL) is active on co-packaged optics: 2 of its SEC report(s) mention the topic; fiscal 2026 revenue 35.95B USD (large by revenue), growth +20.6%, R&D 0.1% of revenue. Next-runner score 30/100 (heuristic).
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [@trendforce: Heading into 2027, #TrendForce flags what to watch across key tech segments: Foundry: Reve…](https://x.com/trendforce/status/2118320138286157953) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_859b4e09a8
- [Coherent Corp. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/820318/000082031826000023/iivi-20260930.htm) | SEC EDGAR | 2026-11-04 | retrieved 2026-11-09 | excerpt_only | id src_eb084f7245
- [Veeco Instruments Inc Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/103145/000110465926122721/veco-20260930x10q.htm) | SEC EDGAR | 2026-11-04 | retrieved 2026-11-09 | excerpt_only | id src_10ad34c466
- [Formfactor Inc Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1039399/000103939926000043/form-20260926.htm) | SEC EDGAR | 2026-11-03 | retrieved 2026-11-09 | excerpt_only | id src_635ef44763
- [@eetimes: Five Things You Didn’t Know About Co-Packaged Optics https://t.co/9b7vcYeVlp https://t.co/…](https://x.com/eetimes/status/2117617868787384756) | X API | 2026-11-03 | retrieved 2026-11-09 | full_text | id src_3b0c8869a4
- [@CounterPointTR: 𝗠𝗮𝗿𝘃𝗲𝗹𝗹 𝗕𝘂𝘆𝘀 𝗟𝘂𝗺𝗲𝗻𝘁𝘂𝗺 𝘁𝗼 𝗖𝗹𝗶𝗺𝗯 𝘁𝗵𝗲 𝗔𝗜 𝗟𝗮𝘀𝗲𝗿 𝗪𝗮𝗹𝗹: 𝗪𝗵𝗮𝘁 𝘁𝗵𝗲 $𝟭𝟭𝟱 𝗕𝗶𝗹𝗹𝗶𝗼𝗻 𝗗𝗲𝗮𝗹 𝗠𝗲𝗮𝗻𝘀 𝗳𝗼𝗿 𝗢𝗽𝘁…](https://x.com/CounterPointTR/status/2117499775654482067) | X API | 2026-11-03 | retrieved 2026-11-09 | full_text | id src_5ebae369cf
- [Marvell Technology, Inc. 8-K press release (exhibit d81187dex991.htm), filed 2026-11-02](https://www.sec.gov/Archives/edgar/data/1835632/000119312526442714/d81187dex991.htm) | SEC EDGAR | 2026-11-02 | retrieved 2026-11-09 | excerpt_only | id src_3f73440f3f
- [Marvell Technology, Inc. 8-K press release (exhibit d81187dex992.htm), filed 2026-11-02](https://www.sec.gov/Archives/edgar/data/1835632/000119312526442714/d81187dex992.htm) | SEC EDGAR | 2026-11-02 | retrieved 2026-11-09 | excerpt_only | id src_c6445eaee5
- [Aeluma, Inc. Form 10-K, filed 2026-09-16](https://www.sec.gov/Archives/edgar/data/1828805/000121390026100584/ea0305364-10k_aeluma.htm) | SEC EDGAR | 2026-09-16 | retrieved 2026-11-09 | excerpt_only | id src_f574b69c51
- [Silicon Photonics for Co‐Packaged Optics: A Review of Core PIC Components and Industry Strategies](https://doi.org/10.1002/admt.71266) | OpenAlex | 2026-08-20 | retrieved 2026-11-09 | abstract_only | id src_2ce7a34363
- [Co-packaged optics for high-performance computing and artificial intelligence](https://doi.org/10.1038/s41928-026-01681-6) | OpenAlex | 2026-08-19 | retrieved 2026-11-09 | metadata_only | id src_34b3ddf46b
- [Lumentum Holdings Inc. Form 10-K, filed 2026-08-17](https://www.sec.gov/Archives/edgar/data/1633978/000162828026057358/lite-20260627.htm) | SEC EDGAR | 2026-08-17 | retrieved 2026-11-09 | excerpt_only | id src_063f2955ba
- [Photonic Interconnects & Co-Packaged Optics](https://doi.org/10.4071/001c.167017) | OpenAlex | 2026-08-12 | retrieved 2026-11-09 | abstract_only | id src_89eb116049
- [A study of lithography process comparison for Co-Package Optics](https://doi.org/10.1109/ectc51846.2026.00371) | OpenAlex | 2026-05-26 | retrieved 2026-11-09 | abstract_only | id src_b284d4ae0c
- [ASE Technology Holding Co., Ltd. Form 20-F, filed 2026-04-01](https://www.sec.gov/Archives/edgar/data/1122411/000119312526135585/d50802d20f.htm) | SEC EDGAR | 2026-04-01 | retrieved 2026-11-09 | excerpt_only | id src_32cc4a635b
- [3D optoelectronics and co-packaged optics: when solving the wrong problems stalls deployment](https://doi.org/10.48550/arxiv.2603.21313) | OpenAlex | 2026-03-22 | retrieved 2026-11-09 | abstract_only | id src_57b1133fd7
- [Thermal management in copackaged optics: from device assembly to system operation](https://doi.org/10.1117/1.apn.5.3.034001) | OpenAlex | 2026-03-19 | retrieved 2026-11-09 | abstract_only | id src_415abc0f36
- [Marvell Technology, Inc. Form 10-K (FORM 10-K), filed 2026-03-11](https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm) | SEC EDGAR | 2026-03-11 | retrieved 2026-11-09 | excerpt_only | id src_ce00447bcf
- [Amkor Technology, Inc. Form 10-K, filed 2026-02-20](https://www.sec.gov/Archives/edgar/data/1047127/000104712726000014/amkr-20251231.htm) | SEC EDGAR | 2026-02-20 | retrieved 2026-11-09 | excerpt_only | id src_b1aef12fc9
- [Advanced Micro Devices Inc Form 10-K, filed 2026-02-04](https://www.sec.gov/Archives/edgar/data/2488/000000248826000018/amd-20251227.htm) | SEC EDGAR | 2026-02-04 | retrieved 2026-11-09 | excerpt_only | id src_ba0fa71be5
- [3D Heterogeneous Integration of Back-Emitting VCSEL Arrays via Flip-Chip Bonding for Co-Packaged Optics Systems](https://doi.org/10.1109/jstqe.2025.3650463) | OpenAlex | 2026-01-05 | retrieved 2026-11-09 | abstract_only | id src_c246b858cb
- [Co-packaged Optics - an encyclopedia article](https://doi.org/10.61835/9m3) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | metadata_only | id src_bff4d58588
- [Unlocking the Potential of Co-Packaged Optics in AI and HPC: Opportunities and Challenges](https://doi.org/10.1109/mcom.001.2500504) | OpenAlex | 2025-12-17 | retrieved 2026-11-09 | abstract_only | id src_a072730865
- [3D Optoelectronics and Co-Packaged Optics: Innovations, Challenges, and Future Trends](https://doi.org/10.1109/jstqe.2025.3641790) | OpenAlex | 2025-12-08 | retrieved 2026-11-09 | abstract_only | id src_7ae86c3396
- [Heterogeneous Integration Technology Drives the Evolution of Co-Packaged Optics](https://doi.org/10.3390/mi16091037) | OpenAlex | 2025-09-10 | retrieved 2026-11-09 | abstract_only | id src_711ed43b25
- [Heterogeneous Integration in Co-Packaged Optics](https://doi.org/10.1109/jetcas.2025.3590744) | OpenAlex | 2025-07-21 | retrieved 2026-11-09 | abstract_only | id src_926601ff5d
- [Simulation and experimental investigation of liquid-cooling thermal management for high-bandwidth co-packaged optics](https://doi.org/10.1007/s12200-025-00156-4) | OpenAlex | 2025-05-14 | retrieved 2026-11-09 | abstract_only | id src_e464945272
- [Reflowable Ceramics Multifiber Ferrule for Co-Packaged Optics](https://doi.org/10.23919/icep-iaac64884.2025.11002876) | OpenAlex | 2025-04-15 | retrieved 2026-11-09 | abstract_only | id src_31ad129a0e
- [Progress in Research on Co-Packaged Optics](https://doi.org/10.3390/mi15101211) | OpenAlex | 2024-09-29 | retrieved 2026-11-09 | abstract_only | id src_e674fc828f
- [Liquid-Cooled Heat Dissipation Technology for Co-Packaged Optics over 12.8 Tbps](https://doi.org/10.1109/icept63120.2024.10668507) | OpenAlex | 2024-08-07 | retrieved 2026-11-09 | abstract_only | id src_56c4a4a88a
- [Polymer Waveguides for Co-Packaged Optics](https://doi.org/10.1109/ectc51529.2024.00278) | OpenAlex | 2024-05-28 | retrieved 2026-11-09 | abstract_only | id src_fd8baf4efb
- [High Density Integration of Silicon Photonic Chiplets for 51.2T Co-packaged Optics](https://doi.org/10.1109/ectc51529.2024.00022) | OpenAlex | 2024-05-28 | retrieved 2026-11-09 | abstract_only | id src_056c3f48da
- [Co-packaged Optics](https://doi.org/10.1007/978-981-97-2140-5_6) | OpenAlex | 2024-01-01 | retrieved 2026-11-09 | metadata_only | id src_6e1e90b306
- [A record energy efficient QSFP ELS for co-packaged optics](https://doi.org/10.1049/icp.2023.2364) | OpenAlex | 2023-11-13 | retrieved 2026-11-09 | abstract_only | id src_df64c9fa65
- [Co-Packaged Optics Opportunities in Radio-Access Networks](https://doi.org/10.23919/etr.2023.10438941) | OpenAlex | 2023-11-01 | retrieved 2026-11-09 | abstract_only | id src_7538c6b701
- [Perspectives for Co-Packaged Optics in Radio Access Networks](https://doi.org/10.1109/icton59386.2023.10207522) | OpenAlex | 2023-07-02 | retrieved 2026-11-09 | abstract_only | id src_d37647044d
- [Glass Substrate for Co-Packaged Optics](https://doi.org/10.4071/001c.74749) | OpenAlex | 2023-05-01 | retrieved 2026-11-09 | abstract_only | id src_be6936e374
- [Co-packaged optics (CPO): status, challenges, and solutions](https://doi.org/10.1007/s12200-022-00055-y) | OpenAlex | 2023-03-20 | retrieved 2026-11-09 | abstract_only | id src_8bc0d86153
- [Glass Platform for Co-Packaged Optics](https://doi.org/10.1109/jstqe.2023.3247245) | OpenAlex | 2023-01-01 | retrieved 2026-11-09 | abstract_only | id src_a10849db6e

## Gaps, limitations and errors
- Missing data: Patent evidence: the Patent agent did not run, so there is no patent-momentum rating and no assignee-level evidence.
- Missing data: Price & timing evidence: no T findings were provided, so how far related stocks have moved and near-term timing risk cannot be assessed.
- Missing data: Customer adoption evidence: no finding names a customer or design win for CPO products.
- Missing data: Quantitative performance and reliability data: abstracts give few comparative numbers, and no long-term reliability, thermal-cycling, field or serviceability data [R2][R6].
- Missing data: Manufacturing yield and cost data: yield, alignment, and cost/economic viability are described as goals or barriers, not demonstrated results [R3][R6].
- Missing data: Independent confirmation of glass-substrate results: the two glass papers appear to describe the same process stream, and fibre-connector loss is omitted [C2].
- Missing data: No company evidence for the thermal-management theme specifically; no vendor is named in the cooling findings [R1][R2].
- Missing data: File-level financial context for some Scout names is incomplete (e.g., Jabil's CPO role is not established in the cited excerpt) [K6].
- Limitation: This assessment uses only the supplied findings; it is not based on reading the underlying papers, filings or articles in full.
- Limitation: Several Market findings reflect companies describing their own products or roadmaps; such statements are not independent proof of capability or adoption.
- Limitation: X findings are social signals from the last 7 days and are treated as unverified claims, not facts [X1][X2][X3].
- Limitation: Research volume is high but research activity is not commercial success; the OpenAlex count is the exact phrase only, excludes synonyms/abbreviations and is not normalised for overall publishing growth.
- Limitation: Many Science findings carry only medium or low confidence and are contradicted or weakened by Risk challenges [C1]-[C8], so scenario confidences are mostly low.
- Limitation: Company Scout next-runner scores are transparent heuristics, not predictions of returns; several flagged companies are small or micro-cap with limited disclosure and higher risk.
- Limitation: No patent and no price/timing evidence were available, which materially limits the patent-momentum and risk_adjustment views and the near-term horizon.
- Limitation: No buy/sell/hold recommendation, price target or expected return is or should be inferred from this assessment; horizons are stated only in terms of what the cited evidence does and does not support.
- Chief review gap: No quantitative performance data (pJ/bit, bandwidth density, cost-per-bit) comparing CPO to pluggable or near-packaged optics; R6 explicitly notes benefits are described only qualitatively
- Chief review gap: No technical comparison of CPO versus LPO (linear pluggable optics) or NPO (near-packaged optics) as competing approaches to the same bandwidth/energy problem
- Chief review gap: No evidence on production deployment status or timeline to volume shipping from any paper source
- Chief review gap: Patent agent was not run, so IP landscape and potential patent barriers are unassessed (not fixable by paper search)
- Chief review gap: Market evidence is strong on who is involved but thin on revenue scale or design-win status for CPO specifically
- Chief review gap: No quantitative cost-per-bit or total-cost-of-ownership comparison between CPO, near-packaged optics (NPO), and pluggable transceivers; R6 explicitly notes displacement risk cannot be assessed
- Chief review gap: No long-term reliability, thermal-cycling, or field-deployment data; all thermal and yield evidence is lab-scale or simulation-backed (R2, R3, R5)
- Chief review gap: Patent agent was not run, so IP landscape, freedom-to-operate, and competitive moat analysis are absent
- Chief review gap: Manufacturing yield figures are qualitative; no wafer-level or module-level yield numbers are reported in any finding
- Chief review gap: NPO vs CPO trade-off is mentioned but unresolved in the literature; no paper provides a head-to-head outcome
- Reference checks changed 1 statement(s) in the assessment (see notes in italics above).
- ERROR [science/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [science/arXiv]: network error (ReadTimeout: The read operation timed out)
- ERROR [science/arXiv]: network error (ReadTimeout: The read operation timed out)
- ERROR [science/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [science/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [risk/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [risk/arXiv]: network error (ReadTimeout: The read operation timed out)
- ERROR [risk/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [risk/arXiv]: rate limited by arXiv (limit: 1 request / 3 s)
- ERROR [patent/Google Patents (SerpApi)]: counts: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [patent/Google Patents (SerpApi)]: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 3 | 10070 | 3702 | 0.00540 |
| x | z-ai/glm-5.3-flash | 1 | 2006 | 487 | 0.00040 |
| market | z-ai/glm-5.3 | 1 | 5811 | 1995 | 0.02193 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 21634 | 10856 | 0.15183 |
| science | deepseek/deepseek-v4.1-flash | 2 | 8569 | 8410 | 0.01135 |
| investment | deepseek/deepseek-v4.1-flash | 1 | 8377 | 8091 | 0.01222 |
| x (data) | X API pay-per-use | 2 | 0 | 0 | 0.01500 |

Total estimated cost: $0.21813 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
