"""
AI Undetectability Leaderboard Experiment

This script implements a prototype leaderboard for testing AI text undetectability
across two tracks: inference and post-editing.

Tracks:
1. Inference: Modify prompts to produce less detectable AI text
2. Post-editing: Apply paraphrasing to existing AI text to humanize it
"""

import os
import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple
import numpy as np
import torch
from tqdm import tqdm
from openai import OpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics import roc_auc_score, precision_recall_curve
from scipy import stats
import pandas as pd

# Set random seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

# Configuration
CONFIG = {
    "seed": SEED,
    "model": "gpt-4o-mini",  # Use gpt-4o-mini for cost-efficiency
    "detection_model": "gpt2",  # For perplexity-based detection
    "n_samples": 50,  # Number of samples per condition
    "max_tokens": 200,  # Max tokens for generation
    "temperature": 0.7,
    "timestamp": datetime.now().isoformat()
}


class PerplexityDetector:
    """
    Perplexity-based AI text detector.

    AI text tends to have lower perplexity (more predictable patterns)
    than human text. This is a simplified version of metrics used in
    DetectGPT and Binoculars.
    """

    def __init__(self, model_name: str = "gpt2", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Loading detection model {model_name} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        self.model.eval()

        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def compute_perplexity(self, text: str) -> float:
        """Compute perplexity of text using the model."""
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss
                perplexity = torch.exp(loss).item()

            return perplexity
        except Exception as e:
            print(f"Error computing perplexity: {e}")
            return float('inf')

    def detect(self, text: str) -> float:
        """
        Return detection score (higher = more likely AI).
        We use negative log perplexity since AI text has lower perplexity.
        """
        perplexity = self.compute_perplexity(text)
        if perplexity == float('inf'):
            return 0.5
        # Lower perplexity = more AI-like, so we invert
        # Normalize to 0-1 range approximately
        score = 1.0 / (1.0 + np.log(perplexity + 1))
        return score


class BurstinessDetector:
    """
    Burstiness-based AI text detector.

    Human text tends to have more variable sentence lengths and
    vocabulary diversity compared to AI text.
    """

    def detect(self, text: str) -> float:
        """
        Return detection score based on text regularity.
        Higher score = more likely AI (less bursty/more regular).
        """
        # Split into sentences
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

        if len(sentences) < 2:
            return 0.5

        # Compute sentence length variance (lower variance = more AI-like)
        lengths = [len(s.split()) for s in sentences]
        length_std = np.std(lengths) if len(lengths) > 1 else 0

        # Word uniqueness ratio
        words = text.lower().split()
        if len(words) == 0:
            return 0.5
        unique_ratio = len(set(words)) / len(words)

        # Combine: lower variance + lower uniqueness = more AI-like
        # Normalize to 0-1 (inverted so higher = more AI)
        regularity_score = 1.0 / (1.0 + length_std / 10)
        uniformity_score = 1.0 - unique_ratio

        score = 0.5 * regularity_score + 0.5 * uniformity_score
        return min(1.0, max(0.0, score))


class EnsembleDetector:
    """Ensemble of multiple detectors."""

    def __init__(self, device: str = None):
        self.perplexity_detector = PerplexityDetector(device=device)
        self.burstiness_detector = BurstinessDetector()

    def detect(self, text: str) -> Dict[str, float]:
        """Return detection scores from all detectors and ensemble."""
        perplexity_score = self.perplexity_detector.detect(text)
        burstiness_score = self.burstiness_detector.detect(text)
        ensemble_score = 0.6 * perplexity_score + 0.4 * burstiness_score

        return {
            "perplexity": perplexity_score,
            "burstiness": burstiness_score,
            "ensemble": ensemble_score
        }


class TextGenerator:
    """Generates AI text with various prompt strategies."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = 200,
                 temperature: float = 0.7) -> str:
        """Generate text using OpenAI API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""


class PostEditor:
    """Post-editing methods to humanize AI text."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def paraphrase_simple(self, text: str) -> str:
        """Simple paraphrasing to make text more human-like."""
        prompt = f"""Rewrite the following text to sound more natural and human-like,
while preserving the main ideas:

{text}

Rewritten text:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error paraphrasing: {e}")
            return text

    def paraphrase_style(self, text: str, style: str = "casual") -> str:
        """Style-specific paraphrasing."""
        style_prompts = {
            "casual": "Make it sound like a casual conversation between friends",
            "personal": "Add personal experiences and opinions to make it feel authentic",
            "varied": "Vary sentence lengths and structures significantly"
        }

        prompt = f"""Rewrite the following text. {style_prompts.get(style, "")}.
Keep the main ideas but make it feel like a real person wrote it:

{text}

Rewritten text:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in style paraphrasing: {e}")
            return text


def load_test_prompts() -> List[str]:
    """Load diverse test prompts for text generation."""
    prompts = [
        "Write a short paragraph about the importance of sleep for health.",
        "Explain why renewable energy is important for the future.",
        "Describe your favorite season and what makes it special.",
        "Write about the benefits of reading books regularly.",
        "Explain how technology has changed education.",
        "Describe a memorable travel experience.",
        "Write about the importance of maintaining work-life balance.",
        "Explain the benefits of regular exercise.",
        "Describe what makes a good friend.",
        "Write about the impact of social media on society.",
        "Explain why learning a new language is valuable.",
        "Describe the process of making a cup of coffee.",
        "Write about the benefits of meditation.",
        "Explain how cooking at home is healthier than eating out.",
        "Describe what you would do on a perfect day off.",
        "Write about the importance of environmental conservation.",
        "Explain why teamwork is important in the workplace.",
        "Describe the appeal of a popular hobby.",
        "Write about how music affects our mood.",
        "Explain the importance of financial planning.",
        "Describe the experience of learning something new.",
        "Write about why pets make good companions.",
        "Explain the benefits of volunteering in your community.",
        "Describe what makes a house feel like a home.",
        "Write about the importance of mental health awareness.",
    ]
    return prompts


def load_human_samples() -> List[str]:
    """Load human-written text samples from the dataset."""
    samples_path = "datasets/ai_text_detection_pile_samples/samples.json"

    try:
        with open(samples_path, 'r') as f:
            data = json.load(f)

        human_samples = [
            item["text"][:1000]  # Truncate for consistency
            for item in data
            if item.get("source") == "human"
        ]
        return human_samples[:20]  # Use first 20 samples
    except Exception as e:
        print(f"Error loading human samples: {e}")
        # Return some fallback human-like samples
        return [
            "I've always found mornings to be the most productive part of my day. There's something about the quiet hours before the world wakes up that allows me to focus better. I usually start with a cup of coffee and some light reading before diving into work.",
            "The neighborhood where I grew up had this old oak tree that everyone used as a meeting spot. Kids would gather there after school, and adults would chat in its shade during summer evenings. It's funny how a simple tree can hold so many memories.",
        ]


def compute_quality_metrics(original: str, modified: str) -> Dict[str, float]:
    """Compute quality metrics between original and modified text."""
    # Simple word overlap as proxy for semantic similarity
    orig_words = set(original.lower().split())
    mod_words = set(modified.lower().split())

    if len(orig_words) == 0 or len(mod_words) == 0:
        overlap = 0.0
    else:
        overlap = len(orig_words & mod_words) / len(orig_words | mod_words)

    # Length ratio
    length_ratio = len(modified) / max(len(original), 1)

    return {
        "word_overlap": overlap,
        "length_ratio": length_ratio
    }


def run_inference_track_experiment(
    generator: TextGenerator,
    detector: EnsembleDetector,
    prompts: List[str],
    n_samples: int = 10
) -> Dict[str, Any]:
    """
    Run inference track experiment: test different prompt strategies.

    Strategies:
    1. Baseline: Standard generation
    2. Human-style: Prompt to write like a human
    3. Personal: Add personal anecdotes
    4. Varied: Use varied sentence structures
    """
    results = {
        "baseline": [],
        "human_style": [],
        "personal": [],
        "varied": []
    }

    strategies = {
        "baseline": {
            "system": None,
            "prefix": ""
        },
        "human_style": {
            "system": "You are a human writer, not an AI. Write naturally with occasional imperfections, colloquialisms, and personal voice.",
            "prefix": ""
        },
        "personal": {
            "system": "Write as a real person sharing their thoughts. Include personal anecdotes, opinions, and natural speech patterns. Use contractions and informal language where appropriate.",
            "prefix": "From my experience, "
        },
        "varied": {
            "system": "Write with highly varied sentence structures. Mix very short sentences with longer ones. Start sentences differently. Use fragments occasionally. Be unpredictable.",
            "prefix": ""
        }
    }

    sample_prompts = random.sample(prompts, min(n_samples, len(prompts)))

    for strategy_name, strategy in strategies.items():
        print(f"\nTesting inference strategy: {strategy_name}")
        strategy_results = []

        for prompt in tqdm(sample_prompts, desc=strategy_name):
            full_prompt = strategy["prefix"] + prompt

            text = generator.generate(
                full_prompt,
                system_prompt=strategy["system"],
                max_tokens=CONFIG["max_tokens"],
                temperature=CONFIG["temperature"]
            )

            if text:
                scores = detector.detect(text)
                strategy_results.append({
                    "prompt": prompt,
                    "text": text,
                    "detection_scores": scores,
                    "strategy": strategy_name
                })

            time.sleep(0.5)  # Rate limiting

        results[strategy_name] = strategy_results

    return results


def run_postediting_track_experiment(
    generator: TextGenerator,
    editor: PostEditor,
    detector: EnsembleDetector,
    prompts: List[str],
    n_samples: int = 10
) -> Dict[str, Any]:
    """
    Run post-editing track experiment: test different paraphrasing strategies.

    Strategies:
    1. Baseline: No editing
    2. Simple paraphrase: Basic rewriting
    3. Casual style: Casual tone paraphrasing
    4. Personal style: Add personal elements
    """
    results = {
        "baseline": [],
        "simple_paraphrase": [],
        "casual_style": [],
        "personal_style": []
    }

    sample_prompts = random.sample(prompts, min(n_samples, len(prompts)))

    # First generate baseline AI text
    print("\nGenerating baseline AI text for post-editing...")
    baseline_texts = []
    for prompt in tqdm(sample_prompts, desc="Baseline generation"):
        text = generator.generate(
            prompt,
            max_tokens=CONFIG["max_tokens"],
            temperature=CONFIG["temperature"]
        )
        if text:
            baseline_texts.append({"prompt": prompt, "text": text})
        time.sleep(0.5)

    # Test each post-editing strategy
    strategies = {
        "baseline": None,  # No editing
        "simple_paraphrase": ("simple", None),
        "casual_style": ("style", "casual"),
        "personal_style": ("style", "personal")
    }

    for strategy_name, strategy in strategies.items():
        print(f"\nTesting post-editing strategy: {strategy_name}")
        strategy_results = []

        for item in tqdm(baseline_texts, desc=strategy_name):
            original_text = item["text"]

            if strategy is None:
                # Baseline: no editing
                edited_text = original_text
            elif strategy[0] == "simple":
                edited_text = editor.paraphrase_simple(original_text)
            else:
                edited_text = editor.paraphrase_style(original_text, strategy[1])

            if edited_text:
                scores = detector.detect(edited_text)
                quality = compute_quality_metrics(original_text, edited_text)

                strategy_results.append({
                    "prompt": item["prompt"],
                    "original_text": original_text,
                    "edited_text": edited_text,
                    "detection_scores": scores,
                    "quality_metrics": quality,
                    "strategy": strategy_name
                })

            if strategy is not None:
                time.sleep(0.5)  # Rate limiting for API calls

        results[strategy_name] = strategy_results

    return results


def evaluate_human_baseline(
    detector: EnsembleDetector,
    human_samples: List[str]
) -> Dict[str, Any]:
    """Evaluate detector on human-written text to establish baseline."""
    print("\nEvaluating human text baseline...")
    results = []

    for text in tqdm(human_samples, desc="Human baseline"):
        scores = detector.detect(text)
        results.append({
            "text": text[:200] + "...",  # Truncate for storage
            "detection_scores": scores,
            "label": "human"
        })

    return results


def compute_metrics(
    ai_scores: List[float],
    human_scores: List[float]
) -> Dict[str, float]:
    """Compute detection metrics (AUROC, TPR@FPR)."""
    # Combine labels and scores
    labels = [1] * len(ai_scores) + [0] * len(human_scores)
    scores = ai_scores + human_scores

    if len(set(labels)) < 2:
        return {"auroc": 0.5, "tpr_at_1pct_fpr": 0.0, "tpr_at_5pct_fpr": 0.0}

    # AUROC
    auroc = roc_auc_score(labels, scores)

    # TPR at specific FPR thresholds
    # For this we need to find threshold where FPR <= target
    human_scores_sorted = sorted(human_scores, reverse=True)
    n_human = len(human_scores)

    # Threshold for 1% FPR
    idx_1pct = max(0, int(0.01 * n_human) - 1)
    threshold_1pct = human_scores_sorted[idx_1pct] if idx_1pct < n_human else 1.0
    tpr_1pct = sum(1 for s in ai_scores if s >= threshold_1pct) / max(len(ai_scores), 1)

    # Threshold for 5% FPR
    idx_5pct = max(0, int(0.05 * n_human) - 1)
    threshold_5pct = human_scores_sorted[idx_5pct] if idx_5pct < n_human else 1.0
    tpr_5pct = sum(1 for s in ai_scores if s >= threshold_5pct) / max(len(ai_scores), 1)

    return {
        "auroc": auroc,
        "tpr_at_1pct_fpr": tpr_1pct,
        "tpr_at_5pct_fpr": tpr_5pct
    }


def analyze_results(
    inference_results: Dict[str, Any],
    postediting_results: Dict[str, Any],
    human_baseline: List[Dict],
    detector_name: str = "ensemble"
) -> pd.DataFrame:
    """Analyze and compile results into a leaderboard format."""

    # Get human scores for baseline
    human_scores = [r["detection_scores"][detector_name] for r in human_baseline]

    leaderboard_data = []

    # Analyze inference track
    for strategy_name, strategy_results in inference_results.items():
        if not strategy_results:
            continue

        ai_scores = [r["detection_scores"][detector_name] for r in strategy_results]
        metrics = compute_metrics(ai_scores, human_scores)

        # Evasion rate (1 - detection rate at 5% FPR)
        evasion_rate = 1.0 - metrics["tpr_at_5pct_fpr"]

        leaderboard_data.append({
            "track": "Inference",
            "method": strategy_name,
            "auroc": metrics["auroc"],
            "tpr_1pct_fpr": metrics["tpr_at_1pct_fpr"],
            "tpr_5pct_fpr": metrics["tpr_at_5pct_fpr"],
            "evasion_rate": evasion_rate,
            "quality_score": 1.0,  # Inference doesn't modify output
            "mean_detection_score": np.mean(ai_scores)
        })

    # Analyze post-editing track
    for strategy_name, strategy_results in postediting_results.items():
        if not strategy_results:
            continue

        ai_scores = [r["detection_scores"][detector_name] for r in strategy_results]
        metrics = compute_metrics(ai_scores, human_scores)

        # Evasion rate
        evasion_rate = 1.0 - metrics["tpr_at_5pct_fpr"]

        # Quality score (word overlap as proxy)
        quality_scores = [r["quality_metrics"]["word_overlap"] for r in strategy_results]
        avg_quality = np.mean(quality_scores) if quality_scores else 0.0

        leaderboard_data.append({
            "track": "Post-editing",
            "method": strategy_name,
            "auroc": metrics["auroc"],
            "tpr_1pct_fpr": metrics["tpr_at_1pct_fpr"],
            "tpr_5pct_fpr": metrics["tpr_at_5pct_fpr"],
            "evasion_rate": evasion_rate,
            "quality_score": avg_quality,
            "mean_detection_score": np.mean(ai_scores)
        })

    df = pd.DataFrame(leaderboard_data)

    # Sort by evasion rate (higher is better for evasion)
    df = df.sort_values("evasion_rate", ascending=False)

    return df


def main():
    """Main experiment execution."""
    print("=" * 60)
    print("AI Undetectability Leaderboard Experiment")
    print("=" * 60)
    print(f"\nConfiguration: {json.dumps(CONFIG, indent=2)}")

    # Initialize components
    print("\n[1/6] Initializing detector ensemble...")
    detector = EnsembleDetector()

    print("\n[2/6] Initializing text generator...")
    generator = TextGenerator(model=CONFIG["model"])

    print("\n[3/6] Initializing post-editor...")
    editor = PostEditor(model=CONFIG["model"])

    # Load data
    print("\n[4/6] Loading test data...")
    prompts = load_test_prompts()
    human_samples = load_human_samples()
    print(f"Loaded {len(prompts)} prompts and {len(human_samples)} human samples")

    # Establish human baseline
    human_baseline = evaluate_human_baseline(detector, human_samples)

    # Run experiments
    print("\n[5/6] Running experiments...")

    print("\n--- Inference Track ---")
    inference_results = run_inference_track_experiment(
        generator, detector, prompts, n_samples=CONFIG["n_samples"] // 5
    )

    print("\n--- Post-editing Track ---")
    postediting_results = run_postediting_track_experiment(
        generator, editor, detector, prompts, n_samples=CONFIG["n_samples"] // 5
    )

    # Analyze results
    print("\n[6/6] Analyzing results...")
    leaderboard = analyze_results(
        inference_results, postediting_results, human_baseline
    )

    print("\n" + "=" * 60)
    print("LEADERBOARD RESULTS")
    print("=" * 60)
    print(leaderboard.to_string(index=False))

    # Save results
    results = {
        "config": CONFIG,
        "inference_results": inference_results,
        "postediting_results": postediting_results,
        "human_baseline": human_baseline,
        "leaderboard": leaderboard.to_dict(orient="records")
    }

    with open("results/experiment_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    leaderboard.to_csv("results/leaderboard.csv", index=False)

    print("\nResults saved to results/experiment_results.json")
    print("Leaderboard saved to results/leaderboard.csv")

    return results, leaderboard


if __name__ == "__main__":
    results, leaderboard = main()
