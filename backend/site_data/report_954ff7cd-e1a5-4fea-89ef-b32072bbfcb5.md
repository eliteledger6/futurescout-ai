# FUTURESCOUT AI research report: vision-language-action model

Generated: 2026-11-09 08:06 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, investment
- Agents NOT run in this version: patent, market, x. Conclusions therefore have no patent, company, customer, manufacturing or supply-chain, social-media evidence.

## Verdict (forecast, computed from the report)
**Too little evidence to judge yet**, confidence low.
Qualifiers: high risk flagged by the Risk agent; research is running well ahead of commercial reality; low confidence (30%): thin evidence or high risk.

These are computer programs that try to let a machine see a scene, understand a spoken or written instruction, and then physically do the task. The research is exploding — hundreds of new papers a year — and there are impressive demonstrations, but the studies also show the machines often fail when the situation…

Why:
- Research Momentum rated 5/5: Code-computed OpenAlex counts for the exact phrase rise from 22 (2024) to 259 (2025), a 1077% year-on-year jump, and the current partial year continues rising (149 in the comparable 2025 window to 981 in 2026).
- Technical Feasibility rated 2/5: Core mechanisms are demonstrated in research: open 7B models beating larger closed models on multi-task manipulation (S1), tokenization unlocking high-frequency dexterous tasks (S2), and co-training for open-world tasks (S4).
- Papers 2024→2025: 22→259 (+1077%)
- So far in 2026 (to 10-10): 981 papers vs 149 by the same date in 2025 (+558%, rising)

Watch out for:
- Generalization may be much narrower than headlines suggest.
- Reliability fixes require extra data, compute or rollout budget, which conflicts with latency requirements (R4, R5, R8).
- Cited efficiency evidence is partly mismatched to its claim, so the efficiency narrative currently rests on fewer sources than it appears (C3).
- Reliability techniques such as test-time compute conflict directly with latency goals (R3, R5).

What would change this view:
- Stronger if: Independent (non-author) evaluations on real robots that report task success, not offline action error or simulation leaderboards, would materially strengthen the case currently resting on self-reported results (C2, C4).
- Weaker if: Independent real-robot evaluations showing that success rates do not survive scene changes or difficulty variation would undercut the capability case (R1, R2).
- Stronger if: Independent reproduction of small-model training and inference claims on non-author hardware, with measured latency and success (C3, S3).
- Weaker if: Independent measurements showing small VLAs cannot reach usable success rates at consumer-device latency would invalidate this theme (S3, R5, C3).

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
The evidence for vision-language-action (VLA) models is almost entirely academic: research output using the exact phrase jumped from 22 works in 2024 to 259 in 2025 and is still accelerating in 2026 (149 to 981 year-to-date), so research momentum is very strong (research-activity metrics). The science findings show real technical progress — open 7B models can beat larger closed models on multi-task manipulation (S1), action tokenization matters a lot for dexterous high-frequency tasks (S2), small single-GPU models are appearing (S3), and co-training across heterogeneous data is the main route to open-world generalization (S4). But the risk findings show that state-of-the-art VLAs often memorize rather than generalize, neglect safety constraints and produce rankings that flip with difficulty (R2), that instruction-action binding fails when scenes change (R1), and that single-attempt reliability is far below what a model's output distribution contains (R3, R4). Deployment claims are explicitly described as unproven at scale with reliability and speed still open (R7), and the strongest positive claims are weakened by challenges C1-C5 (self-reported results, confounded comparisons, over-stated convergence). No patent, market, X, price or Company Scout findings were supplied, so nothing here establishes customers, revenue, supply chain or competitive position. The main uncertainty is whether the gap between benchmark/pilot capability and dependable real-world manipulation can be closed, and at what data and compute cost (R8).

## Technology Opportunity Score
**Not reportable.** Indicative value 53.3 / 100 uses only 45% of the scoring weight; do not compare it with other technologies.

Risk: rating 4/5 does not change the score; it multiplies confidence by 0.6.

Commercialization Gap (research momentum rating minus commercial readiness rating): +4


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S11 | Code-computed OpenAlex counts for the exact phrase rise from 22 (2024) to 259 (2025), a 1077% year-on-year jump, and the current partial year continues rising (149 in the comparable 2025 window to 981 in 2026). Momentum is still building, not fading. This measures publication volume only, not commercial value. |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 2 | S1, S2, S4, R1, R2, R3 | Core mechanisms are demonstrated in research: open 7B models beating larger closed models on multi-task manipulation (S1), tokenization unlocking high-frequency dexterous tasks (S2), and co-training for open-world tasks (S4). But feasibility for dependable use is not established: benchmarks report memorization rather than generalization (R2), instruction-action binding failures (R1), and single-attempt success far below sampled performance (R3). |
| Commercial Readiness | 15% | 1 | R7 | No market findings or filings were provided. The only readiness-relevant evidence is that real-world deployment claims remain unproven at scale, with the strongest deployment-oriented result reporting failure rates reduced rather than eliminated and reliability and speed described as open challenges (R7). This supports a very low readiness rating, not a positive one. |
| Customer Adoption | 10% | missing | none | no valid 0-5 rating given |
| Industry Investment | 10% | missing | none | no valid 0-5 rating given |
| Competitive Position | 10% | missing | none | no valid 0-5 rating given |
| Supply-Chain Readiness | 15% | missing | none | no valid 0-5 rating given |

Formula: score = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100 (risk does not reduce it). confidence = evidence confidence x (1 - 0.10 x risk rating), where evidence confidence combines evidence coverage, the confidence of the cited ratings and the share of verified facts. Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. Score and confidence are explainable heuristics, not a validated prediction of stock performance; confidence is not a probability of profit.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.
- Only 45% of the total weighting has cited evidence (minimum 50%). The number is indicative only and must not be compared with other technologies.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Generalist VLA policies for robot manipulation

Technologies: vision-language-action models, robot manipulation policies, action tokenization, co-training on heterogeneous robot and web data, VLM-to-policy transfer

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The papers point to rapid academic iteration rather than near-term deployment: small and open models are being released (S1, S3) and design patterns for discrete action tokens are forming (S5), but the benchmarks report memorization instead of generalization and unsafe behaviour (R2) and single-attempt success far below sampled performance (R3). No finding in this set addresses commercial availability, so the near-term view is research-led only. *(forecast)* [S1, S3, S5, R2, R3] | high |
| medium_1_3y | The plausible medium-term content of the evidence is pilot and first-customer style use where failures can be tolerated, because mitigations such as counterfactual training, test-time critics and environment staging exist but leave large residual failure rates and are mostly evaluated in simulation (R4). Adaptation is described as data- and compute-intensive (about 20,000 hours of real data and about 130 post-training episodes per task) (R8), and inference cost and low execution frequency are stated barriers to real-time use (R5). *(forecast)* [R4, R5, R8] | medium |
| long_3_5y | Nothing in the findings supports a long-horizon statement about broad deployment; the strongest deployment-oriented result still reports failure rates reduced rather than eliminated (R7), and open-world generalization is presented without success rates (S4, C1). Whether reliability, safety and latency are solved within this window is not addressed by any cited finding. *(forecast)* [R7, S4, C1] | low |

