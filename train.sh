#!/bin/sh
echo $1

#ketos segtrain -bl -f alto  -t /data/htr/ariane/train.mufichecker.txt -e /data/htr/ariane/val.mufichecker.txt -o LineOnl_Complx_$1 --device cuda:0 --threads 10 --augment --merge-baselines Default:default --merge-baselines Default:Numbering --merge-baselines Default:Main --merge-baselines Default:DropCapitalLine --epochs 50 --schedule reduceonplateau --suppress-regions --merge-baselines Default:Interlinear --merge-baselines Default:Rubric -s "[1,1800,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32 Cr3,3,256 Gn32 Lbx32 Lby32 Cr1,1,32 Gn32 Lby32 Lbx32]"

# Train full
echo "Training LineAndRegionSimple_$1"
ketos segtrain -bl -f alto  -t /data/htr/ariane/train.mufichecker.txt -e /data/htr/ariane/val.mufichecker.txt \
    -o LineAndRegionsSimple_$1 --device cuda:0 --threads 10 --augment --epochs 50 --schedule reduceonplateau

echo "Training SegmentMsIncunbable_$1"
ketos segtrain -bl -f alto  -t train.txt -e val.txt \
    -o LineAndRegionsComplexe_$1 --device cuda:0 --workers 10 --augment  --schedule reduceonplateau \
    -s "[1,1800,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32 Cr3,3,256 Gn32 Lbx32 Lby32 Cr1,1,32 Gn32 Lby32 Lbx32]"

# Train Simple
echo "Training MergedLines_$1"
ketos segtrain -bl -f alto  -t /data/htr/ariane/train.mufichecker.txt -e /data/htr/ariane/val.mufichecker.txt \
    -o LineOnly_$1 --device cuda:0 --threads 10 --augment \
    --merge-baselines Default:default \
    --merge-baselines Default:Numbering \
    --merge-baselines Default:Main \
    --merge-baselines Default:DropCapitalLine --epochs 50 --schedule reduceonplateau \
    --merge-baselines Default:Interlinear \
    --merge-baselines Default:Rubric \
    --suppress-regions \
    -s "[1,1800,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32 Cr3,3,256 Gn32 Lbx32 Lby32 Cr1,1,32 Gn32 Lby32 Lbx32]"

echo "Training MergedRegions_$1"
ketos segtrain -bl -f alto  -t /data/htr/ariane/train.mufichecker.txt -e /data/htr/ariane/val.mufichecker.txt \
    -o MergedRegions_$1 --device cuda:0 --threads 10 --augment --epochs 50 --schedule reduceonplateau  \
    -s "[1,1800,0,3 Cr7,7,64,2,2 Gn32 Cr3,3,128,2,2 Gn32 Cr3,3,128 Gn32 Cr3,3,256 Gn32 Cr3,3,256 Gn32 Lbx32 Lby32 Cr1,1,32 Gn32 Lby32 Lbx32]" \
    --suppress-baselines \
    --merge-regions Default:Damage \
    --merge-regions Default:Stamp \
    --merge-regions Default:Main \
    --merge-regions Default:DropCapital \
    --merge-regions Default:text \
    --merge-regions Default:Figure \
    --merge-regions Default:RunningTitle \
    --merge-regions Default:Decoration \
    --merge-regions Default:Title \
    --merge-regions Default:MusicNotation \
    --merge-regions Default:DropCapitalLine \
    --merge-regions Default:Numbering \
    --merge-regions Default:Margin 
