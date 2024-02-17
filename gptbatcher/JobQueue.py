import asyncio
import time
from typing import Callable, List, Any, Tuple


class JobQueue:
    def __init__(self, tokens: int):
        self.tokens = asyncio.Semaphore(tokens)
        self.results = []

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
        finally:
            elapsed_time = time.time() - start_time
            if elapsed_time < 60:
                await asyncio.sleep(60 - elapsed_time)
            self.release_token()

    async def run_all(self, jobs: List[Tuple[Callable[..., Any], Tuple[Any, ...]]]) -> List[Any]:
        tasks = [self.run_job(job, *args) for job, args in jobs]
        await asyncio.gather(*tasks)
        return self.results
    
    def run(self, jobs: List[Tuple[Callable[..., Any], Tuple[Any, ...]]]) -> List[Any]:
        return asyncio.run(self.run_all(jobs))
