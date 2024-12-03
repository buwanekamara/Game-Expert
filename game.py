from experta import Rule, KnowledgeEngine, Fact, MATCH

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
# Section 2: Expert System
# =====================================================
class VideoGameExpertSystem(KnowledgeEngine):
    def __init__(self, knowledge_base):
        super().__init__()
        self.knowledge_base = knowledge_base  # Reference to the knowledge base
        self.recommended_games = []
        self.filtered_games = []

    @Rule(
        Fact(action="recommend"), 
        Fact(genre=MATCH.genre), 
        Fact(platform=MATCH.platform), 
        Fact(budget=MATCH.budget)
    )
    def recommend_games(self, genre, platform, budget):
        """Find games based on genre, platform, and budget."""
        self.recommended_games = [
            game for game in self.knowledge_base
            if game["genre"].lower() == genre.lower() and 
               (platform.lower() == "any" or game["platform"].lower() == platform.lower()) and
               (budget is None or game["price"] <= budget)
        ]
        
        if self.recommended_games:
            print("\nRecommended Games:")
            for game in self.recommended_games:
                print(f"- {game['name']} (${game['price']}) - Buy here: {game['link']}")
        else:
            print("\nNo games match your criteria.")

    @Rule(
        Fact(action="lookup"), 
        Fact(name=MATCH.name)
    )
    def lookup_game(self, name):
        """Retrieve game details by name."""
        game = next((g for g in self.knowledge_base if g["name"].lower() == name.lower()), None)
        if game:
            print(f"\nDetails for {game['name']}:")
            print(f"- Genre: {game['genre']}")
            print(f"- Platform: {game['platform']}")
            print(f"- Price: ${game['price']}")
            print(f"- Developer: {game['developer']}")
            print(f"- Publisher: {game['publisher']}")
            print(f"- Buy here: {game['link']}")
        else:
            print(f"\nNo game found with the name '{name}'.")

    @Rule(
        Fact(action="developer_games"), 
        Fact(developer=MATCH.developer)
    )
    def developer_games(self, developer):
        """Find all games by a developer."""
        developer_games = [game for game in self.knowledge_base if game["developer"].lower() == developer.lower()]
        if developer_games:
            print(f"\nGames developed by {developer}:")
            for game in developer_games:
                print(f"- {game['name']} (${game['price']}) - Buy here: {game['link']}")
        else:
            print(f"\nNo games found for developer '{developer}'.")

# =====================================================
# Section 3: Main Program
# =====================================================
def main():
    engine = VideoGameExpertSystem(games)
    engine.reset()

    print("Welcome to the Video Game Expert System!")
    print("Options:")
    print("1. Recommend a game")
    print("2. Look up game details")
    print("3. Find all games by a developer")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        genre = input("Enter the genre: ").strip()
        platform = input("Enter the platform (or 'Any' to skip): ").strip()
        budget_input = input("Enter your budget (or leave blank to skip): ").strip()
        budget = float(budget_input) if budget_input else None

        engine.declare(Fact(action="recommend"), Fact(genre=genre), Fact(platform=platform), Fact(budget=budget))
    elif choice == "2":
        name = input("Enter the game name: ").strip()
        engine.declare(Fact(action="lookup"), Fact(name=name))
    elif choice == "3":
        developer = input("Enter the developer name: ").strip()
        engine.declare(Fact(action="developer_games"), Fact(developer=developer))
    else:
        print("Invalid choice! Please restart the program.")
        return

    engine.run()

if __name__ == "__main__":
    main()

