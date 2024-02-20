import asyncio
import time
from typing import Callable, List, Any, Tuple


class JobQueue:
    def __init__(
        self, tokens: int, jobs: List[Tuple[Callable[..., Any], Tuple[Any, ...]]]
    ):
        self.tokens = asyncio.Semaphore(tokens)
        self.results = []
        self.errors = []
        self.jobs = jobs

    async def acquire_token(self):
        await self.tokens.acquire()

    def release_token(self):
        self.tokens.release()

    async def run_job(self, job: Callable[..., Any], *args) -> None:
        await self.acquire_token()
        start_time = time.time()
        try:
            result = await job(*args)
            self.results.append(result)
        except Exception as e:
            self.errors.append(e)
        finally:
            while len(self.results) + len(self.errors) < len(self.jobs):
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:
                    await asyncio.sleep(1)
                else:
                    break
            self.release_token()

    async def run_all(self) -> List[Any]:
        tasks = [self.run_job(job, *args) for job, args in self.jobs]
        await asyncio.gather(*tasks)
        return self.results

    def run(self) -> List[Any]:
        return asyncio.run(self.run_all())
