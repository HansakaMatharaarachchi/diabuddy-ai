from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_PATH = ROOT_DIR / "vectorstores" / "faiss"
RAW_DATA_PATH = ROOT_DIR / "data" / "raw_data"
