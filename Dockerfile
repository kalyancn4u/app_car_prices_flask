# =============================================================================
# PRODUCTION image — serves the API with gunicorn.
#
# This is the one to use for the AWS ECS assignment. Build it with:
#     docker build -t car-price-api .
#
# Why gunicorn and not "python app.py"? Flask's own dev server is single-
# threaded, reloads code on every request in debug mode, and its own docs say
# it "is not designed to be particularly efficient, stable, or secure" for
# real traffic. gunicorn is a production-grade WSGI server: it runs several
# worker processes so it can handle concurrent requests (e.g. a grader's
# script + your own curl test at the same time) without one call blocking
# the other. See Dockerfile.dev for the simpler alternative and README.md
# for the full explanation.
# =============================================================================
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer between builds —
# it only re-runs pip install when requirements.txt actually changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code and the pre-trained model artifacts.
# training/ is deliberately NOT copied: it needs pandas' full training-time
# footprint and the raw CSV, neither of which the running API needs.
COPY app.py car_model.py wsgi.py ./
COPY models/ ./models/

EXPOSE 5000

# 2 workers is a reasonable default for the small Fargate task sizes (0.25-0.5
# vCPU) used in the class assignment; raise it if you give the task more CPU.
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:app"]
