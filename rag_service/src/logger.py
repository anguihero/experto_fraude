import logging

def setup_logger():
    # Configura logging global
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/rag_service.log"),
            logging.StreamHandler()
        ]
    )