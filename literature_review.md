# Literature Review: AI Undetectability Leaderboard

## Research Area Overview

The field of AI-generated text detection has rapidly evolved with the proliferation of large language models (LLMs) like ChatGPT, GPT-4, and Claude. This research domain encompasses two opposing objectives:
1. **Detection**: Developing methods to identify AI-generated text
2. **Evasion**: Creating techniques to make AI-generated text less detectable

This literature review synthesizes the current state of both detection and evasion methods, along with benchmarking efforts that evaluate their effectiveness.

---

## Key Papers

### 1. RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors

- **Authors**: Liam Dugan, Alyssa Hwang, Filip Trhlík, Josh Magnus Ludan, Andrew Zhu, Hainiu Xu, Daphne Ippolito, Chris Callison-Burch
- **Year**: 2024
- **Source**: ACL 2024
- **File**: `papers/2405.07940_RAID_Benchmark.pdf`

**Key Contribution**: The largest and most challenging benchmark for AI-generated text detection, containing 6M+ generations spanning 11 models, 8 domains, 11 adversarial attacks, and 4 decoding strategies.

**Methodology**:
- Creates a comprehensive dataset with human-written and machine-generated text across diverse domains (abstracts, recipes, books, Reddit, news, reviews, poetry, Wikipedia)
- Includes 11 generators: GPT-2 XL, GPT-3, GPT-4, ChatGPT, Cohere, Mistral-7B, MPT-30B, LLaMA 2 70B
- Tests 12 detectors (8 open-source, 4 commercial) including RoBERTa-based, GLTR, DetectGPT, Binoculars, GPTZero

**Key Findings**:
- Current detectors are easily fooled by adversarial attacks and variations in sampling strategies
- Metric-based detectors suffer from high false positive rates when thresholded naively
- Provides public leaderboard at https://raid-bench.xyz/

**Relevance**: This is the most comprehensive benchmark and directly relevant to building an undetectability leaderboard.

---

### 2. MGTBench: Benchmarking Machine-Generated Text Detection

- **Authors**: Xinlei He, Xinyue Shen, Zeyuan Chen, Michael Backes, Yang Zhang
- **Year**: 2024
- **Source**: ACM CCS 2024
- **File**: `papers/2303.14822_MGTBench.pdf`

**Key Contribution**: First benchmark framework for MGT detection against powerful LLMs, implementing 10+ detection methods.

**Methodology**:
- Tests 13 detection methods against 6 LLMs (ChatGLM, Dolly, ChatGPT-turbo, GPT4All, StableLM, Claude)
- Uses 3 benchmark datasets: Essay, WP (Writing Prompts), Reuters
- Includes metric-based methods (Log-Likelihood, Rank, Entropy, DetectGPT, GLTR) and model-based methods (OpenAI Detector, LM Detector, ConDA, GPTZero)

**Key Findings**:
- LM Detector (fine-tuned BERT) outperforms other methods
- 200 words is sufficient length for satisfactory detection
- Detection methods are highly susceptible to adversarial attacks (paraphrasing, random spacing, perturbations)

**Relevance**: Provides modular benchmarking framework that can be extended for undetectability research.

---

### 3. A Watermark for Large Language Models

- **Authors**: John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, Tom Goldstein
- **Year**: 2023
- **Source**: ICML 2023
- **File**: `papers/2301.10226_DetectGPT.pdf` (Note: This is the watermarking paper despite filename)

**Key Contribution**: A watermarking framework that embeds imperceptible signals into generated text for algorithmic detection.

**Methodology**:
- Selects a randomized "green list" of tokens before each word generation
- Softly promotes green tokens during sampling using a logit bias δ
- Detection uses z-test on proportion of green tokens

**Key Findings**:
- Watermark detectable with as few as 25 tokens
- Negligible impact on text quality
- Detection possible without access to model API or parameters

**Relevance**: Represents the "active" detection approach that could be included in a pretraining track.

---

### 4. Paraphrasing Evades Detectors of AI-Generated Text, but Retrieval is an Effective Defense

- **Authors**: Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, Mohit Iyyer
- **Year**: 2023
- **Source**: NeurIPS 2023
- **File**: `papers/2303.13408_Paraphrasing_Evades_Detectors.pdf`

**Key Contribution**: Introduces DIPPER (Discourse Paraphraser), an 11B parameter model that successfully evades multiple detectors.

**Methodology**:
- Fine-tuned T5-XXL for paragraph-level paraphrasing
- Control knobs for lexical diversity (0-100) and content reordering (0-100)
- Tests against watermarking, GPTZero, DetectGPT, OpenAI's classifier

**Key Findings**:
- DIPPER drops DetectGPT accuracy from 70.3% to 4.6% (at 1% FPR)
- Paraphrasing is highly effective attack against all tested detectors
- Proposes retrieval-based defense: searching database of prior generations

