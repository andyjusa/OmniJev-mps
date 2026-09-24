#!/usr/bin/env python3
"""Latency of the served model, in the shape Jev publishes it (per question, per request).

Sweeps image budget x questions per request, single stream, batch 1, warm-up discarded:
  max_pixels   how much of the image the model looks at (tokens grow with it)
  questions    1, 3, 6, 12 typed questions about the same state (packed into one pass)
Prints a table of median and p90 wall time per request and per question, and writes JSON.

usage: speed_bench.py --ckpt DIR --model DIR --image IMG [--out results/speed.json] [--reps 12]
"""
import argparse
import json
import os
import statistics
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mso.infer import MSO1  # noqa: E402

Q = [("q%d" % i, q) for i, q in enumerate([
    {"type": "choice", "instructions": "Which operation comes next?", "options": [{"key": k, "text": k} for k in ("click", "type text", "scroll", "wait")] + [{"abstain": True}]},
    {"type": "noul", "instructions": "This screen shows an error dialog."},
    {"type": "score", "instructions": "How irreversible is the next action?", "levels": ["harmless", "needs care", "irreversible"]},
    {"type": "choice", "instructions": "What is the main object?", "options": [{"key": k, "text": k} for k in ("a board", "a screen", "a person", "a robot", "a street")] + [{"abstain": True}]},
    {"type": "noul", "instructions": "The scene is indoors."},
    {"type": "score", "instructions": "How cluttered is the scene?", "levels": ["empty", "some", "busy", "packed"]},
    {"type": "choice", "instructions": "Which region is most relevant?", "options": [{"key": "r%d" % i, "region": {"box": [200 * i, 100, 200 * i + 180, 300]}} for i in range(4)] + [{"abstain": True}]},
    {"type": "noul", "instructions": "Something in this image is moving."},
    {"type": "score", "instructions": "How risky is acting on this screen?", "levels": ["safe", "check first", "dangerous"]},
    {"type": "choice", "instructions": "What should happen next?", "options": [{"key": k, "text": k} for k in ("continue", "stop", "ask a human")] + [{"abstain": True}]},
    {"type": "noul", "instructions": "The task looks finished."},
    {"type": "choice", "instructions": "Which colour dominates?", "options": [{"key": k, "text": k} for k in ("white", "black", "blue", "green", "red")] + [{"abstain": True}]},
])]


def sync(dev):
    if dev.type == "cuda":
        torch.cuda.synchronize()
    elif dev.type == "mlu":
        torch.mlu.synchronize()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--reps", type=int, default=12)
    ap.add_argument("--pixels", default="256,512,768")
    ap.add_argument("--counts", default="1,3,6,12")
    a = ap.parse_args()
    rows = []
    for px in [int(x) for x in a.pixels.split(",")]:
        m = MSO1(a.ckpt, a.model, max_pixels=px * 28 * 28)
        dev = m.dev
        for n in [int(x) for x in a.counts.split(",")]:
            qs = dict(Q[:n])
            m.system_one({"images": [a.image]}, qs, packed=True)
            sync(dev)
            walls = []
            for _ in range(a.reps):
                sync(dev)
                t = time.time()
                m.system_one({"images": [a.image]}, qs, packed=True)
                sync(dev)
                walls.append(time.time() - t)
            walls.sort()
            p50, p90 = statistics.median(walls), walls[int(0.9 * (len(walls) - 1))]
            tok = getattr(m, "last_input_tokens", 0)
            rows.append({"max_pixels_tokens": px, "questions": n, "p50_ms": round(1000 * p50), "p90_ms": round(1000 * p90),
                         "per_question_ms": round(1000 * p50 / n, 1), "input_tokens": int(tok)})
            print("px %4d | %2d q | p50 %6.0f ms | p90 %6.0f ms | per question %5.1f ms | %d input tokens"
                  % (px, n, 1000 * p50, 1000 * p90, 1000 * p50 / n, tok), flush=True)
        del m
        if dev.type == "cuda":
            torch.cuda.empty_cache()
    if a.out:
        json.dump({"device": str(dev), "ckpt": a.ckpt, "rows": rows}, open(a.out, "w"), indent=1)
        print("->", a.out)


if __name__ == "__main__":
    main()
