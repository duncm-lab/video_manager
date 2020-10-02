import logging

logging.basicConfig(filename = cfg.SYNC_VIDEO_LOG,
        level = getattr(logging, cfg.LOG_LEVEL))

logger = logging.getLogger()
