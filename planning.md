# Research Plan: AI Undetectability Leaderboard

## Motivation & Novelty Assessment

### Why This Research Matters

The ability to detect AI-generated text is crucial for maintaining trust in digital communication, academic integrity, and content authenticity. Simultaneously, there is growing interest in making AI-generated text less detectable—for legitimate purposes like improving naturalness, assisting users who need to produce human-like text, and understanding the limitations of current detection systems. Creating a standardized leaderboard allows systematic comparison of methods across different intervention points (inference, post-editing, fine-tuning, pretraining), enabling researchers to understand the trade-offs between detectability and text quality across different approaches.

### Gap in Existing Work

Based on the literature review, several significant gaps exist:

1. **No unified multi-track benchmark**: RAID, MGTBench, and M4GT-Bench focus primarily on detection methods, not on systematically evaluating evasion techniques across different intervention points. There is no benchmark that organizes evasion methods by *where* in the pipeline they operate.

2. **Quality preservation metrics underexplored**: Most evasion research reports detection evasion rates but doesn't systematically track how much semantic content is preserved. This is particularly important for post-editing where the goal is to maintain information while reducing detectability.

3. **Lack of standardized comparison across tracks**: Prompt-based evasion (SICO), paraphrasing (DIPPER), and other methods are evaluated in isolation against different detectors, making cross-method comparison difficult.

4. **Missing infrastructure for the four tracks**: The user's proposed structure (inference, post-editing, fine-tuning, pretraining) does not exist as an organized benchmark framework.

### Our Novel Contribution

We propose a **four-track AI undetectability leaderboard framework** that:
1. Defines standardized evaluation protocols for each track (inference, post-editing, fine-tuning, pretraining)
2. Uses a fixed detector ensemble for fair comparison across all tracks
3. Measures both evasion success AND quality preservation using Pareto-optimal frontiers
4. Provides baseline implementations and evaluation code for each track

This research will prototype the leaderboard by:
- Testing baseline methods for each track against a detector ensemble
- Measuring evasion rates (AUROC, TPR@FPR thresholds)
- Measuring quality preservation (semantic similarity, information retention)
- Identifying which track offers the best evasion-quality trade-off

### Experiment Justification

| Experiment | Why Needed |
|------------|-----------|
| Exp 1: Baseline detection setup | Establish the ground truth detection performance before any evasion; this is essential for measuring improvement |
| Exp 2: Inference track evaluation | Test SICO-style prompt modifications to see if inference-time interventions can reduce detection while maintaining quality |
| Exp 3: Post-editing track evaluation | Test paraphrasing approaches (DIPPER-style) to measure post-hoc humanization effectiveness |
| Exp 4: Cross-track comparison | Compare all methods on same test set to produce unified leaderboard rankings |
| Exp 5: Quality-evasion trade-off analysis | Produce Pareto frontiers to understand which track offers best trade-offs |

---

## Research Question

**Primary Question**: Can a unified leaderboard framework with four tracks (inference, post-editing, fine-tuning, pretraining) systematically benchmark AI text undetectability methods while maintaining output quality?

**Sub-Questions**:
1. How do inference-time interventions (prompt engineering) compare to post-editing (paraphrasing) for evasion?
2. What is the quality-evasion trade-off for each track?
3. Which detectors are most robust across different evasion methods?

---

## Background and Motivation

AI-generated text detection is an arms race: as detectors improve, evasion techniques advance. The literature shows:
- Detectors like DetectGPT, Binoculars, and RADAR achieve >90% accuracy on unperturbed AI text
- DIPPER paraphrasing drops DetectGPT from 70.3% to 4.6% detection rate
- SICO prompting reduces detector AUC by ~0.5 on average
- No unified framework compares these methods systematically

This research establishes a prototypical leaderboard to enable fair, systematic comparison.

---

## Hypothesis Decomposition

**H1**: Inference-time modifications (prompt engineering) can reduce detection rates without accessing model internals.
*Measurable*: Detection AUROC drops by ≥0.1 compared to baseline prompts.

**H2**: Post-editing (paraphrasing) provides stronger evasion than inference-time methods but may degrade content quality.
*Measurable*: Post-editing achieves lower detectability but lower semantic similarity to original.

**H3**: A fixed detector ensemble provides more robust evaluation than single detectors.
*Measurable*: Ensemble rankings are more stable across test sets than individual detector rankings.

