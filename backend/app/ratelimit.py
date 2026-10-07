import threading
import time


class LoginRateLimiter:
    """Pembatas percobaan login sederhana, in-memory, per-IP.

    Kalau ada >= max_failures kegagalan dalam window_seconds terakhir,
    IP diblokir selama lockout_seconds. Berhasil login -> hitungan di-reset.

    Catatan: pakai request.client.host (IP langsung). Kalau di belakang
    reverse proxy (nginx), pastikan Uvicorn jalan dengan
    --proxy-headers --forwarded-allow-ips, atau ganti cara ambil IP-nya.
    """

    def __init__(
        self,
        max_failures: int = 5,
        window_seconds: int = 300,
        lockout_seconds: int = 900,
    ):
        self.max_failures = max_failures
        self.window_seconds = window_seconds
        self.lockout_seconds = lockout_seconds
        self._failures: dict[str, list[float]] = {}
        self._locked_until: dict[str, float] = {}
        self._lock = threading.Lock()

    def _prune(self, key: str, now: float) -> list[float]:
        fails = [t for t in self._failures.get(key, []) if now - t < self.window_seconds]
        if fails:
            self._failures[key] = fails
        else:
            self._failures.pop(key, None)
        return fails

    def retry_after(self, key: str) -> int | None:
        """Detik sisa blokir, atau None kalau IP ini masih boleh coba."""
        now = time.monotonic()
        with self._lock:
            until = self._locked_until.get(key)
            if until is not None:
                if now < until:
                    return max(1, int(until - now) + 1)
                self._locked_until.pop(key, None)

            # Bersihkan entri basi biar dict nggak tumbuh tanpa batas.
            if len(self._failures) > 10_000:
                for k in list(self._failures):
                    self._prune(k, now)
                for k in [k for k, t in self._locked_until.items() if t <= now]:
                    self._locked_until.pop(k, None)

            fails = self._prune(key, now)
            if len(fails) >= self.max_failures:
                deadline = fails[-1] + self.lockout_seconds
                self._locked_until[key] = deadline
                return max(1, int(deadline - now) + 1)
            return None

    def record_failure(self, key: str) -> None:
        with self._lock:
            now = time.monotonic()
            fails = self._prune(key, now)
            fails.append(now)
            self._failures[key] = fails
            if len(fails) >= self.max_failures:
                self._locked_until[key] = now + self.lockout_seconds

    def reset(self, key: str) -> None:
        with self._lock:
            self._failures.pop(key, None)
            self._locked_until.pop(key, None)


login_limiter = LoginRateLimiter()
