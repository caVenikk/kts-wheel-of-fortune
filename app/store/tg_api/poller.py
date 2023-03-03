import asyncio
from asyncio import Task
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        try:
            if self.poll_task:
                await asyncio.wait_for(self.poll_task, timeout=1)
        except TimeoutError:
            pass

    async def poll(self):
        while self.is_running:
            tg_updates = await self.store.tg_api.poll()
            # if updates:
            #     await self.store.bots_manager.handle_updates(updates)