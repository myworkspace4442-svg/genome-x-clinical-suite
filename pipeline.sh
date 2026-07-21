#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}   GENOME-X PIPELINE AUTOMATOR (LINUX DEV)   ${NC}"
echo -e "${GREEN}=============================================${NC}"

echo "⚙️ [DevOps]: Launching Genome-X Suite via Docker Compose..."
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ [Success]: Genome-X Engine is now running optimally!${NC}"
    echo "🌍 Access the Interactive UI Dashboard at: http://localhost:8501"
else
    echo "❌ [Error]: Pipeline deployment failed. Check Linux Docker logs."
fi


#!/bin/bash

WATCH_DIR="./data_cache"
REF_AMR="reference/amr_card.fasta"

echo "🔍 Monitoring $WATCH_DIR for genomic files..."

inotifywait -m -e close_write --format '%w%f' "$WATCH_DIR" | while read FILE
do
    if [[ "$FILE" =~ \.(fastq|fq|fasta|fa)$ ]]; then
        echo "🚀 File detected: $FILE"
        
        # 1. BWA alignment (AMR Database နဲ့ တိုက်စစ်ခြင်း)
        bwa mem -t 4 "$REF_AMR" "$FILE" > output.sam
        
        # 2. SAMtoBAM & Sorting
        samtools view -S -b output.sam | samtools sort -o output_sorted.bam
        samtools index output_sorted.bam
        
        # 3. Align ဖြစ်သွားတဲ့ AMR Genes တွေကို စာရင်းထုတ်ယူခြင်း
        samtools idxstats output_sorted.bam | awk '$3>0 {print $1 "\t" $3}' > amr_results.txt
        
        echo "✅ AMR Analysis Completed! Results saved in amr_results.txt"
    fi
done
