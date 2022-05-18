#!/usr/bin/env bash

permedcoe execute application Snakefile --workflow_manager snakemake --flags "--cores 1"

# Using shortcuts:
# permedcoe x app Snakefile -w snakemake -f "--cores 1"