**Relevance**: Critical for the "post-editing" track - paraphrasing is the most effective evasion technique.

---

### 5. Large Language Models can be Guided to Evade AI-Generated Text Detection (SICO)

- **Authors**: Ning Lu, Shengcai Liu, Rui He, Yew-Soon Ong, Qi Wang, Ke Tang
- **Year**: 2024
- **Source**: TMLR 2024
- **File**: `papers/2305.10847_SICO_Guided_Evasion.pdf`

**Key Contribution**: SICO (Substitution-based In-Context example Optimization) automatically constructs prompts to evade detectors without external paraphrasers.

**Methodology**:
- Uses only 40 human-written examples and limited LLM inferences
- Iteratively substitutes words/sentences in in-context examples
- Task-specific prompts work universally against multiple detectors

**Key Findings**:
- Decreases detector AUC by ~0.5 on average
- Enables GPT-3.5 to successfully evade 6 detectors
- More cost-efficient than external paraphrasers

**Relevance**: Relevant to "inference" track - modifying prompts to produce less detectable output.

---

### 6. M4GT-Bench: Evaluation Benchmark for Black-Box Machine-Generated Text Detection

- **Authors**: Yuxia Wang, Jonibek Mansurov, Petar Ivanov, et al.
- **Year**: 2024
- **Source**: MBZUAI
- **File**: `papers/2402.11175_M4GT_Bench.pdf`

**Key Contribution**: Multi-lingual, multi-domain, multi-generator corpus with three detection tasks.

**Methodology**:
- Task 1: Binary human vs. machine classification (mono/multilingual)
- Task 2: Multi-way generator attribution
- Task 3: Mixed text change-point detection (where human text transitions to AI)
- Includes 6 generators across multiple languages

**Key Findings**:
- Provides unique multilingual evaluation (Arabic, Bulgarian, Chinese, German, Italian, Russian, Urdu)
- Tests generalization to unseen generators (GPT-4)

**Relevance**: Provides multi-task framework beyond simple binary detection.

---

### 7. Optimizing Adaptive Attacks against Watermarks for Language Models

- **Authors**: Abdulrahman Diaa, Toluwani Aremu, Nils Lukas
- **Year**: 2024
- **Source**: arXiv
- **File**: `papers/2410.02440_Adaptive_Attacks_Watermarks.pdf`

**Key Contribution**: Shows that adaptive attacks can evade all surveyed watermarking methods with <7 GPU hours.

**Methodology**:
- Uses preference-based optimization (DPO) to tune paraphrasers against watermarks
- No-box, offline attacker setting (no access to watermark key or samples)
- Tests against Kirchenbauer, Aaronson, Christ, and other watermarks

**Key Findings**:
- Achieves >96% evasion rate with negligible quality impact
- Training against any watermark transfers to unseen watermarks
- Attacks are Pareto optimal in quality-evasion tradeoff

**Relevance**: Demonstrates fundamental limits of watermarking robustness.

---

### 8. Humanizing Machine-Generated Content: Evading AI-Text Detection through Adversarial Attack

- **Authors**: Ying Zhou, Ben He, Le Sun
- **Year**: 2024
- **Source**: ACL 2024
- **File**: `papers/2404.01907_Humanizing_MGC_Adversarial.pdf`

**Key Contribution**: Proposes adversarial attack methods to "humanize" machine-generated text.

**Methodology**:
- Word-level and sentence-level perturbations
- Targets both training-based and statistical detectors

**Relevance**: Provides post-editing approaches for the undetectability benchmark.

---

### 9. DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature

- **Authors**: Eric Mitchell, Yoonho Lee, Alexander Khazatsky, Christopher D. Manning, Chelsea Finn
- **Year**: 2023
- **Source**: ICML 2023

**Key Contribution**: Zero-shot detection based on log probability curvature.

**Methodology**:
- AI-generated text lies in negative curvature regions of model's log probability
- Compares log probability of original vs. perturbed text
- No training required

**Relevance**: Widely-used baseline detector in benchmarks.

---

### 10. Binoculars: Zero-Shot Detection of LLM-Generated Text

- **Authors**: Abhimanyu Hans, Avi Schwarzschild, Valeriia Cherepanova, et al.
- **Year**: 2024
- **Source**: ICML 2024

**Key Contribution**: State-of-the-art zero-shot detection using contrasting two related LLMs.

**Methodology**:
- Computes score from ratio of perplexities between two related models
- No training data required

**Key Findings**:
- Detects 90%+ of ChatGPT outputs at 0.01% FPR
- Strong domain generalization

**Relevance**: Current SOTA baseline for detection.

---

### 11. RADAR: Robust AI-Text Detection via Adversarial Learning