**H4**: There exists a Pareto-optimal frontier showing trade-offs between evasion and quality.
*Measurable*: Plotting evasion rate vs. quality shows clear trade-off patterns.

---

## Proposed Methodology

### Approach

We will implement a prototype leaderboard testing 2 tracks (inference and post-editing) due to resource constraints:
- **Inference track**: Modify prompts to produce less detectable outputs from a fixed model (GPT-4 via API)
- **Post-editing track**: Apply paraphrasing/rewriting to AI-generated text

Fine-tuning and pretraining tracks require substantial compute and are noted as future work.

### Experimental Steps

1. **Data Preparation**
   - Use RAID dataset samples (diverse domains, known human/AI labels)
   - Create test set of ~500 samples (mixed human and AI-generated)
   - Prepare prompts for generating new AI text

2. **Detector Ensemble Setup**
   - Implement or adapt: DetectGPT (zero-shot curvature), Binoculars (cross-model perplexity)
   - Use as ensemble: average scores for final decision
   - Validate on known RAID samples

3. **Inference Track Implementation**
   - Baseline: Standard GPT-4 generation
   - Intervention 1: Human-style prompts ("Write as a human would...")
   - Intervention 2: In-context examples from human text
   - Intervention 3: Style-specific instructions (informal, personal anecdotes)

4. **Post-Editing Track Implementation**
   - Baseline: Unmodified AI text
   - Intervention 1: LLM-based paraphrasing (GPT-4 as paraphraser)
   - Intervention 2: Multiple-pass rewriting
   - Intervention 3: Sentence-level restructuring

5. **Quality Metrics**
   - Semantic similarity: BERTScore between original and modified text
   - Information retention: LLM-judged assessment of content preservation
   - Fluency: Perplexity measurement

6. **Evaluation Protocol**
   - Run all methods on same test prompts
   - Collect detector scores
   - Compute AUROC, TPR@1%FPR, TPR@5%FPR
   - Compute quality metrics
   - Produce leaderboard rankings

### Baselines

| Track | Baseline | Expected Performance |
|-------|----------|---------------------|
| Inference | Standard GPT-4 greedy | High detection (~90% AUROC) |
| Post-editing | No editing | High detection (~90% AUROC) |

### Evaluation Metrics

**Detection Metrics** (lower = better evasion):
- AUROC: Area under ROC curve
- TPR@1%FPR: True positive rate at 1% false positive rate
- TPR@5%FPR: True positive rate at 5% false positive rate

**Quality Metrics** (higher = better):
- BERTScore: Semantic similarity (0-1)
- Information Retention: LLM-judged score (1-5)

**Combined Metric**:
- Pareto optimality: Identify methods on the efficient frontier

### Statistical Analysis Plan

- Report mean ± std across 3 random seeds where applicable
- Use bootstrap confidence intervals for AUROC
- McNemar's test for comparing paired detection accuracy
- Significance level: α = 0.05

---

## Expected Outcomes

**Supporting H1-H4**:
- Inference modifications reduce detection by 10-30%
- Post-editing reduces detection by 40-70%
- Post-editing has lower semantic similarity than inference modifications
- Clear Pareto frontier exists

**Refuting hypotheses**:
- If inference modifications have no effect, H1 is refuted
- If post-editing preserves quality while evading detection, H2 is modified

---

## Timeline and Milestones

| Phase | Activities |
|-------|------------|
| Setup (30 min) | Environment, data loading, detector implementation |
| Inference track (60 min) | Generate samples with different prompts, evaluate |
| Post-editing track (60 min) | Apply paraphrasing, evaluate |
| Analysis (45 min) | Statistical tests, visualizations, Pareto analysis |
| Documentation (30 min) | REPORT.md, README.md |

---

## Potential Challenges

1. **API rate limits**: Mitigate by caching responses, using smaller samples
2. **Detector implementation complexity**: Use existing code from `code/` directory
3. **Quality metric subjectivity**: Use multiple metrics for robustness
4. **Detector variance**: Use ensemble to reduce noise

---

## Success Criteria

1. ✓ Successfully run experiments for 2 tracks
2. ✓ Produce detection metrics for all methods
3. ✓ Produce quality metrics for all methods
4. ✓ Generate leaderboard ranking table
5. ✓ Identify Pareto-optimal methods
6. ✓ Document findings in REPORT.md