**Bull case:** Open, moderately sized models already beat much larger closed models on multi-task manipulation success (S1), tokenization choices unlock high-frequency dexterous tasks (S2), and co-training across multiple robots, web data and subtasks reportedly enables long-horizon dexterous tasks in previously unseen homes (S4). The field has matured enough to have a survey organizing components, low-level policies and high-level planners (S11), and alternative instruction channels such as gesture are being explored (S10), which broadens the design space. *(ai_interpretation)* [S1, S2, S4, S10, S11]

**Base case:** Capability is real but uneven: state-of-the-art VLAs memorize rather than generalize and neglect safety constraints (R2), high in-distribution success can break when a changed scene needs a different action (R1), and single-attempt reliability sits far below the capability latent in the output distribution, needing extra search or compute to close the gap (R3, R4). The named gap between upstream embodied reasoning and downstream policy learning (S8) is still an open research problem, and adaptation remains expensive (R8). *(ai_interpretation)* [R1, R2, R3, R4, R8, S8]

**Bear case:** The headline generalization claims may be narrower than presented: the cited abstract for the co-training result gives no success rates (C1), the open-versus-closed comparison is confounded and self-reported on the authors' own task suite (C2), and the claimed convergence on discrete action tokens is overstated because a competing diffusion paradigm is also cited and only shown to be matched (C4). Safety and interpretability are weak — a proposed failure predictor reaches only about 70% accuracy and physical actions can be irreversible (R6) — while test-time deliberation worsens the latency problem (R5), and deployment at scale remains unproven (R7). *(ai_interpretation)* [C1, C2, C4, R5, R6, R7]

**Catalysts:**
- Independent (non-author) evaluations on real robots that report task success, not offline action error or simulation leaderboards, would materially strengthen the case currently resting on self-reported results (C2, C4). *(ai_interpretation)* [C2, C4]
- Evidence that the mitigations for instruction-action binding and unsafe behaviour hold up outside simulation, with residual failure rates reported (R1, R4). *(ai_interpretation)* [R1, R4]
- Evidence that inference cost and execution frequency are compatible with real-time control, since deliberation-style add-ons currently worsen latency (R5). *(ai_interpretation)* [R5]

**Risks:**
- Generalization may be much narrower than headlines suggest; robustness scores can hide instruction-action binding failures (R1) and rankings reverse across difficulty levels (R2). *(ai_interpretation)* [R1, R2]
- Reliability fixes require extra data, compute or rollout budget, which conflicts with latency requirements (R4, R5, R8). *(ai_interpretation)* [R4, R5, R8]
- Safety and interpretability are unresolved for systems whose physical actions can cause irreversible harm, with weak failure-prediction accuracy (R6). *(ai_interpretation)* [R6]
- Deployment claims at scale are unproven and the strongest deployment-oriented result still reports non-eliminated failures (R7). *(ai_interpretation)* [R7]

**What would invalidate this thesis:**
- Independent real-robot evaluations showing that success rates do not survive scene changes or difficulty variation would undercut the capability case (R1, R2). *(ai_interpretation)* [R1, R2]
- Demonstrations that reliability gains require compute or data far beyond practical budgets, or that latency cannot be brought down, would invalidate the scaling path (R4, R5, R8). *(ai_interpretation)* [R4, R5, R8]
- Evidence that the co-training generalization result does not replicate outside the original authors' setting would remove the main bull pillar (S4, C1). *(ai_interpretation)* [S4, C1]

**Conflicting evidence:**
- C1: S4 presents broad open-world generalization as achieved, but the cited abstract gives no success rates or failure analysis, and other evidence shows policies of that class can fail when the required action changes. *(ai_interpretation)* [C1, S4, R1]
- C2: S1's claim that parameter scale is not the main driver is confounded — the abstract credits data diversity and new components — and it is a self-reported result on the authors' own 29-task suite. *(ai_interpretation)* [C2, S1]
- C4: S5's convergence claim is overstated — a cited paper treats diffusion VLAs as the main competing paradigm and reports only that discrete tokenization can match it, and headline gains are on simulation benchmarks. *(ai_interpretation)* [C4, S5]

**Companies named by cited evidence:**
- none (no company evidence in the cited findings)

### Efficient, small and edge-deployable VLA

Technologies: small VLA models, single-GPU training, consumer/CPU inference, asynchronous inference, action tokenization (DCT compression), token pruning and test-time compute scheduling

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The efficiency track is supported mainly by SmolVLA-style small community-trainable models with asynchronous inference (S3), but the same finding is weakened because ShowUI is a screenshot GUI-agent model and its abstract describes neither single-GPU training nor asynchronous inference (C3), and the 'comparable to 10x larger' claim is self-reported. Compression-based action tokenization is reported to unlock high-frequency dexterous tasks (S2). *(forecast)* [S2, S3, C3] | medium |
| medium_1_3y | Cost and speed are framed as open problems, not solved ones: inference cost and low execution frequency are stated barriers to real-time use, and deliberation-style add-ons such as test-time compute may worsen them (R5), while token pruning and scheduling are proposed as a response (R5). No finding quantifies achievable cost, throughput or hardware in a product context. *(forecast)* [R5] | medium |
| long_3_5y | The supplied findings say nothing that supports a long-horizon view on efficient VLA hardware, unit economics or deployment scale; this horizon is not covered by the evidence. *(forecast)* [R5] | low |

**Bull case:** If small models can be trained on a single GPU and run consumer or CPU inference with perception and action prediction decoupled from execution (S3), and if better action tokenization unlocks high-frequency dexterous behaviour (S2), the cost and latency bar for real deployments could fall materially. Token pruning and scheduling are being studied specifically to address inference cost (R5). *(ai_interpretation)* [S2, S3, R5]

**Base case:** The efficiency evidence is thinner than the capability evidence: one of the two cited sources for the efficiency track does not actually describe the claimed features (C3), and latency remains explicitly open because reliability add-ons such as test-time compute trade against it (R5). Adaptation is still compute- and data-hungry, with one foundation model needing about 20,000 hours of real data (R8). *(ai_interpretation)* [C3, R5, R8]

**Bear case:** Efficiency may be inseparable from capability loss: post-training is reported to narrow generalist capability, so adaptation effort and generalization trade off (R8), and the small-model claims are self-reported without independent verification (C3). If the mitigation for reliability is more search and more compute (R3, R4), the efficiency thesis and the reliability thesis pull in opposite directions (R5). *(ai_interpretation)* [C3, R3, R4, R5, R8]

**Catalysts:**
- Independent reproduction of small-model training and inference claims on non-author hardware, with measured latency and success (C3, S3). *(ai_interpretation)* [C3, S3]
- Results showing token pruning or scheduling closes the latency gap without reducing success (R5). *(ai_interpretation)* [R5]

