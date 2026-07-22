FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN groupadd --system app && useradd --system --gid app --home /app app
WORKDIR /app

COPY requirements/production.txt requirements/base.txt requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY --chown=app:app . .
RUN mkdir -p /app/staticfiles /app/media && chown -R app:app /app/staticfiles /app/media
USER app
RUN SECRET_KEY=build-only-secret DEBUG=True python manage.py collectstatic --noinput --settings=backend.settings.development

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health/', timeout=3)" || exit 1
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
