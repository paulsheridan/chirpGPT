import time
from collections import defaultdict
from fastapi import HTTPException

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_HOUR = 100


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def _cleanup_old_requests(self, ip: str, window_seconds: int):
        current_time = time.time()
        cutoff = current_time - window_seconds
        self.requests[ip] = [t for t in self.requests[ip] if t > cutoff]

    def check_rate_limit(self, ip: str) -> None:
        current_time = time.time()

        self._cleanup_old_requests(ip, 60)
        minute_count = len(self.requests[ip])
        if minute_count >= RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=429,
                detail="Woah there, little birdie! You're sending messages too fast. Wait a moment.",
            )

        self._cleanup_old_requests(ip, 3600)
        hour_count = len(self.requests[ip])
        if hour_count >= RATE_LIMIT_PER_HOUR:
            raise HTTPException(
                status_code=429,
                detail="Squak! You've reached your hourly limit. Give your wings a rest.",
            )

        self.requests[ip].append(current_time)


rate_limiter = RateLimiter()
