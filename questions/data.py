"""
data.py
-------
Question bank for the quiz bot.

Provides :func:`get_questions` to sample questions from a chosen category,
and the :data:`CATEGORIES` constant listing all available categories.
"""

import random
from typing import List

from models.question import BaseQuestion, MultipleChoiceQuestion, TrueFalseQuestion

CATEGORIES = ["Science", "History", "Geography", "Sports", "Technology"]

# ---------------------------------------------------------------------------
# Question bank
# ---------------------------------------------------------------------------

_BANK: dict[str, List[BaseQuestion]] = {
    "Science": [
        MultipleChoiceQuestion(
            "What is the chemical symbol for Gold?",
            "Science", "easy", "Au", ["Ag", "Fe", "Gd"]
        ),
        MultipleChoiceQuestion(
            "How many bones are in the adult human body?",
            "Science", "medium", "206", ["204", "210", "198"]
        ),
        MultipleChoiceQuestion(
            "What planet is known as the Red Planet?",
            "Science", "easy", "Mars", ["Venus", "Jupiter", "Saturn"]
        ),
        MultipleChoiceQuestion(
            "What is the powerhouse of the cell?",
            "Science", "easy", "Mitochondria",
            ["Nucleus", "Ribosome", "Golgi apparatus"]
        ),
        MultipleChoiceQuestion(
            "What is the speed of light (approx.) in km/s?",
            "Science", "medium", "300,000",
            ["150,000", "500,000", "1,000,000"]
        ),
        MultipleChoiceQuestion(
            "Which element has the atomic number 1?",
            "Science", "easy", "Hydrogen", ["Helium", "Oxygen", "Carbon"]
        ),
        MultipleChoiceQuestion(
            "What is the hardest natural substance on Earth?",
            "Science", "easy", "Diamond", ["Quartz", "Titanium", "Graphene"]
        ),
        MultipleChoiceQuestion(
            "Which gas do plants absorb during photosynthesis?",
            "Science", "easy", "Carbon Dioxide",
            ["Oxygen", "Nitrogen", "Hydrogen"]
        ),
        TrueFalseQuestion(
            "Sound travels faster in water than in air.",
            "Science", "medium", True
        ),
        TrueFalseQuestion(
            "The human body has more bacteria than human cells.",
            "Science", "hard", True
        ),
        MultipleChoiceQuestion(
            "What is the most abundant gas in Earth's atmosphere?",
            "Science", "medium", "Nitrogen",
            ["Oxygen", "Carbon Dioxide", "Argon"]
        ),
        MultipleChoiceQuestion(
            "In which organ does digestion primarily occur?",
            "Science", "medium", "Small intestine",
            ["Stomach", "Large intestine", "Liver"]
        ),
    ],

    "History": [
        MultipleChoiceQuestion(
            "In which year did World War II end?",
            "History", "easy", "1945", ["1939", "1942", "1950"]
        ),
        MultipleChoiceQuestion(
            "Who was the first President of the United States?",
            "History", "easy", "George Washington",
            ["Abraham Lincoln", "Thomas Jefferson", "John Adams"]
        ),
        MultipleChoiceQuestion(
            "The Berlin Wall fell in which year?",
            "History", "medium", "1989", ["1991", "1987", "1985"]
        ),
        MultipleChoiceQuestion(
            "Which empire was ruled by Julius Caesar?",
            "History", "easy", "Roman Empire",
            ["Greek Empire", "Ottoman Empire", "Byzantine Empire"]
        ),
        MultipleChoiceQuestion(
            "Who wrote the 'I Have a Dream' speech?",
            "History", "easy", "Martin Luther King Jr.",
            ["Malcolm X", "Rosa Parks", "Barack Obama"]
        ),
        TrueFalseQuestion(
            "Napoleon Bonaparte was born in France.",
            "History", "medium", False
        ),
        MultipleChoiceQuestion(
            "The French Revolution began in which year?",
            "History", "medium", "1789", ["1776", "1804", "1815"]
        ),
        MultipleChoiceQuestion(
            "Which country first landed humans on the Moon?",
            "History", "easy", "USA", ["USSR", "China", "UK"]
        ),
        TrueFalseQuestion(
            "The Great Wall of China is visible from space with the naked eye.",
            "History", "medium", False
        ),
        MultipleChoiceQuestion(
            "Who was the first woman to win a Nobel Prize?",
            "History", "hard", "Marie Curie",
            ["Rosalind Franklin", "Ada Lovelace", "Florence Nightingale"]
        ),
        MultipleChoiceQuestion(
            "Which ancient wonder was located in Alexandria?",
            "History", "medium", "The Lighthouse",
            ["The Colossus", "The Mausoleum", "The Hanging Gardens"]
        ),
        MultipleChoiceQuestion(
            "The Titanic sank in which year?",
            "History", "easy", "1912", ["1908", "1915", "1920"]
        ),
    ],

    "Geography": [
        MultipleChoiceQuestion(
            "What is the capital of Australia?",
            "Geography", "medium", "Canberra",
            ["Sydney", "Melbourne", "Brisbane"]
        ),
        MultipleChoiceQuestion(
            "Which is the longest river in the world?",
            "Geography", "medium", "Nile",
            ["Amazon", "Yangtze", "Mississippi"]
        ),
        MultipleChoiceQuestion(
            "On which continent is the Sahara Desert?",
            "Geography", "easy", "Africa",
            ["Asia", "Australia", "South America"]
        ),
        MultipleChoiceQuestion(
            "What is the smallest country in the world?",
            "Geography", "medium", "Vatican City",
            ["Monaco", "San Marino", "Liechtenstein"]
        ),
        MultipleChoiceQuestion(
            "Which country has the most natural lakes?",
            "Geography", "hard", "Canada",
            ["Russia", "USA", "Finland"]
        ),
        TrueFalseQuestion(
            "Brazil is the largest country in South America by area.",
            "Geography", "easy", True
        ),
        MultipleChoiceQuestion(
            "Mount Everest is located on the border of which two countries?",
            "Geography", "medium", "Nepal and China",
            ["Nepal and India", "China and India", "Nepal and Bhutan"]
        ),
        MultipleChoiceQuestion(
            "What is the capital of Canada?",
            "Geography", "medium", "Ottawa",
            ["Toronto", "Vancouver", "Montreal"]
        ),
        TrueFalseQuestion(
            "Russia is the largest country in the world by land area.",
            "Geography", "easy", True
        ),
        MultipleChoiceQuestion(
            "The Amazon River flows into which ocean?",
            "Geography", "easy", "Atlantic Ocean",
            ["Pacific Ocean", "Indian Ocean", "Caribbean Sea"]
        ),
        MultipleChoiceQuestion(
            "Which city is known as the City of Canals?",
            "Geography", "easy", "Venice",
            ["Amsterdam", "Bangkok", "Copenhagen"]
        ),
        MultipleChoiceQuestion(
            "What is the capital of South Africa's government (executive)?",
            "Geography", "hard", "Pretoria",
            ["Cape Town", "Johannesburg", "Durban"]
        ),
    ],

    "Sports": [
        MultipleChoiceQuestion(
            "How many players are on a standard football (soccer) team?",
            "Sports", "easy", "11", ["10", "12", "9"]
        ),
        MultipleChoiceQuestion(
            "In which sport would you perform a slam dunk?",
            "Sports", "easy", "Basketball",
            ["Volleyball", "Baseball", "Tennis"]
        ),
        MultipleChoiceQuestion(
            "Which country has won the most FIFA World Cups?",
            "Sports", "medium", "Brazil",
            ["Germany", "Italy", "Argentina"]
        ),
        TrueFalseQuestion(
            "A marathon is exactly 42.195 km long.",
            "Sports", "medium", True
        ),
        MultipleChoiceQuestion(
            "In tennis, what is the term for zero points?",
            "Sports", "easy", "Love",
            ["Zero", "Nil", "Nought"]
        ),
        MultipleChoiceQuestion(
            "The Olympic Games originated in which country?",
            "Sports", "easy", "Greece",
            ["Italy", "France", "Egypt"]
        ),
        MultipleChoiceQuestion(
            "How many holes are in a standard golf course?",
            "Sports", "easy", "18", ["9", "12", "16"]
        ),
        MultipleChoiceQuestion(
            "Which sport uses a shuttlecock?",
            "Sports", "easy", "Badminton",
            ["Squash", "Lacrosse", "Polo"]
        ),
        TrueFalseQuestion(
            "Michael Jordan won 6 NBA championships with the Chicago Bulls.",
            "Sports", "medium", True
        ),
        MultipleChoiceQuestion(
            "What is the maximum break in snooker?",
            "Sports", "hard", "147", ["150", "142", "145"]
        ),
        MultipleChoiceQuestion(
            "In which year were the first modern Olympic Games held?",
            "Sports", "medium", "1896", ["1900", "1892", "1888"]
        ),
        MultipleChoiceQuestion(
            "Which country invented the sport of basketball?",
            "Sports", "medium", "USA",
            ["Canada", "UK", "Germany"]
        ),
        MultipleChoiceQuestion(
            "How many players are on a rugby union team?",
            "Sports", "easy", "15", ["11", "13", "12"]
        ),
        MultipleChoiceQuestion(
            "In which sport do you perform a 'smash'?",
            "Sports", "easy", "Tennis",
            ["Football", "Cricket", "Golf"]
        ),
    ],

    "Technology": [
        MultipleChoiceQuestion(
            "What does 'HTTP' stand for?",
            "Technology", "easy",
            "HyperText Transfer Protocol",
            ["High Transfer Text Protocol",
             "Hyper Terminal Transfer Protocol",
             "HyperText Transmission Protocol"]
        ),
        MultipleChoiceQuestion(
            "Who co-founded Apple with Steve Jobs?",
            "Technology", "easy", "Steve Wozniak",
            ["Bill Gates", "Linus Torvalds", "Dennis Ritchie"]
        ),
        MultipleChoiceQuestion(
            "In what year was the first iPhone released?",
            "Technology", "medium", "2007", ["2005", "2009", "2003"]
        ),
        TrueFalseQuestion(
            "Python is a compiled programming language.",
            "Technology", "medium", False
        ),
        MultipleChoiceQuestion(
            "What does 'GPU' stand for?",
            "Technology", "easy", "Graphics Processing Unit",
            ["General Processing Unit",
             "Global Processing Unit",
             "Graphics Program Utility"]
        ),
        MultipleChoiceQuestion(
            "Which company developed the Python programming language?",
            "Technology", "hard", "None — it was created by Guido van Rossum",
            ["Google", "Microsoft", "MIT"]
        ),
        MultipleChoiceQuestion(
            "What is the binary representation of the decimal number 10?",
            "Technology", "medium", "1010",
            ["1001", "1100", "0110"]
        ),
        TrueFalseQuestion(
            "The first computer bug was an actual insect.",
            "Technology", "medium", True
        ),
        MultipleChoiceQuestion(
            "What does 'RAM' stand for?",
            "Technology", "easy", "Random Access Memory",
            ["Read Access Memory",
             "Rapid Access Module",
             "Read And Modify"]
        ),
        MultipleChoiceQuestion(
            "Which protocol assigns IP addresses automatically?",
            "Technology", "medium", "DHCP",
            ["DNS", "FTP", "SSH"]
        ),
        MultipleChoiceQuestion(
            "What language is primarily used for styling web pages?",
            "Technology", "easy", "CSS",
            ["HTML", "JavaScript", "PHP"]
        ),
        MultipleChoiceQuestion(
            "Which sorting algorithm has the best average-case time complexity?",
            "Technology", "hard", "Merge Sort / Quick Sort O(n log n)",
            ["Bubble Sort O(n²)",
             "Insertion Sort O(n²)",
             "Selection Sort O(n²)"]
        ),
    ],
}


def get_questions(category: str, count: int) -> List[BaseQuestion]:
    """Sample *count* questions from the given category.

    If *category* is ``"Random"``, questions are drawn from all categories.

    Args:
        category (str): Category name or ``"Random"``.
        count (int): Number of questions to return.

    Returns:
        List[BaseQuestion]: Randomly sampled questions (shuffled).
    """
    if category == "Random":
        pool: List[BaseQuestion] = []
        for questions in _BANK.values():
            pool.extend(questions)
    else:
        pool = _BANK.get(category, [])

    return random.sample(pool, min(count, len(pool)))
