# Resources Catalog

This document catalogs all resources gathered for the AI Undetectability Leaderboard research project, including papers, datasets, and code repositories.

---

## Summary

| Category | Count | Description |
|----------|-------|-------------|
| Papers | 12 | Research papers on AI text detection and evasion |
| Datasets | 3+ | Benchmark datasets for training and evaluation |
| Code Repositories | 7 | Implementations of detectors and evasion methods |

---

## Papers

**Total papers downloaded: 12**

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| RAID: A Shared Benchmark for Robust Evaluation | Dugan et al. | 2024 | papers/2405.07940_RAID_Benchmark.pdf | Largest benchmark (6M+ samples), 11 attacks |
| MGTBench: Benchmarking MGT Detection | He et al. | 2024 | papers/2303.14822_MGTBench.pdf | First comprehensive benchmark framework |
| A Watermark for Large Language Models | Kirchenbauer et al. | 2023 | papers/2301.10226_DetectGPT.pdf | Watermarking framework for LLMs |
| Paraphrasing Evades Detectors (DIPPER) | Krishna et al. | 2023 | papers/2303.13408_Paraphrasing_Evades_Detectors.pdf | DIPPER paraphraser, 70%→4.6% evasion |
| SICO: Guided Evasion of AI-Text Detection | Lu et al. | 2024 | papers/2305.10847_SICO_Guided_Evasion.pdf | Prompt-based evasion method |
| M4GT-Bench: Multilingual Benchmark | Wang et al. | 2024 | papers/2402.11175_M4GT_Bench.pdf | Multi-lingual, multi-task benchmark |
| Optimizing Adaptive Attacks on Watermarks | Diaa et al. | 2024 | papers/2410.02440_Adaptive_Attacks_Watermarks.pdf | 96%+ watermark evasion |
| Humanizing Machine-Generated Content | Zhou et al. | 2024 | papers/2404.01907_Humanizing_MGC_Adversarial.pdf | Adversarial humanization attacks |
| Undetectable Watermarks | -- | 2023 | papers/2309.17054_Undetectable_Watermarks.pdf | Theoretical watermark limits |
| SynthID (Nature) | Google DeepMind | 2024 | papers/2310.06356_SynthID_Nature.pdf | Production watermarking system |
| Attacking LLM Watermarks | -- | 2024 | papers/2402.16187_Attacking_LLM_Watermarks.pdf | Watermark attack methods |

See `papers/README.md` for detailed descriptions.

---

## Datasets

**Total datasets identified: 5+ major benchmarks**

### Primary Dataset: RAID

| Attribute | Value |
|-----------|-------|
| **Name** | RAID (Robust AI Detection) |
| **Source** | HuggingFace: `liamdugan/raid` |
| **Size** | 6.2M+ samples (802MB train, 81MB test without attacks) |
| **Task** | Binary AI-text detection |
| **Models** | 11 (GPT-2, GPT-3, GPT-4, ChatGPT, LLaMA 2, Mistral, etc.) |
| **Domains** | 8 (abstracts, books, news, poetry, recipes, reddit, reviews, wikipedia) |
| **Attacks** | 11 (homoglyph, paraphrase, synonym, spacing, etc.) |
| **License** | Apache 2.0 |

**Download Instructions:**
```python
from datasets import load_dataset
raid = load_dataset("liamdugan/raid")
# Or via pip: pip install raid-bench
```

**Sample Location:** `datasets/raid_samples/samples.json`

---

### Secondary Dataset: AI Text Detection Pile

| Attribute | Value |
|-----------|-------|
| **Name** | AI Text Detection Pile |
| **Source** | HuggingFace: `artem9k/ai-text-detection-pile` |
| **Size** | ~2GB |
| **Task** | Binary AI-text detection |
| **Format** | Text with source labels |

**Download Instructions:**
```python
from datasets import load_dataset
pile = load_dataset("artem9k/ai-text-detection-pile")
```

**Sample Location:** `datasets/ai_text_detection_pile_samples/samples.json`

---

### Other Relevant Datasets

| Dataset | Source | Size | Use Case |
|---------|--------|------|----------|
| HC3 | Hello-SimpleAI/HC3 | 26.9K | ChatGPT vs Human QA |
| TuringBench | turingbench/TuringBench | 200K | Multi-model detection |
| M4GT-Bench | MBZUAI | 65K+ | Multilingual detection |
| MGTBench | Google Drive (via repo) | 2.8K+ | Detection benchmarking |

---

## Code Repositories

**Total repositories cloned: 7**

### 1. RAID Benchmark
| Attribute | Value |
|-----------|-------|
| **Name** | RAID Benchmark |
| **URL** | https://github.com/liamdugan/raid |
| **Location** | `code/raid-benchmark/` |
| **Purpose** | Comprehensive detection benchmark with leaderboard |
| **Key Files** | `raid/`, `leaderboard/`, `experiments/` |
| **Install** | `pip install raid-bench` |