**Risks:**
- Cited efficiency evidence is partly mismatched to its claim, so the efficiency narrative currently rests on fewer sources than it appears (C3). *(ai_interpretation)* [C3]
- Reliability techniques such as test-time compute conflict directly with latency goals (R3, R5). *(ai_interpretation)* [R3, R5]
- Post-training narrows generalist capability, so cheaper, more adapted models may be less general (R8). *(ai_interpretation)* [R8]

**What would invalidate this thesis:**
- Independent measurements showing small VLAs cannot reach usable success rates at consumer-device latency would invalidate this theme (S3, R5, C3). *(ai_interpretation)* [S3, R5, C3]
- Evidence that high-frequency dexterous tasks remain out of reach regardless of tokenization scheme would weaken the core technical claim (S2). *(ai_interpretation)* [S2]

**Conflicting evidence:**
- C3: S3 cites ShowUI as support for small single-GPU trainable VLAs with asynchronous inference, but ShowUI is a GUI-agent model whose abstract describes neither, so only SmolVLA supports the claim and its comparison is self-reported. *(ai_interpretation)* [C3, S3]
- R5 versus R3/R4: reliability add-ons that raise success conflict with the low-latency goal that the efficiency track pursues. *(ai_interpretation)* [R3, R4, R5]

**Companies named by cited evidence:**
- none (no company evidence in the cited findings)

### VLA beyond robot arms: screen agents and embodied navigation

Technologies: GUI visual agents from screenshots, click/action prediction, visual-token reduction, hierarchical navigation with locomotion policies, gesture as a parallel instruction channel

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | VLA-style models applied to digital environments use UI screenshots as perception and click/action prediction as output with visual-token reduction to control compute (S6), and embodied navigation is proposed as a hierarchy where the model emits mid-level language or spatial commands and a separate locomotion policy produces joint actions (S7). Alternative instruction modalities such as gesture are a research direction (S10). No finding addresses products, users or revenue for any of these. *(forecast)* [S6, S7, S10] | medium |
| medium_1_3y | The cited navigation evidence is a single low-confidence finding (S7) and the GUI evidence is a single source (S6); there is no evidence on reliability, safety or cost for either branch, so the medium-term view can only be described as unaddressed by these findings. *(forecast)* [S6, S7] | low |
| long_3_5y | No cited finding covers this horizon for screen agents or navigation; the assessment is low confidence because the evidence base is one or two papers per branch. *(forecast)* [S6, S7] | low |

**Bull case:** The same action-as-token pattern (S5) transfers to digital interfaces, where a screenshot-in, click-out model with visual-token reduction controls compute (S6), and to legged navigation via a hierarchical split that avoids one model mapping language straight to joint torques (S7). Gesture as a parallel instruction channel addresses spatial ambiguity among similar objects (S10). *(ai_interpretation)* [S5, S6, S7, S10]

**Base case:** These are separate application branches with thin, mostly single-source evidence (S6, S7) and no reported failure analysis. In the broader manipulation setting the same class of model shows instruction-action binding failures and memorization (R1, R2), which the navigation and screen branches have not been shown to escape. *(ai_interpretation)* [S6, S7, R1, R2]

**Bear case:** Screen and navigation claims rest on one low-confidence finding each (S6, S7), and the field-wide failure modes — superficial visual perception and neglected safety constraints (R2), plus black-box behaviour where actions can be irreversible (R6) — apply most directly to agents that click or move autonomously. The gesture channel is exploratory only (S10). *(ai_interpretation)* [S6, S7, S10, R2, R6]

**Catalysts:**
- Reported task success and failure analysis for screen agents or navigation, which the current findings do not provide (S6, S7). *(ai_interpretation)* [S6, S7]
- Evidence that the hierarchical navigation split preserves reliability as environments change (S7, R1). *(ai_interpretation)* [S7, R1]

**Risks:**
- Single-source, low-confidence evidence for navigation and screen agents (S6, S7). *(ai_interpretation)* [S6, S7]
- Safety and interpretability weaknesses apply most acutely to agents that act autonomously in digital or physical environments (R6, R2). *(ai_interpretation)* [R2, R6]

**What would invalidate this thesis:**
- Evidence that hierarchical navigation or screen agents inherit the same instruction-action binding failures and safety neglect would weaken this theme (R1, R2, R6). *(ai_interpretation)* [R1, R2, R6]

**Conflicting evidence:**
- No direct conflict among the cited findings for this theme; the main weakness is that the evidence is one or two papers per branch (S6, S7) rather than contradicting results. *(ai_interpretation)* [S6, S7]

