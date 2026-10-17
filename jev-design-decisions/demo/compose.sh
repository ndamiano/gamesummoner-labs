#!/usr/bin/env bash
# Cut one demo: the ask typed in, the clock card with the real stage times, then gameplay.
# Usage: ./compose.sh <name> <play.mp4> "Stage=seconds" ...
set -eu
cd "$(dirname "$0")"
name=$1; play=$2; shift 2
PY=../../../venv/bin/python
$PY card.py ${name}_card.mp4 "$@"
norm="scale=960:640,fps=30,format=yuv420p"
ffmpeg -v error -y -i ${name}_prompt.mp4 -vf "$norm" -c:v libx264 -crf 10 ${name}_a.mp4
ffmpeg -v error -y -ss 1.6 ${PLAY_END:+-to $PLAY_END} -i "$play" -vf "$norm" -c:v libx264 -crf 10 ${name}_c.mp4
printf "file '%s'\n" ${name}_a.mp4 ${name}_card.mp4 ${name}_c.mp4 > ${name}_list.txt
ffmpeg -v error -y -f concat -safe 0 -i ${name}_list.txt -c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -movflags +faststart ${name}.mp4
ffmpeg -v error -y -i ${name}.mp4 -vf "fps=15,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" ${name}.gif
rm -f ${name}_a.mp4 ${name}_c.mp4 ${name}_card.mp4 ${name}_list.txt
ffprobe -v error -show_entries format=duration -of csv=p=0 ${name}.mp4