---

### 2. MGTBench
| Attribute | Value |
|-----------|-------|
| **Name** | MGTBench |
| **URL** | https://github.com/xinleihe/MGTBench |
| **Location** | `code/mgtbench/` |
| **Purpose** | Benchmarking framework for MGT detection methods |
| **Key Files** | `benchmark.py`, detection methods in `methods/` |
| **Install** | `conda env create -f environment.yml` |

---

### 3. DetectGPT
| Attribute | Value |
|-----------|-------|
| **Name** | DetectGPT |
| **URL** | https://github.com/eric-mitchell/detect-gpt |
| **Location** | `code/detect-gpt/` |
| **Purpose** | Zero-shot detection using probability curvature |
| **Key Files** | `run.py`, `detect_gpt.py` |
| **Usage** | `python run.py --base_model_name gpt2` |

---

### 4. LM Watermarking
| Attribute | Value |
|-----------|-------|
| **Name** | LM Watermarking (Kirchenbauer) |
| **URL** | https://github.com/jwkirchenbauer/lm-watermarking |
| **Location** | `code/lm-watermarking/` |
| **Purpose** | Watermarking and detection for LLM outputs |
| **Key Files** | `extended_watermark_processor.py`, `watermark_reliability_release/` |

---

### 5. Binoculars
| Attribute | Value |
|-----------|-------|
| **Name** | Binoculars |
| **URL** | https://github.com/ahans30/Binoculars |
| **Location** | `code/binoculars/` |
| **Purpose** | SOTA zero-shot LLM detection (ICML 2024) |
| **Key Files** | `binoculars.py` |
| **Install** | `pip install -e .` |

---

### 6. DIPPER Paraphrases
| Attribute | Value |
|-----------|-------|
| **Name** | AI Detection Paraphrases |
| **URL** | https://github.com/martiansideofthemoon/ai-detection-paraphrases |
| **Location** | `code/dipper-paraphrases/` |
| **Purpose** | DIPPER paraphraser for evasion attacks (NeurIPS 2023) |
| **Key Files** | `dipper_paraphrases/paraphrase.py` |
| **Model** | HuggingFace: `kalpeshk2011/dipper-paraphraser-xxl` |

---

### 7. RADAR Detector
| Attribute | Value |
|-----------|-------|
| **Name** | RADAR |
| **URL** | https://github.com/IBM/RADAR |
| **Location** | `code/radar-detector/` |
| **Purpose** | Adversarially robust AI-text detector (NeurIPS 2023) |
| **Key Files** | Training scripts, detector model |

---

## Resource Gathering Notes

### Search Strategy
1. Used paper-finder service for initial literature search
2. Searched HuggingFace Datasets API for AI-text detection datasets
3. Identified key repositories from paper references
4. Prioritized resources with active maintenance and clear documentation

### Selection Criteria
- **Papers**: High citation count, relevance to detection/evasion, recency (2023-2024)
- **Datasets**: Size, diversity of generators/domains, attack coverage
- **Code**: Official implementations, reproducibility, documentation quality

### Challenges Encountered
- Some older datasets (HC3, TuringBench) use deprecated HuggingFace loader scripts
- Large dataset sizes require streaming or sampling for initial exploration
- Some papers have different filenames than expected (mismatch with arXiv IDs)

### Gaps and Workarounds
- Fine-tuning track evasion methods are underrepresented in literature
- Created samples of large datasets for quick validation

---

## Recommendations for Experiment Design

### Primary Dataset
**RAID** - Most comprehensive benchmark with:
- Multiple generators (11)
- Adversarial attacks built-in (11)
- Established leaderboard infrastructure
- Active community

### Baseline Methods

**Detectors (evaluate evasion against):**
1. DetectGPT (zero-shot, open-source)
2. Binoculars (SOTA zero-shot)
3. RADAR (robust to paraphrasing)
4. GPTZero (commercial baseline)

**Evasion Methods (baselines for each track):**

| Track | Baseline Method | Repository |
|-------|-----------------|------------|
| Inference | SICO prompting | Paper implementation |
| Post-editing | DIPPER paraphrasing | `code/dipper-paraphrases/` |
| Fine-tuning | LoRA-based modification | To be implemented |
| Pretraining | Watermark removal | `code/lm-watermarking/` |

### Evaluation Protocol
1. Use RAID test set with hidden labels
2. Evaluate against detector ensemble
3. Report: AUROC, TPR@1%FPR, TPR@5%FPR
4. Measure quality: BERTScore, perplexity
5. Compute Pareto frontier of evasion vs. quality

### Code to Adapt/Reuse
- `code/raid-benchmark/`: Leaderboard infrastructure
- `code/detect-gpt/`: Detection baselines
- `code/dipper-paraphrases/`: Paraphrasing attacks
- `code/binoculars/`: SOTA detection baseline
