#!/bin/bash

# Script to convert audio file to SVG waveform
# Usage: ./music_to_svg.sh <input_audio_file> <output_svg_file>

set -e

# Check if required tools are installed
command -v ffmpeg >/dev/null 2>&1 || { echo "Error: ffmpeg is required but not installed." >&2; exit 1; }
command -v inkscape >/dev/null 2>&1 || { echo "Error: inkscape is required but not installed." >&2; exit 1; }

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_audio_file> <output_svg_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_SVG="$2"
TEMP_PNG="${OUTPUT_SVG%.svg}.png"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

# Generate waveform PNG using ffmpeg
echo "Generating waveform PNG..."
ffmpeg -i "$INPUT_FILE" -filter_complex "showwavespic=colors=black" \
  -frames:v 1 "$TEMP_PNG" -y

# Convert PNG to SVG using inkscape
echo "Converting PNG to SVG..."
inkscape -p "$TEMP_PNG" -o "$OUTPUT_SVG"

# Clean up temporary PNG file
rm -f "$TEMP_PNG"

echo "Done! SVG saved to: $OUTPUT_SVG"