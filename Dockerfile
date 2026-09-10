# RETIRED. The production build is infra/Dockerfile.backend, which
# infra/deploy.sh builds.
#
# This file still did `COPY model/ ./model/` — a directory removed when the
# full-code model replaced the 50-code one — and it never baked the backbone,
# so any image built from it would call HuggingFace at boot. Left failing on
# purpose rather than deleted, so a stray `docker build .` says why instead of
# quietly producing the wrong image.
FROM alpine:3.20
RUN echo "Use: docker build -f infra/Dockerfile.backend -t shifamind-api ." && exit 1
