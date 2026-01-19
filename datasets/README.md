# Downloaded Datasets

This directory contains datasets for the AI Undetectability Leaderboard research project. Large data files are NOT committed to git due to size. Follow the download instructions below.

## Directory Structure

```
datasets/
├── README.md                           # This file
├── .gitignore                          # Excludes large data files
├── raid_samples/                       # Sample data from RAID
│   └── samples.json                    # 10 example records
├── ai_text_detection_pile_samples/     # Sample data from AI Text Pile
│   └── samples.json                    # 10 example records
└── hc3_samples/                        # Reserved for HC3 samples
```

---

## Dataset 1: RAID (Recommended Primary Dataset)

### Overview
- **Source**: HuggingFace `liamdugan/raid`
- **Size**: 6.2M+ samples (802MB train, 81MB test without attacks)
- **Format**: HuggingFace Dataset / Parquet
- **Task**: Binary AI-text detection + adversarial robustness
- **Splits**: train, test (hidden labels), extra (code, Czech, German)
- **License**: Apache 2.0

### Features
- 11 language models (GPT-2 XL, GPT-3, GPT-4, ChatGPT, LLaMA 2, Mistral, etc.)
- 8 domains (abstracts, books, news, poetry, recipes, reddit, reviews, wikipedia)
- 4 decoding strategies (greedy, sampling, with/without repetition penalty)
- 11 adversarial attacks (homoglyph, paraphrase, synonym, misspelling, etc.)

### Download Instructions

**Using HuggingFace Datasets (recommended):**
```python
from datasets import load_dataset

# Full dataset
raid = load_dataset("liamdugan/raid")

# Streaming (for large data)
raid_stream = load_dataset("liamdugan/raid", split="train", streaming=True)

# Save locally
raid.save_to_disk("datasets/raid")
```

**Using raid-bench package:**
```bash
pip install raid-bench
```

```python
from raid.utils import load_data

train_df = load_data(split="train")
test_df = load_data(split="test")
```

**Direct download:**
```bash
wget https://huggingface.co/datasets/liamdugan/raid/resolve/main/train.parquet -P datasets/raid/
wget https://huggingface.co/datasets/liamdugan/raid/resolve/main/test.parquet -P datasets/raid/
```

### Loading the Dataset

```python
from datasets import load_from_disk
raid = load_from_disk("datasets/raid")

# Or from HuggingFace directly
from datasets import load_dataset
raid = load_dataset("liamdugan/raid")

# Access data
print(raid["train"][0])  # First training example
```

### Sample Data

Example records (see `raid_samples/samples.json`):
```json
{
  "id": "e5e058ce-be2b-459d-af36-32532aaba5ff",
  "model": "human",
  "domain": "abstracts",
  "attack": "none",
  "generation": "The recent advancements in artificial intelligence..."
}
```

### Notes
- Test set labels are hidden for leaderboard evaluation
- Use `raid.run_evaluation()` for automatic scoring
- See https://raid-bench.xyz/ for leaderboard submission

---

## Dataset 2: AI Text Detection Pile

### Overview
- **Source**: HuggingFace `artem9k/ai-text-detection-pile`
- **Size**: ~2GB
- **Format**: HuggingFace Dataset
- **Task**: Binary AI-text detection
- **License**: Check source

### Download Instructions

```python
from datasets import load_dataset

# Full dataset
pile = load_dataset("artem9k/ai-text-detection-pile")

# Streaming (recommended for large data)
pile_stream = load_dataset("artem9k/ai-text-detection-pile", split="train", streaming=True)

# Save locally
pile.save_to_disk("datasets/ai_text_detection_pile")
```

### Sample Data

Example (see `ai_text_detection_pile_samples/samples.json`):
```json
{
  "source": "human",
  "id": 12345,
  "text": "Example human-written text..."
}
```

---

## Dataset 3: HC3 (Human-ChatGPT Comparison)

### Overview
- **Source**: HuggingFace `Hello-SimpleAI/HC3`
- **Size**: 26.9K samples
- **Format**: HuggingFace Dataset
- **Task**: Human vs ChatGPT comparison in QA
- **Languages**: English, Chinese

### Download Instructions

```python
from datasets import load_dataset

# Note: Uses deprecated script, may need older datasets version
hc3 = load_dataset("Hello-SimpleAI/HC3", "all")

# Or download raw data from GitHub
# https://github.com/Hello-SimpleAI/chatgpt-comparison-detection
```

---

## Dataset 4: MGTBench Datasets

### Overview
- **Source**: Google Drive (via MGTBench repository)
- **Size**: ~2.8K+ samples
- **Format**: CSV/JSON
- **Task**: Detection benchmarking
- **Datasets**: Essay, WP (Writing Prompts), Reuters

### Download Instructions

1. Clone MGTBench repository:
```bash
git clone https://github.com/xinleihe/MGTBench.git
```

2. Download datasets from Google Drive link in repository README

3. Place in appropriate directory:
```bash
mv MGTBench/data/* datasets/mgtbench/
```

---

## Additional Datasets

### M4GT-Bench (Multilingual)
- **Source**: MBZUAI (check paper for access)
- **Languages**: English, Arabic, Bulgarian, Chinese, German, Italian, Russian, Urdu
- **Tasks**: Binary detection, generator attribution, change-point detection

### TuringBench
- **Source**: HuggingFace `turingbench/TuringBench`
- **Size**: 200K samples
- **Note**: Uses deprecated loader script

---

## Git Ignore Configuration

Large data files are excluded from git. The `.gitignore` includes:
```
# Exclude all data files (can be large)
*

# But include documentation and small samples
!.gitignore
!README.md
!**/README.md
!**/samples/
!**/samples.json
```

To verify what's tracked:
```bash
git status datasets/
```
