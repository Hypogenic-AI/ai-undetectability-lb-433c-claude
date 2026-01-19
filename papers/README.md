# Downloaded Papers

This directory contains research papers relevant to AI text detection and undetectability.

## Paper List

### Benchmarks and Evaluation

1. **RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors**
   - File: `2405.07940_RAID_Benchmark.pdf`
   - Authors: Liam Dugan, Alyssa Hwang, Filip Trhlík, et al.
   - Year: 2024 (ACL)
   - arXiv: 2405.07940
   - Why relevant: Largest benchmark (6M+ samples), includes adversarial attacks, public leaderboard

2. **MGTBench: Benchmarking Machine-Generated Text Detection**
   - File: `2303.14822_MGTBench.pdf`
   - Authors: Xinlei He, Xinyue Shen, Zeyuan Chen, Michael Backes, Yang Zhang
   - Year: 2024 (ACM CCS)
   - arXiv: 2303.14822
   - Why relevant: First comprehensive benchmarking framework, modular design

3. **M4GT-Bench: Evaluation Benchmark for Black-Box Machine-Generated Text Detection**
   - File: `2402.11175_M4GT_Bench.pdf`
   - Authors: Yuxia Wang, et al.
   - Year: 2024
   - arXiv: 2402.11175
   - Why relevant: Multilingual benchmark, three task formulations

### Detection Methods

4. **DetectGPT: Zero-Shot Machine-Generated Text Detection using Probability Curvature**
   - File: `2301.10226_DetectGPT.pdf`
   - Authors: Eric Mitchell, et al. (also contains Kirchenbauer watermarking)
   - Year: 2023 (ICML)
   - arXiv: 2301.10226
   - Why relevant: Widely-used zero-shot detection baseline

5. **SynthID: Scalable Watermarking for Identifying Large Language Model Outputs**
   - File: `2310.06356_SynthID_Nature.pdf`
   - Authors: Google DeepMind
   - Year: 2024 (Nature)
   - Why relevant: Production-deployed watermarking system

### Evasion Methods

6. **Paraphrasing Evades Detectors of AI-Generated Text, but Retrieval is an Effective Defense**
   - File: `2303.13408_Paraphrasing_Evades_Detectors.pdf`
   - Authors: Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, Mohit Iyyer
   - Year: 2023 (NeurIPS)
   - arXiv: 2303.13408
   - Why relevant: DIPPER paraphraser achieves 70%→4.6% detection drop

7. **Large Language Models can be Guided to Evade AI-Generated Text Detection (SICO)**
   - File: `2305.10847_SICO_Guided_Evasion.pdf`
   - Authors: Ning Lu, Shengcai Liu, Rui He, et al.
   - Year: 2024 (TMLR)
   - arXiv: 2305.10847
   - Why relevant: Prompt-based evasion without external paraphrasers

8. **Humanizing Machine-Generated Content: Evading AI-Text Detection through Adversarial Attack**
   - File: `2404.01907_Humanizing_MGC_Adversarial.pdf`
   - Authors: Ying Zhou, Ben He, Le Sun
   - Year: 2024 (ACL)
   - arXiv: 2404.01907
   - Why relevant: Adversarial humanization techniques

### Watermarking and Attacks

9. **A Watermark for Large Language Models (Kirchenbauer)**
   - File: `2301.13848_Kirchenbauer_Watermarking.pdf`
   - Authors: John Kirchenbauer, Jonas Geiping, Yuxin Wen, et al.
   - Year: 2023 (ICML)
   - arXiv: 2301.10226
   - Why relevant: Foundational watermarking method

10. **Undetectable Watermarks**
    - File: `2309.17054_Undetectable_Watermarks.pdf`
    - Year: 2023
    - arXiv: 2309.17054
    - Why relevant: Theoretical limits of watermarking

11. **Attacking LLM Watermarks**
    - File: `2402.16187_Attacking_LLM_Watermarks.pdf`
    - Year: 2024
    - arXiv: 2402.16187
    - Why relevant: Watermark attack methods

12. **Optimizing Adaptive Attacks against Watermarks for Language Models**
    - File: `2410.02440_Adaptive_Attacks_Watermarks.pdf`
    - Authors: Abdulrahman Diaa, Toluwani Aremu, Nils Lukas
    - Year: 2024
    - arXiv: 2410.02440
    - Why relevant: 96%+ watermark evasion with DPO-tuned paraphrasers

## Usage Notes

- Papers are named with format: `{arXiv_ID}_{short_title}.pdf`
- See `../literature_review.md` for detailed analysis and key findings
- Most papers include supplementary materials in appendices
