# AI Undetectability Leaderboard

A prototype framework for systematically benchmarking methods that make AI-generated text less detectable while preserving quality.

## Overview

This research establishes a four-track leaderboard for AI text undetectability:
- **Inference Track**: Prompt modifications to generate less detectable text
- **Post-editing Track**: Paraphrasing/rewriting AI text to humanize it
- **Fine-tuning Track**: (Future) Adapter-based model modifications
- **Pretraining Track**: (Future) Training-time interventions

## Key Findings

| Rank | Track | Method | Evasion Rate | Quality Score |
|------|-------|--------|--------------|---------------|
| 1 | Inference | human_style | **70%** | 1.00 |
| 2 | Inference | varied | **70%** | 1.00 |
| 3 | Post-editing | casual_style | **70%** | 0.16 |
| 4 | Post-editing | simple_paraphrase | **70%** | 0.42 |

**Main Results:**
- Inference-time prompt modifications achieve 70% evasion with 100% quality preservation
- Post-editing matches evasion rates but significantly degrades content quality
- Personalization strategies paradoxically *increase* detectability
- The "human_style" system prompt is the most effective method tested

## Repository Structure

```
.
├── src/
│   ├── experiment.py      # Main experiment code
│   └── visualize.py       # Visualization generation
├── datasets/
│   ├── raid_samples/      # AI-generated text samples
│   └── ai_text_detection_pile_samples/  # Human-written samples
├── results/
│   ├── experiment_results.json  # Full experimental data
│   └── leaderboard.csv          # Leaderboard rankings
├── figures/
│   ├── leaderboard_comparison.png
│   ├── evasion_vs_quality.png
│   ├── detection_scores_dist.png
│   └── track_summary.png
├── planning.md            # Research plan
└── REPORT.md              # Full research report
```

## Reproduction

### Environment Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv add numpy pandas matplotlib seaborn scikit-learn torch transformers datasets openai anthropic tqdm httpx bert-score scipy
```

### Running Experiments

```bash
# Run main experiment
python src/experiment.py

# Generate visualizations
python src/visualize.py
```

### Requirements

- Python 3.10+
- OpenAI API key (set `OPENAI_API_KEY` environment variable)
- GPU recommended (2x RTX 3090 used in original experiments)
- ~15 minutes execution time

## Methodology

### Detection Ensemble

1. **Perplexity Detector**: GPT-2 based log-likelihood scoring
   - Lower perplexity = more AI-like
2. **Burstiness Detector**: Structural pattern analysis
   - Lower variance = more AI-like
3. **Ensemble**: Weighted combination (60% perplexity, 40% burstiness)

### Evasion Strategies Tested

**Inference Track:**
- Baseline: Standard generation
- Human Style: System prompt for human-like writing
- Personal: Add personal anecdotes/opinions
- Varied: Varied sentence structures

**Post-editing Track:**
- Baseline: No editing
- Simple Paraphrase: Basic rewriting
- Casual Style: Informal tone
- Personal Style: Add personal elements

## Limitations

- Small sample size (10 per method) limits statistical power
- Only GPT-4o-mini tested as generator
- Detection limited to perplexity + burstiness (no semantic analysis)
- Fine-tuning and pretraining tracks not implemented

## Citation

If you use this work, please cite:

```bibtex
@misc{ai-undetectability-leaderboard-2026,
  title={AI Undetectability Leaderboard: A Framework for Benchmarking Text Humanization},
  author={Research Team},
  year={2026},
  url={https://github.com/ai-undetectability-leaderboard}
}
```

## License

MIT License

## Related Work

- [RAID Benchmark](https://raid-bench.xyz/) - Detection benchmark
- [MGTBench](https://github.com/xinleihe/MGTBench) - Detection framework
- [DIPPER](https://github.com/martiansideofthemoon/ai-detection-paraphrases) - Paraphrasing attacks
- [Binoculars](https://github.com/ahans30/Binoculars) - Zero-shot detection
