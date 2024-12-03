

from experta import *

# =====================================================
# Section 1: Facts (Knowledge Base)
# =====================================================
games = [
    {
        "name": "The Witcher 3",
        "genre": "RPG",
        "platform": "PC",
        "price": 30,
        "link": "https://store.steampowered.com/app/292030/The_Witcher_3/",
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt"
    },
    {
        "name": "God of War",
        "genre": "Action",
        "platform": "PS5",
        "price": 50,
        "link": "https://store.playstation.com/god-of-war",
        "developer": "Santa Monica Studio",
        "publisher": "Sony Interactive Entertainment"
    },
    {
        "name": "Age of Empires IV",
        "genre": "Strategy",
        "platform": "PC",
        "price": 40,
        "link": "https://store.steampowered.com/app/1466860/Age_of_Empires_IV/",
        "developer": "Relic Entertainment",
        "publisher": "Xbox Game Studios"
    },
    {
        "name": "Spider-Man: Miles Morales",
        "genre": "Action",
        "platform": "PS5",
        "price": 50,
        "link": "https://store.playstation.com/spider-man-morales",
        "developer": "Insomniac Games",
        "publisher": "Sony Interactive Entertainment"
    }
]

# =====================================================
# Section 2: Rules (Expert System with Relationships)
# =====================================================
class VideoGameExpert(KnowledgeEngine):
    @Rule(Fact(action='recommend'))
    def recommend_games_procedural(self):
        """Step-by-step recommendation system with strict input matching."""

        # Define expected genres and platforms
        valid_genres = {game["genre"].lower() for game in games}  # Extract unique genres
        valid_platforms = {game["platform"].lower() for game in games}  # Extract unique platforms

        # Step 1: Ask for Genre (Mandatory)
        while True:
            genre = input(f"Enter the genre ({', '.join(valid_genres)}): ").strip().lower()
            if genre in valid_genres:
                break
            print(f"There's no gaming genre called '{genre}'. Please choose from: {', '.join(valid_genres)}.")

        # Step 2: Ask for Platform (Optional)
        while True:
            platform = input(f"Enter the platform ({', '.join(valid_platforms)}) or type 'Any' to skip: ").strip().lower()
            if platform == "any":
                platform = None  # Skip platform filter
                break
            if platform in valid_platforms:
                break
            print(f"There's no gaming platform called '{platform}'. Please choose from: {', '.join(valid_platforms)} or type 'Any' to skip.")

        # Step 3: Ask for Budget (Optional)
        budget = None
        while True:
            budget_input = input("Enter your budget (e.g., 50) or type 'Any' to skip: ").strip()
            if budget_input.lower() == "any" or not budget_input:  # Skip budget
                break
            try:
                budget = float(budget_input)
                if budget < 0:
                    print("Budget cannot be negative. Please enter a valid number or 'Any' to skip.")
                    continue
                break
            except ValueError:
                print("Invalid budget input. Please enter a number or 'Any' to skip.")

        # Step 4: Filter Games
        filtered_games = [game for game in games if game["genre"].lower() == genre]
        if platform:
            filtered_games = [game for game in filtered_games if game["platform"].lower() == platform]

        budget_filtered_games = filtered_games
        if budget is not None:
            budget_filtered_games = [game for game in filtered_games if game["price"] <= budget]

        # Step 5: Display Results
        if budget_filtered_games:
            print("\nRecommended games:")
            for game in budget_filtered_games:
                print(f"- {game['name']} (${game['price']}) - Buy here: {game['link']}")
        else:
            print("\nNo games match your budget. Showing all matching games based on genre and platform:")
            if filtered_games:
                for game in filtered_games:
                    print(f"- {game['name']} (${game['price']}) - Buy here: {game['link']}")
            else:
                print("Sorry, no games match your criteria.")

    @Rule(Fact(action='lookup'), Fact(name=MATCH.name))
    def game_details(self, name):
        """Retrieve details of a specific game by name with input validation."""
        while True:
            game = next((g for g in games if g["name"].lower() == name.lower()), None)
            if game:
                print(f"\nDetails for {game['name']}:")
                print(f"- Genre: {game['genre']}")
                print(f"- Platform: {game['platform']}")
                print(f"- Price: ${game['price']}")
                print(f"- Developer: {game['developer']}")
                print(f"- Publisher: {game['publisher']}")
                print(f"- Buy here: {game['link']}")
                break
            else:
                print(f"\nSorry, no details found for '{name}'.")
                name = input("Please enter a valid game name: ").strip()

    @Rule(Fact(action='developer_games'), Fact(developer=MATCH.developer))
    def games_by_developer(self, developer):
        """Retrieve all games developed by a specific developer with input validation."""
        while True:
            developer_games = [game for game in games if game["developer"].lower() == developer.lower()]
            if developer_games:
                print(f"\nGames developed by {developer}:")
                for game in developer_games:
                    print(f"- {game['name']} (${game['price']}) - Buy here: {game['link']}")
                break
            else:
                print(f"\nSorry, no games found for developer '{developer}'.")
                developer = input("Please enter a valid developer name: ").strip()

# =====================================================
# Section 3: Main Program
# =====================================================
def main():
    engine = VideoGameExpert()
    engine.reset()

    print("Welcome to the Video Game Expert System!")
    print("Options:")
    print("1. Recommend a game")
    print("2. Look up game details")
    print("3. Find all games by a developer\n")  # Removed Option 4

    choice = input("Enter your choice (1, 2, or 3): ")  # Removed 4 from options

    if choice == "1":
        engine.declare(Fact(action='recommend'))
    elif choice == "2":
        name = input("Enter the game name to look up details: ").strip()
        engine.declare(Fact(action='lookup'), Fact(name=name))
    elif choice == "3":
        developer = input("Enter the developer name: ").strip()
        engine.declare(Fact(action='developer_games'), Fact(developer=developer))
    else:
        print("Invalid choice! Please restart the program.")

    engine.run()

if __name__ == "__main__":
    main()

