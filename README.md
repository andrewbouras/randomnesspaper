# RANDOMNESSPAPER

This repository contains the supplementary materials for the paper titled "Integrating Randomness in Large Language Models: A Linear Congruential Generator Approach for Generating Clinically Relevant Content".

## Table of Contents

- [Overview](#overview)
- [Structure](#structure)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Overview

The generation of diverse, high-quality outputs from language models (LLMs) is essential for various applications, including education and content creation. Achieving true randomness and avoiding repetition remains a significant challenge. This study employs the Linear Congruential Generator (LCG) method for systematic fact selection, combined with AI-powered content generation. Using LCG, we ensured unique combinations of gastrointestinal physiology and pathology facts across multiple rounds, integrating these facts into prompts for GPT-4o to create clinically relevant, vignette-style outputs. 

This repository includes all necessary scripts and data files to reproduce the results presented in the paper.

## Structure

The repository is organized as follows:

  - `fact_mapping.py` - Script for mapping facts to indices.
  - `mcq_generation_summary_lcg.csv` - CSV file summarizing the MCQ generation rounds using LCG.
  - `python.py` - Main script for generating MCQs using LCG and GPT-4o.
- `data/` - Directory to store additional data files.
- `env/` - Directory for the virtual environment setup (if used).
- `LICENSE` - License file for the repository.
- `README.md` - This file.
- `requirements.txt` - List of Python dependencies required for the project.

## Installation

To set up the environment and install the required dependencies, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/andrewbouras/RANDOMNESSPAPER.git
    cd RANDOMNESSPAPER
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To generate MCQs using the LCG method and GPT-4, follow these steps:

1. Ensure the base prompt and fact mapping are correctly set up in the `Concept Prompts/` directory.

2. Run the `python.py` script to start the generation process:
    ```sh
    python Concept\ Prompts/python.py
    ```

3. The generated MCQs and their summaries will be saved in the `mcq_generation_summary_lcg.csv` file.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact:

Andrew Bouras, B.S.  
Nova Southeastern University, College of Osteopathic Medicine  
Email: ab4646@mynsu.nova.edu

