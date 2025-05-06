#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=2:00:00
#SBATCH --mem=160GB
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100-80g:2
#SBATCH --job-name=eval

module load any/python/3.8.3-conda
source ~/.bashrc
conda activate lm-harness
lm_eval --model hf \
        --verbosity INFO \
        --model_args pretrained=meta-llama/Meta-Llama-3.1-70B-Instruct,dtype="bfloat16",parallelize="True" \
        --gen_kwargs top_p=1,do_sample=False,temperature=0 \
        --tasks olympiad \
        --batch_size 1 \
        --output_path testing_results \
        --write_out \
        --log_samples \
        --show_config