#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! docker image inspect ta-ind-tex:trixie >/dev/null 2>&1; then
  docker build -t ta-ind-tex:trixie -f .environment/Dockerfile.tex .
fi
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD:/work" ta-ind-tex:trixie sh -ec '
cd /work/informe
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd /work
pdflatex -interaction=nonstopmode -halt-on-error entrega-sga.tex
'