- **Authors**: Xiaomeng Hu, Pin-Yu Chen, Tsung-Yi Ho
- **Year**: 2023
- **Source**: NeurIPS 2023

**Key Contribution**: Joint adversarial training of paraphraser and detector for robustness.

**Methodology**:
- Paraphraser learns to evade detector
- Detector learns to catch paraphrased text
- Iterative adversarial game

**Key Findings**:
- Improves robustness by 31.64% over baseline methods
- Transfers to unseen LLMs

**Relevance**: Represents robust detection approach.

---

## Common Methodologies

### Detection Methods
| Category | Methods | Used In Papers |
|----------|---------|----------------|
| Metric-based | Log-Likelihood, Rank, Entropy, DetectGPT, Binoculars | RAID, MGTBench, M4GT |
| Training-based | RoBERTa classifiers, BERT fine-tuning, RADAR | RAID, MGTBench |
| Watermarking | Kirchenbauer (KGW), SynthID | Watermark papers |
| Commercial | GPTZero, Originality, Winston, ZeroGPT | RAID |

### Evasion Methods
| Category | Methods | Effectiveness |
|----------|---------|---------------|
| Paraphrasing | DIPPER, T5-based | Very High (70%→4.6% detection) |
| Prompt-based | SICO, in-context examples | High (~50% AUC drop) |
| Simple attacks | Homoglyphs, spacing, misspelling | Moderate |
| Watermark attacks | DPO-tuned paraphrasers | Very High (96%+ evasion) |

---

## Standard Baselines

### Detectors
1. **DetectGPT** - Zero-shot curvature-based
2. **Binoculars** - Zero-shot cross-model perplexity
3. **OpenAI Classifier** - Commercial
4. **GPTZero** - Commercial
5. **RADAR** - Adversarially robust
6. **Ghostbuster** - Feature-based classifier

### Evasion Techniques
1. **DIPPER paraphrasing** - SOTA for post-editing
2. **SICO prompting** - SOTA for inference-time
3. **Simple perturbations** - Homoglyphs, spacing, synonyms

---

## Evaluation Metrics

| Metric | Description | Usage |
|--------|-------------|-------|
| AUROC | Area Under ROC Curve | Primary detection metric |
| Accuracy@FPR | Accuracy at fixed false positive rate (e.g., 1%, 5%) | Practical evaluation |
| F1 Score | Harmonic mean of precision/recall | Balanced evaluation |
| TPR@FPR | True positive rate at fixed FPR | Security-focused |

---

## Datasets in the Literature

| Dataset | Size | Domains | Generators | Attacks |
|---------|------|---------|------------|---------|
| RAID | 6.2M | 8 | 11 | 11 |
| MGTBench | 2.8K+ | 3 | 6 | 3 |
| M4GT-Bench | 65K+ | 6 | 6 | Limited |
| HC3 | 26.9K | QA | ChatGPT | None |
| TuringBench | 200K | Multiple | Multiple | None |

---

## Gaps and Opportunities

### Research Gaps
1. **Unified Benchmark**: No single benchmark covers all four tracks (inference, post-editing, fine-tuning, pretraining)
2. **Quality Preservation**: Limited work on maintaining text quality while evading detection
3. **Multi-model Attacks**: Most attacks target single detectors, not ensembles
4. **Adaptive Defenses**: Few detectors adapt to known attack patterns
5. **Real-world Evaluation**: Limited testing on actual misuse scenarios

### Leaderboard Opportunities
1. **Track Structure**: Organize by evasion method type:
   - Inference track: Prompt-based evasion (SICO)
   - Post-editing track: Paraphrasing (DIPPER)
   - Fine-tuning track: Adapter-based modifications
   - Pretraining track: Training-time interventions (watermark removal)

2. **Metrics for Undetectability**:
   - Evasion rate against detector ensemble
   - Quality preservation (semantic similarity, fluency)
   - Computational cost

---

## Recommendations for Our Experiment

### Recommended Datasets
1. **RAID** (Primary) - Most comprehensive, with attacks and leaderboard infrastructure
2. **M4GT-Bench** - For multilingual evaluation
3. **HC3** - For domain-specific testing

### Recommended Baselines
**Detectors to evaluate against:**
- DetectGPT, Binoculars, RADAR (open-source SOTA)
- GPTZero (commercial baseline)

**Evasion baselines:**
- DIPPER paraphrasing (post-editing track)
- SICO prompting (inference track)
- Simple attacks (baseline)

### Recommended Metrics
- Primary: AUROC, TPR@1%FPR, TPR@5%FPR
- Quality: Semantic similarity (BERTScore), Fluency (perplexity)
- Combined: Pareto frontier of evasion vs. quality

### Methodological Considerations
1. Use fixed detector ensemble for fair comparison
2. Report quality metrics alongside evasion rates
3. Test generalization across domains and generators
4. Consider computational cost of evasion methods
