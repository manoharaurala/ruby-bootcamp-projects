import asyncio
from agents import Agent, Runner

my_agent = Agent(
    name="Finance Agent",
    instructions="Answer finance questions clearly and concisely.",
)


async def main():
    result = await Runner.run(my_agent, "Hello")   # 'await' is allowed inside an 'async def'
    print(result.final_output)

asyncio.run(main())                                 # starts the async world and runs main()
