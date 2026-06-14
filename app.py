from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)


def generate_recipes(item, diet_filter=None, healthy_filter=None):
    item = item.lower().strip()

    paneer_recipes = [
        {
            "name": "Paneer Butter Masala",
            "description": "Rich, creamy North Indian curry with soft paneer in tomato-butter gravy.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "15 min",
            "cook_time": "25 min",
            "total_time": "40 min",
            "calories": 420,
            "servings": 2,
            "ingredients": [
                "200g paneer", "2 tbsp butter", "1 large onion", "2 tomatoes",
                "8 cashews", "3 garlic cloves", "1 tsp kasuri methi",
                "1 tsp red chilli powder", "1/2 cup fresh cream", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Heat 2 tbsp butter and sauté chopped onions until soft and golden.", "time": "6 min"},
                {"step": 2, "text": "Add tomatoes, cashews, and garlic; cook until mushy and oil separates.", "time": "10 min"},
                {"step": 3, "text": "Cool slightly and blend into a smooth gravy.", "time": "3 min"},
                {"step": 4, "text": "Return gravy to pan; add butter, kasuri methi, and chilli powder. Simmer.", "time": "5 min"},
                {"step": 5, "text": "Add paneer cubes and simmer gently.", "time": "10 min"},
                {"step": 6, "text": "Stir in fresh cream and serve hot with naan or rice.", "time": "1 min"}
            ]
        },
        {
            "name": "Chilli Paneer",
            "description": "Crispy paneer tossed in tangy Indo-Chinese sauce with capsicum.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "10 min",
            "cook_time": "15 min",
            "total_time": "25 min",
            "calories": 380,
            "servings": 2,
            "ingredients": [
                "250g paneer", "3 tbsp cornflour", "1 capsicum", "1 onion",
                "2 tbsp soy sauce", "1 tbsp vinegar", "2 tbsp green chilli sauce",
                "1 tsp red chilli paste", "spring onion", "oil for frying"
            ],
            "steps": [
                {"step": 1, "text": "Cut paneer into cubes; coat with cornflour and shallow fry until crispy.", "time": "8 min"},
                {"step": 2, "text": "In a wok, heat oil and sauté garlic, onion, and capsicum.", "time": "3 min"},
                {"step": 3, "text": "Add soy sauce, vinegar, green chilli sauce, and red chilli paste.", "time": "2 min"},
                {"step": 4, "text": "Toss fried paneer on high flame until fully coated.", "time": "2 min"},
                {"step": 5, "text": "Garnish with spring onion and serve immediately.", "time": "1 min"}
            ]
        },
        {
            "name": "Paneer Tikka",
            "description": "Charred, smoky paneer skewers marinated in spiced yogurt.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "25 min",
            "cook_time": "12 min",
            "total_time": "37 min",
            "calories": 290,
            "servings": 2,
            "ingredients": [
                "200g paneer", "1/2 cup curd", "1 tsp turmeric",
                "1 tsp chilli powder", "1 tbsp ginger-garlic paste",
                "1 onion (cubed)", "1 capsicum (cubed)", "salt", "butter"
            ],
            "steps": [
                {"step": 1, "text": "Mix curd with turmeric, chilli powder, ginger-garlic paste, and salt.", "time": "3 min"},
                {"step": 2, "text": "Add paneer, onion, and capsicum cubes; marinate for 20 minutes.", "time": "20 min"},
                {"step": 3, "text": "Skewer pieces and grill on pan or oven until charred on edges.", "time": "10 min"},
                {"step": 4, "text": "Brush with butter and serve with mint chutney.", "time": "2 min"}
            ]
        },
        {
            "name": "Paneer Biryani",
            "description": "Fragrant layered rice with spiced paneer and saffron.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "20 min",
            "cook_time": "35 min",
            "total_time": "55 min",
            "calories": 510,
            "servings": 3,
            "ingredients": [
                "1.5 cups basmati rice", "200g paneer", "2 onions",
                "1/2 cup curd", "2 tbsp biryani masala", "saffron soaked in warm milk",
                "2 tbsp ghee", "whole spices (bay leaf, cardamom, cinnamon)"
            ],
            "steps": [
                {"step": 1, "text": "Soak rice 20 min; boil with whole spices until 90% cooked. Drain.", "time": "15 min"},
                {"step": 2, "text": "Sauté paneer with biryani masala, onion, and curd until fragrant.", "time": "12 min"},
                {"step": 3, "text": "Layer rice and paneer masala in a heavy pot.", "time": "3 min"},
                {"step": 4, "text": "Pour saffron milk and ghee over the top layer.", "time": "2 min"},
                {"step": 5, "text": "Cover tightly and dum cook on low heat.", "time": "15 min"},
                {"step": 6, "text": "Rest 5 minutes, fluff gently, and serve with raita.", "time": "5 min"}
            ]
        },
        {
            "name": "Paneer Sandwich",
            "description": "Grilled sandwich with spiced paneer filling.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "10 min",
            "cook_time": "8 min",
            "total_time": "18 min",
            "calories": 320,
            "servings": 2,
            "ingredients": [
                "150g paneer", "4 bread slices", "1/4 onion", "1/4 capsicum",
                "1/2 tsp pepper", "1/2 tsp chilli flakes", "butter", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Mash paneer with finely chopped onion, capsicum, pepper, chilli flakes, and salt.", "time": "5 min"},
                {"step": 2, "text": "Butter bread slices on one side each.", "time": "2 min"},
                {"step": 3, "text": "Spread paneer filling and close sandwich.", "time": "2 min"},
                {"step": 4, "text": "Grill in toaster or pan until golden brown on both sides.", "time": "6 min"},
                {"step": 5, "text": "Cut diagonally and serve with ketchup.", "time": "1 min"}
            ]
        },
        {
            "name": "Paneer Paratha",
            "description": "Stuffed whole-wheat flatbread with seasoned paneer.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "15 min",
            "cook_time": "20 min",
            "total_time": "35 min",
            "calories": 350,
            "servings": 2,
            "ingredients": [
                "150g paneer (grated)", "1 cup wheat flour", "2 tbsp coriander",
                "1 green chilli", "ghee", "salt", "water for dough"
            ],
            "steps": [
                {"step": 1, "text": "Grate paneer; mix with coriander, chopped chilli, and salt.", "time": "5 min"},
                {"step": 2, "text": "Knead soft wheat dough and rest 10 minutes.", "time": "10 min"},
                {"step": 3, "text": "Roll small disc, stuff paneer mix, seal, and roll gently again.", "time": "5 min"},
                {"step": 4, "text": "Cook on hot tawa with ghee until golden spots appear on both sides.", "time": "15 min"},
                {"step": 5, "text": "Serve hot with curd or pickle.", "time": "1 min"}
            ]
        }
    ]

    egg_recipes = [
        {
            "name": "Egg Curry",
            "description": "Boiled eggs simmered in spiced onion-tomato gravy.",
            "diet": "non-veg",
            "healthy": True,
            "prep_time": "10 min",
            "cook_time": "25 min",
            "total_time": "35 min",
            "calories": 280,
            "servings": 2,
            "ingredients": [
                "4 eggs", "2 onions", "2 tomatoes", "1 tsp ginger-garlic paste",
                "1 tsp turmeric", "1 tsp chilli powder", "1 tsp coriander powder",
                "2 tbsp oil", "fresh coriander", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Boil eggs for 9 minutes, cool in water, peel, and make shallow slits.", "time": "12 min"},
                {"step": 2, "text": "Sauté onion until golden; add ginger-garlic and tomato.", "time": "8 min"},
                {"step": 3, "text": "Add turmeric, chilli powder, coriander powder; cook until oil separates.", "time": "5 min"},
                {"step": 4, "text": "Add 1 cup water, boil, then add eggs and simmer.", "time": "10 min"},
                {"step": 5, "text": "Garnish with coriander and serve with rice or roti.", "time": "1 min"}
            ]
        },
        {
            "name": "Egg Fried Rice",
            "description": "Classic wok-style fried rice with scrambled eggs and vegetables.",
            "diet": "non-veg",
            "healthy": False,
            "prep_time": "10 min",
            "cook_time": "12 min",
            "total_time": "22 min",
            "calories": 410,
            "servings": 2,
            "ingredients": [
                "2 eggs", "2 cups cooked rice", "1/2 cup mixed vegetables",
                "2 tbsp soy sauce", "1 tsp vinegar", "1/2 tsp pepper", "2 tbsp oil", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Scramble eggs in hot oil until just set; set aside.", "time": "3 min"},
                {"step": 2, "text": "Stir-fry vegetables on high heat until crisp-tender.", "time": "4 min"},
                {"step": 3, "text": "Add rice, soy sauce, vinegar, pepper, and salt; toss well.", "time": "3 min"},
                {"step": 4, "text": "Fold in scrambled eggs and toss for 2 more minutes.", "time": "2 min"},
                {"step": 5, "text": "Serve hot immediately.", "time": "1 min"}
            ]
        },
        {
            "name": "Masala Omelette",
            "description": "Fluffy Indian-style omelette loaded with onions and spices.",
            "diet": "non-veg",
            "healthy": True,
            "prep_time": "5 min",
            "cook_time": "6 min",
            "total_time": "11 min",
            "calories": 220,
            "servings": 1,
            "ingredients": [
                "2 eggs", "1/4 onion", "1 green chilli", "1 small tomato",
                "1/4 tsp turmeric", "salt", "pepper", "1 tbsp butter"
            ],
            "steps": [
                {"step": 1, "text": "Beat eggs with chopped onion, chilli, tomato, turmeric, salt, and pepper.", "time": "3 min"},
                {"step": 2, "text": "Melt butter in a non-stick pan over medium heat.", "time": "1 min"},
                {"step": 3, "text": "Pour mixture and cook until edges set; flip carefully.", "time": "3 min"},
                {"step": 4, "text": "Cook other side 1–2 minutes and serve with toast.", "time": "2 min"}
            ]
        },
        {
            "name": "Egg Noodles",
            "description": "Quick stir-fried noodles with eggs and crunchy vegetables.",
            "diet": "non-veg",
            "healthy": False,
            "prep_time": "8 min",
            "cook_time": "12 min",
            "total_time": "20 min",
            "calories": 390,
            "servings": 2,
            "ingredients": [
                "150g noodles", "2 eggs", "1 cup mixed vegetables",
                "2 tbsp soy sauce", "1 tbsp chilli sauce", "1 tbsp oil", "garlic", "spring onion"
            ],
            "steps": [
                {"step": 1, "text": "Boil noodles according to package; drain and toss with a little oil.", "time": "6 min"},
                {"step": 2, "text": "Scramble eggs separately and keep aside.", "time": "3 min"},
                {"step": 3, "text": "Stir-fry garlic and vegetables on high flame.", "time": "4 min"},
                {"step": 4, "text": "Add noodles, sauces, and eggs; toss until evenly coated.", "time": "3 min"},
                {"step": 5, "text": "Top with spring onion and serve hot.", "time": "1 min"}
            ]
        },
        {
            "name": "Egg Sandwich",
            "description": "Creamy boiled-egg filling grilled between buttered bread.",
            "diet": "non-veg",
            "healthy": True,
            "prep_time": "12 min",
            "cook_time": "5 min",
            "total_time": "17 min",
            "calories": 310,
            "servings": 2,
            "ingredients": [
                "3 eggs", "4 bread slices", "2 tbsp mayonnaise",
                "1 tsp mustard", "pepper", "salt", "butter"
            ],
            "steps": [
                {"step": 1, "text": "Hard-boil eggs for 9 minutes, peel, and mash finely.", "time": "10 min"},
                {"step": 2, "text": "Mix with mayonnaise, mustard, pepper, and salt.", "time": "2 min"},
                {"step": 3, "text": "Spread on bread, close sandwich, and butter outside.", "time": "2 min"},
                {"step": 4, "text": "Toast on pan until golden and serve warm.", "time": "5 min"}
            ]
        },
        {
            "name": "Egg Bhurji",
            "description": "Spiced scrambled eggs with onion, tomato, and masala.",
            "diet": "non-veg",
            "healthy": True,
            "prep_time": "5 min",
            "cook_time": "8 min",
            "total_time": "13 min",
            "calories": 240,
            "servings": 2,
            "ingredients": [
                "3 eggs", "1 onion", "1 tomato", "1 green chilli",
                "1/2 tsp turmeric", "1/2 tsp chilli powder", "2 tbsp oil", "salt", "coriander"
            ],
            "steps": [
                {"step": 1, "text": "Sauté onion, chilli, and tomato until soft.", "time": "4 min"},
                {"step": 2, "text": "Add turmeric, chilli powder, and salt.", "time": "1 min"},
                {"step": 3, "text": "Pour beaten eggs and stir continuously on medium heat.", "time": "4 min"},
                {"step": 4, "text": "Cook until fluffy but moist; garnish with coriander.", "time": "2 min"},
                {"step": 5, "text": "Serve with buttered pav or roti.", "time": "1 min"}
            ]
        }
    ]

    potato_recipes = [
        {
            "name": "Aloo Paratha",
            "description": "Classic stuffed flatbread with spiced mashed potato filling.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "20 min",
            "cook_time": "20 min",
            "total_time": "40 min",
            "calories": 370,
            "servings": 2,
            "ingredients": [
                "3 medium potatoes", "1 cup wheat flour", "1 onion",
                "1 green chilli", "1 tsp coriander powder", "ghee", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Boil potatoes until tender; peel and mash.", "time": "15 min"},
                {"step": 2, "text": "Mix mash with onion, chilli, coriander powder, and salt.", "time": "3 min"},
                {"step": 3, "text": "Knead wheat dough and rest 10 minutes.", "time": "10 min"},
                {"step": 4, "text": "Stuff potato mix in dough balls and roll carefully.", "time": "5 min"},
                {"step": 5, "text": "Cook on tawa with ghee until golden on both sides.", "time": "15 min"},
                {"step": 6, "text": "Serve with butter and curd.", "time": "1 min"}
            ]
        },
        {
            "name": "Masala Aloo Fry",
            "description": "Crispy pan-fried potato cubes with mustard and cumin tempering.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "15 min",
            "cook_time": "12 min",
            "total_time": "27 min",
            "calories": 260,
            "servings": 2,
            "ingredients": [
                "3 potatoes", "1 tsp mustard seeds", "1 tsp cumin",
                "1/2 tsp turmeric", "1 tsp chilli powder", "2 tbsp oil", "curry leaves", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Boil potatoes until just tender; peel and cube.", "time": "12 min"},
                {"step": 2, "text": "Heat oil; splutter mustard, cumin, and curry leaves.", "time": "2 min"},
                {"step": 3, "text": "Add potatoes, turmeric, chilli powder, and salt.", "time": "2 min"},
                {"step": 4, "text": "Pan-fry on medium heat until edges turn crispy.", "time": "8 min"},
                {"step": 5, "text": "Serve as a side with dal-rice or roti.", "time": "1 min"}
            ]
        },
        {
            "name": "Potato Wedges",
            "description": "Oven-baked seasoned potato wedges with a crispy edge.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "10 min",
            "cook_time": "25 min",
            "total_time": "35 min",
            "calories": 220,
            "servings": 2,
            "ingredients": [
                "3 potatoes", "2 tbsp olive oil", "1 tsp chilli flakes",
                "1 tsp garlic powder", "1 tsp paprika", "salt", "pepper"
            ],
            "steps": [
                {"step": 1, "text": "Cut potatoes into thick wedges and pat dry.", "time": "5 min"},
                {"step": 2, "text": "Toss with oil, chilli flakes, garlic powder, paprika, salt, and pepper.", "time": "3 min"},
                {"step": 3, "text": "Arrange on baking tray in a single layer.", "time": "2 min"},
                {"step": 4, "text": "Bake at 200°C (or air fry) until golden and crisp.", "time": "22 min"},
                {"step": 5, "text": "Serve with mayo or ketchup.", "time": "1 min"}
            ]
        },
        {
            "name": "Creamy Potato Soup",
            "description": "Comforting blended potato soup with butter and herbs.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "10 min",
            "cook_time": "25 min",
            "total_time": "35 min",
            "calories": 190,
            "servings": 2,
            "ingredients": [
                "4 potatoes", "1 small onion", "2 cups milk",
                "2 tbsp butter", "1 cup vegetable stock", "pepper", "salt", "fresh herbs"
            ],
            "steps": [
                {"step": 1, "text": "Sauté onion in butter until translucent.", "time": "4 min"},
                {"step": 2, "text": "Add diced potatoes and stock; boil until very soft.", "time": "15 min"},
                {"step": 3, "text": "Blend half the soup for thickness; return to pot.", "time": "3 min"},
                {"step": 4, "text": "Stir in milk, pepper, and salt; simmer gently.", "time": "5 min"},
                {"step": 5, "text": "Serve warm topped with herbs.", "time": "1 min"}
            ]
        },
        {
            "name": "Aloo Tikki",
            "description": "Crispy street-style potato patties served with chutney.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "15 min",
            "cook_time": "15 min",
            "total_time": "30 min",
            "calories": 300,
            "servings": 4,
            "ingredients": [
                "4 potatoes", "2 tbsp breadcrumbs", "1 tsp chaat masala",
                "1 green chilli", "2 tbsp coriander", "oil for shallow frying", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Boil and mash potatoes; mix with masala, chilli, coriander, and salt.", "time": "12 min"},
                {"step": 2, "text": "Shape into flat patties and coat lightly with breadcrumbs.", "time": "5 min"},
                {"step": 3, "text": "Shallow fry on medium heat until deep golden.", "time": "12 min"},
                {"step": 4, "text": "Drain on paper and serve with mint and tamarind chutney.", "time": "2 min"}
            ]
        },
        {
            "name": "Honey Chilli Potato",
            "description": "Sweet-spicy Indo-Chinese potato strips with sesame garnish.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "12 min",
            "cook_time": "18 min",
            "total_time": "30 min",
            "calories": 340,
            "servings": 2,
            "ingredients": [
                "3 potatoes", "3 tbsp cornflour", "2 tbsp honey",
                "2 tbsp chilli sauce", "1 tbsp soy sauce", "sesame seeds",
                "spring onion", "oil for frying"
            ],
            "steps": [
                {"step": 1, "text": "Cut potatoes into thin strips; coat with cornflour.", "time": "5 min"},
                {"step": 2, "text": "Deep or shallow fry until crispy and golden.", "time": "10 min"},
                {"step": 3, "text": "In a pan, combine honey, chilli sauce, and soy sauce; heat briefly.", "time": "2 min"},
                {"step": 4, "text": "Toss fried potatoes in sauce on high flame.", "time": "2 min"},
                {"step": 5, "text": "Garnish with sesame seeds and spring onion.", "time": "1 min"}
            ]
        }
    ]

    pasta_recipes = [
        {
            "name": "Creamy Alfredo Pasta",
            "description": "Silky white sauce pasta with garlic, cream, and parmesan.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "10 min",
            "cook_time": "18 min",
            "total_time": "28 min",
            "calories": 480,
            "servings": 2,
            "ingredients": [
                "200g pasta", "1 cup cream", "3 tbsp butter", "4 garlic cloves",
                "1/2 cup parmesan", "pepper", "salt", "parsley"
            ],
            "steps": [
                {"step": 1, "text": "Boil pasta in salted water until al dente; reserve 1/2 cup pasta water.", "time": "10 min"},
                {"step": 2, "text": "Sauté minced garlic in butter until fragrant.", "time": "2 min"},
                {"step": 3, "text": "Pour cream and simmer gently; add parmesan, pepper, and salt.", "time": "4 min"},
                {"step": 4, "text": "Toss pasta in sauce; add pasta water if needed for silkiness.", "time": "2 min"},
                {"step": 5, "text": "Garnish with parsley and serve immediately.", "time": "1 min"}
            ]
        },
        {
            "name": "Arrabbiata Pasta",
            "description": "Spicy tomato pasta with garlic, chilli, and olive oil.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "8 min",
            "cook_time": "20 min",
            "total_time": "28 min",
            "calories": 360,
            "servings": 2,
            "ingredients": [
                "200g pasta", "4 tomatoes", "4 garlic cloves",
                "2 tbsp olive oil", "1 tsp red chilli flakes", "basil", "salt"
            ],
            "steps": [
                {"step": 1, "text": "Boil pasta until al dente; drain.", "time": "10 min"},
                {"step": 2, "text": "Sauté garlic and chilli flakes in olive oil.", "time": "2 min"},
                {"step": 3, "text": "Add crushed tomatoes and simmer until thick.", "time": "10 min"},
                {"step": 4, "text": "Toss pasta in sauce and finish with fresh basil.", "time": "3 min"},
                {"step": 5, "text": "Serve hot with extra chilli flakes if desired.", "time": "1 min"}
            ]
        },
        {
            "name": "Veggie Pesto Pasta",
            "description": "Bright basil pesto pasta loaded with sautéed vegetables.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "12 min",
            "cook_time": "15 min",
            "total_time": "27 min",
            "calories": 390,
            "servings": 2,
            "ingredients": [
                "200g pasta", "2 tbsp pesto", "1 cup mixed vegetables",
                "2 tbsp olive oil", "cherry tomatoes", "parmesan", "salt", "pepper"
            ],
            "steps": [
                {"step": 1, "text": "Cook pasta until al dente; drain.", "time": "10 min"},
                {"step": 2, "text": "Sauté vegetables in olive oil until tender-crisp.", "time": "6 min"},
                {"step": 3, "text": "Stir in pesto and a splash of pasta water.", "time": "2 min"},
                {"step": 4, "text": "Add pasta, halved cherry tomatoes, salt, and pepper; toss.", "time": "3 min"},
                {"step": 5, "text": "Top with parmesan and serve.", "time": "1 min"}
            ]
        },
        {
            "name": "Cheesy Baked Macaroni",
            "description": "Golden oven-baked macaroni in rich cheddar cheese sauce.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "15 min",
            "cook_time": "25 min",
            "total_time": "40 min",
            "calories": 520,
            "servings": 3,
            "ingredients": [
                "250g macaroni", "2 tbsp butter", "2 tbsp flour", "2 cups milk",
                "1.5 cups cheddar", "breadcrumbs", "salt", "pepper", "paprika"
            ],
            "steps": [
                {"step": 1, "text": "Boil macaroni until just cooked; drain.", "time": "8 min"},
                {"step": 2, "text": "Make roux with butter and flour; whisk in milk until thick.", "time": "8 min"},
                {"step": 3, "text": "Melt in cheddar, salt, and pepper to make cheese sauce.", "time": "4 min"},
                {"step": 4, "text": "Mix pasta with sauce; transfer to baking dish.", "time": "3 min"},
                {"step": 5, "text": "Top with breadcrumbs and paprika; bake until bubbly and golden.", "time": "15 min"},
                {"step": 6, "text": "Rest 3 minutes before serving.", "time": "3 min"}
            ]
        },
        {
            "name": "Aglio e Olio",
            "description": "Minimalist Italian pasta with garlic, olive oil, and parsley.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "5 min",
            "cook_time": "12 min",
            "total_time": "17 min",
            "calories": 310,
            "servings": 2,
            "ingredients": [
                "200g spaghetti", "6 garlic cloves", "1/4 cup olive oil",
                "1 tsp red chilli flakes", "parsley", "salt", "lemon zest"
            ],
            "steps": [
                {"step": 1, "text": "Boil spaghetti in salted water until al dente.", "time": "9 min"},
                {"step": 2, "text": "Slowly sauté thinly sliced garlic in olive oil until light gold.", "time": "4 min"},
                {"step": 3, "text": "Add chilli flakes off heat.", "time": "1 min"},
                {"step": 4, "text": "Toss drained pasta in garlic oil with parsley and lemon zest.", "time": "2 min"},
                {"step": 5, "text": "Serve immediately with extra olive oil drizzle.", "time": "1 min"}
            ]
        },
        {
            "name": "Pink Sauce Pasta",
            "description": "Creamy tomato-pink sauce pasta — mild and kid-friendly.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "10 min",
            "cook_time": "18 min",
            "total_time": "28 min",
            "calories": 430,
            "servings": 2,
            "ingredients": [
                "200g pasta", "1/2 cup tomato puree", "1/2 cup cream",
                "2 tbsp butter", "1 onion", "2 garlic cloves", "oregano", "salt", "pepper"
            ],
            "steps": [
                {"step": 1, "text": "Boil pasta until al dente; drain.", "time": "10 min"},
                {"step": 2, "text": "Sauté onion and garlic in butter until soft.", "time": "5 min"},
                {"step": 3, "text": "Add tomato puree and cook 5 minutes.", "time": "5 min"},
                {"step": 4, "text": "Stir in cream, oregano, salt, and pepper; simmer gently.", "time": "4 min"},
                {"step": 5, "text": "Toss pasta in pink sauce and serve hot.", "time": "2 min"}
            ]
        }
    ]

    noodle_recipes = [
        {
            "name": "Veg Hakka Noodles",
            "description": "Street-style stir-fried noodles with crunchy vegetables.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "12 min",
            "cook_time": "10 min",
            "total_time": "22 min",
            "calories": 400,
            "servings": 2,
            "ingredients": [
                "200g noodles", "2 cups mixed vegetables", "2 tbsp soy sauce",
                "1 tbsp vinegar", "1 tbsp chilli sauce", "2 tbsp oil", "garlic", "spring onion"
            ],
            "steps": [
                {"step": 1, "text": "Boil noodles, rinse under cold water, and toss with a little oil.", "time": "6 min"},
                {"step": 2, "text": "Stir-fry garlic and vegetables on very high heat.", "time": "4 min"},
                {"step": 3, "text": "Add soy sauce, vinegar, and chilli sauce.", "time": "1 min"},
                {"step": 4, "text": "Add noodles and toss quickly for 2–3 minutes.", "time": "3 min"},
                {"step": 5, "text": "Garnish with spring onion and serve hot.", "time": "1 min"}
            ]
        },
        {
            "name": "Schezwan Noodles",
            "description": "Fiery noodles tossed in homemade-style schezwan sauce.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "10 min",
            "cook_time": "12 min",
            "total_time": "22 min",
            "calories": 420,
            "servings": 2,
            "ingredients": [
                "200g noodles", "3 tbsp schezwan sauce", "1 cup vegetables",
                "2 tbsp soy sauce", "1 tbsp oil", "garlic", "spring onion"
            ],
            "steps": [
                {"step": 1, "text": "Boil and drain noodles; set aside.", "time": "6 min"},
                {"step": 2, "text": "Sauté garlic and vegetables in oil.", "time": "4 min"},
                {"step": 3, "text": "Add schezwan sauce and soy sauce; cook 1 minute.", "time": "2 min"},
                {"step": 4, "text": "Toss noodles on high flame until evenly coated.", "time": "3 min"},
                {"step": 5, "text": "Serve with spring onion garnish.", "time": "1 min"}
            ]
        },
        {
            "name": "Thai Peanut Noodles",
            "description": "Nutty, tangy noodles with peanut butter and lime dressing.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "10 min",
            "cook_time": "8 min",
            "total_time": "18 min",
            "calories": 380,
            "servings": 2,
            "ingredients": [
                "200g noodles", "3 tbsp peanut butter", "1 tbsp soy sauce",
                "1 tbsp lime juice", "1 tsp honey", "vegetables", "crushed peanuts", "chilli flakes"
            ],
            "steps": [
                {"step": 1, "text": "Whisk peanut butter, soy sauce, lime juice, and honey into a sauce.", "time": "3 min"},
                {"step": 2, "text": "Boil noodles and drain.", "time": "6 min"},
                {"step": 3, "text": "Stir-fry vegetables briefly in a hot pan.", "time": "3 min"},
                {"step": 4, "text": "Toss noodles, vegetables, and peanut sauce together.", "time": "2 min"},
                {"step": 5, "text": "Top with crushed peanuts and chilli flakes.", "time": "1 min"}
            ]
        },
        {
            "name": "Maggi Masala Noodles",
            "description": "Elevated instant noodles with extra veggies and a tadka twist.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "5 min",
            "cook_time": "8 min",
            "total_time": "13 min",
            "calories": 350,
            "servings": 1,
            "ingredients": [
                "1 Maggi packet", "1/4 onion", "1/4 tomato", "1 green chilli",
                "1/2 tsp garam masala", "1 tsp butter", "coriander"
            ],
            "steps": [
                {"step": 1, "text": "Sauté onion, tomato, and chilli in butter.", "time": "3 min"},
                {"step": 2, "text": "Add 1 cup water and Maggi tastemaker; bring to boil.", "time": "2 min"},
                {"step": 3, "text": "Add noodles and cook until water is almost absorbed.", "time": "3 min"},
                {"step": 4, "text": "Sprinkle garam masala and coriander; serve hot.", "time": "1 min"}
            ]
        },
        {
            "name": "Garlic Butter Noodles",
            "description": "Simple buttery noodles with loads of garlic and herbs.",
            "diet": "veg",
            "healthy": False,
            "prep_time": "5 min",
            "cook_time": "10 min",
            "total_time": "15 min",
            "calories": 360,
            "servings": 2,
            "ingredients": [
                "200g noodles", "4 tbsp butter", "6 garlic cloves",
                "parsley", "chilli flakes", "parmesan", "salt", "pepper"
            ],
            "steps": [
                {"step": 1, "text": "Boil noodles until tender; drain.", "time": "7 min"},
                {"step": 2, "text": "Melt butter and sauté minced garlic until golden.", "time": "3 min"},
                {"step": 3, "text": "Toss noodles in garlic butter with salt and pepper.", "time": "2 min"},
                {"step": 4, "text": "Finish with parsley, chilli flakes, and parmesan.", "time": "1 min"}
            ]
        },
        {
            "name": "Soup Noodles Bowl",
            "description": "Warm broth bowl with noodles, greens, and light seasoning.",
            "diet": "veg",
            "healthy": True,
            "prep_time": "8 min",
            "cook_time": "15 min",
            "total_time": "23 min",
            "calories": 250,
            "servings": 2,
            "ingredients": [
                "150g noodles", "3 cups vegetable broth", "1 cup spinach",
                "1 carrot (sliced)", "1 tbsp soy sauce", "ginger", "garlic", "spring onion"
            ],
            "steps": [
                {"step": 1, "text": "Sauté ginger and garlic in a pot.", "time": "2 min"},
                {"step": 2, "text": "Add broth, soy sauce, and carrot; simmer 8 minutes.", "time": "8 min"},
                {"step": 3, "text": "Add noodles and cook until tender.", "time": "5 min"},
                {"step": 4, "text": "Stir in spinach until wilted.", "time": "2 min"},
                {"step": 5, "text": "Serve hot topped with spring onion.", "time": "1 min"}
            ]
        }
    ]

    ingredient_map = {
        "paneer": paneer_recipes,
        "cottage cheese": paneer_recipes,
        "egg": egg_recipes,
        "eggs": egg_recipes,
        "potato": potato_recipes,
        "aloo": potato_recipes,
        "pasta": pasta_recipes,
        "macaroni": pasta_recipes,
        "noodles": noodle_recipes,
        "noodle": noodle_recipes,
        "maggi": noodle_recipes
    }

    recipes = None
    for key in ingredient_map:
        if key in item:
            bank = ingredient_map[key][:]
            random.shuffle(bank)
            recipes = bank[:6]
            break

    if recipes is None:
        generic = [
            {
                "name": f"{item.title()} Curry",
                "description": f"A hearty homestyle curry starring fresh {item}.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "10 min",
                "cook_time": "20 min",
                "total_time": "30 min",
                "calories": 280,
                "servings": 2,
                "ingredients": [f"2 cups {item}", "1 onion", "2 tomatoes", "spices", "2 tbsp oil", "salt"],
                "steps": [
                    {"step": 1, "text": f"Chop {item} and sauté with onions until fragrant.", "time": "6 min"},
                    {"step": 2, "text": "Add tomatoes and spices; cook until oil separates.", "time": "8 min"},
                    {"step": 3, "text": f"Add {item} and enough water to cover.", "time": "2 min"},
                    {"step": 4, "text": "Simmer until soft and flavors meld.", "time": "12 min"},
                    {"step": 5, "text": "Serve hot with rice or roti.", "time": "1 min"}
                ]
            },
            {
                "name": f"Spicy {item.title()} Fry",
                "description": f"Crispy pan-fried {item} with bold spices and lemon.",
                "diet": "veg",
                "healthy": False,
                "prep_time": "8 min",
                "cook_time": "12 min",
                "total_time": "20 min",
                "calories": 310,
                "servings": 2,
                "ingredients": [f"2 cups {item}", "1 tsp chilli powder", "1/2 tsp turmeric", "lemon", "oil", "salt"],
                "steps": [
                    {"step": 1, "text": f"Cut {item} into bite-size pieces.", "time": "5 min"},
                    {"step": 2, "text": "Toss with spices and salt.", "time": "2 min"},
                    {"step": 3, "text": "Shallow fry on medium-high heat until crispy.", "time": "10 min"},
                    {"step": 4, "text": "Squeeze lemon and serve hot.", "time": "1 min"}
                ]
            },
            {
                "name": f"{item.title()} Sandwich",
                "description": f"Quick grilled sandwich filled with seasoned {item}.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "8 min",
                "cook_time": "6 min",
                "total_time": "14 min",
                "calories": 290,
                "servings": 1,
                "ingredients": [f"1 cup {item}", "2 bread slices", "mayonnaise", "lettuce", "pepper", "butter"],
                "steps": [
                    {"step": 1, "text": f"Season sliced or mashed {item} with pepper and salt.", "time": "3 min"},
                    {"step": 2, "text": "Layer filling, lettuce, and sauce between bread.", "time": "2 min"},
                    {"step": 3, "text": "Butter outside and grill until golden.", "time": "6 min"},
                    {"step": 4, "text": "Serve warm.", "time": "1 min"}
                ]
            },
            {
                "name": f"{item.title()} Salad",
                "description": f"Fresh, light salad with grilled {item} and greens.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "10 min",
                "cook_time": "5 min",
                "total_time": "15 min",
                "calories": 180,
                "servings": 2,
                "ingredients": [f"1 cup {item}", "lettuce", "cucumber", "olive oil", "lemon", "pepper"],
                "steps": [
                    {"step": 1, "text": f"Lightly grill or roast {item}.", "time": "5 min"},
                    {"step": 2, "text": "Toss with lettuce, cucumber, olive oil, and lemon.", "time": "4 min"},
                    {"step": 3, "text": "Season with pepper and serve chilled.", "time": "2 min"}
                ]
            },
            {
                "name": f"{item.title()} Wrap",
                "description": f"Flavor-packed wrap with sautéed {item} and crunchy veggies.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "10 min",
                "cook_time": "8 min",
                "total_time": "18 min",
                "calories": 320,
                "servings": 2,
                "ingredients": [f"1 cup {item}", "2 tortillas", "onion", "capsicum", "sauces", "spices"],
                "steps": [
                    {"step": 1, "text": f"Sauté {item} with spices until tender.", "time": "6 min"},
                    {"step": 2, "text": "Warm tortillas and add filling plus fresh veggies.", "time": "3 min"},
                    {"step": 3, "text": "Roll tightly and grill seam-side down.", "time": "4 min"},
                    {"step": 4, "text": "Slice and serve.", "time": "1 min"}
                ]
            },
            {
                "name": f"{item.title()} Rice Bowl",
                "description": f"One-bowl meal with {item}, rice, and sesame finish.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "8 min",
                "cook_time": "12 min",
                "total_time": "20 min",
                "calories": 340,
                "servings": 2,
                "ingredients": [f"1 cup {item}", "2 cups cooked rice", "soy sauce", "garlic", "sesame seeds", "oil"],
                "steps": [
                    {"step": 1, "text": f"Stir-fry {item} with garlic and soy sauce.", "time": "6 min"},
                    {"step": 2, "text": "Add cooked rice and toss on high heat.", "time": "4 min"},
                    {"step": 3, "text": "Top with sesame seeds and serve.", "time": "2 min"}
                ]
            }
        ]
        random.shuffle(generic)
        recipes = generic[:6]

        if diet_filter in ("veg", "non-veg"):
         recipes = [r for r in recipes if r.get("diet") == diet_filter]

        if healthy_filter == "healthy":
         recipes = [r for r in recipes if r.get("healthy") is True]
        elif healthy_filter == "unhealthy":
         recipes = [r for r in recipes if r.get("healthy") is False]

        return recipes[:6]


# Root route – serves the main HTML page
@app.route("/")
def index():
    return send_from_directory(".", "pantry.html")

@app.route("/style.css")
def serve_css():
    return send_from_directory(".", "style.css")

@app.route("/get_recipe", methods=["POST"])
def get_recipe():
    item = request.form.get("item", "")
    diet = request.form.get("diet", "all")
    healthy = request.form.get("healthy", "all")

    if not item.strip():
        return jsonify({"error": "Please enter an ingredient!"}), 400

    recipes = generate_recipes(
        item,
        diet_filter=None if diet == "all" else diet,
        healthy_filter=None if healthy == "all" else healthy,
    )

    if not recipes:
        return jsonify({"error": "No recipes match your filters. Try changing them."})

    return jsonify({"recipes": recipes})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)