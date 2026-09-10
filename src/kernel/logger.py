import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fx_platform.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fx_platform")
