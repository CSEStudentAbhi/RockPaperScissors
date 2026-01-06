import os
import google.generativeai as genai
from game_logic import tools_list, reset_game

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: GOOGLE_API_KEY not found in environment.")
    api_key = input("Please enter your Google Gen AI API Key: ").strip()

genai.configure(api_key=api_key)

sys_instruct = """
You are the Official Referee for a game of Rock-Paper-Scissors-Plus.

**Your Goal:**
Facilitate a "Best of 3" game between the User and the Bot (Simulated by the tools).

**Rules:**
1.  Valid moves: Rock, Paper, Scissors.
2.  Special move: Bomb (Can only be used ONCE per entire game).
3.  Bomb beats everything. Bomb vs Bomb is a draw.
4.  Invalid inputs waste a round (count as a loss of turn).
5.  Max 3 rounds total.

**Operational Procedure:**
1.  **AT START**: Briefly explain the rules (keep it under 5 lines).
2.  **GAME LOOP**:
    *   Ask user for their move.
    *   **CRITICAL**: You MUST call the `play_round(user_move)` tool with their input. DO NOT determine the winner yourself.
    *   Synthesize the tool output into a clear, exciting commentary.
    *   State the winner of the round and the current score.
3.  **GAME OVER**:
    *   When the tool says `game_over: true`, announce the final winner clearly.
    *   Do not ask for another move after the game is over. Ask if they want to play again (if yes, say "Please restart the script" or handle if instructed).

**Tone**: Fair, energetic, and precise.
"""

def main():
    print("--- AI Referee Initializing ---")
    
    model_candidates = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    
    model = None
    chat = None
    
    for model_name in model_candidates:
        try:
            print(f"Attempting to connect to model: {model_name}...")
            model = genai.GenerativeModel(
                model_name=model_name, 
                tools=tools_list,
                system_instruction=sys_instruct
            )
            chat = model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message("Hello Referee, let's start the game.")
            print(f"Connected to {model_name} successfully!")
            print(f"\nReferee: {response.text}")
            break
        except Exception as e:
            print(f"Failed to connect to {model_name}: {e}")
            model = None
            chat = None

    if not chat:
        print("Could not connect to any default models. Please check your API Key or Model availability.")
        return

    while True:
        try:
            user_input = input("\nYour Move > ")
            if user_input.lower() in ['quit', 'exit']:
                print("Exiting game.")
                break
            
            response = chat.send_message(user_input)
            print(f"\nReferee: {response.text}")

            if "Game Over" in response.text:
                print("\n(Session Ended. Run again to play new game)")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    reset_game()
    main()
