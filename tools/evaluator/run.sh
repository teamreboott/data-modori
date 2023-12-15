export CUDA_VISIBLE_DEVICES=$2
export TOKENIZERS_PARALLELISM=false

RESULT_DIR='results/all'
TASKS='kobest_hellaswag,kobest_copa,kobest_boolq,kobest_sentineg,kohatespeech'
GPU_NO=0

# Huggingface Model
MODEL=$1

MODEL_PATH=$(echo $MODEL | awk -F/ '{print $(NF-1) "/" $NF}')

echo "mkdir -p $RESULT_DIR/$MODEL_PATH/$CURRENT_TRAINED_TOKENS"
mkdir -p $RESULT_DIR/$MODEL_PATH/$CURRENT_TRAINED_TOKENS

python main.py \
--model hf-causal-experimental-lora \
--model_args pretrained=$MODEL,use_accelerate=true,trust_remote_code=true \
--tasks $TASKS \
--num_fewshot 0 \
--no_cache \
--batch_size 32 \
--output_path $RESULT_DIR/$MODEL/0_shot.json