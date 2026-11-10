# FUTURESCOUT AI research report: AI agents

Generated: 2026-11-09 08:02 UTC

**Research information only, not investment advice.** This report is produced by AI agents from the sources listed below. It does not recommend buying or selling anything, does not predict prices, and does not promise any return. Forecasts are uncertain and may be wrong.

How to read the labels: `verified_fact` = a quoted passage in a cited source supports it. `ai_interpretation` = the AI's reading of the evidence. `forecast` = a prediction. `assumption` = no supporting evidence cited. `unverified_claim` = asserted but not confirmed.

## Coverage
- Agents that produced output: chief, science, risk, market, x, timing, scout, investment
- Agents NOT run in this version: patent. Conclusions therefore have no patent evidence.

## Verdict (forecast, computed from the report)
**Building: real activity, not yet proven commercially** — score 56.5, confidence medium.

AI agents are software programs that can carry out tasks on their own, using tools and other programs, rather than just answering questions. The evidence says this is really taking off: research on it is growing extremely fast, and most big software companies - plus a number of smaller ones - now sell agent…

Why:
- Research Momentum rated 5/5: Code-computed OpenAlex counts for the exact phrase 'AI agents' rose from 1,077 works in 2024 to 4,480 in 2025 (+316% YoY), and the current partial year is running at 13,252 versus 2,977 at the same point in 2025 (+345%), indicating momentum is still building rather than fading.
- Industry Investment rated 5/5: Industry commitment is broad and specific: a $128.3m acquisition of an enterprise agent-connectivity platform (M3), new managed agent services (M2), agent capability embedded across Microsoft (M4), Alphabet (M5), Meta (M6) and Oracle (M7) portfolios, Agentforce marketed as a platform by Salesforce (M1), agent products launched by six mid- and small-caps (M8, K1-K6), and Meta explicitly saying it expects to increase agentic AI investment while acknowledging it may not generate profits from it (M6).
- Papers 2024→2025: 1077→4480 (+316%)
- So far in 2026 (to 10-10): 13252 papers vs 2977 by the same date in 2025 (+345%, rising)

