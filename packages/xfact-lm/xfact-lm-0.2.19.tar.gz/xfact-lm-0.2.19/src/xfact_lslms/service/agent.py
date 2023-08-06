import logging
import os
import time

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModelForMaskedLM
import argparse
from parallelformers import parallelize
import torch

from xfact_lslms.log_helper import setup_logging
from xfact_lslms.service.amq_communications import CommunicationLayer

logger = logging.getLogger(__name__)

MAX_BATCH_SIZE = 16

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', default='t5-base', help='Use model name or path provided by huggingface Library')
    parser.add_argument('--model_type', choices=['seq2seq','causal','masked'], default='seq2seq', help='The type of LM from [seq2seq, causal, masked]')
    parser.add_argument('--model_parallel', action='store_true')
    parser.add_argument('--cache_dir', default=None)
    parser.add_argument('--fp16', action='store_true', help='Use carefully as it can cause instability and bugs')
    parser.add_argument('--bf16', action='store_true', help='Use carefully as it can cause instability and bugs')

    return parser.parse_args()


@torch.no_grad()
class LanguageModelAgent():
    def __init__(self, args):
        
        if args.bf16:
            self.dtype = torch.bfloat16
        elif args.fp16:
            self.dtype = torch.float16
        else:
            self.dtype = torch.float32

        model_args = {
            'pretrained_model_name_or_path': args.model_name,
            'cache_dir': args.cache_dir if args.cache_dir and os.path.exists(args.cache_dir) else None,
            #'torch_dtype': self.dtype
            #'low_cpu_mem_usage': True,
        }

        logger.info(f'Loading model: {args.model_name}')
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_name)

        if args.model_type == 'seq2seq':
            self.model = AutoModelForSeq2SeqLM.from_pretrained(**model_args)
        elif args.model_type == 'causal':
            self.model = AutoModelForCausalLM.from_pretrained(**model_args)
        else:
            self.model = AutoModelForMaskedLM.from_pretrained(**model_args)

        logger.info(f'Model Loaded: {args.model_name}')
        if args.model_parallel:
            num_gpus = torch.cuda.device_count()
            parallelize(self.model, num_gpus=num_gpus, fp16=args.fp16)
            self.device = 'cpu'
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)

        self.model.eval()
        self.model_memory_usage()
        self.bechmark()

    def model_memory_usage(self):
        mem_params = sum([param.nelement()*param.element_size() for param in self.model.parameters()])
        mem_bufs = sum([buf.nelement()*buf.element_size() for buf in self.model.buffers()])
        mem = mem_params + mem_bufs

        for i in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if mem < 1024.0:
                break
            mem /= 1024.0
        logger.info(f'Memory Used by model: {mem:.{3}f} {i}')

    def get_max_batch_size(self):
        return MAX_BATCH_SIZE

    def bechmark(self):
        text = "Explain how babies are born?"
        max_length = 300
        generate_kwargs={"max_length": max_length}

        logger.info(f'Starting Benchmark')
        start = time.time()
        for _ in range(100):
            self.infer(batch=text, generate_kwargs=generate_kwargs, tokenizer_kwargs={})
        end = time.time()
        logger.info(f'Benchmark results: Using model {args.model_name} with single prompt performs {100/(end-start):.{3}f} it/s with max_length: {max_length}')
        
        text = ["Explain how babies are born?"]*MAX_BATCH_SIZE
        start = time.time()
        for _ in range(100):
            self.infer(batch=text, generate_kwargs=generate_kwargs, tokenizer_kwargs={})
        end = time.time()
        logger.info(f'Benchmark reults: Using model {args.model_name} with batch size {MAX_BATCH_SIZE} performs {100/(end-start):.{3}f} it/s with max_length: {max_length}')

    @torch.no_grad()
    def infer(self, batch, tokenizer_kwargs, generate_kwargs):
        if type(batch) == list and len(batch) > MAX_BATCH_SIZE:
            return {'error': f'Use max batch size of {MAX_BATCH_SIZE}'}
        else:
            input_ids = self.tokenizer(batch, return_tensors="pt", **tokenizer_kwargs).to(self.device)
            outs = self.model.generate(**input_ids, **generate_kwargs).cpu()
            predictions = self.tokenizer.batch_decode(outs, skip_special_tokens=True)

        logger.debug(f"Predicting on {batch}")
        logger.debug(f"Predicted {predictions}")

        return {
            "input_text": batch,
            "decoded_text": predictions
        }


if __name__ == "__main__":
    setup_logging()
    args = get_args()
    
    lm = LanguageModelAgent(args)
    comms = CommunicationLayer(args, lambda message: lm.infer(**message))
    comms.listen()