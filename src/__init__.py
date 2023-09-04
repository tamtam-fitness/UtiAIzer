# import sentry_sdk


# sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
# if settings.ENV not in ["local", "test"]:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         integrations=[sentry_logging],
#         environment=settings.ENV,
#         traces_sample_rate=1.0,
#     )
