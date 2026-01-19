# Cloned Repositories

This directory contains cloned code repositories for AI text detection and evasion research.

## Repository Overview

| Repository | Purpose | URL |
|------------|---------|-----|
| raid-benchmark | Comprehensive detection benchmark | https://github.com/liamdugan/raid |
| mgtbench | Detection benchmarking framework | https://github.com/xinleihe/MGTBench |
| detect-gpt | Zero-shot detection (probability curvature) | https://github.com/eric-mitchell/detect-gpt |
| lm-watermarking | LLM watermarking (Kirchenbauer) | https://github.com/jwkirchenbauer/lm-watermarking |
| binoculars | SOTA zero-shot detection (ICML 2024) | https://github.com/ahans30/Binoculars |
| dipper-paraphrases | DIPPER paraphraser for evasion | https://github.com/martiansideofthemoon/ai-detection-paraphrases |
| radar-detector | Adversarially robust detector | https://github.com/IBM/RADAR |

---

## 1. RAID Benchmark

**Location**: `raid-benchmark/`

**Purpose**: Largest and most comprehensive benchmark for AI-generated text detection.

**Key Files**:
- `raid/` - Main package with data loading and evaluation
- `leaderboard/` - Leaderboard submission infrastructure
- `experiments/` - Experiment scripts

**Installation**:
```bash
pip install raid-bench
```

**Usage**:
```python
from raid import run_detection, run_evaluation
from raid.utils import load_data

train_df = load_data(split="train")
predictions = run_detection(my_detector, train_df)
results = run_evaluation(predictions, train_df)
```

---

## 2. MGTBench

**Location**: `mgtbench/`

**Purpose**: Modular benchmarking framework for MGT detection methods.

**Key Files**:
- `benchmark.py` - Main benchmarking script
- `methods/` - Detection method implementations
- `data/` - Dataset loaders

**Installation**:
```bash
cd mgtbench
conda env create -f environment.yml
```

**Usage**:
```bash
python benchmark.py --dataset Essay --detectLLM Claude --method Log-Likelihood
```

---

## 3. DetectGPT

**Location**: `detect-gpt/`

**Purpose**: Zero-shot detection using probability curvature.

**Key Files**:
- `run.py` - Main detection script
- `detect_gpt.py` - Core detection algorithm

**Usage**:
```bash
python run.py --base_model_name gpt2 --mask_filling_model_name t5-small
```

---

## 4. LM Watermarking

**Location**: `lm-watermarking/`

**Purpose**: Watermarking and detection for LLM outputs.

**Key Files**:
- `extended_watermark_processor.py` - Extended implementation (recommended)
- `watermark_reliability_release/` - Reliability experiments

**Usage**:
```python
from watermark_processor import WatermarkLogitsWarper

# During generation
warper = WatermarkLogitsWarper(gamma=0.5, delta=2.0)
# Modifies logits to embed watermark
```

---

## 5. Binoculars

**Location**: `binoculars/`

**Purpose**: SOTA zero-shot detection using cross-model perplexity (ICML 2024).

**Key Files**:
- `binoculars.py` - Core detection module

**Installation**:
```bash
cd binoculars
pip install -e .
```

**Usage**:
```python
from binoculars import Binoculars

detector = Binoculars()
score = detector.compute_score(text)
```

---

## 6. DIPPER Paraphrases

**Location**: `dipper-paraphrases/`

**Purpose**: DIPPER paraphraser for evasion attacks (NeurIPS 2023).

**Key Files**:
- `dipper_paraphrases/paraphrase.py` - Paraphrasing script
- `dipper_paraphrases/paraphrase_minimal.py` - Minimal version

**Model**:
```python
# Download from HuggingFace
model_name = "kalpeshk2011/dipper-paraphraser-xxl"
```

**Usage**:
```python
# Set lexical diversity (0-100) and order diversity (0-100)
output = dipper.paraphrase(text, lex_diversity=60, order_diversity=0)
```

---

## 7. RADAR Detector

**Location**: `radar-detector/`

**Purpose**: Adversarially robust AI-text detector (NeurIPS 2023).

**Key Features**:
- Joint training of paraphraser and detector
- Robust to paraphrasing attacks
- Tested on 8 LLMs

**Usage**: See repository README for training and evaluation scripts.

---

## Notes

- All repositories are cloned with `--depth 1` to minimize size
- Check individual repository READMEs for detailed documentation
- Some repositories may require GPU for inference
- Model weights are typically downloaded separately from HuggingFace
