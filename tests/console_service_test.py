import logging, asyncio
from industrious import asyncio_windows_monkeypatch
from industrious.console_service import ConsoleService

asyncio_windows_monkeypatch()

if __name__ == '__main__':
    cs = ConsoleService()

    @cs.command(name="test", description="A test command", aliases=["lmao"], usage="[nope]")
    async def test(command):
        cs.console.print("Test Complete!")

    asyncio.run(cs.start())

    # asyncio.get_event_loop().run_forever()