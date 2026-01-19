"""
Visualization script for AI Undetectability Leaderboard results.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


def load_results():
    """Load experiment results."""
    with open("results/experiment_results.json", "r") as f:
        results = json.load(f)
    leaderboard = pd.read_csv("results/leaderboard.csv")
    return results, leaderboard


def plot_leaderboard_comparison(leaderboard: pd.DataFrame, save_path: str = "figures/leaderboard_comparison.png"):
    """Create bar chart comparing methods by track."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Evasion rate comparison
    ax1 = axes[0]
    colors = ['#2ecc71' if t == 'Inference' else '#3498db' for t in leaderboard['track']]
    bars = ax1.barh(range(len(leaderboard)), leaderboard['evasion_rate'], color=colors)
    ax1.set_yticks(range(len(leaderboard)))
    ax1.set_yticklabels([f"{row['track']}: {row['method']}" for _, row in leaderboard.iterrows()])
    ax1.set_xlabel('Evasion Rate (1 - TPR@5% FPR)')
    ax1.set_title('Evasion Rate by Method\n(Higher = Better Evasion)')
    ax1.set_xlim(0, 1)

    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax1.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                f'{width:.2f}', va='center', fontsize=10)

    # AUROC comparison
    ax2 = axes[1]
    colors = ['#2ecc71' if t == 'Inference' else '#3498db' for t in leaderboard['track']]
    bars = ax2.barh(range(len(leaderboard)), 1 - leaderboard['auroc'], color=colors)
    ax2.set_yticks(range(len(leaderboard)))
    ax2.set_yticklabels([f"{row['track']}: {row['method']}" for _, row in leaderboard.iterrows()])
    ax2.set_xlabel('1 - AUROC (Lower Detection Performance)')
    ax2.set_title('Detection Difficulty (1-AUROC)\n(Higher = Harder to Detect)')
    ax2.set_xlim(0, 0.5)

    # Add legend
    legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor='#2ecc71', label='Inference Track'),
                       plt.Rectangle((0, 0), 1, 1, facecolor='#3498db', label='Post-editing Track')]
    ax1.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_evasion_vs_quality(leaderboard: pd.DataFrame, save_path: str = "figures/evasion_vs_quality.png"):
    """Create Pareto frontier plot of evasion rate vs quality."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot each track with different markers
    for track in leaderboard['track'].unique():
        track_data = leaderboard[leaderboard['track'] == track]
        marker = 'o' if track == 'Inference' else 's'
        color = '#2ecc71' if track == 'Inference' else '#3498db'

        ax.scatter(track_data['quality_score'], track_data['evasion_rate'],
                  s=200, marker=marker, c=color, label=track, edgecolors='black', linewidth=1)

        # Add method labels
        for _, row in track_data.iterrows():
            ax.annotate(row['method'],
                       (row['quality_score'], row['evasion_rate']),
                       xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax.set_xlabel('Quality Score (Word Overlap with Original)', fontsize=12)
    ax.set_ylabel('Evasion Rate (1 - TPR@5% FPR)', fontsize=12)
    ax.set_title('Evasion Rate vs. Quality Trade-off\n(Pareto Analysis)', fontsize=14)
    ax.legend(loc='best', fontsize=11)
    ax.set_xlim(-0.05, 1.1)
    ax.set_ylim(-0.05, 1.05)

    # Add quadrant labels
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.text(0.75, 0.75, 'Ideal\n(High Quality, High Evasion)', ha='center', va='center',
           fontsize=10, color='green', alpha=0.7)
    ax.text(0.25, 0.25, 'Poor\n(Low Quality, Low Evasion)', ha='center', va='center',
           fontsize=10, color='red', alpha=0.7)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_detection_scores_distribution(results: dict, save_path: str = "figures/detection_scores_dist.png"):
    """Plot distribution of detection scores for different methods."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Collect scores for each category
    categories = {
        'Human Baseline': [r['detection_scores']['ensemble'] for r in results['human_baseline']],
        'AI Baseline': [r['detection_scores']['ensemble'] for r in results['inference_results']['baseline']],
        'Inference: Human Style': [r['detection_scores']['ensemble'] for r in results['inference_results']['human_style']],
        'Post-editing: Simple Paraphrase': [r['detection_scores']['ensemble'] for r in results['postediting_results']['simple_paraphrase']]
    }

    colors = ['#27ae60', '#e74c3c', '#3498db', '#9b59b6']

    # Plot histograms
    ax = axes[0, 0]
    for i, (label, scores) in enumerate(categories.items()):
        ax.hist(scores, bins=15, alpha=0.6, label=label, color=colors[i])
    ax.set_xlabel('Ensemble Detection Score')
    ax.set_ylabel('Count')
    ax.set_title('Detection Score Distribution by Category')
    ax.legend(fontsize=9)

    # Box plots
    ax = axes[0, 1]
    data_for_box = [scores for scores in categories.values()]
    bp = ax.boxplot(data_for_box, labels=list(categories.keys()), patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_ylabel('Ensemble Detection Score')
    ax.set_title('Detection Score Distribution (Box Plot)')
    ax.tick_params(axis='x', rotation=45)

    # Inference track comparison
    ax = axes[1, 0]
    inference_methods = ['baseline', 'human_style', 'personal', 'varied']
    inference_scores = [[r['detection_scores']['ensemble'] for r in results['inference_results'][m]]
                       for m in inference_methods]
    bp = ax.boxplot(inference_scores, labels=inference_methods, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#2ecc71')
        patch.set_alpha(0.6)
    ax.set_xlabel('Inference Method')
    ax.set_ylabel('Detection Score')
    ax.set_title('Inference Track: Detection Scores by Method')

    # Post-editing track comparison
    ax = axes[1, 1]
    postediting_methods = ['baseline', 'simple_paraphrase', 'casual_style', 'personal_style']
    postediting_scores = [[r['detection_scores']['ensemble'] for r in results['postediting_results'][m]]
                         for m in postediting_methods]
    bp = ax.boxplot(postediting_scores, labels=postediting_methods, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#3498db')
        patch.set_alpha(0.6)
    ax.set_xlabel('Post-editing Method')
    ax.set_ylabel('Detection Score')
    ax.set_title('Post-editing Track: Detection Scores by Method')
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def plot_track_summary(leaderboard: pd.DataFrame, save_path: str = "figures/track_summary.png"):
    """Create summary visualization by track."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Group by track
    track_summary = leaderboard.groupby('track').agg({
        'evasion_rate': ['mean', 'max'],
        'auroc': ['mean', 'min'],
        'quality_score': 'mean'
    }).round(3)

    # Evasion rate by track
    ax = axes[0]
    tracks = ['Inference', 'Post-editing']
    means = [leaderboard[leaderboard['track'] == t]['evasion_rate'].mean() for t in tracks]
    maxs = [leaderboard[leaderboard['track'] == t]['evasion_rate'].max() for t in tracks]
    x = np.arange(len(tracks))
    width = 0.35
    ax.bar(x - width/2, means, width, label='Mean', color='#3498db', alpha=0.7)
    ax.bar(x + width/2, maxs, width, label='Best', color='#2ecc71', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(tracks)
    ax.set_ylabel('Evasion Rate')
    ax.set_title('Evasion Rate by Track')
    ax.legend()
    ax.set_ylim(0, 1)

    # AUROC by track (lower is better for evasion)
    ax = axes[1]
    means = [leaderboard[leaderboard['track'] == t]['auroc'].mean() for t in tracks]
    mins = [leaderboard[leaderboard['track'] == t]['auroc'].min() for t in tracks]
    ax.bar(x - width/2, means, width, label='Mean', color='#e74c3c', alpha=0.7)
    ax.bar(x + width/2, mins, width, label='Best (lowest)', color='#f39c12', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(tracks)
    ax.set_ylabel('AUROC (lower = harder to detect)')
    ax.set_title('Detection AUROC by Track')
    ax.legend()
    ax.set_ylim(0, 1)

    # Quality score by track
    ax = axes[2]
    quality_scores = [leaderboard[leaderboard['track'] == t]['quality_score'].mean() for t in tracks]
    colors = ['#2ecc71', '#3498db']
    bars = ax.bar(tracks, quality_scores, color=colors, alpha=0.7)
    ax.set_ylabel('Quality Score (Word Overlap)')
    ax.set_title('Average Quality Preservation by Track')
    ax.set_ylim(0, 1.1)
    for bar, val in zip(bars, quality_scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
               f'{val:.2f}', ha='center', fontsize=12)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")


def create_leaderboard_table(leaderboard: pd.DataFrame, save_path: str = "figures/leaderboard_table.png"):
    """Create a nice visualization of the leaderboard table."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')

    # Format the dataframe for display
    display_df = leaderboard[['track', 'method', 'auroc', 'evasion_rate', 'quality_score']].copy()
    display_df = display_df.round(3)
    display_df.columns = ['Track', 'Method', 'AUROC', 'Evasion Rate', 'Quality Score']

    # Add rank column
    display_df.insert(0, 'Rank', range(1, len(display_df) + 1))

    # Create table
    table = ax.table(cellText=display_df.values,
                    colLabels=display_df.columns,
                    cellLoc='center',
                    loc='center',
                    colColours=['#34495e'] * len(display_df.columns))

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.8)

    # Color code by track
    for i in range(len(display_df)):
        if display_df.iloc[i]['Track'] == 'Inference':
            for j in range(len(display_df.columns)):
                table[(i + 1, j)].set_facecolor('#e8f5e9')
        else:
            for j in range(len(display_df.columns)):
                table[(i + 1, j)].set_facecolor('#e3f2fd')

    # Style header
    for j in range(len(display_df.columns)):
        table[(0, j)].set_text_props(color='white', fontweight='bold')

    ax.set_title('AI Undetectability Leaderboard\n(Sorted by Evasion Rate)', fontsize=14, pad=20)

    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")


def main():
    """Generate all visualizations."""
    print("Generating visualizations...")

    # Create figures directory if needed
    Path("figures").mkdir(exist_ok=True)

    # Load data
    results, leaderboard = load_results()

    # Generate all plots
    plot_leaderboard_comparison(leaderboard)
    plot_evasion_vs_quality(leaderboard)
    plot_detection_scores_distribution(results)
    plot_track_summary(leaderboard)
    create_leaderboard_table(leaderboard)

    print("\nAll visualizations saved to figures/ directory")


if __name__ == "__main__":
    main()
