"""Entry point for the AI Study Assistant application."""

from agent.config import load_config
from agent.study_agent import StudyAgent
from utils.helpers import format_response, setup_logging, save_session_transcript


def print_welcome() -> None:
    """Print welcome message and instructions."""
    print("\n")
    print("*" * 80)
    print(" " * 20 + "Welcome to AI Study Assistant")
    print("*" * 80)
    print("\nThis tool helps you create study plans and answer learning questions.")
    print("Type 'exit' to quit, 'save' to save your session, or 'clear' to start fresh.\n")


def main() -> None:
    """Start the AI Study Assistant application with interactive loop."""
    # Setup
    setup_logging()
    
    try:
        config = load_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return
    
    # Initialize agent
    agent = StudyAgent(config)
    
    # Print welcome message
    print_welcome()
    
    # Main interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            # Handle special commands
            if user_input.lower() == "exit":
                print("\nThank you for using AI Study Assistant. Goodbye!")
                break
            
            if user_input.lower() == "clear":
                agent.clear_history()
                print("✓ Conversation history cleared. Starting fresh!\n")
                continue
            
            if user_input.lower() == "save":
                # Get conversation history from agent's internal state
                history = agent._conversation_history.get_messages()
                if history:
                    filepath = save_session_transcript(history)
                    print(f"✓ Session saved to: {filepath}\n")
                else:
                    print("✗ No conversation to save yet.\n")
                continue
            
            # Skip empty input
            if not user_input:
                continue
            
            # Get response from agent
            print("\nAssistant: Processing your request...")
            response = agent.run(user_input)
            print(format_response(response))
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Use 'exit' to quit gracefully.")
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    main()
