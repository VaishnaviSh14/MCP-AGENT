import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os


async def run_memory_chat():
    """Run a chat using MCP's Agent with built-in conversation memory"""

    # Load environment variables
    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    config_file = "server/weather.json"

    print("Initializing chat...")

    # Create MCP client and agent
    client = MCPClient.from_config_file(config_file)

    # ✅ Use correct Groq model name
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

    # Create agent with memory enabled
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("Type 'clear' to clear conversation history.")
    print("================================\n")

    try:
        while True:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation.")
                break

            # Clear history
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.\n")
                continue

            print("Assistant: ", end="", flush=True)

            try:
                # Run the agent with the user input
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Cleanup client sessions safely
        if client and client.sessions:
            try:
                await client.close_all_sessions()
            except Exception as e:
                print(f"Warning during cleanup: {e}")


if __name__ == "__main__":
    asyncio.run(run_memory_chat())
