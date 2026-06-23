"""공통 로거. 토큰/키 값은 절대 그대로 출력하지 않는다 — mask() 로 앞 4자리만 남긴다."""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def mask(secret: str | None) -> str:
    if not secret:
        return ""
    return secret[:4] + "***"
