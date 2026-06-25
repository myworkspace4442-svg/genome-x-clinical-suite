import argparse
from database import insert_result

parser = argparse.ArgumentParser()
parser.add_argument("--seq1", required=True)
parser.add_argument("--seq2", required=True)
parser.add_argument("--out", required=True)

args = parser.parse_args()
# DNA နှစ်ခုကို တိုက်စစ်ပြီး အမှတ်ပေးမယ့် စက်ရုပ်
score = 0
min_len = min(len(args.seq1), len(args.seq2))

for i in range(min_len):
    if args.seq1[i] == args.seq2[i]:
        score += 2   # DNA ချင်း တူရင် +၂ မှတ် ပေါင်းမယ်
    else:
        score -= 1   # DNA ချင်း မတူရင် -၁ မှတ် နှုတ်မယ်
with open(args.out, "w") as f:
    f.write(f"Alignment Score: {score}\n")
    f.write(f"Sequence 1: {args.seq1}\n")
    f.write(f"Sequence 2: {args.seq2}\n")
print(f"Alignment Score: {score}")
insert_result("Manual_J", args.seq1, args.seq2, score, args.out)