**Companies named by cited evidence:**
- none (no company evidence in the cited findings)

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2022: 1, 2023: 1, 2024: 22, 2025: 259, 2026: 1109}
Research Acceleration 2024->2025: 22 -> 259 (1077.3% YoY). OpenAlex works whose title or abstract contains the exact phrase "vision-language-action model", per publication year. Synonyms and abbreviations are not counted, and the number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-10): 2025 149 -> 2026 981 (558.4%, trend: rising). OpenAlex works with the exact phrase 'vision-language-action model' in title or abstract published 1 Jan–10 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence medium)* Open-source VLA releases show that a 7B-parameter model trained on large real-robot demonstration corpora can beat a much larger closed model on multi-task manipulation success, suggesting parameter scale is not the only driver of generalist manipulation performance.
  - source: [OpenVLA: An Open-Source Vision-Language-Action Model](https://doi.org/10.48550/arxiv.2406.09246) (OpenAlex, 2024-06-13, abstract_only)
  - excerpt: "OpenVLA demonstrates strong results for generalist manipulation, outperforming closed models such as RT-2-X (55B) by 16.5% in absolute task success rate across 29 tasks and multiple robot embodiments, with 7x fewer parameters."
  - reasoning: Single abstract (preprint), so the number cannot be cross-checked against other papers in this set; it is a self-reported benchmark comparison.
- **[S2]** *(verified_fact, confidence medium)* Autoregressive VLA policies depend heavily on how continuous actions are tokenized, and compression-based tokenization (discrete cosine transform) is reported to unlock high-frequency dexterous tasks where simple per-dimension binning fails.
  - source: [FAST: Efficient Action Tokenization for Vision-Language-Action Models](https://doi.org/10.15607/rss.2025.xxi.012) (OpenAlex, 2025-06-21, abstract_only)
  - excerpt: "we propose a new compression-based tokenization scheme for robot actions, based on the discrete cosine transform."
  - reasoning: Conference paper (RSS 2025) rather than a preprint, but the evidence here is still abstract-level only.
- **[S3]** *(verified_fact, confidence medium)* A distinct efficiency track is emerging: small community-trainable VLAs target single-GPU training and consumer/CPU inference, with asynchronous inference decoupling perception and action prediction from execution.
  - source: [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](https://doi.org/10.48550/arxiv.2506.01844) (OpenAlex, 2025-06-02, abstract_only)
  - source: [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](https://arxiv.org/abs/2411.17465v1) (arXiv, 2024-11-26, abstract_only)
  - excerpt: "SmolVLA is designed to be trained on a single GPU and deployed on consumer-grade GPUs or even CPUs."
  - reasoning: SmolVLA states the capability directly; ShowUI independently shows a lightweight 2B model with token-selection efficiency gains, so the 'smaller and cheaper' direction is supported by two papers, though both are preprints.
- **[S4]** *(verified_fact, confidence medium)* Broad open-world generalization in VLAs is being pursued through co-training on heterogeneous data (multiple robots, web data, semantic subtask prediction, detections) rather than any single data source, with reported long-horizon dexterous tasks in previously unseen homes.
  - source: [$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization](https://doi.org/10.48550/arxiv.2504.16054) (OpenAlex, 2025-04-22, abstract_only)
  - excerpt: "we demonstrate for the first time that an end-to-end learning-enabled robotic system can perform long-horizon and dexterous manipulation skills, such as cleaning a kitchen or bedroom, in entirely new homes."
  - reasoning: Preprint with self-reported 'first' claim; no independent replication appears in this paper set.
- **[S5]** *(ai_interpretation, confidence medium)* There is a converging design pattern of representing actions as discrete tokens inside the same sequence as vision and language, either by expressing actions as text tokens for co-fine-tuning or by natively autoregressing vision, language and action as discrete tokens.
  - source: [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://doi.org/10.48550/arxiv.2307.15818) (OpenAlex, 2023-07-28, abstract_only)
  - source: [Unified Vision-Language-Action Model](https://arxiv.org/abs/2506.19850v1) (arXiv, 2025-06-24, abstract_only)
  - source: [FAST: Efficient Action Tokenization for Vision-Language-Action Models](https://doi.org/10.15607/rss.2025.xxi.012) (OpenAlex, 2025-06-21, abstract_only)
  - reasoning: RT-2 established the 'actions as text tokens' recipe; UniVLA generalizes it to a native unified token formulation with world modeling; FAST addresses the tokenizer itself. Taken together these abstracts point to tokenization as the backbones of the paradigm, not an implementation detail. All are preprints and none reports an apples-to-apples comparison against the others.
- **[S6]** *(verified_fact, confidence medium)* A separate application branch applies VLA-style models to digital environments, using UI screenshots as perception and click/action prediction as output, with visual-token reduction to control compute.
  - source: [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](https://arxiv.org/abs/2411.17465v1) (arXiv, 2024-11-26, abstract_only)
  - excerpt: "ShowUI, a lightweight 2B model using 256K data, achieves a strong 75.1% accuracy in zero-shot screenshot grounding."
  - reasoning: Preprint; the 'action' here is GUI interaction rather than physical manipulation, so it should not be read as evidence about robotics.
- **[S7]** *(verified_fact, confidence low)* For embodied navigation, a hierarchical split is proposed where the VLA emits mid-level language/spatial commands that a separate locomotion RL policy converts into joint actions, rather than one model mapping language directly to low-level leg control.
  - source: [NaVILA: Legged Robot Vision-Language-Action Model for Navigation](https://arxiv.org/abs/2412.04453v2) (arXiv, 2024-12-05, abstract_only)
  - excerpt: "NaVILA first generates mid-level actions with spatial information in the form of language, (e.g., "moving forward 75cm"), which serves as an input for a visual locomotion RL policy for execution."
  - reasoning: One preprint abstract; the benchmark improvements are asserted without numbers in the abstract.
- **[S8]** *(verified_fact, confidence medium)* A named gap in the literature is the disconnect between upstream VLM-based embodied reasoning and downstream VLA policy learning, with proposed remedies including large embodied-reasoning datasets and systematic study of which VLM initialization best transfers to policy fine-tuning.
  - source: [Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027v2) (arXiv, 2025-10-13, abstract_only)
  - excerpt: "Vlaser achieves state-of-the-art performance across a range of embodied reasoning benchmarks - including spatial reasoning, embodied grounding, embodied QA, and task planning."
  - reasoning: Preprint; the paper itself frames the reasoning-to-control gap as an open issue, which supports treating it as an unresolved problem rather than a solved one.
- **[S9]** *(verified_fact, confidence low)* Robustness of RGB-based VLA manipulation is an active concern: photometric perturbations and adversarial conditions are reported to degrade action prediction, with explainability modules proposed to detect perturbations and explain their effects.
  - source: [Explainable Adversarial-Robust Vision-Language-Action Model for Robotic Manipulation](https://arxiv.org/abs/2512.11865v1) (arXiv, 2025-12-05, abstract_only)
  - excerpt: "the proposed model reduces Current Action L1 loss by 21.7% and Next Actions L1 loss by 18.4% compared to the baseline"
  - reasoning: Single preprint abstract in a narrow application domain (smart farming); the baseline is the authors' own OpenVLA-OFT variant, so the gain is relative, not absolute.
- **[S10]** *(verified_fact, confidence low)* Alternative instruction modalities beyond text are being explored, with gesture encoded into the latent space as a parallel instruction channel to resolve spatial ambiguity among similar objects.
  - source: [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](https://arxiv.org/abs/2605.22812v1) (arXiv, 2026-05-21, abstract_only)
  - excerpt: "we introduce gesture as a parallel instruction modality"
  - reasoning: One very recent preprint (2026) with only qualitative claims visible in the abstract; no numeric results are given.
- **[S11]** *(verified_fact, confidence medium)* The field now has a published survey organizing VLA research into three lines: individual model components, low-level control policies, and high-level task planners that decompose long-horizon instructions.
  - source: [A Survey on Vision--Language--Action Models for Embodied AI](https://doi.org/10.1109/tnnls.2025.3650584) (OpenAlex, 2026-04-28, abstract_only)
  - excerpt: "we present the first survey on VLAs for embodied AI"
  - reasoning: Journal-published survey (IEEE TNNLS), useful as a structuring reference; it is a secondary source and its 'first' claim is the authors' own.

**Emerging directions:**
- world modeling from large-scale video as a post-training stage for VLA policies
- compression-based action tokenization (DCT) and universal action tokenizers
- small, community-data-trained VLAs with asynchronous perception/action inference
- co-training across heterogeneous robots, web data and semantic subtask prediction for open-world generalization
- VLM-to-VLA transfer engineering: dataset scale, initialization choice, domain-shift mitigation
- VLA-style control in digital domains (GUI screenshot grounding and navigation agents)
- non-text instruction channels such as gesture encoded in latent space
- hierarchical and two-level architectures separating high-level reasoning/planning from low-level execution
- adversarial/photometric robustness plus natural-language explanation of policy behavior

**Open problems:**
- How far VLA policies generalize outside the lab environment remains described as an open question.
- Domain shift between internet-scale vision-language pre-training data and embodied-specific policy data.
- The gap between upstream VLM-based embodied reasoning and downstream low-level policy learning.
- Action tokenization for high-frequency, dexterous behavior where standard binning schemes fail.
- Resolving spatial ambiguity when instructions are textual only and scenes contain multiple similar objects.
- Vulnerability of RGB-based perception and manipulation to photometric perturbations and adversarial conditions.
- Translating high-level language instructions all the way to low-level joint actions (e.g., legged locomotion) without an intermediate abstraction.
- Limited realism and low-level control fidelity of existing navigation benchmarks.

**Limitations:**
- Analysis is based on titles and abstracts only; no full texts, method sections, or appendices were read.
- The sample is 12 items and includes only one published survey and one conference paper; most are arXiv preprints and are not peer reviewed.
- Reported success rates, loss reductions and speed-ups come from different benchmarks, baselines, robot embodiments and evaluation protocols, so they are not directly comparable.
- Some items carry future or very recent publication dates, so their claims have had little time for independent replication.
- Coverage is skewed toward manipulation; only one navigation paper and one digital/GUI paper are present, so generalizations across the whole VLA space are weakly supported.
- No citation, dataset or code-availability statistics were used in the findings by design.
- Nothing here is evidence of commercial success, deployment scale or investment merit.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['VLA model generalization failure', 'robot foundation model safety', 'VLA compute cost scaling', 'sim-to-real gap manipulation', 'VLA reproducibility benchmark', 'robot policy certification standard']

- **[R1]** *(verified_fact, confidence medium)* VLA policies with high in-distribution success can fail when a changed scene requires a different action. The failure is often 'instruction-action binding': the policy responds to language and vision but does not combine them. Aggregate robustness scores can hide this.
  - source: [When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models](https://doi.org/10.48550/arxiv.2609.39971) (OpenAlex, 2026-09-30, abstract_only)
  - source: [Same Scene, Different Task: Skill Alignment for Compositional Generalization in VLAs](https://doi.org/10.48550/arxiv.2610.00524) (OpenAlex, 2026-09-30, abstract_only)
  - excerpt: "can exceed 90% success on in-distribution tasks and withstand nuisance changes that preserve the required action, yet fail under counterfactual changes that demand a different action."
  - reasoning: The main source is a single preprint (not peer reviewed) that analyses fine-tuned pi0.5 and GR00T-N1.7 policies. A second preprint (src_5404a243b7) reports a related 'vision shortcut' failure on unseen skill combinations. The two agree directionally, but both are arXiv preprints from the same recent period, so independence is limited.
- **[R2]** *(verified_fact, confidence medium)* A dedicated benchmark reports that state-of-the-art VLAs memorize rather than generalize, perceive visually in a superficial way, and neglect safety constraints. Model rankings also reverse across difficulty levels, so a single leaderboard number can mislead.
  - source: [VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models](https://doi.org/10.48550/arxiv.2512.22539) (OpenAlex, 2025-12-27, abstract_only)
  - excerpt: "Our extensive evaluation of state-of-the-art VLAs reveals critical limitations: memorization over generalization, superficial visual perception, and a neglect of safety constraints."
  - reasoning: This rests on one preprint. Its benchmark is simulated, with fine-tuning restricted to the easiest level, so the results may not transfer to real deployments. The rank-reversal point is stated in the abstract, though the abstract names no models.
- **[R3]** *(ai_interpretation, confidence low)* Single-attempt reliability appears much lower than the capability latent in a model's output distribution. In one study, success rose from 33% at pass@1 to 92% at pass@32 for frozen VLAs. This suggests sampled actions are often poorly evaluated, and that fixes need extra search or compute, in this case MCTS in simulation.
  - source: [Look Before You Leap: Distilling Tree Search into Action Evaluation for Frozen VLA Models](https://doi.org/10.48550/arxiv.2607.03751) (OpenAlex, 2026-07-04, abstract_only)
  - source: [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](https://doi.org/10.48550/arxiv.2605.01194) (OpenAlex, 2026-05-02, abstract_only)
  - reasoning: The pass@k figures come from one preprint abstract, with 'overall success rates rising from 33% at pass@1 to 92% at pass@32'. Reaching high pass@k is not deployable, because a robot cannot retry 32 times when actions are irreversible. The proposed fix (src_05d281302e) depends on simulator-based tree search during training, which assumes a faithful simulator. VLA-ATTC (src_e7c1b22281) also adds deliberation compute. Both are preprints, and I infer the reliability gap from the abstracts only.
- **[R4]** *(ai_interpretation, confidence medium)* Recently proposed mitigations leave large residual failure rates and are evaluated mostly on simulated benchmarks. Examples include counterfactual training (36% to 59% position-swap success), test-time critics (failure rate cut by 'over 50%' on LIBERO-LONG), and environment staging. Each adds data, compute or rollout requirements.
  - source: [When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models](https://doi.org/10.48550/arxiv.2609.39971) (OpenAlex, 2026-09-30, abstract_only)
  - source: [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](https://doi.org/10.48550/arxiv.2605.01194) (OpenAlex, 2026-05-02, abstract_only)
  - source: [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](https://doi.org/10.48550/arxiv.2603.20659) (OpenAlex, 2026-03-21, abstract_only)
  - reasoning: The abstracts show ECT leaving roughly 40% of position-swap trials failing, and VLA-ATTC reducing rather than eliminating failures. StageCraft reports a 40% absolute gain in real-world tasks but needs policy rollouts with success labels and is training-free. All three are unreviewed arXiv preprints, and none was compared head-to-head with the others. Evidence from simulation (LIBERO, LIBERO-PRO, CALVIN) may overstate real-world robustness.
- **[R5]** *(verified_fact, confidence low)* Inference cost and low execution frequency are stated barriers to real-time use. Deliberation-style add-ons such as test-time compute may make this worse, creating a possible tension between reliability and latency.
  - source: [SP-VLA: A Joint Model Scheduling and Token Pruning Approach for VLA Model Acceleration](https://doi.org/10.48550/arxiv.2506.12723) (OpenAlex, 2025-06-15, abstract_only)
  - source: [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](https://doi.org/10.48550/arxiv.2605.01194) (OpenAlex, 2026-05-02, abstract_only)
  - excerpt: "their high computational cost and low execution frequency hinder their suitability for real-time tasks such as robotic manipulation and autonomous navigation."
  - reasoning: The quoted limitation comes from the motivation section of a single preprint proposing an acceleration method. The tension with test-time compute is my inference across two abstracts, and neither reports a combined latency study. The acceleration paper's abstract is truncated, so its measured speedups and any accuracy cost are not visible to me.
- **[R6]** *(ai_interpretation, confidence low)* Safety and interpretability are weak points. VLAs are described as black boxes whose physical actions can cause irreversible harm. A proposed failure predictor reaches only about 70% accuracy on real-world tasks, and a benchmark finds safety constraints neglected.
  - source: [Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory](https://doi.org/10.48550/arxiv.2606.19998) (OpenAlex, 2026-06-18, abstract_only)
  - source: [VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models](https://doi.org/10.48550/arxiv.2512.22539) (OpenAlex, 2025-12-27, abstract_only)
  - source: [FPC-VLA: A vision-language-action framework with a supervisor for failure prediction and correction](https://doi.org/10.1016/j.eswa.2026.131742) (OpenAlex, 2026-02-24, metadata_only)
  - reasoning: Tri-Info (src_adbdfa51d0) is an unreviewed preprint. Its abstract says it 'reach[es] 70% accuracy on real-world tasks', so roughly 30% of cases are misjudged, which is far from a safety-grade monitor. Its framing as 'black boxes' is the authors' own. The safety-neglect result comes from simulation (src_47c1fab0de). FPC-VLA (src_79c88fa08e) has no abstract available, so I cannot assess its supervisor approach; this is a gap, not a negative finding.
- **[R7]** *(verified_fact, confidence medium)* Real-world deployment claims remain unproven at scale. The strongest deployment-oriented result still reports failure rates that are reduced, not eliminated, and describes reliability and speed for practical use as an open challenge.
  - source: [π*₀.₆: a VLA That Learns From Experience](https://doi.org/10.15607/rss.2026.xxii.087) (OpenAlex, 2026-07-13, abstract_only)
  - excerpt: "but achieving the reliability and speed required for practical deployment remains challenging."
  - reasoning: The abstract itself says RECAP 'roughly halves the task failure rate' on some of the hardest tasks, which implies substantial residual failures. The demonstrations (laundry folding, box assembly, espresso) are selected tasks, and the abstract gives no number of sites, hours or independent replications. This is a conference paper by the model's developers, so it is self-reported. Continued improvement also depends on collecting ongoing real-world experience and human corrections, which carries a cost the abstract does not quantify.
- **[R8]** *(ai_interpretation, confidence low)* Adapting generalist VLAs still appears data- and compute-intensive. One foundation model needed about 20,000 hours of real data and 130 post-training episodes per task. Separately, post-training is said to narrow generalist capability, so adaptation effort and generalization trade off.
  - source: [A Pragmatic VLA Foundation Model](https://doi.org/10.48550/arxiv.2601.18692) (OpenAlex, 2026-01-26, abstract_only)
  - source: [Look Before You Leap: Distilling Tree Search into Action Evaluation for Frozen VLA Models](https://doi.org/10.48550/arxiv.2607.03751) (OpenAlex, 2026-07-04, abstract_only)
  - source: [Tactile-VLA: Unlocking Vision-Language-Action Model's Physical Knowledge for Tactile Generalization](https://doi.org/10.48550/arxiv.2507.09160) (OpenAlex, 2025-07-12, abstract_only)
  - reasoning: LingBot-VLA (src_dd2cf29d23) reports 'each completing 100 tasks with 130 post-training episodes per task', and the data and benchmark results are self-reported in a preprint. src_05d281302e claims post-training 'narrows the generalist capability', which is its own motivating claim and not independently tested in the abstract. Tactile-VLA (src_b568c0dbaa) claims zero-shot contact-rich generalization from 'a few demonstrations', but its abstract gives no quantitative results or task counts, so the breadth of that claim cannot be judged. All three are preprints.

**Possible hype:**
- 'Generalist robot policy' / 'generalist robotic agents': benchmark and counterfactual studies show failures on small scene or instruction changes, and memorization over generalization.
- 'Remarkable capabilities and generalization' in VLA papers: this rests largely on in-distribution or simulated benchmarks (LIBERO, CALVIN), and aggregate scores can hide specific failure modes.
- 'Zero-shot generalization in contact-rich tasks' (Tactile-VLA): the abstract gives no quantitative results, task counts or baselines.
- 'Ready for real-world deployment' framing for foundation models: the abstracts describe throughput and benchmark wins, not long-term failure statistics, safety validation or independent replication.
- Headline failure-rate reductions ('over 50%', '40% absolute'): these are measured from a baseline that was already failing frequently, on selected benchmarks, so the absolute reliability reached is still unclear.

**Challenges to the Science findings:**
- Targets ['S4'], severity medium:
  - **[C1]** *(unverified_claim, confidence low)* S4 presents broad open-world generalization via co-training as an achieved result, but the cited abstract gives no success rates or failure analysis. Other evidence shows that pi0.5-class policies can fail when the required action changes, so 'generalization' may be narrower than the finding implies.
    - source: [$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization](https://doi.org/10.48550/arxiv.2504.16054) (OpenAlex, 2025-04-22, abstract_only)
    - source: [When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models](https://doi.org/10.48550/arxiv.2609.39971) (OpenAlex, 2026-09-30, abstract_only)
    - source: [VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models](https://doi.org/10.48550/arxiv.2512.22539) (OpenAlex, 2025-12-27, abstract_only)
    - excerpt: "VLA models can exceed 90% success on in-distribution tasks and withstand nuisance changes that preserve the required action, yet fail under counterfactual changes that demand a different action."
    - reasoning: The pi0.5 abstract supports only that long-horizon tasks were demonstrated in new homes. It gives no rates and no stress-test results. The diagnostic preprint analyzes fine-tuned pi0.5 and reports a position-swap success of 36% before mitigation. VLA-Arena reports memorization over generalization. The finding needs a caveat that real-world generalization is unquantified and shows instruction-action binding failures. Both diagnostic sources are recent preprints with few citations.
    - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- Targets ['S1'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S1 reads the OpenVLA-vs-RT-2-X comparison as evidence that parameter scale is not the main driver. The abstract itself credits a mix of data diversity and new model components, so the comparison is confounded. It is also a self-reported result from the model's own authors on their chosen 29-task suite.
    - source: [OpenVLA: An Open-Source Vision-Language-Action Model](https://doi.org/10.48550/arxiv.2406.09246) (OpenAlex, 2024-06-13, abstract_only)
    - excerpt: "As a product of the added data diversity and new model components, OpenVLA demonstrates strong results for generalist manipulation"
    - reasoning: Scale is not isolated from data, vision encoder and architecture, so the 'scale is not the only driver' reading is an inference. VLA-Arena reports that rankings reverse across difficulty levels and that a single number can mislead. A single task-success margin therefore says little about generalization. The finding is labeled verified_fact but the interpretive step is not.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S3'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S3 cites ShowUI as support for an efficiency track of small, community-trainable VLAs with single-GPU training and asynchronous inference. ShowUI is a GUI-agent model for screenshots, and its abstract describes neither single-GPU training nor asynchronous inference. Only SmolVLA supports the finding, and its 'comparable to 10x larger' claim is self-reported.
    - source: [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](https://arxiv.org/abs/2411.17465v1) (arXiv, 2024-11-26, abstract_only)
    - source: [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](https://doi.org/10.48550/arxiv.2506.01844) (OpenAlex, 2025-06-02, abstract_only)
    - excerpt: "ShowUI, a lightweight 2B model using 256K data, achieves a strong 75.1% accuracy in zero-shot screenshot grounding."
    - reasoning: ShowUI's efficiency claims concern token selection and data curation for GUI tasks. They are not about consumer-hardware robot deployment. Grouping the two papers inflates the apparent breadth of the 'efficiency track'. SmolVLA's abstract also does not say which benchmarks or which larger models it matches.
- Targets ['S5'], severity medium:
  - **[C4]** *(ai_interpretation, confidence medium)* S5 says there is a converging pattern of discrete action tokens in one sequence. The cited evidence includes a paper that treats diffusion VLAs as the main competing paradigm. Its abstract reports only that discrete tokenization can 'match' them. UniVLA's headline gains are on simulation benchmarks. The convergence claim is overstated.
    - source: [FAST: Efficient Action Tokenization for Vision-Language-Action Models](https://doi.org/10.15607/rss.2025.xxi.012) (OpenAlex, 2025-06-21, abstract_only)
    - source: [Unified Vision-Language-Action Model](https://arxiv.org/abs/2506.19850v1) (arXiv, 2025-06-24, abstract_only)
    - source: [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://doi.org/10.48550/arxiv.2307.15818) (OpenAlex, 2023-07-28, abstract_only)
    - excerpt: "match the performance of diffusion VLAs, while reducing training time by up to 5x."
    - reasoning: Three papers using tokenized actions show the pattern exists. They do not show convergence. The FAST abstract frames diffusion VLAs as the reference standard and claims parity, not superiority. UniVLA's reported 95.5% on LIBERO is a simulation result, and benchmark-saturated scores are not robust evidence of a dominant design. The finding should say tokenization and continuous or diffusion action heads coexist.
- Targets ['S9'], severity low:
  - **[C5]** *(ai_interpretation, confidence medium)* S9 treats the explainable adversarial-robust VLA as evidence that photometric robustness is addressed and explainable. The reported metric is a reduction in action L1 loss, an offline action-prediction error, not task success or physical safety. The setting is narrow (smart farming) and it comes from one preprint.
    - source: [Explainable Adversarial-Robust Vision-Language-Action Model for Robotic Manipulation](https://arxiv.org/abs/2512.11865v1) (arXiv, 2025-12-05, abstract_only)
    - excerpt: "the proposed model reduces Current Action L1 loss by 21.7% and Next Actions L1 loss by 18.4% compared to the baseline"
    - reasoning: L1 gains of about 18-22% do not show that manipulation survives attacks or that the explanations are faithful. The abstract reports no success rates, no real-robot trials and no evaluation of the explanations. S9 should be read as a concern plus an early, weakly validated mitigation.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source

**Limitations:**
- Only abstracts or metadata were available, and several abstracts are truncated, so experimental details, baselines and error bars could not be checked.
- Almost all sources are arXiv preprints and are not peer reviewed. The only conference paper (src_26f51138d8) is by the developers of the model it presents.
- The corpus is 12 papers on one topic, heavily weighted to manipulation. It has little on cost, hardware or supply-chain dependence, power or thermal limits at the edge, regulation, or alternative approaches (for example classical control or world-model-based planning), so those risks are unassessed.
- FPC-VLA (src_79c88fa08e) has no abstract, so it contributed no evidence.
- Many papers report results on the same few benchmarks and base models (pi0.5, GR00T), so the evidence is probably less independent than the paper count suggests.
- Papers proposing fixes naturally stress failures, so the failure rates they report may reflect chosen stress conditions rather than typical deployment.
- Only titles, metadata and abstracts were reviewed. Full-paper details such as baselines, seeds, and per-task results could soften or sharpen these challenges.
- Several risk sources are very recent preprints with 0-13 citations and no peer review, so the contrary evidence is itself weak.
- I did not challenge S2, S6, S7, S8, S10 or S11. Their claims match the abstracts at the level stated, although S7, S10 and S8 each rest on a single paper's own framing.
- FPC-VLA had no abstract available, so it could not be used.

## Evidence: company filings and news
Status: no_data. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: vision-language-action model, vision-language-action, VLA model, robot foundation model, embodied AI, autonomous manipulation

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Tesla (TSLA) | 2 | 0 | large: 94.8B USD | -2.9% | 6.8% of revenue |  |
| Intuitive Surgical (ISRG) | 2 | 0 | large: 10.1B USD | +20.5% | 13.0% of revenue | 2 press release(s) read |
| Teradyne (TER) | 2 | 0 | mid: 2.1B USD | -1.7% | n/a | 2 press release(s) read |
| Rockwell Automation (ROK) | 2 | 0 | mid: 8.3B USD | +0.9% | 8.1% of revenue | 2 press release(s) read |
| Mobileye Global (MBLY) | 2 | 0 | mid: 1.9B USD | +14.5% | 60.8% of revenue | 2 press release(s) read |
| Symbotic (SYM) | 2 | 0 | mid: 2.2B USD | +25.7% | 9.6% of revenue | 2 press release(s) read |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._


**Limitations:**
- No filing passage or news headline mentioning the keywords was found; no analysis was performed.

## Evidence: patents
Status: partial. Worldwide patent publications from Google Patents (SerpApi) matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: no_data. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.


**Limitations:**
- No company was identified by the Market agent, so no prices were fetched.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: partial. 2 distinct company names from 0 patent publications, 2 company-affiliated papers and 0 SEC filers; 0 matched to the SEC ticker file (0 outside the configured list), 2 not SEC-listed (private, foreign or not found).

**Found but not in the SEC ticker file (private, foreign, or name not matched):** Huawei Technologies (China) (0P/1A/0F), Hugging Face (0P/1A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._


**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [When Instructions Retrieve Trajectories: Diagnosing and Mitigating Generalization Failures in VLA Models](https://doi.org/10.48550/arxiv.2609.39971) | OpenAlex | 2026-09-30 | retrieved 2026-11-09 | abstract_only | id src_560001b3c3
- [Same Scene, Different Task: Skill Alignment for Compositional Generalization in VLAs](https://doi.org/10.48550/arxiv.2610.00524) | OpenAlex | 2026-09-30 | retrieved 2026-11-09 | abstract_only | id src_5404a243b7
- [π*₀.₆: a VLA That Learns From Experience](https://doi.org/10.15607/rss.2026.xxii.087) | OpenAlex | 2026-07-13 | retrieved 2026-11-09 | abstract_only | id src_26f51138d8
- [Look Before You Leap: Distilling Tree Search into Action Evaluation for Frozen VLA Models](https://doi.org/10.48550/arxiv.2607.03751) | OpenAlex | 2026-07-04 | retrieved 2026-11-09 | abstract_only | id src_05d281302e
- [Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory](https://doi.org/10.48550/arxiv.2606.19998) | OpenAlex | 2026-06-18 | retrieved 2026-11-09 | abstract_only | id src_adbdfa51d0
- [GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations](https://arxiv.org/abs/2605.22812v1) | arXiv | 2026-05-21 | retrieved 2026-11-09 | abstract_only | id src_cb945f40a6
- [VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model](https://doi.org/10.48550/arxiv.2605.01194) | OpenAlex | 2026-05-02 | retrieved 2026-11-09 | abstract_only | id src_e7c1b22281
- [A Survey on Vision--Language--Action Models for Embodied AI](https://doi.org/10.1109/tnnls.2025.3650584) | OpenAlex | 2026-04-28 | retrieved 2026-11-09 | abstract_only | id src_6ad9679910
- [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](https://doi.org/10.48550/arxiv.2603.20659) | OpenAlex | 2026-03-21 | retrieved 2026-11-09 | abstract_only | id src_6fb289a18b
- [FPC-VLA: A vision-language-action framework with a supervisor for failure prediction and correction](https://doi.org/10.1016/j.eswa.2026.131742) | OpenAlex | 2026-02-24 | retrieved 2026-11-09 | metadata_only | id src_79c88fa08e
- [A Pragmatic VLA Foundation Model](https://doi.org/10.48550/arxiv.2601.18692) | OpenAlex | 2026-01-26 | retrieved 2026-11-09 | abstract_only | id src_dd2cf29d23
- [VLA-Arena: An Open-Source Framework for Benchmarking Vision-Language-Action Models](https://doi.org/10.48550/arxiv.2512.22539) | OpenAlex | 2025-12-27 | retrieved 2026-11-09 | abstract_only | id src_47c1fab0de
- [Explainable Adversarial-Robust Vision-Language-Action Model for Robotic Manipulation](https://arxiv.org/abs/2512.11865v1) | arXiv | 2025-12-05 | retrieved 2026-11-09 | abstract_only | id src_b146628884
- [Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027v2) | arXiv | 2025-10-13 | retrieved 2026-11-09 | abstract_only | id src_55a367f044
- [Tactile-VLA: Unlocking Vision-Language-Action Model's Physical Knowledge for Tactile Generalization](https://doi.org/10.48550/arxiv.2507.09160) | OpenAlex | 2025-07-12 | retrieved 2026-11-09 | abstract_only | id src_b568c0dbaa
- [Unified Vision-Language-Action Model](https://arxiv.org/abs/2506.19850v1) | arXiv | 2025-06-24 | retrieved 2026-11-09 | abstract_only | id src_1700ca3fa1
- [FAST: Efficient Action Tokenization for Vision-Language-Action Models](https://doi.org/10.15607/rss.2025.xxi.012) | OpenAlex | 2025-06-21 | retrieved 2026-11-09 | abstract_only | id src_facc747bfb
- [SP-VLA: A Joint Model Scheduling and Token Pruning Approach for VLA Model Acceleration](https://doi.org/10.48550/arxiv.2506.12723) | OpenAlex | 2025-06-15 | retrieved 2026-11-09 | abstract_only | id src_9948861b34
- [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](https://doi.org/10.48550/arxiv.2506.01844) | OpenAlex | 2025-06-02 | retrieved 2026-11-09 | abstract_only | id src_01ea258f81
- [$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization](https://doi.org/10.48550/arxiv.2504.16054) | OpenAlex | 2025-04-22 | retrieved 2026-11-09 | abstract_only | id src_c73ee17da5
- [NaVILA: Legged Robot Vision-Language-Action Model for Navigation](https://arxiv.org/abs/2412.04453v2) | arXiv | 2024-12-05 | retrieved 2026-11-09 | abstract_only | id src_b517db5e05
- [ShowUI: One Vision-Language-Action Model for GUI Visual Agent](https://arxiv.org/abs/2411.17465v1) | arXiv | 2024-11-26 | retrieved 2026-11-09 | abstract_only | id src_4463fe5b96
- [OpenVLA: An Open-Source Vision-Language-Action Model](https://doi.org/10.48550/arxiv.2406.09246) | OpenAlex | 2024-06-13 | retrieved 2026-11-09 | abstract_only | id src_a0d7a46688
- [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://doi.org/10.48550/arxiv.2307.15818) | OpenAlex | 2023-07-28 | retrieved 2026-11-09 | abstract_only | id src_94dd97af57

## Gaps, limitations and errors
- Missing data: Patent agent did not run: no patent findings and no code-computed patent counts, so patent momentum is unrated.
- Missing data: Market agent did not run: no SEC filing excerpts, no revenue, pricing, customer or contract evidence, and no company disclosure on VLA products.
- Missing data: X agent did not run: no social or company-announcement signals to use as catalysts.
- Missing data: No price and timing findings were supplied, so no context on how far related stocks have already moved.
- Missing data: No Company Scout (K) findings: no patent assignees, employer affiliations or SEC filers with financials. The scout note lists Huawei Technologies (China) and Hugging Face as non-SEC names seen (0 patents, 1 paper each), but this comes without a finding id and is not usable as company evidence.
- Missing data: No company evidence yet: no finding in this set names a company, product, customer or revenue figure.
- Missing data: No evidence on cost per unit, hardware requirements, manufacturing, standards or regulation for VLA systems.
- Missing data: No real-robot success rates for the open-world generalization claim (C1) and no independent replication of the open-versus-closed comparison (C2).
- Limitation: This assessment rests almost entirely on paper titles and abstracts plus one benchmark and one survey; abstracts under-report failure rates and negative results.
- Limitation: Research activity metrics count only works whose title or abstract contains the exact phrase 'vision-language-action model'; synonyms and abbreviations are excluded and counts are not normalised for overall growth in publishing, so the acceleration figure overstates relative momentum.
- Limitation: Most reported results are self-reported by the models' own authors and several are confined to simulation benchmarks (C2, C4, R4).
- Limitation: No commercial, patent, price or social evidence was available, so commercial_readiness, customer_adoption, industry_investment, competitive_position and supply_chain_readiness cannot be properly rated.
- Limitation: The Risk challenges C1, C3 and C5 are low-severity or unverified claims about individual papers; they weaken specific science findings rather than the field as a whole, and are treated as such.
- Limitation: Nothing here is a prediction of returns; ratings are evidence-coverage judgements, not recommendations.
- Chief review gap: Market agent not run: no company filings, funding, or commercial deployment signals available to assess competitive landscape or commercial viability
- Chief review gap: Patent agent not run: no IP landscape data to assess freedom-to-operate or key patent holders
- Chief review gap: X agent not run: no community or practitioner sentiment signals
- Chief review gap: Sim-to-real transfer is only indirectly addressed (R4 notes most mitigations are evaluated in simulation; R7 notes real-world deployment unproven) but no dedicated finding quantifies the sim-to-real gap for VLA policies specifically
- Reference checks changed 3 statement(s) in the assessment (see notes in italics above).
- ERROR [patent/Google Patents (SerpApi)]: counts: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [patent/Google Patents (SerpApi)]: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 2 | 3963 | 1649 | 0.00237 |
| science | deepseek/deepseek-v4.1-flash | 1 | 5061 | 3988 | 0.00630 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 24837 | 9214 | 0.14181 |
| investment | deepseek/deepseek-v4.1-flash | 1 | 5981 | 7947 | 0.01073 |
| investment (rescore) | deepseek/deepseek-v4.1-flash | 1 | 6342 | 6891 | 0.00957 |

Total estimated cost: $0.17078 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
