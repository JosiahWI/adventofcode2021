#!/usr/bin/env python3

# solution to part 1 only

import asyncio
import pathlib

class FishTimer:

    def __init__(self, fish_times):
        self._fish_times = fish_times
        self._timers = []

    async def simulate(self, days=80):
        for time in self._fish_times:
            await self.fishy(time)

        await asyncio.sleep(3 * (days + 0.9))
        for task in self._timers:
            task.cancel()
        return len(self._timers)

    @classmethod
    def from_input(cls, fp):
        # the inputs have time 0 as the last day, but for asyncio we
        # need time 1 remaining as the last day.
        return cls([int(time) + 1 for time in fp.readline().split(",")])

    async def fishy(self, initial_start_time):
        task = asyncio.create_task(self.time_fish(initial_start_time))
        self._timers.append(task)

    async def time_fish(self, initial_start_time):
        sleep_time = initial_start_time
        while True:
            await asyncio.sleep(sleep_time * 3)
            await self.fishy(initial_start_time=9)
            sleep_time = 7

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        timer = FishTimer.from_input(fp)

    loop = asyncio.get_event_loop()
    fish_after_eighty_days = loop.run_until_complete(timer.simulate())
    print(f"Part 1: {fish_after_eighty_days}")