Watch out for:
- Final task success hides unreliable behaviour: about 31% of successful runs in one benchmark still failed a harness reliability criterion, and run-level error rates are decoupled from final success
- Rare but highly critical failures (validation, output errors) can cascade across steps, so average error rates understate tail risk
- The strongest quantitative reliability claims in the set are the weakest methodologically (label construction for the 0.970 ROC-AUC.
- Whether safety improves without utility loss is contested across the alignment papers, and the dispute rests on author-selected benchmarks

What would change this view:
- Stronger if: Companies disclosing agent-specific revenue, seat counts or customer numbers rather than product descriptions
- Weaker if: Filings stop attributing new products or revenue categories to agents, or vendors quietly drop agent branding while continuing the same features
- Stronger if: An enterprise or regulator adopting a specific, published reliability or assurance standard for agents
- Weaker if: Evidence that platform vendors deliver sufficient evaluation, guardrails and logging natively, removing demand for independent tooling

_Our read of the technology's momentum and risk over one to five years, labelled forecast. It is research information, not advice to buy or sell anything, and it names no entry point._

## Summary
The evidence shows AI agents moving from research to commercial products fast: research mentions of the exact phrase grew from 1,077 works in 2024 to 4,480 in 2025 (+316%), and the current partial year is running at +345% versus the same period, so momentum is still building rather than fading. In parallel, nearly every large enterprise software vendor and several mid-caps now describe shipping agent platforms or features (Salesforce Agentforce, Amazon Bedrock Managed Agents, Microsoft Dynamics, Alphabet Gemini Enterprise, Meta Muse, Oracle OCI, Snowflake's $128.3m Natoma acquisition, plus smaller names such as Atlassian, BILL, Figma, Klaviyo, Amplitude and DigitalOcean). What the evidence does not show is verified end-customer adoption, agent-attributable revenue or pricing power: company filings describe their own products, and the only adoption-like numbers are social posts, which are unverified. The research side simultaneously documents unresolved problems - benchmark design that misleads (S1), process-level deviations hidden by final-output checks (S2, weakened by C1), an unaddressed agent attack surface (S3, weakened by C3), and reliability reporting that is explicitly unvalidated (R8) - while governance and authorization proposals (S4, S5, S9, S11) are conceptual or prototype-stage and challenged (C4, C5, C6). The main uncertainty is therefore not whether agents are being built and sold, but whether reliability, security and accountability mature faster than deployments, and whether any of this converts into durable economics rather than feature parity. Related equities do not give a clean read: four of five agent-linked names checked have pulled back sharply over the past month with elevated volatility (T3-T11). Patent evidence is absent because the patent agent did not run.

## Technology Opportunity Score
**Score: 56.5 / 100** (confidence: medium; evidence coverage 90%)

Risk adjustment: rating 3/5 lowered the score by 18.0% (base 68.9).

Commercialization Gap (research momentum rating minus commercial readiness rating): +1


| Dimension | Weight | Rating (0-5) | Evidence | Reasoning |
|---|---|---|---|---|
| Research Momentum | 15% | 5 | S1, S2, S3, S4, S5, S7, S8, S10, S11 | Code-computed OpenAlex counts for the exact phrase 'AI agents' rose from 1,077 works in 2024 to 4,480 in 2025 (+316% YoY), and the current partial year is running at 13,252 versus 2,977 at the same point in 2025 (+345%), indicating momentum is still building rather than fading. The measure counts only the exact phrase, is not normalised for overall publishing growth, and the current year is partial, but the direction is unambiguous. Supporting breadth: agent research now spans benchmarks (S1), evaluation (S2), security (S3), authorization (S4), governance (S5), taxonomies (S7), scientific applications (S8), methodology (S10) and safety layers (S11). |
| Patent Momentum | 10% | missing | none | no valid 0-5 rating given |
| Technical Feasibility | 15% | 3 | M1, M2, M3, M4, M5, M6, M7, M8, S2, R1, R2, R3, R4, R5, C1 | Agents demonstrably run and are shipping in products (M1-M8), so this is beyond pure theory. But the findings show unresolved core problems: final-output tests miss process-level deviations in tool selection, arguments, execution order and database integrity (S2, with C1 limiting the strength of that specific result), about 31% of successful runs still fail a reliability criterion in one benchmark (R2), highly critical validation and output failures can cascade (R1), tool use widens the attack surface via compromised outputs and injected instructions (R4), and memory-driven self-evolution can reduce trustworthiness (R3). Whether safety can be improved without losing utility is contested (R5). Capability is proven; dependable autonomy is not. |
| Commercial Readiness | 15% | 4 | M1, M2, M3, M4, M5, M6, M7, M8, K1, K2, K3, K4, K5, K6 | Commercial readiness is well evidenced at the product level: Salesforce markets Agentforce across business functions (M1), Amazon offers a public preview of Bedrock Managed Agents and Strands Box (M2), Snowflake paid $128.3m for Natoma, an enterprise MCP platform (M3), Microsoft ships agentic AI in Dynamics (M4), Alphabet offers Gemini Enterprise (M5), Meta launched Muse (M6), Oracle embeds agentic AI in OCI (M7), and six mid- and small-cap software companies commercialised or launched agent products in 2025-2026 (M8, K1-K6). Rated 4 rather than 5 because the evidence is vendor self-description of products, with no cited disclosure of agent-attributable revenue, pricing or unit economics. |
| Customer Adoption | 10% | 2 | M3, M8, M9, M10, X4 | There is no verified customer-adoption evidence in this set. Market findings describe companies' own products and risk disclosures, which does not establish that customers are buying or deploying them; the only adoption-like number - a claim that over half of enterprises already run agentic AI in production - is an unverified social post (X4). The strongest indirect signals are that vendors keep investing (M3 acquisition, M8 launches) and that filers treat agents as a competitive and security risk, which implies awareness rather than proven purchase (M9, M10). Rated 2 on the strength of those indirect signals only. |
| Industry Investment | 10% | 5 | M1, M2, M3, M4, M5, M6, M7, M8, K1, K2, K3, K4, K5, K6 | Industry commitment is broad and specific: a $128.3m acquisition of an enterprise agent-connectivity platform (M3), new managed agent services (M2), agent capability embedded across Microsoft (M4), Alphabet (M5), Meta (M6) and Oracle (M7) portfolios, Agentforce marketed as a platform by Salesforce (M1), agent products launched by six mid- and small-caps (M8, K1-K6), and Meta explicitly saying it expects to increase agentic AI investment while acknowledging it may not generate profits from it (M6). The scale of committed spend is clear even though the returns are not. |
| Competitive Position | 10% | 3 | M1, M2, M4, M5, M6, M7, M8, M9, M10, K1, K2, K3, K4, K5, K6 | The field is crowded at every layer, which limits any single player's defensibility: four mega-cap platforms (M4, M5, M6, M7) plus Salesforce (M1), Amazon (M2) and Oracle (M7) all ship agents, and at least six smaller software companies have their own agent offerings (M8, K1-K6), so differentiation is unclear from these findings. Two findings suggest position can be actively eroded by agents: one platform warns third-party autonomous agents may circumvent its pricing and reduce its control over distribution and monetization (M9), and competitive disruption from autonomous agents is a cited risk theme (M10). Aggregate-hosted data and workflow incumbency is a plausible advantage, but no finding quantifies share, retention or switching costs. |
| Supply-Chain Readiness | 15% | 2 | M2, M3, X6 | Evidence on the agent supply chain is indirect: a managed service for building and deploying production agents with an open-source sandbox for behaviour rules (M2) and the acquisition and embedding of an enterprise Model Context Protocol platform for agent connectivity (M3) imply that a tooling and protocol layer exists. Beyond that, the findings say nothing about capacity, pricing, critical dependencies, model access or the reliability of underlying providers, and the claim that frameworks like LangChain, LangGraph and MCP are becoming mainstream developer skills is an unverified social signal (X6). Rated 2 on connectivity evidence alone. |

Formula: base = sum(weight x rating/5) / sum(weight of evidenced dimensions) x 100; score = base x (1 - max_penalty x risk_rating/5). Dimensions without cited findings are 'missing', not zero.

- Weights are initial assumptions, not fitted to data. The score is an explainable heuristic, not a validated prediction of stock performance.
- Sources are de-duplicated by URL/DOI/title. A single announcement reported by several outlets is not yet merged into one event.
- Confidence lowered to 'medium': coverage is 90%, but the cited ratings themselves are mostly of lower confidence.

## Investment themes
_Scenarios and horizon views are AI forecasts/interpretations tied to the cited findings. They are not facts._

### Enterprise agent platforms and the application-layer land grab

Technologies: autonomous AI agents, agentic AI embedded in business applications, managed agent runtimes, Model Context Protocol (MCP) integrations

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The near-term evidence is dominated by product launches and platform positioning rather than results. Salesforce markets Agentforce across business functions (M1), Amazon previewed Bedrock Managed Agents and Strands Box (M2), Snowflake bought Natoma, an enterprise MCP platform, for $128.3m (M3), and Microsoft (M4), Alphabet (M5), Meta (M6) and Oracle (M7) all describe agentic AI shipping inside their portfolios. Several mid- and small-caps launched agent products in 2025-2026 (M8, K1-K6). What the evidence does not support is any near-term read on adoption, attach rates or revenue contribution - no filing cited gives agent-specific revenue or customer counts, and the only adoption-like figure is an unverified social post (X4). Price/timing findings show most related names have pulled back sharply over the past month with elevated volatility (T3, T4, T5, T6, T7, T8, T9, T10, T11), which is risk context only, not a timing signal. *(ai_interpretation)* [M1, M2, M3, M4, M5, M6, M7, M8, K1, K2, K3, K4, K5, K6, X4, T11] | medium |
| medium_1_3y | The medium-term case rests on agents becoming a standard layer of enterprise software rather than a feature. The evidence for direction is broad but self-reported: nine separate filers describe agent products (M1-M7, M8), and one company explicitly flags that third-party autonomous agents may circumvent its pricing and reduce control over distribution (M9). The evidence does not establish which layer captures the economics - platform, application, data or runtime - and the reliability findings (R1, R2, R8) suggest enterprise deployment depth will depend on tooling that is still immature. No cited finding quantifies market size, win rates or retention. *(forecast)* [M1, M2, M3, M4, M5, M6, M7, M8, M9, R1, R2, R8] | medium |
| long_3_5y | The long-horizon evidence is the overall research trend plus governance proposals, not commercial results: work on agents continues to accelerate (2024: 1,077 works; 2025: 4,480; 2026 partial year 13,252 versus 2,977 at the same point last year), and governance researchers propose identifiers, monitoring and logging as the shape of future regimes (S5) though these are untested (C6). Nothing in the findings supports a specific long-run revenue, margin or market-share path, and the risk work (R1-R8) shows the failure modes that could cap autonomy levels. Long-term confidence is therefore low. *(ai_interpretation)* [S5, S7, S12, R1, R8, C6] | low |

**Bull case:** Every major enterprise software vendor plus a long tail of mid-caps now ships agent capability, and one paid $128.3m for an agent-connectivity platform, which is evidence of real budgets behind the theme rather than marketing alone (M1-M8, M3). Smaller filers with named agent products and disclosed revenue growth - Atlassian (+26.0%), Klaviyo (+31.6%), Figma (+41.0%), DigitalOcean (+15.5%) - show the theme reaching beyond the mega-caps (K1-K6). Research supply is growing faster than almost any other topic in this evidence set, which supports a deep talent and component pipeline, and governance work is at least converging on concrete mechanisms such as agent identifiers and activity logging (S5, S7). *(ai_interpretation)* [M1, M2, M3, M4, M5, M8, K1, K2, K4, K5, S5, S7]

**Base case:** Agents become a normal, widely shipped software layer over 1-5 years, but the commercial evidence so far is company self-description rather than adoption proof, and the reliability and security literature shows the barriers to unattended operation are real. Deployments likely proceed with human oversight first, which delays the operational savings that justify premium pricing; meanwhile competitive intensity is high because nearly every filer in this set offers something similar (M1-M8), and at least one platform company warns agents could erode its own pricing control (M9). The most defensible assumption is breadth of participation with unresolved economics. *(forecast)* [M1, M2, M3, M4, M5, M6, M7, M8, M9, R1, R2, R8]

**Bear case:** A material share of the agent case rests on findings the risk layer has already undercut. Process-level reliability numbers come from one preprint and one proprietary use case (C1 attacking S2), the claim that frameworks do not address agent vulnerabilities is the authors' own assertion from a 2024 preprint (C3 against S3), and authorization, proof-carrying and runtime-gating proposals are one prototype and one theoretical paper (C5 against S11). If agents fail visibly - injected tool output, cascading state errors, memory that degrades with self-evolution (R1, R3, R4) - enterprises can slow rollouts, and there is no validated way to prove an agent is ready for more autonomy (R8). Filings already list autonomous agent behaviour as a hard-to-audit risk and agents as a new attack and fraud surface (M10), and Figma states third-party agents may circumvent its pricing (M9). In that world the theme is a cost centre and a liability line rather than a revenue driver. *(ai_interpretation)* [C1, C3, C5, R1, R3, R4, R8, M9, M10]

**Catalysts:**
- Companies disclosing agent-specific revenue, seat counts or customer numbers rather than product descriptions *(forecast)* [M1, M4, M8]
- An agreed reliability or assurance standard that lets enterprises justify lower supervision of agents *(forecast)* [R8, S5, S10]
- A high-profile agent security or fraud incident forcing faster procurement of guardrails and authorization *(forecast)* [S3, R4, M10]
- Continued MCP-style interoperability adoption between platforms and third-party agents *(forecast)* [M3, M9]

**Risks:**
- Final task success hides unreliable behaviour: about 31% of successful runs in one benchmark still failed a harness reliability criterion, and run-level error rates are decoupled from final success *(ai_interpretation)* [R2]
- Rare but highly critical failures (validation, output errors) can cascade across steps, so average error rates understate tail risk *(ai_interpretation)* [R1]
- Agents that keep learning from accumulated memory can become less trustworthy over time, including on benign tasks *(ai_interpretation)* [R3]
- Tool use widens the attack surface - compromised tool outputs and injected instructions are threat channels beyond adversarial prompts *(ai_interpretation)* [R4]
- Company filings themselves flag unpredictable autonomous agent behaviour, agents as an attack and fraud vector, and competitive disruption from autonomous agents *(ai_interpretation)* [M10]
- Third-party autonomous agents may circumvent a platform's pricing and reduce its control over distribution and monetization *(ai_interpretation)* [M9]
- Most agent-linked equities checked have pulled back sharply over the past month with elevated volatility (Alphabet -20.3% over 3 months and 52.6% annualised volatility; Snowflake 61.3% annualised; Palantir 58.9% annualised), which raises timing risk around any theme exposure *(ai_interpretation)* [T3, T4, T9, T10, T7, T8, T11]

**What would invalidate this thesis:**
- Filings stop attributing new products or revenue categories to agents, or vendors quietly drop agent branding while continuing the same features *(forecast)* [M1, M4, M8]
- A widely reported agent-caused security, fraud or data-integrity failure that leads enterprises to restrict autonomous operation *(forecast)* [S3, R1, R4, M10]
- Evidence that agent platforms mainly cannibalise existing seat-based software revenue rather than expanding spend, consistent with the pricing-circumvention warning in one filing *(forecast)* [M9]
- Reliability research showing the failure modes are not improving, or that assurance frameworks remain unvalidated and unused by buyers *(forecast)* [R2, R8]

**Conflicting evidence:**
- C1 weakens S2: the 'process-level drift' result comes from 240 trials in a single enterprise system with no longitudinal observation, counts the authors' own template flags rather than demonstrated harm, and the paper itself lists longitudinal validation as future work. *(ai_interpretation)* [C1, S2]
- C3 weakens S3: the claim that agent frameworks and agent research do not address the identified vulnerabilities is the authors' own assertion from a mid-2024 preprint, and the paper's defences were evaluated only by its own experiments. *(ai_interpretation)* [C3, S3]
- C4 weakens S4: one authorization source extends OAuth 2.0 and OpenID Connect, while the other calls itself a preliminary, falsifiable hypothesis with a zk-SNARK proof of concept, so 'multiple works converging' overstates maturity. *(ai_interpretation)* [C4, S4]
- C5 weakens S11: the 'shared research direction' toward runtime gating rests on one proof of concept on a single platform and one purely theoretical paper that defers empirical work. *(ai_interpretation)* [C5, S11]
- C6 weakens S5, S9 and S12: the visibility, infrastructure and sector-impact claims come from position, conceptual or governance papers with no empirical test of effectiveness, and feasibility, circumvention and privacy costs are unquantified. *(ai_interpretation)* [C6, S5, S9, S12]
- R5 shows the safety literature contradicts itself: some papers say agent safety methods trade away task utility, others claim their own methods avoid that trade-off, and the claims rest on author-selected benchmarks, so the conflict is not resolvable from this evidence. *(ai_interpretation)* [R5]
- Company filings describe agent products and risk exposure but are not adoption proof; the only adoption-like figure in the set is an unverified social post claiming over half of enterprises run agentic AI in production. *(ai_interpretation)* [M1, M8, X4]

**Companies named by cited evidence:**
- Salesforce, Inc.: Markets Agentforce as a platform for building and deploying autonomous agents across business functions, embedded in its applications with Slack as the conversational interface (M1); also cites agents as a new attack and fraud vector (M10). [M1, M10]
- Amazon.com, Inc.: Launched a public preview of Bedrock Managed Agents for production enterprise agents and previewed the open-source Strands Box sandbox for agent behaviour rules (M2). [M2]
- Snowflake Inc.: Acquired Natoma, an enterprise Model Context Protocol platform for AI agents, for preliminary consideration of $128.3m, and positions its data platform as an agent foundation (M3). Price/timing: down 19.7% over 1 month with 61.3% annualised volatility (T9, T10). [M3, T9, T10]
- Microsoft Corp: Ships agentic AI within its Dynamics business applications portfolio for small and large organizations (M4); cites autonomous agent behaviour that is hard to predict or audit as a risk (M10). [M4, M10]
- Alphabet Inc.: Offers Gemini Enterprise for teams to discover, create, share and run AI agents and uses agents internally (M5); cites agents as a risk theme (M10). Price/timing: down 20.3% over 3 months, 14.5% below its 50-day average, 52.6% annualised volatility (T3, T4). [M5, M10, T3, T4]
- Meta Platforms, Inc.: Launched Muse, an agentic AI, and says it expects to increase investment in generative and agentic AI while acknowledging it may not generate profits from them (M6); cites agents as an attack vector (M10). Price/timing: down 15.4% over 1 month with 41.0% annualised volatility (T5, T6). [M6, M10, T5, T6]
- Oracle Corp: Embeds generative and agentic AI in its OCI cloud infrastructure offerings and across many product offerings (M7). [M7]
- Atlassian Corp (TEAM): Named in company-scout evidence as active on AI agents (5 SEC report mentions) with fiscal 2026 revenue $6.57bn, growth +26.0% and R&D at 49.7% of revenue; next-runner score 50/100, a transparent heuristic and not a prediction. Mid-cap scale but more disclosure risk than mega-caps. [K2]
- DigitalOcean Holdings, Inc. (DOCN): Named in company-scout evidence as active on AI agents (6 SEC report mentions) with fiscal 2025 revenue $0.90bn, growth +15.5% and R&D 17.9% of revenue; next-runner score 50/100. Small by revenue, so thinner disclosure and higher risk. [K1]
- Amplitude, Inc. (AMPL): Named in company-scout evidence as active on AI agents (4 SEC report mentions) with fiscal 2025 revenue $0.34bn, growth +14.7% and R&D 28.4% of revenue; next-runner score 50/100. Small company, less information available. [K3]
- Klaviyo, Inc. (KVYO): Named in company-scout evidence as active on AI agents (4 SEC report mentions) with fiscal 2025 revenue $1.23bn, growth +31.6% and R&D 23.6% of revenue; next-runner score 50/100. Mid-cap, and also cites autonomous agents as a competitive disruption risk (M10). [K4, M10]
- Figma, Inc. (FIG): Named in company-scout evidence as active on AI agents (3 SEC report mentions) with fiscal 2025 revenue $1.06bn, growth +41.0% and R&D 97.5% of revenue; next-runner score 50/100. It states third-party autonomous agents may circumvent its pricing and reduce its control over distribution, and opened its MCP server to third-party agents in March 2026 (M9). Higher risk profile. [K5, M9]
- BILL Holdings, Inc. (BILL): Named in company-scout evidence as active on AI agents (5 SEC report mentions) with fiscal 2026 revenue $1.65bn, growth +13.0% and R&D 18.2% of revenue; next-runner score 45/100. Mid-cap; also cites agents as an attack and fraud vector (M10). [K6, M10]

### Reliability, security and evaluation tooling for agents

Technologies: process-level agent evaluation, agent failure taxonomies and benchmarking harnesses, agent safety alignment, runtime action gating and proof-carrying correctness checks, agent visibility, identifiers and activity logging

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The gap is documented but the tooling evidence is early. Detailed failure taxonomies show frequent recoverable errors (tool use, state tracking) alongside rarer highly critical ones (validation, output) that can cascade (R1), and process-level checks catch deviations that final-output tests miss (S2, though C1 limits that result). One benchmark finds about 31% of successful runs still fail a reliability criterion (R2). Set against that, the assurance framework proposed for reporting agent reliability is explicitly conceptual and unvalidated (R8), and the strongest-looking prediction result may be inflated by how its labels were built (R6). No cited finding names a vendor selling or a customer paying for this tooling, so near-term evidence is problem definition, not market. *(ai_interpretation)* [R1, R2, R8, R6, S2, C1] | medium |
| medium_1_3y | If enterprises expand agent autonomy, standardised evaluation and guardrails become a prerequisite, and the research direction is real: alignment work, failure-trajectory self-evolution, and harness reliability benchmarking all exist (R2, R4, R5). But the evidence for a durable commercial layer is absent here - it rests on the implication of vendor risk disclosures (M10) rather than on any tooling company, contract or deployment named in these findings. Whether safety can be improved without losing utility is openly contested (R5), which is exactly the question a buyer would need answered. *(forecast)* [R2, R4, R5, M10] | low |
| long_3_5y | Over 3-5 years the plausible shape is agent identity, monitoring and logging embedded in governance regimes, as proposed by visibility and infrastructure papers (S5, S9), and cryptographically or formally verifiable authorization binding agent, request, context and policy (S4). The findings give no basis to size that market or to say who supplies it: the authorization direction is one framework proposal plus one explicit hypothesis-with-PoC (C4), the runtime gating direction is one prototype and one theoretical paper (C5), and the governance mechanisms are untested proposals with unquantified circumvention and privacy costs (C6). Long-horizon confidence is low. *(forecast)* [S4, S5, S9, C4, C5, C6] | low |

**Bull case:** The failure evidence is unusually concrete for a young field, which is what a tooling market needs to form: documented failure taxonomies with severity and cascading behaviour (R1), benchmarks showing final success masks unreliable runs (R2), and a clear statement that no agreed, validated way to report agent reliability exists (R8). Multi-agent coordination robustness and memory-driven trust decay are flagged as open problems with early methods attached (R3, R7), and agent-specific attack channels via tools and injected instructions are identified rather than hypothetical (R4). Governance research converges on concrete mechanisms - agent identifiers, real-time monitoring, activity logging (S5) - and on authorization bound to request, context and policy (S4), which is the earliest plausible form of an enforceable control plane. *(ai_interpretation)* [R1, R2, R3, R4, R7, R8, S4, S5]

**Base case:** Evaluation, alignment and governance remain primarily research and framework activity in this evidence set, with adoption pulled along by platform vendors embedding their own guardrails rather than by a distinct tooling market. Progress is real but incremental: methods exist, results are contested, and the strongest quantitative claims are the ones most vulnerable to methodological criticism (R5, R6, R7, C1, C4, C5). Expect capability and constraint to advance together, with supervision levels rising slowly because no validated readiness test exists (R8). *(forecast)* [R5, R6, R7, R8, C1, C4, C5]

**Bear case:** The bear case is that the constraint layer stays academic and gets absorbed into platform features at no separate margin. The evidence supports this reading: no company in these findings is named as selling reliability, evaluation or governance tooling, the assurance framework is explicitly unvalidated (R8), the most impressive predictive result may reflect label construction rather than predictive power (R6), multi-agent robustness evidence is a 2024 preprint with theoretical resilience claims (R7), and several headline 'solutions' are one prototype or one hypothesis (C4, C5). Where safety methods do work, the literature disputes whether they cost task performance (R5), which removes the buyer's main reason to pay separately. Meanwhile governance mechanisms such as visibility and logging are proposals with unquantified feasibility, circumvention and privacy costs (C6), and proposed agent authorization standards could equally be delivered by incumbent identity vendors. *(ai_interpretation)* [R5, R6, R7, R8, C4, C5, C6]

**Catalysts:**
- An enterprise or regulator adopting a specific, published reliability or assurance standard for agents *(forecast)* [R8, S5, S10]
- Independent replication of agent reliability-prediction or evaluation results outside the original authors' benchmark *(forecast)* [R6, R2, S10]
- Security research showing agent tool-chain attacks succeeding in production, forcing budget into guardrails *(forecast)* [S3, R4, M10]

**Risks:**
- The strongest quantitative reliability claims in the set are the weakest methodologically (label construction for the 0.970 ROC-AUC; self-built benchmarks), so progress may be overstated *(ai_interpretation)* [R6, R2, C2]
- Whether safety improves without utility loss is contested across the alignment papers, and the dispute rests on author-selected benchmarks *(ai_interpretation)* [R5]
- Governance and infrastructure mechanisms are proposed but untested, with feasibility, circumvention and privacy or concentration-of-power costs unquantified *(ai_interpretation)* [S5, S9, C6]
- Agents that keep learning from memory may degrade in trustworthiness after deployment, which no current metric in this evidence set captures *(ai_interpretation)* [R3]

**What would invalidate this thesis:**
- Evidence that platform vendors deliver sufficient evaluation, guardrails and logging natively, removing demand for independent tooling *(forecast)* [M1, M4, M5]
- Repeated failure to replicate process-level evaluation, reliability prediction or safety-alignment gains outside the original authors' settings *(forecast)* [R6, R5, C1]
- Adoption of a competing, non-cryptographic authorization approach that makes the verifiable-authorization line redundant *(forecast)* [S4, C4]

**Conflicting evidence:**
- C2 weakens S6: the structural failure of binary detectors and the perfect agent F1 come from a controlled 30-run benchmark of browser-automation agents, the authors attribute the signal to a Playwright artifact, and a saturated self-built test is weak evidence for general detection. *(ai_interpretation)* [C2, S6]
- C5 weakens S11 and C4 weakens S4, meaning the two most concrete 'control plane' stories in the science set are one prototype plus one theoretical paper and one protocol extension plus one falsifiable hypothesis respectively. *(ai_interpretation)* [C5, C4, S11, S4]
- R7 shows the multi-agent robustness evidence is thin: the only directly relevant paper is a 2024 preprint with theoretical resilience claims, tested empirically only on a sensor-network case study, with hallucination and adversarial agents used as motivation rather than measured. *(ai_interpretation)* [R7]

**Companies named by cited evidence:**
- none (no company evidence in the cited findings)

### Agent authorization, identity and agent-to-agent commerce rails

Technologies: cryptographically verifiable agent authorization, delegated identity for agents, agent identifiers and activity logging, Model Context Protocol connectivity, agent-initiated transactions and payments

| Horizon | Assessment | Confidence |
|---|---|---|
| near_0_12m | The only near-term evidence of agent-to-agent and agent-to-commerce infrastructure comes from social posts, which are unverified claims and cannot carry a rating: reportedly a Personal Agent Protocol 0.1 with OAuth-style scoped auth from payment and commerce providers, and a crypto-cloud service letting agents buy API calls (X2). On the filing side, the concrete evidence is a company paying $128.3m for an enterprise Model Context Protocol platform (M3) and a design platform opening its MCP server to third-party agents in March 2026 while warning those agents may circumvent its pricing (M9). The research side offers one protocol extension and one self-described preliminary hypothesis with a zk-SNARK proof of concept (S4, C4). Near-term evidence is therefore thin and mostly directional. *(ai_interpretation)* [X2, M3, M9, S4, C4] | low |
| medium_1_3y | The medium-term question is whether agent authorization settles into extensions of existing identity and access protocols or into a new layer. The evidence points at extension in one case (an OAuth 2.0 and OpenID Connect extension) and at a replacement-style argument in another that existing mechanisms lack cryptographic evidence of policy satisfaction (S4, C4), so the outcome is genuinely open. Governance proposals for agent identifiers, real-time monitoring and activity logging (S5) would, if adopted, create the identifiers such commerce would need, but they report no empirical test (C6). No finding names a customer, standard body adoption or contract for this layer. *(forecast)* [S4, S5, C4, C6] | low |
| long_3_5y | Over 3-5 years the plausible long-horizon story - agents transacting, delegating and being held accountable through verifiable authorization and external infrastructure - is exactly the part of the evidence base that is least tested. The infrastructure argument that internal shaping is insufficient and shared protocols for attributing and remedying actions are needed is an unverified claim in this set (S9), runtime gating and proof-carrying checks are one prototype and one theoretical paper (S11, C5), and the actuarial per-action gating idea defers empirical work to companion papers (C5). Confidence is low and the shape, if any, cannot be inferred from these findings. *(forecast)* [S9, S11, C5] | low |

**Bull case:** If agents are to act autonomously on behalf of users and firms, they need identity, scoped permissions and an auditable record, and the research direction is moving toward binding the agent, its request, the execution context and policy satisfaction into a verifiable relation that extends established protocols rather than replacing them (S4). Governance work already proposes the ingredients - agent identifiers, real-time monitoring, activity logging applicable from centralized to decentralized deployments (S5) - and external agent infrastructure is argued as a necessary complement to internal shaping (S9). On the commercial side, platforms are already standardising agent-to-tool connectivity: a $128.3m acquisition of an enterprise MCP platform (M3) and a design platform opening its MCP server to third-party agents (M9), with reported commerce and crypto-rail experiments in the social data (X2). *(ai_interpretation)* [S4, S5, S9, M3, M9, X2]

**Base case:** Authorization and agent commerce most likely arrive as extensions to identity and access systems that enterprises already run, with agent identifiers and scoped credentials added by existing suppliers, rather than as a new verifiable-authorization layer. The filing evidence supports connectivity standardisation (M3, M9) more than it supports new authorization primitives, and the strongest research claims are a hypothesis with a proof of concept and a prototype (C4, C5). Access to agent-mediated commerce could also cut both ways for platform owners, as one filing warns agents may circumvent pricing and reduce control over distribution and monetization (M9). *(forecast)* [M3, M9, S4, C4, C5]

**Bear case:** The bear case is that this is a standards problem with no clear revenue pool and a governance problem with no enforcement. The infrastructure argument is an unverified claim in this evidence set (S9), visibility mechanisms are proposals with unquantified feasibility, circumvention and privacy or concentration-of-power costs (C6), and the two most concrete control-plane works are one prototype and one theoretical paper (C5, S11) plus one protocol extension and one falsifiable hypothesis (C4). Meanwhile the only near-term commerce signals are unverified social posts (X2), and the clearest commercial fact in the theme - a platform opening its MCP server - came with an explicit warning that third-party agents may undermine its pricing and control over distribution (M9). If that dynamic spreads, agent connectivity could be value-destructive for incumbent application layers rather than accretive. *(ai_interpretation)* [S9, C6, C5, S11, C4, X2, M9]

**Catalysts:**
- A standards body or large platform formally adopting an agent authorization or identity extension in production *(forecast)* [S4, M3, M9]
- A regulated requirement for agent activity logging or attribution, making visibility mechanisms mandatory rather than optional *(forecast)* [S5, S12]
- Verified evidence of agent-initiated transactions at scale with disclosed volumes, replacing the current social-post claims *(forecast)* [X2]

**Risks:**
- The commercial evidence for agent-to-agent commerce is unverified social posts and cannot be relied on *(ai_interpretation)* [X2]
- Authorization and runtime-gating claims rest on a hypothesis with a proof of concept and a single-platform prototype, not on demonstrated control of side effects in adversarial deployments *(ai_interpretation)* [C4, C5, S11]
- Governance mechanisms may be circumventable, raise privacy concerns, or concentrate power, and none of these costs is quantified in the findings *(ai_interpretation)* [C6, S5, S9]
- Agent connectivity may erode platform pricing and distribution control, as one filer states directly *(ai_interpretation)* [M9]

**What would invalidate this thesis:**
- Incumbent identity and access vendors absorb agent authorization as a feature of existing protocols, leaving no distinct layer *(forecast)* [S4, C4]
- MCP-style connectivity does not become a paid layer, for example because it is commoditised as open infrastructure *(forecast)* [M3, M9]
- Reported agent commerce and payment-rail projects fail to appear in any verifiable disclosure *(forecast)* [X2]

**Conflicting evidence:**
- C6 directly undercuts the S5/S9 governance basis of this theme: visibility and infrastructure papers propose mechanisms but report no empirical test, and feasibility, circumvention and privacy costs remain unquantified. *(ai_interpretation)* [C6, S5, S9]
- C4 undercuts the framing that authorization research is converging: one source extends existing protocols while the other argues existing mechanisms lack cryptographic evidence of policy satisfaction and calls itself preliminary. *(ai_interpretation)* [C4, S4]
- The connectivity evidence points in two directions: a large paid acquisition of an MCP platform (M3) versus a filer warning that third-party agents may circumvent pricing and cut monetization control (M9). *(ai_interpretation)* [M3, M9]

**Companies named by cited evidence:**
- Snowflake Inc.: Acquired Natoma, an enterprise Model Context Protocol platform for AI agents, for preliminary purchase consideration of $128.3m - the clearest paid evidence in this set of demand for agent-connectivity infrastructure (M3). Price/timing: down 19.7% over 1 month with 61.3% annualised volatility (T9, T10). [M3, T9, T10]
- Figma, Inc. (FIG): Introduced the ability for third-party autonomous agents to create and modify design assets via its MCP server in March 2026, while stating those agents may circumvent its pricing and reduce its control over distribution and monetization (M9). Mid-cap with high R&D ratio and a two-sided exposure to the theme. [M9, K5]

## Evidence: academic research
Status: ok. Based on titles, metadata and abstracts only. No full text was read. arXiv items are preprints and are not peer reviewed.

OpenAlex works per year with the exact topic phrase in title/abstract: {2020: 212, 2021: 277, 2022: 306, 2023: 493, 2024: 1077, 2025: 4480, 2026: 15182}
Research Acceleration 2024->2025: 1077 -> 4480 (316.0% YoY). OpenAlex works whose title or abstract contains the exact phrase "AI agents", per publication year. Synonyms and abbreviations are not counted, and the number is not normalised for overall growth in publishing. The current (partial) year is excluded.
This year so far (1 Jan to 10-10): 2025 2977 -> 2026 13252 (345.1%, trend: rising). OpenAlex works with the exact phrase 'AI agents' in title or abstract published 1 Jan–10 Oct 2026 vs the same dates in 2025. The last 30 days are left out of both years because new papers take weeks to be indexed.

- **[S1]** *(verified_fact, confidence medium)* Research on AI agents is driven by benchmarks, but a widely cited analysis argues current agent benchmarks over-focus on accuracy, leading to needlessly complex and costly state-of-the-art agents and mistaken conclusions about where accuracy gains come from.
  - source: [AI Agents That Matter](https://doi.org/10.48550/arxiv.2407.01502) (OpenAlex, 2024-07-01, abstract_only)
  - excerpt: "there is a narrow focus on accuracy without attention to other metrics. As a result, SOTA agents are needlessly complex and costly"
- **[S2]** *(verified_fact, confidence medium)* Final-output evaluation can miss process-level behavioral drift in enterprise agents: in a controlled study, most runs that passed all final numerical checks still contained an evaluator-detected deviation in tool selection, arguments, execution order, or database integrity.
  - source: [Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills](https://arxiv.org/abs/2610.01833v1) (arXiv, 2026-10-01, abstract_only)
  - excerpt: "Of 175 trials passing all applicable final numerical checks, 162 (92.6 percent; Wilson 95 percent CI: 87.7-95.6 percent) contained another evaluator-detected deviation."
- **[S3]** *(verified_fact, confidence medium)* A system-security analysis of LLM-based agents identifies vulnerabilities that the current agent-building frameworks and agent-improvement research do not address.
  - source: [Security of AI Agents](https://arxiv.org/abs/2406.08689v3) (arXiv, 2024-06-12, abstract_only)
  - excerpt: "These potential vulnerabilities are not addressed by the frameworks used to build the agents, nor by research aimed at improving the agents."
- **[S4]** *(ai_interpretation, confidence medium)* Multiple works propose framing agent authorization as a cryptographically or formally verifiable relation that binds the agent, its request, the execution context, and policy satisfaction, extending established identity and access protocols rather than replacing them.
  - source: [Authenticated Delegation and Authorized AI Agents](https://doi.org/10.48550/arxiv.2501.09674) (OpenAlex, 2025-01-16, abstract_only)
  - source: [Cryptographically verifiable authorization for autonomous AI agents: a falsifiable hypothesis and proof of concept](https://arxiv.org/abs/2607.21325v3) (arXiv, 2026-07-23, abstract_only)
  - reasoning: src_1b70ec88bc proposes an authenticated/authorized delegation framework extending OAuth 2.0 and OpenID Connect; src_ca33c17412 formalizes agent authorization as a cryptographically verifiable relation with a Groth16 zk-SNARK proof of concept. Both address binding agent identity, request, and context, though neither is validated at production scale.
- **[S5]** *(verified_fact, confidence medium)* Governance research proposes concrete visibility mechanisms for AI agents—agent identifiers, real-time monitoring, and activity logging—and analyses how these apply across centralized to decentralized deployments.
  - source: [Visibility into AI Agents](https://doi.org/10.1145/3630106.3658948) (OpenAlex, 2024-06-03, abstract_only)
  - excerpt: "we assess three categories of measures to increase visibility into AI agents: agent identifiers, real-time monitoring, and activity logging."
- **[S6]** *(verified_fact, confidence low)* Binary human-vs-bot detectors structurally misclassify AI agents browsing via browser automation; a three-class detection framework adding an explicit agent class achieved perfect agent F1 in the reported benchmark.
  - source: [What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation](https://arxiv.org/abs/2607.26935v1) (arXiv, 2026-07-29, abstract_only)
  - excerpt: "an MLP binary classifier misclassifies 39.1% of real AI agents as human and a SAINT binary transformer misclassifies 34.5%"
  - reasoning: The abstract reports strong results but the discriminative signal is described as a Playwright browser-automation artifact rather than evidence of agent reasoning, which limits how broadly the detection method generalizes.
- **[S7]** *(verified_fact, confidence medium)* Review literature distinguishes 'AI Agents' (modular LLM/LIM-driven systems for task-specific automation) from 'Agentic AI' (multi-agent collaboration, dynamic task decomposition, persistent memory, coordinated autonomy).
  - source: [AI Agents vs. Agentic AI: A Conceptual taxonomy, applications and challenges](https://doi.org/10.1016/j.inffus.2025.103599) (OpenAlex, 2025-08-22, abstract_only)
  - excerpt: "Agentic AI systems, which, in contrast to AI Agents, represent a paradigm shift marked by multi-agent collaboration, dynamic task decomposition, persistent memory, and coordinated autonomy."
- **[S8]** *(verified_fact, confidence medium)* A review positions 'AI scientists' as collaborative biomedical agents that combine human creativity with AI analysis of large datasets and autonomous planning of discovery workflows.
  - source: [Empowering biomedical discovery with AI agents](https://doi.org/10.1016/j.cell.2024.09.022) (OpenAlex, 2024-10-01, abstract_only)
  - excerpt: "We envision "AI scientists" as systems capable of skeptical learning and reasoning that empower biomedical research through collaborative agents"
- **[S9]** *(unverified_claim, confidence low)* A separate line of work argues that shaping agent behaviour internally is insufficient and that external 'agent infrastructure'—shared protocols for attributing actions, shaping interactions, and remedying harmful actions—is needed for ecosystems of heterogeneous agents.
  - source: [Infrastructure for AI Agents](https://doi.org/10.48550/arxiv.2501.10114) (OpenAlex, 2025-01-17, abstract_only)
  - excerpt: "we propose the concept of agent infrastructure: technical systems and shared protocols external to agents that are designed to mediate and influence their interactions with and impacts on their environments."
  - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- **[S10]** *(verified_fact, confidence medium)* Methodological papers call for extending preregistration practices to 'in silico' experiments with AI agents, cataloguing researcher degrees of freedom such as model selection, prompt wording, settings, and outcome-contingent redesign.
  - source: [Preregistration for Experiments with AI Agents](https://arxiv.org/abs/2606.11217v1) (arXiv, 2026-05-03, abstract_only)
  - excerpt: "preregistration practices -- central to improving the credibility of human subjects experiments -- should now be extended to experiments with AI agents"
- **[S11]** *(ai_interpretation, confidence low)* Several works propose runtime safety layers for agents—proof-carrying correctness checks for untrusted agents operating on production data, and a per-action actuarial/toll runtime that gates executed actions—showing a shared research direction toward constraining autonomous side effects rather than only training agents to behave.
  - source: [Safe, Untrusted, "Proof-Carrying" AI Agents: toward the agentic lakehouse](https://arxiv.org/abs/2510.09567v1) (arXiv, 2025-10-10, abstract_only)
  - source: [Foundations of a Time-Consistent Counterfactual Actuarial Runtime for Autonomous AI Agents](https://arxiv.org/abs/2605.26508v1) (arXiv, 2026-05-26, abstract_only)
  - reasoning: src_53cfb1f43d demonstrates a proof-of-concept where untrusted agents repair data pipelines under correctness checks inspired by proof-carrying code; src_b829c26a18 is a foundational, largely theoretical framework for per-action risk tolls. Both are arXiv preprints, and src_b829c26a18 states its empirical companion work is separate.
- **[S12]** *(verified_fact, confidence low)* Industry-facing analyses argue agentic systems can reshape sectors via decentralized decision-making and real-time automation, but flag accountability attribution, legacy-system compatibility, and bias as critical open challenges requiring governance frameworks.
  - source: [AI Agents and Agentic Systems: A Multi-Expert Analysis](https://doi.org/10.1080/08874417.2025.2483832) (OpenAlex, 2025-04-24, abstract_only)
  - excerpt: "the integration of these systems raises critical challenges, including issues of attribution and shared accountability in decision-making, compatibility with legacy systems, and addressing biases in AI-driven processes"
  - reasoning: This is a multi-expert perspective paper rather than an empirical study; the claims are forward-looking and not experimentally validated.

**Emerging directions:**
- External agent infrastructure and inter-agent protocols
- Cryptographically verifiable agent authorization (zk-SNARK-based)
- Three-class human/bot/AI-agent detection
- Process-level and trajectory-based agent evaluation
- Runtime safety layers: proof-carrying correctness and per-action actuarial tolls
- Preregistration norms for in silico agent experiments
- Taxonomy separating AI Agents from Agentic AI
- AI scientist agents for biomedical discovery

**Open problems:**
- Lack of holdout sets and reproducibility in agent benchmarks
- Needless complexity and cost of state-of-the-art agents under accuracy-only optimization
- Separation of identity binding, authorization-request binding, and runtime execution binding in secure agent design
- Behavioral drift not captured by final-output evaluation
- Overfitting and shortcut-taking by agents on benchmarks
- Binary detector label spaces that cannot represent AI agents
- Longitudinal validation under actual tool/API evolution
- Emergent behavior and coordination failure in multi-agent systems
- Attribution and shared accountability in agentic decision-making

**Limitations:**
- Analysis is based only on titles, metadata and abstracts; no full papers were read.
- Several items are arXiv preprints and have not been peer reviewed.
- src_3f9ff28552 (Governing AI Agents) is metadata_only with no abstract, so it could not contribute evidence.
- Several sources are conceptual or review papers rather than empirical studies; their claims are not experimentally validated in the abstracts.
- The sample does not represent the entire AI-agent literature; findings are limited to the retrieved set.
- No commercial, deployment-cost or investment conclusions can be drawn from research abstracts.

## Evidence: risks and contrarian findings
Status: ok. Risk search queries: ['AI agent reliability failures', 'LLM agent hallucination', 'agent safety alignment', 'AI agent cost scaling', 'agent evaluation limitations', 'autonomous agent security risks']

- **[R1]** *(verified_fact, confidence medium)* Agent failures differ sharply in severity. Frequent failures such as tool-use and state-tracking errors are largely recoverable, while rarer failures such as validation and output errors are highly critical. Failures can also cascade across steps, so average error rates understate tail risk.
  - source: [A Hierarchical Failure Taxonomy for Reliability Assessment of AI Agents: An Empirical Analysis of the Agent Failure Atlas 2026 Benchmark](https://doi.org/10.6025/jitr/2026/17/4/204-226) (OpenAlex, 2026-01-01, abstract_only)
  - excerpt: "high prevalence but largely recoverable failures (e.g., tool use and state tracking errors) contrast sharply with low prevalence but highly critical failures (e.g., validation and output errors)"
  - reasoning: This rests on a single abstract from a small journal with 0 citations. The 'Agent Failure Atlas 2026' benchmark cannot be checked here. The 3,336 runs are a moderate sample, and the abstract does not say how many tasks, models or domains they cover.
- **[R2]** *(verified_fact, confidence medium)* Final task success can hide unreliable agent behaviour. In one benchmark, about 31% of successful runs still failed at least one harness reliability criterion, and harness scores varied widely across harnesses. A separate study found run-level error rates decoupled from final success.
  - source: [Trial by Trace: Benchmarking AI Agent Harnesses for Reliability and Failure Attribution](https://doi.org/10.48550/arxiv.2610.32285) (OpenAlex, 2026-10-23, abstract_only)
  - source: [A Hierarchical Failure Taxonomy for Reliability Assessment of AI Agents: An Empirical Analysis of the Agent Failure Atlas 2026 Benchmark](https://doi.org/10.6025/jitr/2026/17/4/204-226) (OpenAlex, 2026-01-01, abstract_only)
  - excerpt: "31.1% of runs achieve task success despite failing at least one harness criterion"
  - reasoning: The TraceTrial-Bench result is an arXiv preprint, so it is not peer reviewed. Its evaluation uses LLM-based evidence modules, and the 95 tasks are authored by the benchmark's creators. Read together, the two papers suggest that outcome-only scores can overstate production readiness. Self-correction can also mask underlying errors. That synthesis is my interpretation.
- **[R3]** *(verified_fact, confidence low)* Agents that learn from accumulated memory can become less trustworthy over time, even on benign tasks. A decline in trustworthiness with continual 'self-evolution' is a safety risk for agents that keep learning after deployment.
  - source: [TAME: A Trustworthy Test-Time Evolution of Agent Memory with Systematic Benchmarking](https://arxiv.org/abs/2602.03224v2) (arXiv, 2026-02-03, abstract_only)
  - excerpt: "we construct the Trust-Memevo benchmark and find that agents exhibit an overall decline in trustworthiness across multiple tasks during benign task evolution"
  - reasoning: This is a single arXiv preprint. The Trust-Memevo benchmark was built by the same authors who propose the TAME fix, so the problem and the solution are evaluated on authors' own terms. The headline accuracy gain is reported on AIME, a math benchmark, not on an agentic safety setting. No independent replication is visible.
- **[R4]** *(verified_fact, confidence medium)* Tool-using agents have a wider attack surface than chat models, because compromised tool outputs and injected instructions are threat channels in addition to adversarial user prompts. One preprint claims that frontier models lower attack barriers enough to make current alignment frameworks inadequate for deployment.
  - source: [Agent Safety Alignment via Reinforcement Learning](https://arxiv.org/abs/2507.08270v1) (arXiv, 2025-07-11, abstract_only)
  - source: [AgentDoG 1.5: A Lightweight and Scalable Alignment Framework for AI Agent Safety and Security](https://arxiv.org/abs/2605.29801v1) (arXiv, 2026-05-28, abstract_only)
  - source: [On-Policy Self-Evolution via Failure Trajectories for Agentic Safety Alignment](https://arxiv.org/abs/2605.11882v1) (arXiv, 2026-05-12, abstract_only)
  - excerpt: "advanced frontier AI models drastically lower attack barriers, rendering current agent alignment frameworks inadequate for real-world deployment."
  - reasoning: All three sources are arXiv preprints and are not peer reviewed. The 'inadequate for real-world deployment' statement is the authors' framing to motivate their own method. It is not an empirical finding in the abstract. The threat models come from papers that propose defences, so severity may be emphasised.
- **[R5]** *(ai_interpretation, confidence low)* Whether agent safety can be improved without losing task performance is contested. One paper says existing methods often trade away utility, while others claim their own methods avoid the trade-off. The claims rest on author-selected benchmarks and relative gains, which makes the contradiction hard to resolve.
  - source: [On-Policy Self-Evolution via Failure Trajectories for Agentic Safety Alignment](https://arxiv.org/abs/2605.11882v1) (arXiv, 2026-05-12, abstract_only)
  - source: [Agent Safety Alignment via Reinforcement Learning](https://arxiv.org/abs/2507.08270v1) (arXiv, 2025-07-11, abstract_only)
  - source: [SafeEvolve: Harness-Policy Co-Evolution from Agent Experience for Safety Alignment](https://arxiv.org/abs/2609.02786v1) (arXiv, 2026-09-02, abstract_only)
  - source: [AgentDoG 1.5: A Lightweight and Scalable Alignment Framework for AI Agent Safety and Security](https://arxiv.org/abs/2605.29801v1) (arXiv, 2026-05-28, abstract_only)
  - excerpt: "improving agent safety comes at the cost of degraded task performance"
  - reasoning: FATE's abstract states the trade-off as a problem with existing methods. The other three preprints each claim to solve or reduce it. Some use self-built benchmarks, and results are given as relative reductions in attack success rate (e.g. '3x', '33.5%') without baseline absolute rates in the visible abstracts. Small models (0.8B-8B) are used in some. All are preprints, so it is unclear whether the gains hold against adaptive attackers or in real deployments.
- **[R6]** *(ai_interpretation, confidence medium)* The reliability-prediction result looks strong but is weakened by how it was built. Success labels were reconstructed from aggregate score distributions rather than observed per instance, so the very high ROC-AUC (0.970) may reflect the label construction and not real predictive power.
  - source: [Trajectory Reliability Prediction for Generalist AI Agents: Tool-Use Failure Analysis and Success Forecasting on ZClawBench](https://doi.org/10.51903/jtie.v5i1.539) (OpenAlex, 2026-04-30, abstract_only)
  - excerpt: "the binary target is reconstructed from official model-by-category score distributions and treated as a modeling assumption."
  - reasoning: The abstract itself says the target is a modeling assumption. Features such as task difficulty and no-progress behaviour may partly encode the aggregate scores used to build the labels. That leakage risk is my inference, not something the paper states. The data is one benchmark of 696 trajectories across 116 tasks.
- **[R7]** *(ai_interpretation, confidence low)* Evidence on the robustness of multi-agent LLM coordination is thin in this set. The only directly relevant paper is a 2024 preprint whose resilience claims are theoretical, backed by empirical validation and a sensor-network case study. LLM agent hallucination and adversarial agents are treated as motivation, not measured.
  - source: [IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems](https://arxiv.org/abs/2410.16237v2) (arXiv, 2024-10-21, abstract_only)
  - reasoning: This is a single arXiv preprint (not peer reviewed) and about two years old. The abstract does not report tests with real LLM agents at scale. Absence of such evidence here is a gap, not proof of failure.
- **[R8]** *(verified_fact, confidence medium)* Standardised, validated methods for reporting agent reliability are still immature. A proposed assurance framework (ARAF) with a six-metric profile is conceptual and explicitly unvalidated, so there is no agreed way to show when an agent is ready for greater autonomy.
  - source: [Evaluating Reliability of LLM-Based Agentic AI Systems: A Failure Taxonomy and the Agent Reliability Assurance Framework](https://doi.org/10.5281/zenodo.23283517) (OpenAlex, 2026-01-01, abstract_only)
  - source: [A Hierarchical Failure Taxonomy for Reliability Assessment of AI Agents: An Empirical Analysis of the Agent Failure Atlas 2026 Benchmark](https://doi.org/10.6025/jitr/2026/17/4/204-226) (OpenAlex, 2026-01-01, abstract_only)
  - source: [Trial by Trace: Benchmarking AI Agent Harnesses for Reliability and Failure Attribution](https://doi.org/10.48550/arxiv.2610.32285) (OpenAlex, 2026-10-23, abstract_only)
  - excerpt: "No new experimental results are claimed."
  - reasoning: ARAF is a narrative review hosted on Zenodo, a repository that does not peer review. It says it specifies a validation plan, not results. The other two sources each define their own taxonomy and benchmark, which suggests fragmentation across competing evaluation schemes. That reading is my inference.

**Possible hype:**
- 'Safety and effectiveness can be jointly optimized' - based on self-built and selected benchmarks in preprints, with a contradicting statement from another paper about existing trade-offs
- 'Comparable to leading closed-source models' with ~1k training samples (AgentDoG 1.5) - an authors' claim on their own benchmarks, not independently verified
- Test-time memory evolution framed as 'pivotal for AGI' - the same paper finds trustworthiness declines during benign evolution
- ROC-AUC of 0.970 for success prediction - labels were reconstructed from aggregate scores, not observed
- Benchmark 'task success' as a readiness signal - about 31% of successes in one benchmark still failed harness criteria
- 'Provable resilience' for multi-agent LLM systems - supported only by a 2024 preprint with a sensor-network case study

**Challenges to the Science findings:**
- Targets ['S2'], severity medium:
  - **[C1]** *(ai_interpretation, confidence medium)* S2 describes the result as 'process-level behavioral drift', but the study did not observe drift over time. It compared 240 trials across skills, spec variants, harnesses and models in one enterprise system. The abstract says longitudinal validation under actual API evolution is future work. The 92.6% figure counts deviations flagged by the authors' own template checks (tool selection, arguments, order, database integrity), not demonstrated harm. It also comes from a single preprint and one proprietary use case, so the generalisation to 'enterprise agents' is overstated.
    - source: [Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills](https://arxiv.org/abs/2610.01833v1) (arXiv, 2026-10-01, abstract_only)
    - reasoning: The abstract reports 162 of 175 final-check-passing trials with an 'evaluator-detected deviation' and applies the framework to one Value Aware Resiliency system. It frames longitudinal validation as remaining future work. A deviation from a prescribed trajectory is not necessarily an error. The abstract does not say how many deviations changed outcomes.
- Targets ['S6'], severity medium:
  - **[C2]** *(ai_interpretation, confidence medium)* S6 presents the 'structural' failure of binary detectors and the perfect agent F1 as a general finding. The paper's own results are limited to a controlled benchmark of browser-automation agents, with 100% recall resting on two features. The authors say the signal is a Playwright artifact. A detector built on it may fail for agents that use real input devices, human-in-the-loop operation, API-only access or other automation stacks. A perfect F1 across 30 runs on a self-built benchmark also suggests an easy, possibly saturated test.
    - source: [What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation](https://arxiv.org/abs/2607.26935v1) (arXiv, 2026-07-29, abstract_only)
    - excerpt: "The discriminative signal is a browser-automation artifact, not evidence of agent reasoning: Playwright does not emit the raw pointer-move and wheel-delta streams a physical input device produces"
    - reasoning: The authors themselves tie detection to a tooling artifact. That limits how far 'perfect F1' can be read as evidence for agent detection in general. It is a single preprint with a self-constructed benchmark.
    - citation check: relabelled ai_interpretation: a challenge is a judgement; its quoted excerpt was checked against the source
- Targets ['S3'], severity low:
  - **[C3]** *(ai_interpretation, confidence medium)* S3 is labelled verified_fact, but the claim that these vulnerabilities are not addressed by frameworks or by agent research is the authors' own assertion from their experience with typical agent workflows. It is not an independently verified fact. The paper is a mid-2024 preprint and may be dated, since agent frameworks and safety work have moved quickly. The finding also omits that the paper proposes defences evaluated only by its own experiments.
    - source: [Security of AI Agents](https://arxiv.org/abs/2406.08689v3) (arXiv, 2024-06-12, abstract_only)
    - excerpt: "Through studying and experiencing the workflow of typical AI agents, we have raised several concerns regarding their security."
    - reasoning: The abstract bases the claim on the authors' experience and on defences they designed and tested themselves. The 'not addressed by' statement is a self-reported gap, not a survey result. Later alignment papers in the evidence set (e.g. src_302c5699ae) address tool-channel threats, which weakens the 'not addressed' framing.
- Targets ['S4'], severity medium:
  - **[C4]** *(ai_interpretation, confidence medium)* S4 says 'multiple works' converge on a framing that extends established protocols rather than replacing them. The two sources differ in kind. src_1b70ec88bc extends OAuth 2.0 and OpenID Connect, so it is compatible with existing protocols. src_ca33c17412 calls itself a preliminary, falsifiable hypothesis with a zk-SNARK proof of concept. It argues that existing mechanisms lack cryptographic evidence of policy satisfaction. Presenting a hypothesis and a framework proposal as a converging research direction overstates maturity, and 'rather than replacing' fits only one of the two.
    - source: [Cryptographically verifiable authorization for autonomous AI agents: a falsifiable hypothesis and proof of concept](https://arxiv.org/abs/2607.21325v3) (arXiv, 2026-07-23, abstract_only)
    - source: [Authenticated Delegation and Authorized AI Agents](https://doi.org/10.48550/arxiv.2501.09674) (OpenAlex, 2025-01-16, abstract_only)
    - excerpt: "This study hypothesizes that agent authorization can be formalized as a cryptographically verifiable relation"
    - reasoning: The abstracts describe proposals, not validated or deployed systems. Neither reports adoption or security evaluation against real attacks. The two works also take different positions on compatibility with existing identity and access infrastructure.
- Targets ['S11'], severity low:
  - **[C5]** *(ai_interpretation, confidence medium)* S11 infers a 'shared research direction' from one prototype and one purely theoretical paper. The lakehouse paper is a proof of concept on a single platform (Bauplan) for data-pipeline repair. The actuarial paper establishes mathematical results and defers empirical work to companion papers. Neither shows that runtime gating or proof-carrying checks constrain side effects in realistic, adversarial agent deployments, so the finding overstates the evidential basis.
    - source: [Safe, Untrusted, "Proof-Carrying" AI Agents: toward the agentic lakehouse](https://arxiv.org/abs/2510.09567v1) (arXiv, 2025-10-10, abstract_only)
    - source: [Foundations of a Time-Consistent Counterfactual Actuarial Runtime for Autonomous AI Agents](https://arxiv.org/abs/2605.26508v1) (arXiv, 2026-05-26, abstract_only)
    - excerpt: "We present a proof-of-concept in which agents repair data pipelines using correctness checks inspired by proof-carrying code."
    - reasoning: One source is a case-study prototype and the other is a foundational theory paper whose empirical companion is separate. A thematic similarity between them is not evidence that the approaches work or are converging.
- Targets ['S5', 'S9', 'S12'], severity low:
  - **[C6]** *(ai_interpretation, confidence medium)* Several findings (S5, S9, S12) rest on position, conceptual or governance papers that propose mechanisms but report no empirical test of effectiveness. S5's visibility measures and S9's agent infrastructure are described as 'proposed' or 'an incomplete catalog of research directions'. The findings do not make clear that feasibility, circumvention, and privacy or concentration-of-power costs remain unquantified. The risk is that readers take proposed governance tools to be mature.
    - source: [Visibility into AI Agents](https://doi.org/10.1145/3630106.3658948) (OpenAlex, 2024-06-03, abstract_only)
    - source: [Infrastructure for AI Agents](https://doi.org/10.48550/arxiv.2501.10114) (OpenAlex, 2025-01-17, abstract_only)
    - excerpt: "Further work into understanding the measures and mitigating their negative impacts can help to build a foundation for the governance of AI agents."
    - reasoning: The abstracts describe 'potential implementations' and 'research directions' and give no empirical effectiveness data. The S5 authors themselves flag unresolved negative impacts. The S9 abstract calls its own catalog 'incomplete'.

**Limitations:**
- Only abstracts or metadata were available. No method details, effect sizes, confidence intervals or full experimental setups were checked.
- Most of the 12 papers are arXiv preprints or Zenodo/small-venue items that have not been through rigorous peer review, and most safety papers propose and evaluate their own methods.
- Two papers (src_7ec1f79f00, src_94f0274d75) have no usable abstract, and src_94f0274d75 only repeats its title. They were not used for any finding.
- Several abstracts are truncated (src_7bc9fb98fb, src_d30f187234, src_d302498671, src_109719a0f6, src_2bfdb9a6ea), so some conclusions and caveats may be missing.
- Coverage is narrow. The set focuses on reliability and safety benchmarks and has little on costs, latency, compute, enterprise adoption, legal liability or competing non-agentic approaches.
- The citation count of 24 for src_2bfdb9a6ea, which was published recently in a small journal, is unusually high. I could not verify it, and it was not used as evidence.
- The set has no company-level or deployment-level evidence, so no supplier or vendor concentration risk could be assessed.
- Only titles and abstracts were available, so I could not check methods, baselines or results sections. Some abstracts are truncated.
- Several sources (src_3f9ff28552, src_7ec1f79f00, src_94f0274d75) have no usable abstract, so I could not use them to test any finding.
- I did not challenge S1, S7, S8 or the labelling of S10. Their abstracts support the claims as worded, and S7 and S8 are explicitly framed as review or vision positions.
- Many of the evidence papers are 2026 preprints with few or no citations, so I could not weigh them against community consensus.

## Evidence: company filings and news
Status: ok. Company evidence is limited to short verbatim passages from the latest SEC annual/quarterly reports of the companies in config/companies.yaml that mention the keywords. 8-K press releases (exhibit files) are not read, and companies that do not file with the SEC (e.g. SK hynix, Samsung) are not covered. News items are headlines only: the articles were not read. Company size and trend figures (revenue, growth, R&D, net income) come from the SEC's XBRL company-facts data as reported by each company; the size class is by revenue, not market value. Companies marked 'discovered' were found by a full-text search of all SEC filings for the topic phrase; they are not on the configured list, are often small, and a mention in a filing says nothing about their size, role or prospects.

Keywords searched in filings: AI agents, agentic AI, autonomous agents, agent framework, LLM agents

| Company | Reports read | Mentioning the keywords | Size (revenue, latest FY) | Revenue growth | R&D | Note |
|---|---|---|---|---|---|---|
| Microsoft (MSFT) | 2 | 3 | large: 331.8B USD | +17.8% | 10.7% of revenue | 2 press release(s) read |
| Alphabet (GOOGL) | 2 | 2 | large: 350.0B USD | +13.9% | 14.1% of revenue |  |
| Meta Platforms (META) | 2 | 2 | large: 201.0B USD | +22.2% | 28.5% of revenue |  |
| Amazon (AMZN) | 2 | 1 | large: 716.9B USD | +12.4% | n/a | 2 press release(s) read |
| Oracle (ORCL) | 2 | 1 | large: 67.4B USD | +17.3% | 15.3% of revenue | 2 press release(s) read |
| Palantir Technologies (PLTR) | 2 | 2 | mid: 4.5B USD | +56.2% | 12.5% of revenue | 2 press release(s) read |
| Salesforce (CRM) | 2 | 3 | large: 41.5B USD | +9.6% | 14.4% of revenue | 2 press release(s) read |
| Snowflake (SNOW) | 2 | 2 | mid: 4.7B USD | +29.2% | 42.0% of revenue |  |
| DigitalOcean Holdings, Inc. (DOCN) | 1 | 1 | small: 0.9B USD | +15.5% | 17.9% of revenue | discovered by full-text search |
| Atlassian Corp (TEAM) | 1 | 1 | mid: 6.6B USD | +26.0% | 49.7% of revenue | discovered by full-text search |
| BILL Holdings, Inc. (BILL) | 1 | 1 | mid: 1.7B USD | +13.0% | 18.2% of revenue | discovered by full-text search |
| Extreme Networks Inc (EXTR) | 1 | 1 | mid: 1.3B USD | +12.6% | 18.2% of revenue | discovered by full-text search |
| Amplitude, Inc. (AMPL) | 1 | 1 | small: 0.3B USD | +14.7% | 28.4% of revenue | discovered by full-text search |
| C3.ai, Inc. (AI) | 1 | 1 | small: 0.3B USD | -35.7% | 91.5% of revenue | discovered by full-text search |
| Klaviyo, Inc. (KVYO) | 1 | 1 | mid: 1.2B USD | +31.6% | 23.6% of revenue | discovered by full-text search |
| Figma, Inc. (FIG) | 1 | 1 | mid: 1.1B USD | +41.0% | 97.5% of revenue | discovered by full-text search |

_A report that does not mention the keywords does not show that the company is absent from this market. Size classes (micro < $100M, small < $1B, mid < $10B, large) are by reported revenue, not market value._

- **[M1]** *(verified_fact, confidence high)* Salesforce markets Agentforce as a platform for building and deploying autonomous AI agents across business functions, embedded in its applications and with Slack as the conversational interface.
  - source: [Salesforce, Inc. Form 10-Q, filed 2026-08-27](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm) (SEC EDGAR, 2026-08-27, excerpt_only)
  - source: [Salesforce, Inc. Form 10-K, filed 2026-03-02](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm) (SEC EDGAR, 2026-03-02, excerpt_only)
  - excerpt: "The Company offers Agentforce, a layer of the trusted Agentforce 360 Platform, that enables companies to build and deploy AI agents that can respond to inputs, make decisions and take action autonomously across business functions."
  - reasoning: Both the 10-K and 10-Q describe Agentforce as a shipping product line with customizable agents for sales, service, marketing and commerce, indicating commercial readiness rather than a roadmap item.
- **[M2]** *(verified_fact, confidence medium)* Amazon launched a public preview of Bedrock Managed Agents, a managed service for enterprises to build and deploy production-ready AI agents, and previewed Strands Box, an open-source sandbox for defining agent behavior rules.
  - source: [Amazon Com Inc 8-K press release (exhibit amzn-20260930xex991.htm), filed 2026-10-29](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000038/amzn-20260930xex991.htm) (SEC EDGAR, 2026-10-29, excerpt_only)
  - excerpt: "Launched public preview of Bedrock Managed Agents, which is a managed service powered by OpenAI that makes it faster for enterprises to build and deploy production-ready AI agents."
  - reasoning: Press-release exhibit shows AWS is commercializing agent-building infrastructure, though it is in public preview rather than general availability.
- **[M3]** *(verified_fact, confidence high)* Snowflake acquired Natoma, an enterprise Model Context Protocol platform for AI agents, for preliminary purchase consideration of $128.3 million, and positions its data platform as a foundation for building and deploying AI agents.
  - source: [Snowflake Inc. Form 10-Q, filed 2026-09-04](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000037/snow-20260731.htm) (SEC EDGAR, 2026-09-04, excerpt_only)
  - source: [Snowflake Inc. Form 10-K, filed 2026-03-20](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) (SEC EDGAR, 2026-03-20, excerpt_only)
  - excerpt: "(Natoma), an enterprise Model Context Protocol platform for AI agents. The preliminary purchase consideration was $128.3 million"
  - reasoning: Filing evidence of both M&A investment in agent infrastructure and product-level agent capabilities (e.g., Snowflake Postgres for context-aware agents, AI-powered Site Reliability Engineer).
- **[M4]** *(verified_fact, confidence high)* Microsoft ships agentic AI as part of its Dynamics business applications portfolio for small and large organizations.
  - source: [Microsoft Corp Form 10-K, filed 2026-07-29](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm) (SEC EDGAR, 2026-07-29, excerpt_only)
  - source: [Microsoft Corp Form 10-Q, filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm) (SEC EDGAR, 2026-10-28, excerpt_only)
  - source: [Microsoft Corp 8-K press release (exhibit msft-ex99_1.htm), filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-ex99_1.htm) (SEC EDGAR, 2026-10-28, excerpt_only)
  - excerpt: "Dynamics provides cloud-based and on-premises business solutions for financial management, enterprise resource planning (“ERP”), customer relationship management (“CRM”), and supply chain management, as well as agentic AI and other low code application development platforms"
  - reasoning: Identical language appears in the 10-K, 10-Q and press release, showing agentic AI is a marketed component of Dynamics.
- **[M5]** *(verified_fact, confidence high)* Alphabet offers Gemini Enterprise, a platform for teams to discover, create, share and run AI agents, and is incorporating AI agents into its offerings and internal systems.
  - source: [Alphabet Inc. Form 10-K, filed 2026-02-05](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm) (SEC EDGAR, 2026-02-05, excerpt_only)
  - source: [Microsoft Corp 8-K press release (exhibit msft-ex99_1.htm), filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-ex99_1.htm) (SEC EDGAR, 2026-10-28, excerpt_only)
  - excerpt: "Gemini Enterprise: empowers teams to discover, create, share, and run AI agents all in one secure platform, bringing the best of Google AI to employees through an intuitive chat interface"
  - reasoning: The 10-K describes a shipping enterprise agent platform; the 10-Q confirms ongoing incorporation of agents into offerings.
- **[M6]** *(verified_fact, confidence high)* Meta has launched Muse, an agentic AI, and is making significant investments in generative AI, agentic AI and superintelligence, expecting to increase these investments while acknowledging it may not generate profits from them.
  - source: [Meta Platforms, Inc. Form 10-Q, filed 2026-10-22](https://www.sec.gov/Archives/edgar/data/1326801/000162828026066773/meta-20260930.htm) (SEC EDGAR, 2026-10-22, excerpt_only)
  - excerpt: "For example, we have launched Muse, an agentic AI, which we intend to scale over time."
  - reasoning: The 10-Q shows a launched consumer agentic product plus continued heavy investment; the profit-uncertainty language is the company's own statement.
- **[M7]** *(verified_fact, confidence medium)* Oracle embeds generative and agentic AI in its OCI cloud infrastructure offerings and is building AI into many product offerings.
  - source: [Oracle Corp Form 10-K, filed 2026-06-22](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm) (SEC EDGAR, 2026-06-22, excerpt_only)
  - excerpt: "OCI offerings are designed to deliver our infrastructure technologies, including compute, storage, networking, and cloud-native services, along with new and innovative solutions such as AI Infrastructure, generative AI and agentic AI."
  - reasoning: Positions Oracle mainly as infrastructure for agentic workloads rather than an agent product vendor.
- **[M8]** *(ai_interpretation, confidence medium)* Multiple mid- and small-cap software companies have commercialized or launched AI-agent products in 2025-2026, including DigitalOcean (Gradient AI Agents), Atlassian (AI agents in its app portfolio), BILL (first suite of AI agents under BILL AI), Extreme Networks (Platform ONE with AI agents), Amplitude (Amplitude AI Agents), and C3.ai (C3 Agentic AI Platform).
  - source: [DigitalOcean Holdings, Inc. Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1582961/000162828026069141/docn-20260930.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - source: [Atlassian Corp Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1650372/000165037226000054/team-20260930.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - source: [BILL Holdings, Inc. Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1786352/000162828026071196/bill-20260930.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - source: [Extreme Networks Inc Form 10-Q, filed 2026-10-29](https://www.sec.gov/Archives/edgar/data/1078271/000119312526437803/extr-20260930.htm) (SEC EDGAR, 2026-10-29, excerpt_only)
  - source: [Amplitude, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1866692/000119312526447817/ampl-20260930.htm) (SEC EDGAR, 2026-11-05, excerpt_only)
  - source: [C3.ai, Inc. Form 10-K, filed 2026-06-24](https://www.sec.gov/Archives/edgar/data/1577526/000157752626000078/ai-20260430.htm) (SEC EDGAR, 2026-06-24, excerpt_only)
  - reasoning: Across six independent filings, each company describes concrete agent products or platform capabilities (e.g., BILL: 'we launched BILL AI, including our first suite of AI agents'; Amplitude: 'In June 2025, we introduced Amplitude AI Agents'), suggesting broad commercialization beyond the hyperscalers. Each company's role is limited to what its own excerpt shows.
- **[M9]** *(verified_fact, confidence medium)* Figma reports that third-party autonomous AI agents operating on its platform may circumvent its pricing and reduce its control over distribution and monetization; in March 2026 it introduced the ability for third-party agents to create and modify design assets via its MCP server.
  - source: [Figma, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1579878/000162828026070272/fig-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - excerpt: "In March 2026, we introduced the ability for third-party AI agents to create and modify real design assets directly in Figma files through our MCP server."
  - reasoning: Shows both an agent-access product feature and a disclosed commercial risk from agent-driven distribution.
- **[M10]** *(ai_interpretation, confidence high)* AI agents are a prominent risk theme across filings: companies cite autonomous agent behavior that is hard to predict or audit (Microsoft, Alphabet), agents as a new attack surface and fraud vector (Salesforce, BILL, Meta), and competitive disruption from autonomous agents (Klaviyo, Figma).
  - source: [Microsoft Corp Form 10-Q, filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm) (SEC EDGAR, 2026-10-28, excerpt_only)
  - source: [Microsoft Corp 8-K press release (exhibit msft-ex99_1.htm), filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-ex99_1.htm) (SEC EDGAR, 2026-10-28, excerpt_only)
  - source: [Salesforce, Inc. Form 10-Q, filed 2026-08-27](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm) (SEC EDGAR, 2026-08-27, excerpt_only)
  - source: [BILL Holdings, Inc. Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1786352/000162828026071196/bill-20260930.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - source: [Meta Platforms, Inc. Form 10-K, filed 2026-01-29](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm) (SEC EDGAR, 2026-01-29, excerpt_only)
  - source: [Klaviyo, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1835830/000183583026000046/kvyo-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - source: [Figma, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1579878/000162828026070272/fig-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: A consistent pattern across seven independent filings: agent autonomy is framed as a security, fraud, liability and business-model risk, indicating the market sees unsupervised agent action as a key unresolved commercial issue.
  - citation check: company name(s) not found in the cited sources removed: Alphabet

**Limitations:**
- Only excerpt passages from filings were available, not full reports; companies whose filings did not mention the keywords (e.g., Palantir's product detail beyond AIP hand-off language) cannot be assessed further, and absence of keyword mentions does not mean absence from the market.
- No news headlines were retrieved for this topic, so no market-reaction or third-party coverage could be included.
- Evidence is dominated by risk-factor language; filings disclose risks more thoroughly than commercial metrics, so revenue, customer counts and adoption figures for agent products are largely absent.
- Discovered companies (DOCN, TEAM, BILL, EXTR, AMPL, AI, KVYO, FIG) were found via keyword mentions only; their excerpts show product mentions but not market position, scale of agent revenue or competitive standing.
- Palantir's excerpts mention agentic AI only in risk and investment contexts; no concrete agent product detail was available from its filings in this retrieval.
- No sources provide market size, growth rates or adoption statistics for AI agents, so no quantitative market assessment is possible.

## Social signals from X
Status: ok. Social signals only: posts from the last 7 days by the owner-approved accounts in config/x_watchlist.yaml that mention the keywords (at most 50 posts). A post is what an account says, not a verified fact; company posts are promotional by nature. Accounts not on the watchlist were not searched.

Accounts searched (130): @MicronTech, @SKhynix, @SamsungDSGlobal, @nvidia, @AMD, @intel, @Broadcom, @MarvellTech, @ASMLcompany, @Applied4Tech, @LamResearch, @KLAcorp, @JEDEC, @imec_int, @SemiEngineering, @eetimes, @techinsightsinc, @rambusinc, @AmkorTechnology, @Teradyneinc, @FormFactorInc, @Veeco, @Arm, @Cadence, @Synopsys, @GlobalFoundries, @Qualcomm, @SEMIconex, @hotchipsorg, @IEEESpectrum, @trendforce, @CounterPointTR, @SemiAnalysis_, @ServeTheHome, @tomshardware, @TechTechPotato, @jonpeddie, @SemiconductorsX, @KirkDBorne, @kyleichan, @thePandaily, @HPCwire, @WarGuy_, @PIBKohima, @robvank, @LifeboatHQ, @zhaoweiasu, @BlackEngineer, @ShapesXR, @engadget, @Gadgets360, @eeNewsEurope, @machinelearnflx, @dez_blanchfield, @0xRicker, @Lance_Edelman, @Techmeme, @chr1sa, @Romka2x, @OWW, @CyberRobooo, @Decoded08, @techniahqrobot, @liuziwei7, @johnkoetsier, @preskill, @gp_pulipaka, @QuantumStateX, @Scholarshipps, @QuantumDaily, @scitechgirl, @Amandasatiro07, @thatoptometrist, @QuantumPapers, @the_hindu, @IndiaToday, @EconomicTimes, @ETNOWlive, @GreaterKashmir, @DDIndialive, @c_aashish, @TheQuietSensei, @CBCRajouri, @india_plus_, @alphaaffairsf2f, @dayalugurubjp, @Prabinmen, @PsuWatch, @aseemmanchanda, @bhagwantkhuba, @SUDHIRb9661, @governancenow, @PIB_India, @marinaj4q, @Finsee_main, @skathire, @singularityhub, @ahier, @MolecularCell, @RevvityLifeSci, @idtdna, @NaturePlants, @SimbokeSarah, @ChEnected, @RZubiranS, @BioinfoAdv, @srqstockpicker, @ShorterLab, @nabil125125125, @ThalesDigiSec, @ThejesterVerse, @WOCTechnology, @QuantSecXYZ, @Ronald_vanLoon, @PrameyaEnglish, @craigapplecom, @BLU_Products, @PragativadiNews, @HimanshiTech, @NyongesaSande, @gadgetbytenepal, @bobbymorris280, @TechieUltimatum, @PaidFreeDroid, @nitin_gadkari, @MIB_India, @kishanreddybjp, @IndiaInGuate, @PIBDehradun, @CISACyber
Posts read: 44 (estimated X cost $0.220)

- **[X1]** *(unverified_claim, confidence low)* NVIDIA, at its AI Day Seoul event, framed AI agents as 'the next computing platform' rather than better chatbots, with Jonathan Cohen saying agents now pick models, use tools and handle real work, and claiming its Switchyard work cut costs to about one-third while keeping success rates.
  - source: [@SemiconductorsX: NVIDIA is calling AI agents the next computing platform, not just better chatbots. At AI D…](https://x.com/SemiconductorsX/status/2119639323909984526) (X API, 2026-11-09, full_text)
  - excerpt: "NVIDIA is calling AI agents the next computing platform... Switchyard cut costs to about one-third while keeping success rates"
  - reasoning: Single agent-account post summarizing a company presentation; figures and framing are NVIDIA's own and not independently verified.
- **[X2]** *(unverified_claim, confidence low)* Multiple posts describe agent-to-agent and agent-to-commerce infrastructure maturing: Meta and Sierra reportedly rolled out Personal Agent Protocol 0.1 with Stripe and Shopify adding OAuth-style scoped auth for agent transactions, and the Solana Foundation and Google Cloud reportedly built a service letting AI agents buy API calls on crypto rails.
  - source: [@Decoded08: Passing master credentials to autonomous agents is officially obsolete. Meta and Sierra ro…](https://x.com/Decoded08/status/2117991549799731497) (X API, 2026-11-04, full_text)
  - source: [@Decoded08: Solana Foundation and Google Cloud built https://t.co/3SkK0Ufe9P so AI agents can buy API …](https://x.com/Decoded08/status/2118682379233489085) (X API, 2026-11-06, full_text)
  - source: [@Decoded08: SaaS subscription tiers make zero sense for autonomous agents. Bots don't swipe credit car…](https://x.com/Decoded08/status/2118094980975583301) (X API, 2026-11-04, full_text)
  - excerpt: "Meta and Sierra rolled out Personal Agent Protocol 0.1 with Stripe and Shopify, adding OAuth-style scoped auth so bots transact without seeing raw passwords."
  - reasoning: Three independent owner-added accounts describe the same emerging theme (authenticated, machine-native payments for agents), but each is a secondary social summary of announcements not read directly.
- **[X3]** *(unverified_claim, confidence low)* Apple reportedly identified autonomous AI agents as a business risk in its 2026 annual report, warning that unpredictable agent behavior could expose the company to lawsuits, regulatory action and reputational damage.
  - source: [@HimanshiTech: Apple has identified autonomous AI agents as a potential business risk in its 2026 annual …](https://x.com/HimanshiTech/status/2117796882680607221) (X API, 2026-11-04, full_text)
  - excerpt: "Apple has identified autonomous AI agents as a potential business risk in its 2026 annual report"
  - reasoning: Single post paraphrasing an SEC filing that was not read; risk-factor framing is notable but unverified here.
- **[X4]** *(ai_interpretation, confidence medium)* Several posts signal enterprise adoption and governance concerns around agentic AI: one cites a study saying over half of enterprises already run agentic AI in production networks, another warns 'shadow AI has gone agentic,' and one reports a proposal for AI-agent authorization/permission gates.
  - source: [@Lance_Edelman: Study Says Over Half Of Enterprises Already Run Agentic AI In Production Networks - https:…](https://x.com/Lance_Edelman/status/2119222628787351724) (X API, 2026-11-08, full_text)
  - source: [@Lance_Edelman: Shadow AI has gone agentic. Are organizations ready? - https://t.co/IXSqleA5oE Agentic AI …](https://x.com/Lance_Edelman/status/2119181602651578579) (X API, 2026-11-07, full_text)
  - source: [@Romka2x: TITLE AI News: Agent Permission Gates, AI Centre Grid Plans, European Procurement Push htt…](https://x.com/Romka2x/status/2119224936464109828) (X API, 2026-11-08, full_text)
  - source: [@Decoded08: Hackers pointed AI agents at crypto exchanges. It worked. Crafty Falcon, per CERT-In (4 No…](https://x.com/Decoded08/status/2118319975555362989) (X API, 2026-11-05, full_text)
  - excerpt: "Study Says Over Half Of Enterprises Already Run Agentic AI In Production Networks"
  - reasoning: Four independent accounts converge on the theme that agents are deployed in production while security/governance tooling (permission gates, shadow-AI risk, agent-driven attacks) lags; underlying studies and articles were not read.
- **[X5]** *(unverified_claim, confidence low)* Product launches and benchmarks in the space continue: Perplexity reportedly launched 'Teammates' AI agents for long-running projects (Max subscribers), and OpenAI reportedly introduced 'LifeVal' to measure AI usefulness in everyday tasks based on a survey of 3,995 people.
  - source: [@Decoded08: Perplexity just dropped Teammates – AI agents that own long‑running projects, sync Slack, …](https://x.com/Decoded08/status/2118732953807208451) (X API, 2026-11-06, full_text)
  - source: [@TechieUltimatum: OpenAI Introduces LifeVal, A New Way To Test How Useful AI Is In Everyday Life. AI is no l…](https://x.com/TechieUltimatum/status/2117323394169589973) (X API, 2026-11-02, full_text)
  - excerpt: "Perplexity just dropped Teammates – AI agents that own long-running projects"
  - reasoning: Two separate product-announcement posts from secondary accounts; details truncated and unverified.
- **[X6]** *(ai_interpretation, confidence medium)* A heavy volume of educational/promotional content (Packt book promotions, LangChain/LangGraph and MCP course ads) suggests agent frameworks like LangChain, LangGraph and MCP are being positioned as mainstream developer skills.
  - source: [@KirkDBorne: “An Illustrated Guide to AI Agents — Concepts and Code for Building Agents with LLMs, Tool…](https://x.com/KirkDBorne/status/2119652628061724842) (X API, 2026-11-09, full_text)
  - source: [@KirkDBorne: New release from @PacktPublishing &gt;&gt; "AI Agents and Harnesses Foundations — Building…](https://x.com/KirkDBorne/status/2119614707686596976) (X API, 2026-11-09, full_text)
  - source: [@KirkDBorne: Agentic AI Development with C# and .NET — Build intelligent Applications with GitHub Copil…](https://x.com/KirkDBorne/status/2119651664516800862) (X API, 2026-11-09, full_text)
  - source: [@KirkDBorne: "Multi-Agent AI Engineering: Design, build, and operate AI systems that think and act as c…](https://x.com/KirkDBorne/status/2119650085814333718) (X API, 2026-11-09, full_text)
  - source: [@machinelearnflx: Try AI Agents &amp; Agentic AI with Hugging Face and LangChain. Connect Hugging Face model…](https://x.com/machinelearnflx/status/2119357509374730475) (X API, 2026-11-08, full_text)
  - source: [@machinelearnflx: Take a look at Agentic AI Systems: Build &amp; Deploy with LangChain/LangGraph. Build your…](https://x.com/machinelearnflx/status/2119326556749185372) (X API, 2026-11-08, full_text)
  - source: [@gp_pulipaka: AI Agents and Applications: With LangChain, LangGraph, and MCP! #BigData #Analytics #DataS…](https://x.com/gp_pulipaka/status/2118443746761003034) (X API, 2026-11-05, full_text)
  - source: [@gp_pulipaka: Agentic AI For Platform Engineering: Rethinking Developer Platforms With Agentic AI, RAG, …](https://x.com/gp_pulipaka/status/2118443745116922323) (X API, 2026-11-05, full_text)
  - excerpt: ""AI Agents and Harnesses Foundations — Building from ReAct Loops to Long Horizon Agent Harnesses with LangChain and LangGraph""
  - reasoning: Eight posts, mostly promotional or affiliate-marked, repeatedly emphasize the same toolchain (LangChain/LangGraph/MCP, multi-agent systems, agent 'harnesses'), indicating publisher/marketer focus on agent engineering as a discipline; promotional intent limits evidential weight.
  - citation check: company name(s) not found in the cited posts removed: Packt Publishing

**Limitations:**
- Only posts from a fixed, owner-approved account list over a 7-day window were analyzed; many relevant accounts posted nothing on this topic.
- Most posts are promotional, affiliate-marked, or secondhand summaries of articles and filings that were not read, so claims cannot be verified.
- Several posts (earnings summaries from @Finsee_main) mention AI only tangentially and were excluded from findings.
- Engagement counts reflect attention, not accuracy; the highest-engagement post (src_99a1023ed9) is anecdotal.
- No posts from major semiconductor or standards-body accounts directly addressed AI agents, so the hardware-side signal in this sample is thin.
- Posting volume is low and skewed toward a few prolific accounts (e.g., @KirkDBorne book promotions), which limits pattern strength.

## Evidence: patents
Status: partial. Worldwide patent publications from Google Patents (SerpApi) matching the search terms. Based on titles, applicants and abstracts or search snippets only (no claims or full text). Publications include applications, which are claims of invention, not proof that a technology works. Patents are published about 18 months after filing, so the latest years are undercounted.



**Limitations:**
- No patent publications could be retrieved; no analysis was performed.

## Price and timing risk (part of the Risk agent)
_A risk input, not a buy or sell signal. Past prices do not predict future prices._

Status: partial. Daily closing prices for the companies whose SEC filings mention the topic (Alpha Vantage, last ~100 trading days: the free plan has no longer history, so there is no 52-week or 200-day view). Metrics and the timing-risk level are computed by code from fixed rules. This is a risk input, not a buy or sell signal; past prices do not predict future prices.

| Company | Last close | 1 month | 3 months | vs 50-day avg | 20-day volatility | From window high | Timing risk |
|---|---|---|---|---|---|---|---|
| Microsoft (MSFT) | 530.61 (2026-11-06) | +1.5% | +4.9% | +2.7% | 35.0% | -5.1% | **moderate**: no stretch or pull-back rule triggered |
| Alphabet (GOOGL) | 284.78 (2026-11-06) | -18.2% | -20.3% | -14.5% | 52.6% | -25.9% | **subdued**: 14.5% below its 50-day average and -20.3% over 3 months |
| Meta Platforms (META) | 610.15 (2026-11-06) | -15.4% | +2.6% | -9.6% | 41.0% | -21.8% | **moderate**: no stretch or pull-back rule triggered |
| Palantir Technologies (PLTR) | 160.38 (2026-11-06) | -19.3% | -8.5% | -13.7% | 58.9% | -24.7% | **subdued**: 13.7% below its 50-day average and -8.5% over 3 months |
| Snowflake (SNOW) | 275.88 (2026-11-06) | -19.7% | -17.6% | -15.9% | 61.3% | -28.3% | **subdued**: 15.9% below its 50-day average and -17.6% over 3 months; high volatility (61.3% annualised, 20-day) |

- **[T1]** *(verified_fact, confidence medium)* Microsoft shows no stretch or pull-back: price is 2.7% above its 50-day average, up 4.9% over 3 months, with moderate 35.0% annualised volatility.
  - source: [Microsoft (MSFT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "Price vs 50-day average 2.7%. 20-day annualised volatility 35.0%. -5.1% from the 100-day high"
- **[T2]** *(ai_interpretation, confidence medium)* Microsoft's timing risk reads as moderate: the price sits near its recent average and close to its 100-day high, so there is little run-up stretch, but also little cushion from a pull-back; the ~100-day window is short and a near-high level can continue or reverse.
  - source: [Microsoft (MSFT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T3]** *(verified_fact, confidence medium)* Alphabet is down 20.3% over 3 months and trades 14.5% below its 50-day average, with 52.6% annualised volatility.
  - source: [Alphabet (GOOGL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOGL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "3-month return -20.3%. Price vs 50-day average -14.5%. 20-day annualised volatility 52.6%"
- **[T4]** *(ai_interpretation, confidence medium)* Alphabet's timing risk is subdued in the sense of a large recent pull-back, not low risk: a 25.9% drawdown from the 100-day high with elevated volatility means the price has fallen sharply and could fall further; subdued does not imply the decline is over.
  - source: [Alphabet (GOOGL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOGL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T5]** *(unverified_claim, confidence low)* Meta Platforms is down 15.4% over 1 month and 9.6% below its 50-day average, with 41.0% annualised volatility and no stretch or pull-back rule triggered.
  - source: [Meta Platforms (META) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=META&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -15.4%. Price vs 50-day average -9.6%. 20-day annualised volatility 41.0%"
  - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- **[T6]** *(ai_interpretation, confidence medium)* Meta's timing risk is moderate: a meaningful recent decline offsets any run-up concern, but volatility of 41.0% annualised means price swings remain large in either direction.
  - source: [Meta Platforms (META) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=META&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T7]** *(unverified_claim, confidence low)* Palantir is down 19.3% over 1 month and 13.7% below its 50-day average, with the highest-tier volatility of 58.9% annualised; it remains 50.8% above its 100-day low.
  - source: [Palantir Technologies (PLTR) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PLTR&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -19.3%. Price vs 50-day average -13.7%. 20-day annualised volatility 58.9%"
  - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- **[T8]** *(ai_interpretation, confidence medium)* Palantir's timing risk is subdued by the pull-back rule but remains high in substance: a sharp recent decline combined with ~59% annualised volatility and a price still far above its 100-day low indicates a volatile, still-elevated level rather than a settled one.
  - source: [Palantir Technologies (PLTR) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PLTR&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T9]** *(unverified_claim, confidence low)* Snowflake is down 19.7% over 1 month and 15.9% below its 50-day average, with 61.3% annualised volatility and a 28.3% drawdown from its 100-day high.
  - source: [Snowflake (SNOW) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SNOW&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - excerpt: "1-month return -19.7%. Price vs 50-day average -15.9%. 20-day annualised volatility 61.3%"
  - citation check: downgraded from verified_fact: supporting excerpt missing or not found in the cited source text
- **[T10]** *(ai_interpretation, confidence medium)* Snowflake carries the most volatile profile in this set: the subdued label reflects a large pull-back, but 61.3% annualised volatility means timing uncertainty is high and further large moves in either direction are consistent with the recent pattern.
  - source: [Snowflake (SNOW) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SNOW&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
- **[T11]** *(ai_interpretation, confidence medium)* Cross-company: four of the five AI-agent-linked stocks (Alphabet, Meta, Palantir, Snowflake) have pulled back sharply over the past month and trade well below their 50-day averages, while only Microsoft sits near its recent average; none shows a stretched run-up, but most show elevated volatility.
  - source: [Alphabet (GOOGL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOGL&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Meta Platforms (META) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=META&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Palantir Technologies (PLTR) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PLTR&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Snowflake (SNOW) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SNOW&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)
  - source: [Microsoft (MSFT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact) (Alpha Vantage, 2026-11-06, full_text)

**Limitations:**
- The ~100-trading-day window is short and may not capture longer cycles in these prices.
- Analysis uses only computed price metrics; no fundamentals, valuation, or news context are considered.
- Prices move for reasons unrelated to the AI-agents topic; linkage of price behaviour to the theme is an assumption.
- Rule-based timing labels are heuristic; 'subdued' indicates less recent run-up, not a low-risk level or a likely rebound.
- Past price behaviour does not predict future prices.

## Emerging companies (Company Scout)
_Who is demonstrably working on this topic, found from patent assignees, company author affiliations and SEC filings; matched to the SEC ticker file (never guessed). The next-runner score is a transparent heuristic labelled forecast, not a recommendation. Smaller companies carry more risk and less disclosure._

Status: ok. 18 distinct company names from 0 patent publications, 1 company-affiliated papers and 16 SEC filers; 17 matched to the SEC ticker file (9 outside the configured list), 1 not SEC-listed (private, foreign or not found).

**Candidates outside the configured big-name list:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| DigitalOcean Holdings, Inc. (DOCN) · Services-Computer Programming, Data Processing, Etc. | 0 | 0 | 6 | small: 0.90B USD | +15.5% | 17.9% | **50** |
| Atlassian Corp (TEAM) · Services-Prepackaged Software | 0 | 0 | 5 | mid: 6.57B USD | +26.0% | 49.7% | **50** |
| Amplitude, Inc. (AMPL) · Services-Prepackaged Software | 0 | 0 | 4 | small: 0.34B USD | +14.7% | 28.4% | **50** |
| Klaviyo, Inc. (KVYO) · Services-Prepackaged Software | 0 | 0 | 4 | mid: 1.23B USD | +31.6% | 23.6% | **50** |
| Figma, Inc. (FIG) · Services-Prepackaged Software | 0 | 0 | 3 | mid: 1.06B USD | +41.0% | 97.5% | **50** |
| BILL Holdings, Inc. (BILL) · Services-Prepackaged Software | 0 | 0 | 5 | mid: 1.65B USD | +13.0% | 18.2% | **45** |
| Extreme Networks Inc (EXTR) · Computer Communications Equipment | 0 | 0 | 5 | mid: 1.28B USD | +12.6% | 18.2% | **45** |
| C3.ai, Inc. (AI) · Services-Prepackaged Software | 0 | 0 | 4 | small: 0.25B USD | -35.7% | 91.5% | **45** |
| Infosys Ltd (INFY) · Services-Computer Programming Services | 0 | 1 | 0 | large: 10.94B USD | +7.2% | n/a | **13** |

- DigitalOcean Holdings, Inc.: 6 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +16% (+5); R&D 18% of revenue (+10)
- Atlassian Corp: 5 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +26% (+10); R&D 50% of revenue (+10)
- Amplitude, Inc.: 4 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); small company by revenue (+15): more room to grow, more risk; revenue growth +15% (+5); R&D 28% of revenue (+10)
- Klaviyo, Inc.: 4 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +32% (+10); R&D 24% of revenue (+10)
- Figma, Inc.: 3 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +41% (+10); R&D 98% of revenue (+10)
- BILL Holdings, Inc.: 5 SEC report(s) mentioning the topic (+20); evidence is SEC filing mentions only: check that they are not risk-factor boilerplate (+0); mid-size company by revenue (+10); revenue growth +13% (+5); R&D 18% of revenue (+10)

**Configured incumbents that also showed up:**

| Company | Patents | Papers | Filings | Size (revenue, latest FY) | Revenue growth | R&D / revenue | Next-runner score |
|---|---|---|---|---|---|---|---|
| Snowflake (SNOW) | 0 | 0 | 2 | mid: 4.68B USD | +29.2% | 42.0% | **50** |
| Palantir Technologies (PLTR) | 0 | 0 | 2 | mid: 4.48B USD | +56.2% | 12.5% | **45** |
| Meta Platforms (META) | 0 | 0 | 2 | large: 200.97B USD | +22.2% | 28.5% | **40** |
| Microsoft (MSFT) | 0 | 0 | 3 | large: 331.84B USD | +17.8% | 10.7% | **30** |
| Salesforce (CRM) | 0 | 0 | 3 | large: 41.52B USD | +9.6% | 14.4% | **30** |
| Alphabet (GOOGL) | 0 | 0 | 2 | large: 350.02B USD | +13.9% | 14.1% | **30** |
| Oracle (ORCL) | 0 | 0 | 1 | large: 67.36B USD | +17.3% | 15.3% | **30** |
| Amazon (AMZN) | 0 | 0 | 1 | large: 716.92B USD | +12.4% | n/a | **20** |

**Found but not in the SEC ticker file (private, foreign, or name not matched):** Capgemini (Netherlands) (0P/1A/0F)

_Basis: Next-runner score (0-100, heuristic): patents as assignee up to 25, company-affiliated papers up to 15, SEC reports mentioning the topic up to 20, revenue size micro/small +15 or mid +10, revenue growth up to +10, R&D intensity up to +10; filers whose SEC industry code is outside technology (banks, insurers, retailers...) lose 25 and are listed last, because their mentions are usually risk-factor boilerplate. Counts come from the sources this run retrieved, so they measure attention in this sample, not the whole market. The score is a forecast-labelled heuristic, not a recommendation._

- **[K1]** *(ai_interpretation, confidence low)* DigitalOcean Holdings, Inc. (DOCN) is active on AI agents: 6 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.90B USD (small by revenue), growth +15.5%, R&D 17.9% of revenue. Next-runner score 50/100 (heuristic).
  - source: [DigitalOcean Holdings, Inc. Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1582961/000162828026069141/docn-20260930.htm) (SEC EDGAR, 2026-11-03, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K2]** *(ai_interpretation, confidence low)* Atlassian Corp (TEAM) is active on AI agents: 5 of its SEC report(s) mention the topic; fiscal 2026 revenue 6.57B USD (mid by revenue), growth +26.0%, R&D 49.7% of revenue. Next-runner score 50/100 (heuristic).
  - source: [Atlassian Corp Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1650372/000165037226000054/team-20260930.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K3]** *(ai_interpretation, confidence low)* Amplitude, Inc. (AMPL) is active on AI agents: 4 of its SEC report(s) mention the topic; fiscal 2025 revenue 0.34B USD (small by revenue), growth +14.7%, R&D 28.4% of revenue. Next-runner score 50/100 (heuristic).
  - source: [Amplitude, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1866692/000119312526447817/ampl-20260930.htm) (SEC EDGAR, 2026-11-05, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K4]** *(ai_interpretation, confidence low)* Klaviyo, Inc. (KVYO) is active on AI agents: 4 of its SEC report(s) mention the topic; fiscal 2025 revenue 1.23B USD (mid by revenue), growth +31.6%, R&D 23.6% of revenue. Next-runner score 50/100 (heuristic).
  - source: [Klaviyo, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1835830/000183583026000046/kvyo-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K5]** *(ai_interpretation, confidence low)* Figma, Inc. (FIG) is active on AI agents: 3 of its SEC report(s) mention the topic; fiscal 2025 revenue 1.06B USD (mid by revenue), growth +41.0%, R&D 97.5% of revenue. Next-runner score 50/100 (heuristic).
  - source: [Figma, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1579878/000162828026070272/fig-20260930.htm) (SEC EDGAR, 2026-11-04, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.
- **[K6]** *(ai_interpretation, confidence low)* BILL Holdings, Inc. (BILL) is active on AI agents: 5 of its SEC report(s) mention the topic; fiscal 2026 revenue 1.65B USD (mid by revenue), growth +13.0%, R&D 18.2% of revenue. Next-runner score 45/100 (heuristic).
  - source: [BILL Holdings, Inc. Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1786352/000162828026071196/bill-20260930.htm) (SEC EDGAR, 2026-11-06, excerpt_only)
  - reasoning: Computed by code from the cited sources and SEC XBRL company facts; the score is a transparent heuristic (see the scout basis), not a prediction of returns.

**Limitations:**
- No patent documents were retrieved for this run, so no assignee signal.
- Counts cover only the documents this run retrieved (a sample), not the whole literature or patent office.

## Sources
Every source below was retrieved from a real API by the system. News items are headlines only; X posts are social signals.

- [@KirkDBorne: Agentic AI for DevOps Engineers — Build autonomous CI/CD, infrastructure, and operations w…](https://x.com/KirkDBorne/status/2119654778636521948) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_e2896276a7
- [@KirkDBorne: “An Illustrated Guide to AI Agents — Concepts and Code for Building Agents with LLMs, Tool…](https://x.com/KirkDBorne/status/2119652628061724842) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_acf4d31244
- [@KirkDBorne: Agentic AI Development with C# and .NET — Build intelligent Applications with GitHub Copil…](https://x.com/KirkDBorne/status/2119651664516800862) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_37ca41b0bc
- [@KirkDBorne: "Multi-Agent AI Engineering: Design, build, and operate AI systems that think and act as c…](https://x.com/KirkDBorne/status/2119650085814333718) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_d8b327b24a
- [@KirkDBorne: Mastering QuickBooks 2026 — Complete guide to small business accounting with US QuickBooks…](https://x.com/KirkDBorne/status/2119644157354410426) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_26b52750a0
- [@SemiconductorsX: NVIDIA is calling AI agents the next computing platform, not just better chatbots. At AI D…](https://x.com/SemiconductorsX/status/2119639323909984526) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_e6b01483d2
- [@KirkDBorne: New release from @PacktPublishing &gt;&gt; "AI Agents and Harnesses Foundations — Building…](https://x.com/KirkDBorne/status/2119614707686596976) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_2eb68a7a08
- [@KirkDBorne: Harness Engineering — How to Build AI Agents That Don't Fall Apart, by @0xwhrrari …⤵️ http…](https://x.com/KirkDBorne/status/2119614605173432727) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_ca3d8078c0
- [@machinelearnflx: Take a look at AWS GenAI: RAG, AI Agents and Responsible AI. Build a Multimodal AI Knowled…](https://x.com/machinelearnflx/status/2119676361694482602) | X API | 2026-11-09 | retrieved 2026-11-09 | full_text | id src_356d3245bd
- [@KirkDBorne: "Digital Twins in Action". Get your copy at https://t.co/B9Y8D6SBSj You will learn how to:…](https://x.com/KirkDBorne/status/2119522336332546083) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_93d4caf743
- [@KirkDBorne: Incredible limited-time offer from @PacktPublishing on their Agentic AI (and beyond) new a…](https://x.com/KirkDBorne/status/2119439661684994230) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_8f5a75bd6f
- [@0xRicker: ONE CHINESE STUDENT JUST MADE REA 100× MORE ANNOYING TO USE... A solo dev released BLA - B…](https://x.com/0xRicker/status/2119466114941874312) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_99a1023ed9
- [@machinelearnflx: Try AI Agents &amp; Agentic AI with Hugging Face and LangChain. Connect Hugging Face model…](https://x.com/machinelearnflx/status/2119357509374730475) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_24f216cc22
- [@machinelearnflx: Take a look at Agentic AI Systems: Build &amp; Deploy with LangChain/LangGraph. Build your…](https://x.com/machinelearnflx/status/2119326556749185372) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_fc9b31724b
- [@Romka2x: TITLE AI News: Agent Permission Gates, AI Centre Grid Plans, European Procurement Push htt…](https://x.com/Romka2x/status/2119224936464109828) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_7177cbaac7
- [@Romka2x: TITLE AI News: Agent Permission Gates, AI Centre Grid Plans, European Procurement Push htt…](https://x.com/Romka2x/status/2119224697409683631) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_9b26ab79b8
- [@Lance_Edelman: Study Says Over Half Of Enterprises Already Run Agentic AI In Production Networks - https:…](https://x.com/Lance_Edelman/status/2119222628787351724) | X API | 2026-11-08 | retrieved 2026-11-09 | full_text | id src_dd97e48d0f
- [@LifeboatHQ: How “reverse game theory” could keep AI agents in check https://t.co/l349Fhfzpm](https://x.com/LifeboatHQ/status/2119213277746196485) | X API | 2026-11-07 | retrieved 2026-11-09 | full_text | id src_00a27b88c9
- [@Lance_Edelman: Shadow AI has gone agentic. Are organizations ready? - https://t.co/IXSqleA5oE Agentic AI …](https://x.com/Lance_Edelman/status/2119181602651578579) | X API | 2026-11-07 | retrieved 2026-11-09 | full_text | id src_4f9faf53b0
- [@Lance_Edelman: AI Agents Navigate Unfamiliar OT Systems and Move Equipment in Minutes, Booz Allen Finds -…](https://x.com/Lance_Edelman/status/2119170030260683200) | X API | 2026-11-07 | retrieved 2026-11-09 | full_text | id src_5b199cad92
- [@Decoded08: I mapped the complete context engineering playbook for AI agents that give the right answe…](https://x.com/Decoded08/status/2119113629064708125) | X API | 2026-11-07 | retrieved 2026-11-09 | full_text | id src_8252ebab6f
- [Atlassian Corp Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1650372/000165037226000054/team-20260930.htm) | SEC EDGAR | 2026-11-06 | retrieved 2026-11-09 | excerpt_only | id src_5c65739615
- [BILL Holdings, Inc. Form 10-Q, filed 2026-11-06](https://www.sec.gov/Archives/edgar/data/1786352/000162828026071196/bill-20260930.htm) | SEC EDGAR | 2026-11-06 | retrieved 2026-11-09 | excerpt_only | id src_b9cb51916b
- [@Decoded08: Perplexity just dropped Teammates – AI agents that own long‑running projects, sync Slack, …](https://x.com/Decoded08/status/2118732953807208451) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_4b815e2e2c
- [@Decoded08: Solana Foundation and Google Cloud built https://t.co/3SkK0Ufe9P so AI agents can buy API …](https://x.com/Decoded08/status/2118682379233489085) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_279b749f1f
- [@Finsee_main: $TEAM Q1 2027 earnings: Atlassian lifts its outlook, but second-half growth slows to 9% At…](https://x.com/Finsee_main/status/2118797182169993233) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_09857b3412
- [@Finsee_main: $NET Q3 2026 earnings: Cloudflare sales accelerate, but serving its customers costs more C…](https://x.com/Finsee_main/status/2118792100376350734) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_117111ab49
- [@Finsee_main: $AVPT Q3 2026 earnings: AvePoint subscription sales grow 27%, but heavier spending cuts pr…](https://x.com/Finsee_main/status/2118664576191303919) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_d690671746
- [@ChEnected: Agentic #AI could reshape oil and gas operations https://t.co/dyTjosTU0M https://t.co/685O…](https://x.com/ChEnected/status/2118786759311978525) | X API | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_1bd621d0b0
- [Microsoft (MSFT) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_786c2be361
- [Alphabet (GOOGL) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOGL&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_69aae09bab
- [Meta Platforms (META) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=META&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_0355928b0b
- [Palantir Technologies (PLTR) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=PLTR&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_9294b281a9
- [Snowflake (SNOW) daily prices 2026-06-17 to 2026-11-06](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SNOW&outputsize=compact) | Alpha Vantage | 2026-11-06 | retrieved 2026-11-09 | full_text | id src_cd3319f384
- [Amplitude, Inc. Form 10-Q, filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1866692/000119312526447817/ampl-20260930.htm) | SEC EDGAR | 2026-11-05 | retrieved 2026-11-09 | excerpt_only | id src_7e263b86b9
- [@gp_pulipaka: AI Agents and Applications: With LangChain, LangGraph, and MCP! #BigData #Analytics #DataS…](https://x.com/gp_pulipaka/status/2118443746761003034) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_a12d87db9f
- [@gp_pulipaka: Agentic AI For Platform Engineering: Rethinking Developer Platforms With Agentic AI, RAG, …](https://x.com/gp_pulipaka/status/2118443745116922323) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_3820be78db
- [@Decoded08: Hackers pointed AI agents at crypto exchanges. It worked. Crafty Falcon, per CERT-In (4 No…](https://x.com/Decoded08/status/2118319975555362989) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_0b20570e9a
- [@Finsee_main: $AIP Q3 2026 earnings: Arteris nears its first profit, but backlog additions stall Arteris…](https://x.com/Finsee_main/status/2118457114355994661) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_9e767db716
- [@Finsee_main: $BL Q3 2026 earnings: BlackLine cuts its sales outlook while operating margins expand Blac…](https://x.com/Finsee_main/status/2118455414589125072) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_09060a5a70
- [@Finsee_main: $G Q3 2026 earnings: Genpact's tech sales jump 30%, but unpaid bills drain cash Genpact's …](https://x.com/Finsee_main/status/2118454604509667575) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_6a6fb41837
- [@TheQuietSensei: Bengaluru-based Aina has launched a screen-equipped AI ring. Designed by a former Ultrahum…](https://x.com/TheQuietSensei/status/2118446673584169253) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_22018d2476
- [@Finsee_main: $NTCT Q2 2027 earnings: Netscout raises profit through cost cuts, but product backlog shri…](https://x.com/Finsee_main/status/2118338934581215497) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_dd53c68d28
- [@Finsee_main: $OTEX Q1 2027 earnings: OpenText's core cloud grows 11%, and refinancing cuts its debt Ope…](https://x.com/Finsee_main/status/2118321582124724404) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_cc566a0416
- [@Finsee_main: $CMRC Q3 2026 earnings: Commerce raises its profit plan, but customer retention drops Comm…](https://x.com/Finsee_main/status/2118316873506865544) | X API | 2026-11-05 | retrieved 2026-11-09 | full_text | id src_5096106c6b
- [Klaviyo, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1835830/000183583026000046/kvyo-20260930.htm) | SEC EDGAR | 2026-11-04 | retrieved 2026-11-09 | excerpt_only | id src_f087f41094
- [Figma, Inc. Form 10-Q, filed 2026-11-04](https://www.sec.gov/Archives/edgar/data/1579878/000162828026070272/fig-20260930.htm) | SEC EDGAR | 2026-11-04 | retrieved 2026-11-09 | excerpt_only | id src_340e2ade7f
- [@Decoded08: SaaS subscription tiers make zero sense for autonomous agents. Bots don't swipe credit car…](https://x.com/Decoded08/status/2118094980975583301) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_55b62b780c
- [@QuantumPapers: Discovering Models for Experimental Quantum Systems with Agentic AI Hannah C. Kleidermache…](https://x.com/QuantumPapers/status/2118029767664447863) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_e17be9318a
- [@EconomicTimes: Decoded: Will AI agents outlast the hype? https://t.co/qC2kcnWu6d](https://x.com/EconomicTimes/status/2118028057030099061) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_f2a4a5c446
- [@Decoded08: Passing master credentials to autonomous agents is officially obsolete. Meta and Sierra ro…](https://x.com/Decoded08/status/2117991549799731497) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_513747ea4d
- [@Ronald_vanLoon: The real test for agentic AI is not a benchmark score. It is how many steps a model can ru…](https://x.com/Ronald_vanLoon/status/2117913630695903403) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_f9bb50b48a
- [@HimanshiTech: Apple has identified autonomous AI agents as a potential business risk in its 2026 annual …](https://x.com/HimanshiTech/status/2117796882680607221) | X API | 2026-11-04 | retrieved 2026-11-09 | full_text | id src_ba8d78e2bb
- [Palantir Technologies Inc. Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1321655/000132165526000048/pltr-20260930.htm) | SEC EDGAR | 2026-11-03 | retrieved 2026-11-09 | excerpt_only | id src_c87c07a0c6
- [DigitalOcean Holdings, Inc. Form 10-Q, filed 2026-11-03](https://www.sec.gov/Archives/edgar/data/1582961/000162828026069141/docn-20260930.htm) | SEC EDGAR | 2026-11-03 | retrieved 2026-11-09 | excerpt_only | id src_afbabbfea1
- [@TechieUltimatum: OpenAI Introduces LifeVal, A New Way To Test How Useful AI Is In Everyday Life. AI is no l…](https://x.com/TechieUltimatum/status/2117323394169589973) | X API | 2026-11-02 | retrieved 2026-11-09 | full_text | id src_57efdf3cea
- [Alphabet Inc. Form 10-Q, filed 2026-10-29](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000084/goog-20260930.htm) | SEC EDGAR | 2026-10-29 | retrieved 2026-11-09 | excerpt_only | id src_b85dd4fa2c
- [Amazon Com Inc 8-K press release (exhibit amzn-20260930xex991.htm), filed 2026-10-29](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000038/amzn-20260930xex991.htm) | SEC EDGAR | 2026-10-29 | retrieved 2026-11-09 | excerpt_only | id src_823e0ec9d6
- [Extreme Networks Inc Form 10-Q, filed 2026-10-29](https://www.sec.gov/Archives/edgar/data/1078271/000119312526437803/extr-20260930.htm) | SEC EDGAR | 2026-10-29 | retrieved 2026-11-09 | excerpt_only | id src_1d91615179
- [Microsoft Corp Form 10-Q, filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436133/msft-20260930.htm) | SEC EDGAR | 2026-10-28 | retrieved 2026-11-09 | excerpt_only | id src_fc089e1d48
- [Microsoft Corp 8-K press release (exhibit msft-ex99_1.htm), filed 2026-10-28](https://www.sec.gov/Archives/edgar/data/789019/000119312526436149/msft-ex99_1.htm) | SEC EDGAR | 2026-10-28 | retrieved 2026-11-09 | excerpt_only | id src_e83e747224
- [Trial by Trace: Benchmarking AI Agent Harnesses for Reliability and Failure Attribution](https://doi.org/10.48550/arxiv.2610.32285) | OpenAlex | 2026-10-23 | retrieved 2026-11-09 | abstract_only | id src_109719a0f6
- [Meta Platforms, Inc. Form 10-Q, filed 2026-10-22](https://www.sec.gov/Archives/edgar/data/1326801/000162828026066773/meta-20260930.htm) | SEC EDGAR | 2026-10-22 | retrieved 2026-11-09 | excerpt_only | id src_4530a17168
- [Salesforce, Inc. 8-K press release (exhibit d516983dex991.htm), filed 2026-10-20](https://www.sec.gov/Archives/edgar/data/1108524/000119312526425881/d516983dex991.htm) | SEC EDGAR | 2026-10-20 | retrieved 2026-11-09 | excerpt_only | id src_f7613413ec
- [Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills](https://arxiv.org/abs/2610.01833v1) | arXiv | 2026-10-01 | retrieved 2026-11-09 | abstract_only | id src_eadf0a4977
- [Snowflake Inc. Form 10-Q, filed 2026-09-04](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000037/snow-20260731.htm) | SEC EDGAR | 2026-09-04 | retrieved 2026-11-09 | excerpt_only | id src_299a723945
- [SafeEvolve: Harness-Policy Co-Evolution from Agent Experience for Safety Alignment](https://arxiv.org/abs/2609.02786v1) | arXiv | 2026-09-02 | retrieved 2026-11-09 | abstract_only | id src_d30f187234
- [Salesforce, Inc. Form 10-Q, filed 2026-08-27](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000190/crm-20260731.htm) | SEC EDGAR | 2026-08-27 | retrieved 2026-11-09 | excerpt_only | id src_29c74458de
- [What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation](https://arxiv.org/abs/2607.26935v1) | arXiv | 2026-07-29 | retrieved 2026-11-09 | abstract_only | id src_0899b688eb
- [Microsoft Corp Form 10-K, filed 2026-07-29](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm) | SEC EDGAR | 2026-07-29 | retrieved 2026-11-09 | excerpt_only | id src_454ed8f95a
- [Cryptographically verifiable authorization for autonomous AI agents: a falsifiable hypothesis and proof of concept](https://arxiv.org/abs/2607.21325v3) | arXiv | 2026-07-23 | retrieved 2026-11-09 | abstract_only | id src_ca33c17412
- [AI Agent Reliability in 2025: Failure Modes and Success Rates of Long-Horizon Tasks](https://doi.org/10.5281/zenodo.21300837) | OpenAlex | 2026-07-10 | retrieved 2026-11-09 | abstract_only | id src_94f0274d75
- [C3.ai, Inc. Form 10-K, filed 2026-06-24](https://www.sec.gov/Archives/edgar/data/1577526/000157752626000078/ai-20260430.htm) | SEC EDGAR | 2026-06-24 | retrieved 2026-11-09 | excerpt_only | id src_52a22daa50
- [Oracle Corp Form 10-K, filed 2026-06-22](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm) | SEC EDGAR | 2026-06-22 | retrieved 2026-11-09 | excerpt_only | id src_446ab67f3a
- [AgentDoG 1.5: A Lightweight and Scalable Alignment Framework for AI Agent Safety and Security](https://arxiv.org/abs/2605.29801v1) | arXiv | 2026-05-28 | retrieved 2026-11-09 | abstract_only | id src_de7cd261f4
- [Foundations of a Time-Consistent Counterfactual Actuarial Runtime for Autonomous AI Agents](https://arxiv.org/abs/2605.26508v1) | arXiv | 2026-05-26 | retrieved 2026-11-09 | abstract_only | id src_b829c26a18
- [On-Policy Self-Evolution via Failure Trajectories for Agentic Safety Alignment](https://arxiv.org/abs/2605.11882v1) | arXiv | 2026-05-12 | retrieved 2026-11-09 | abstract_only | id src_d302498671
- [Preregistration for Experiments with AI Agents](https://arxiv.org/abs/2606.11217v1) | arXiv | 2026-05-03 | retrieved 2026-11-09 | abstract_only | id src_d1a4deb402
- [Trajectory Reliability Prediction for Generalist AI Agents: Tool-Use Failure Analysis and Success Forecasting on ZClawBench](https://doi.org/10.51903/jtie.v5i1.539) | OpenAlex | 2026-04-30 | retrieved 2026-11-09 | abstract_only | id src_2bfdb9a6ea
- [Snowflake Inc. Form 10-K, filed 2026-03-20](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm) | SEC EDGAR | 2026-03-20 | retrieved 2026-11-09 | excerpt_only | id src_f1ea5e057a
- [Salesforce, Inc. Form 10-K, filed 2026-03-02](https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm) | SEC EDGAR | 2026-03-02 | retrieved 2026-11-09 | excerpt_only | id src_e679f6930e
- [Palantir Technologies Inc. Form 10-K, filed 2026-02-17](https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm) | SEC EDGAR | 2026-02-17 | retrieved 2026-11-09 | excerpt_only | id src_c18deedf62
- [Alphabet Inc. Form 10-K, filed 2026-02-05](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm) | SEC EDGAR | 2026-02-05 | retrieved 2026-11-09 | excerpt_only | id src_d4c88f484e
- [TAME: A Trustworthy Test-Time Evolution of Agent Memory with Systematic Benchmarking](https://arxiv.org/abs/2602.03224v2) | arXiv | 2026-02-03 | retrieved 2026-11-09 | abstract_only | id src_df025f6828
- [Meta Platforms, Inc. Form 10-K, filed 2026-01-29](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm) | SEC EDGAR | 2026-01-29 | retrieved 2026-11-09 | excerpt_only | id src_659c2a5f45
- [A Hierarchical Failure Taxonomy for Reliability Assessment of AI Agents: An Empirical Analysis of the Agent Failure Atlas 2026 Benchmark](https://doi.org/10.6025/jitr/2026/17/4/204-226) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | abstract_only | id src_073c8d7f19
- [From Failure Modes to Reliability Awareness in Generative and Agentic AI System](https://doi.org/10.1007/978-3-032-18585-3_10) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | metadata_only | id src_7ec1f79f00
- [Evaluating Reliability of LLM-Based Agentic AI Systems: A Failure Taxonomy and the Agent Reliability Assurance Framework](https://doi.org/10.5281/zenodo.23283517) | OpenAlex | 2026-01-01 | retrieved 2026-11-09 | abstract_only | id src_7bc9fb98fb
- [Safe, Untrusted, "Proof-Carrying" AI Agents: toward the agentic lakehouse](https://arxiv.org/abs/2510.09567v1) | arXiv | 2025-10-10 | retrieved 2026-11-09 | abstract_only | id src_53cfb1f43d
- [A cybersecurity AI agent selection and decision support framework](https://arxiv.org/abs/2510.01751v1) | arXiv | 2025-10-02 | retrieved 2026-11-09 | abstract_only | id src_29a5057c0c
- [AI Agents vs. Agentic AI: A Conceptual taxonomy, applications and challenges](https://doi.org/10.1016/j.inffus.2025.103599) | OpenAlex | 2025-08-22 | retrieved 2026-11-09 | abstract_only | id src_165dff5e24
- [Agent Safety Alignment via Reinforcement Learning](https://arxiv.org/abs/2507.08270v1) | arXiv | 2025-07-11 | retrieved 2026-11-09 | abstract_only | id src_302c5699ae
- [AI Agents and Agentic Systems: A Multi-Expert Analysis](https://doi.org/10.1080/08874417.2025.2483832) | OpenAlex | 2025-04-24 | retrieved 2026-11-09 | abstract_only | id src_9703fa92b5
- [Infrastructure for AI Agents](https://doi.org/10.48550/arxiv.2501.10114) | OpenAlex | 2025-01-17 | retrieved 2026-11-09 | abstract_only | id src_52b4d4e94c
- [Authenticated Delegation and Authorized AI Agents](https://doi.org/10.48550/arxiv.2501.09674) | OpenAlex | 2025-01-16 | retrieved 2026-11-09 | abstract_only | id src_1b70ec88bc
- [IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems](https://arxiv.org/abs/2410.16237v2) | arXiv | 2024-10-21 | retrieved 2026-11-09 | abstract_only | id src_209b3f681c
- [Empowering biomedical discovery with AI agents](https://doi.org/10.1016/j.cell.2024.09.022) | OpenAlex | 2024-10-01 | retrieved 2026-11-09 | abstract_only | id src_0a7dff334a
- [AI Agents That Matter](https://doi.org/10.48550/arxiv.2407.01502) | OpenAlex | 2024-07-01 | retrieved 2026-11-09 | abstract_only | id src_d5dde5b7b7
- [Security of AI Agents](https://arxiv.org/abs/2406.08689v3) | arXiv | 2024-06-12 | retrieved 2026-11-09 | abstract_only | id src_a91f4a1cdb
- [Visibility into AI Agents](https://doi.org/10.1145/3630106.3658948) | OpenAlex | 2024-06-03 | retrieved 2026-11-09 | abstract_only | id src_37aaee736d
- [Governing AI Agents](https://doi.org/10.2139/ssrn.4772956) | OpenAlex | 2024-01-01 | retrieved 2026-11-09 | metadata_only | id src_3f9ff28552

## Gaps, limitations and errors
- Missing data: Patent evidence: the patent agent did not run, so there is no patent count, no assignee data and no basis for a patent_momentum rating - Excel-like patent activity may look very different from the research and product picture.
- Missing data: Verified customer adoption: no finding gives agent customer counts, deployment volumes, win rates, retention or renewal data. The only adoption-like figure is an unverified social post (X4).
- Missing data: Agent-attributable economics: no finding discloses agent-specific revenue, pricing, gross margin, attach rate or cost-to-serve for any vendor, so the commercial importance of agents relative to existing products cannot be assessed.
- Missing data: Validation of governance and reliability mechanisms: proposed visibility, logging, authorization and runtime-gating mechanisms are untested, with circumvention, privacy and cost consequences unquantified (C4, C5, C6).
- Missing data: Longitudinal reliability data: the process-level evaluation study is cross-sectional in a single enterprise system, and its authors list longitudinal validation under real API evolution as future work (C1).
- Missing data: No company evidence yet for a standalone reliability, evaluation or governance tooling vendor: no cited finding names a company selling or a customer buying such tooling.
- Missing data: Market-side agent-commerce and payment-rail projects appear only as social posts and are unverified (X2), and the claim that MCP, LangChain and LangGraph are mainstream developer skills is likewise social-only (X6).
- Missing data: Third-party market data: no firm-level revenue estimates, market-size forecasts, TAM and deal-value benchmarks appear in the findings.
- Missing data: Macro and infrastructure constraints on agent deployment - model cost, latency, compute supply and energy - are not addressed by any finding in this set.
- Limitation: This assessment is built only from the findings supplied. Several topics that matter for an investment view (patents, verified adoption, pricing, margins, market size) have no evidence here, and those gaps are recorded in missing_data rather than filled.
- Limitation: The research-activity metric counts only works whose title or abstract contains the exact phrase 'AI agents'. Synonyms and abbreviations are excluded and the count is not normalised for overall growth in publishing, so the growth rate overstates the topic's relative share of science. The current year is partial.
- Limitation: A large part of the scientific evidence is preprints and abstract-level analysis with medium or low source confidence, and the risk challenges (C1-C6) show that several prominent findings overstate their basis, come from a single study, or are position papers rather than tested work.
- Limitation: Market findings are company self-description in SEC filings plus news headlines that were not read; a company describing a technology is not proof of customer adoption, and headlines are unverified claims given little weight.
- Limitation: X findings are social posts from approved accounts in the last 7 days. They indicate what companies are announcing or emphasising, not what is true, and several of the most commercially suggestive items (agent commerce rails, enterprise adoption rates) exist only there.
- Limitation: Patent evidence is entirely absent because the patent agent did not run, so no statement about intellectual-property position, freedom to operate or patent-based momentum is possible.
- Limitation: Price and timing findings cover a short ~100-trading-day window for a subset of companies and are used strictly as risk context; they cannot speak to valuation, entry points or expected returns, and this assessment deliberately contains no price targets or recommendations of any kind.
- Limitation: Horizon views mix verified facts with interpretation and forecast labels, but the underlying evidence is heavily weighted to the last 12-18 months, so statements about 3-5 years are inherently speculative and marked with low confidence where they are made at all.
- Chief review gap: Core agent capability mechanisms (planning algorithms, reasoning architectures, memory systems, tool-use protocols) are only peripherally covered by the taxonomy paper (S5) and benchmark paper (S1); no retrieved paper provides deep technical coverage of how agents plan, reason, or use tools
- Chief review gap: Multi-agent LLM coordination evidence is explicitly thin (R7): only one theoretical 2024 preprint with limited empirical validation
- Chief review gap: Patent agent was not run, so IP landscape and competitive moat analysis is absent (not fixable by paper search)
- Chief review gap: No quantitative data on agent inference costs or token consumption at scale, limiting cost-structure analysis
- Chief review gap: Market findings show product launches but lack specific revenue or adoption metrics for agent products
- Chief review gap: Patent agent was not run, so there is no IP landscape analysis (patent filings, claims scope, freedom-to-operate) which limits competitive moat assessment.
- Chief review gap: Multi-agent coordination robustness evidence is thin (R7): only one theoretical preprint with limited empirical validation; no peer-reviewed study measuring failure rates under adversarial or Byzantine agent conditions.
- Chief review gap: Cost economics of running agents at scale (inference token consumption, per-task cost curves, cost-to-value ratios) lack rigorous paper-based evidence; the only cost claim (NVIDIA Switchyard, X1) is an unverified social signal.
- Chief review gap: No quantitative production deployment metrics (success rates, mean-time-to-failure, human-override frequency) from enterprise deployments are available in the collected evidence; market findings confirm product launches but not operational outcomes.
- Reference checks changed 1 statement(s) in the assessment (see notes in italics above).
- ERROR [patent/Google Patents (SerpApi)]: counts: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [patent/Google Patents (SerpApi)]: patent search is paused to save the SerpApi quota (SERPAPI_CACHE_ONLY=true) and this query is not in the local cache
- ERROR [timing/Alpha Vantage]: CRM: Alpha Vantage limit or notice: Thank you for using Alpha Vantage! Please consider spreading out your free API requests more sparingly (1 request per second). You may subscribe to any of the p

## Model usage and estimated cost
| Agent | Model | Calls | Prompt tokens | Completion tokens | Est. cost (USD) |
|---|---|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | 3 | 12069 | 4090 | 0.00598 |
| x | z-ai/glm-5.3-flash | 1 | 7653 | 1511 | 0.00137 |
| science | deepseek/deepseek-v4.1-flash | 2 | 10482 | 6988 | 0.01153 |
| market | z-ai/glm-5.3 | 1 | 9214 | 2121 | 0.02714 |
| risk | anthropic/claude-sonnet-5-5 | 2 | 26080 | 9705 | 0.14921 |
| timing | z-ai/glm-5.3-flash | 1 | 1607 | 1224 | 0.00074 |
| investment | deepseek/deepseek-v4.1-flash | 1 | 10269 | 9802 | 0.01424 |
| x (data) | X API pay-per-use | 7 | 0 | 0 | 0.22000 |
| investment (rescore) | deepseek/deepseek-v4.1-flash | 1 | 10630 | 13037 | 0.01823 |

Total estimated cost: $0.44844 (from token counts and config/model_config.yaml prices; the NEAR AI invoice is authoritative).
