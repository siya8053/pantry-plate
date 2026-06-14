from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# ----------------------------------------------------------------------
# RECIPE DATABASES
# ----------------------------------------------------------------------

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
        "ingredients": ["200g paneer", "2 tbsp butter", "1 large onion", "2 tomatoes", "8 cashews", "3 garlic cloves", "1 tsp kasuri methi", "1 tsp red chilli powder", "1/2 cup fresh cream", "salt"],
        "steps": [{"step": 1, "text": "Heat butter and sauté onions until golden.", "time": "6 min"}, {"step": 2, "text": "Add tomatoes, cashews, garlic; cook until mushy.", "time": "10 min"}, {"step": 3, "text": "Cool and blend into smooth gravy.", "time": "3 min"}, {"step": 4, "text": "Return gravy to pan; add butter, kasuri methi, chilli powder.", "time": "5 min"}, {"step": 5, "text": "Add paneer cubes and simmer.", "time": "10 min"}, {"step": 6, "text": "Stir in cream and serve hot.", "time": "1 min"}]
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
        "ingredients": ["250g paneer", "3 tbsp cornflour", "1 capsicum", "1 onion", "2 tbsp soy sauce", "1 tbsp vinegar", "2 tbsp green chilli sauce", "1 tsp red chilli paste", "spring onion", "oil for frying"],
        "steps": [{"step": 1, "text": "Coat paneer with cornflour and shallow fry until crispy.", "time": "8 min"}, {"step": 2, "text": "In a wok, sauté garlic, onion, capsicum.", "time": "3 min"}, {"step": 3, "text": "Add soy sauce, vinegar, chilli sauces.", "time": "2 min"}, {"step": 4, "text": "Toss fried paneer on high flame.", "time": "2 min"}, {"step": 5, "text": "Garnish with spring onion and serve.", "time": "1 min"}]
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
        "ingredients": ["200g paneer", "1/2 cup curd", "1 tsp turmeric", "1 tsp chilli powder", "1 tbsp ginger-garlic paste", "1 onion (cubed)", "1 capsicum (cubed)", "salt", "butter"],
        "steps": [{"step": 1, "text": "Mix curd with spices and ginger-garlic paste.", "time": "3 min"}, {"step": 2, "text": "Marinate paneer and veggies for 20 min.", "time": "20 min"}, {"step": 3, "text": "Skewer and grill until charred.", "time": "10 min"}, {"step": 4, "text": "Brush with butter and serve.", "time": "2 min"}]
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
        "ingredients": ["1.5 cups basmati rice", "200g paneer", "2 onions", "1/2 cup curd", "2 tbsp biryani masala", "saffron", "2 tbsp ghee", "whole spices"],
        "steps": [{"step": 1, "text": "Boil rice with whole spices until 90% done.", "time": "15 min"}, {"step": 2, "text": "Sauté paneer with masala and onions.", "time": "12 min"}, {"step": 3, "text": "Layer rice and paneer masala.", "time": "3 min"}, {"step": 4, "text": "Pour saffron milk and ghee.", "time": "2 min"}, {"step": 5, "text": "Dum cook on low heat for 15 min.", "time": "15 min"}, {"step": 6, "text": "Fluff and serve.", "time": "5 min"}]
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
        "ingredients": ["150g paneer", "4 bread slices", "1/4 onion", "1/4 capsicum", "1/2 tsp pepper", "1/2 tsp chilli flakes", "butter", "salt"],
        "steps": [{"step": 1, "text": "Mash paneer with veggies and spices.", "time": "5 min"}, {"step": 2, "text": "Butter bread slices.", "time": "2 min"}, {"step": 3, "text": "Spread filling and close sandwich.", "time": "2 min"}, {"step": 4, "text": "Grill until golden brown.", "time": "6 min"}, {"step": 5, "text": "Cut and serve.", "time": "1 min"}]
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
        "ingredients": ["150g paneer (grated)", "1 cup wheat flour", "2 tbsp coriander", "1 green chilli", "ghee", "salt"],
        "steps": [{"step": 1, "text": "Mix grated paneer with coriander, chilli, salt.", "time": "5 min"}, {"step": 2, "text": "Knead dough and rest.", "time": "10 min"}, {"step": 3, "text": "Stuff and roll parathas.", "time": "5 min"}, {"step": 4, "text": "Cook on tawa with ghee.", "time": "15 min"}, {"step": 5, "text": "Serve hot.", "time": "1 min"}]
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
        "ingredients": ["4 eggs", "2 onions", "2 tomatoes", "1 tsp ginger-garlic paste", "1 tsp turmeric", "1 tsp chilli powder", "1 tsp coriander powder", "2 tbsp oil", "fresh coriander", "salt"],
        "steps": [{"step": 1, "text": "Boil and peel eggs; make slits.", "time": "12 min"}, {"step": 2, "text": "Sauté onions, ginger-garlic, tomatoes.", "time": "8 min"}, {"step": 3, "text": "Add spices and cook until oil separates.", "time": "5 min"}, {"step": 4, "text": "Add water, then eggs, simmer.", "time": "10 min"}, {"step": 5, "text": "Garnish with coriander.", "time": "1 min"}]
    },
    {
        "name": "Egg Fried Rice",
        "description": "Classic wok-style fried rice with scrambled eggs.",
        "diet": "non-veg",
        "healthy": False,
        "prep_time": "10 min",
        "cook_time": "12 min",
        "total_time": "22 min",
        "calories": 410,
        "servings": 2,
        "ingredients": ["2 eggs", "2 cups cooked rice", "1/2 cup mixed vegetables", "2 tbsp soy sauce", "1 tsp vinegar", "1/2 tsp pepper", "2 tbsp oil", "salt"],
        "steps": [{"step": 1, "text": "Scramble eggs, set aside.", "time": "3 min"}, {"step": 2, "text": "Stir-fry vegetables.", "time": "4 min"}, {"step": 3, "text": "Add rice, soy sauce, vinegar, pepper, salt.", "time": "3 min"}, {"step": 4, "text": "Fold in eggs.", "time": "2 min"}, {"step": 5, "text": "Serve hot.", "time": "1 min"}]
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
        "ingredients": ["2 eggs", "1/4 onion", "1 green chilli", "1 small tomato", "1/4 tsp turmeric", "salt", "pepper", "1 tbsp butter"],
        "steps": [{"step": 1, "text": "Beat eggs with chopped veggies and spices.", "time": "3 min"}, {"step": 2, "text": "Melt butter in pan.", "time": "1 min"}, {"step": 3, "text": "Pour mixture and cook until edges set.", "time": "3 min"}, {"step": 4, "text": "Flip and cook other side.", "time": "2 min"}]
    },
    {
        "name": "Egg Noodles",
        "description": "Quick stir-fried noodles with eggs and vegetables.",
        "diet": "non-veg",
        "healthy": False,
        "prep_time": "8 min",
        "cook_time": "12 min",
        "total_time": "20 min",
        "calories": 390,
        "servings": 2,
        "ingredients": ["150g noodles", "2 eggs", "1 cup mixed vegetables", "2 tbsp soy sauce", "1 tbsp chilli sauce", "1 tbsp oil", "garlic", "spring onion"],
        "steps": [{"step": 1, "text": "Boil noodles, drain.", "time": "6 min"}, {"step": 2, "text": "Scramble eggs, keep aside.", "time": "3 min"}, {"step": 3, "text": "Stir-fry garlic and vegetables.", "time": "4 min"}, {"step": 4, "text": "Add noodles, sauces, and eggs.", "time": "3 min"}, {"step": 5, "text": "Garnish with spring onion.", "time": "1 min"}]
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
        "ingredients": ["3 eggs", "4 bread slices", "2 tbsp mayonnaise", "1 tsp mustard", "pepper", "salt", "butter"],
        "steps": [{"step": 1, "text": "Hard-boil eggs and mash.", "time": "10 min"}, {"step": 2, "text": "Mix with mayo, mustard, pepper, salt.", "time": "2 min"}, {"step": 3, "text": "Spread on bread and close sandwich.", "time": "2 min"}, {"step": 4, "text": "Toast on pan.", "time": "5 min"}]
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
        "ingredients": ["3 eggs", "1 onion", "1 tomato", "1 green chilli", "1/2 tsp turmeric", "1/2 tsp chilli powder", "2 tbsp oil", "salt", "coriander"],
        "steps": [{"step": 1, "text": "Sauté onion, chilli, tomato.", "time": "4 min"}, {"step": 2, "text": "Add turmeric, chilli powder, salt.", "time": "1 min"}, {"step": 3, "text": "Pour beaten eggs and stir continuously.", "time": "4 min"}, {"step": 4, "text": "Cook until fluffy, garnish with coriander.", "time": "2 min"}]
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
        "ingredients": ["3 medium potatoes", "1 cup wheat flour", "1 onion", "1 green chilli", "1 tsp coriander powder", "ghee", "salt"],
        "steps": [{"step": 1, "text": "Boil, peel, and mash potatoes.", "time": "15 min"}, {"step": 2, "text": "Mix with onion, chilli, coriander powder, salt.", "time": "3 min"}, {"step": 3, "text": "Knead dough and rest.", "time": "10 min"}, {"step": 4, "text": "Stuff and roll parathas.", "time": "5 min"}, {"step": 5, "text": "Cook on tawa with ghee.", "time": "15 min"}, {"step": 6, "text": "Serve with butter and curd.", "time": "1 min"}]
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
        "ingredients": ["3 potatoes", "1 tsp mustard seeds", "1 tsp cumin", "1/2 tsp turmeric", "1 tsp chilli powder", "2 tbsp oil", "curry leaves", "salt"],
        "steps": [{"step": 1, "text": "Boil and cube potatoes.", "time": "12 min"}, {"step": 2, "text": "Heat oil, splutter mustard, cumin, curry leaves.", "time": "2 min"}, {"step": 3, "text": "Add potatoes, turmeric, chilli powder, salt.", "time": "2 min"}, {"step": 4, "text": "Pan-fry until crispy.", "time": "8 min"}, {"step": 5, "text": "Serve as side.", "time": "1 min"}]
    },
    {
        "name": "Potato Wedges",
        "description": "Oven-baked seasoned potato wedges.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "10 min",
        "cook_time": "25 min",
        "total_time": "35 min",
        "calories": 220,
        "servings": 2,
        "ingredients": ["3 potatoes", "2 tbsp olive oil", "1 tsp chilli flakes", "1 tsp garlic powder", "1 tsp paprika", "salt", "pepper"],
        "steps": [{"step": 1, "text": "Cut potatoes into wedges.", "time": "5 min"}, {"step": 2, "text": "Toss with oil and spices.", "time": "3 min"}, {"step": 3, "text": "Arrange on baking tray.", "time": "2 min"}, {"step": 4, "text": "Bake at 200°C until crisp.", "time": "22 min"}, {"step": 5, "text": "Serve with dip.", "time": "1 min"}]
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
        "ingredients": ["4 potatoes", "1 small onion", "2 cups milk", "2 tbsp butter", "1 cup vegetable stock", "pepper", "salt", "fresh herbs"],
        "steps": [{"step": 1, "text": "Sauté onion in butter.", "time": "4 min"}, {"step": 2, "text": "Add potatoes and stock, boil until soft.", "time": "15 min"}, {"step": 3, "text": "Blend half the soup.", "time": "3 min"}, {"step": 4, "text": "Stir in milk, pepper, salt, simmer.", "time": "5 min"}, {"step": 5, "text": "Serve warm with herbs.", "time": "1 min"}]
    },
    {
        "name": "Aloo Tikki",
        "description": "Crispy street-style potato patties.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "15 min",
        "cook_time": "15 min",
        "total_time": "30 min",
        "calories": 300,
        "servings": 4,
        "ingredients": ["4 potatoes", "2 tbsp breadcrumbs", "1 tsp chaat masala", "1 green chilli", "2 tbsp coriander", "oil for frying", "salt"],
        "steps": [{"step": 1, "text": "Boil and mash potatoes.", "time": "12 min"}, {"step": 2, "text": "Mix with masala, chilli, coriander, salt.", "time": "5 min"}, {"step": 3, "text": "Shape into patties, coat with breadcrumbs.", "time": "5 min"}, {"step": 4, "text": "Shallow fry until golden.", "time": "12 min"}, {"step": 5, "text": "Serve with chutney.", "time": "2 min"}]
    },
    {
        "name": "Honey Chilli Potato",
        "description": "Sweet-spicy Indo-Chinese potato strips.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "12 min",
        "cook_time": "18 min",
        "total_time": "30 min",
        "calories": 340,
        "servings": 2,
        "ingredients": ["3 potatoes", "3 tbsp cornflour", "2 tbsp honey", "2 tbsp chilli sauce", "1 tbsp soy sauce", "sesame seeds", "spring onion", "oil"],
        "steps": [{"step": 1, "text": "Cut potatoes into strips, coat with cornflour.", "time": "5 min"}, {"step": 2, "text": "Deep fry until crispy.", "time": "10 min"}, {"step": 3, "text": "Combine honey, chilli sauce, soy sauce.", "time": "2 min"}, {"step": 4, "text": "Toss fried potatoes in sauce.", "time": "2 min"}, {"step": 5, "text": "Garnish with sesame and spring onion.", "time": "1 min"}]
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
        "ingredients": ["200g pasta", "1 cup cream", "3 tbsp butter", "4 garlic cloves", "1/2 cup parmesan", "pepper", "salt", "parsley"],
        "steps": [{"step": 1, "text": "Boil pasta, reserve pasta water.", "time": "10 min"}, {"step": 2, "text": "Sauté garlic in butter.", "time": "2 min"}, {"step": 3, "text": "Pour cream, add parmesan, pepper, salt.", "time": "4 min"}, {"step": 4, "text": "Toss pasta in sauce, add pasta water if needed.", "time": "2 min"}, {"step": 5, "text": "Garnish with parsley.", "time": "1 min"}]
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
        "ingredients": ["200g pasta", "4 tomatoes", "4 garlic cloves", "2 tbsp olive oil", "1 tsp red chilli flakes", "basil", "salt"],
        "steps": [{"step": 1, "text": "Boil pasta.", "time": "10 min"}, {"step": 2, "text": "Sauté garlic and chilli flakes in oil.", "time": "2 min"}, {"step": 3, "text": "Add crushed tomatoes, simmer until thick.", "time": "10 min"}, {"step": 4, "text": "Toss pasta in sauce.", "time": "3 min"}, {"step": 5, "text": "Finish with basil.", "time": "1 min"}]
    },
    {
        "name": "Veggie Pesto Pasta",
        "description": "Bright basil pesto pasta loaded with vegetables.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "12 min",
        "cook_time": "15 min",
        "total_time": "27 min",
        "calories": 390,
        "servings": 2,
        "ingredients": ["200g pasta", "2 tbsp pesto", "1 cup mixed vegetables", "2 tbsp olive oil", "cherry tomatoes", "parmesan", "salt", "pepper"],
        "steps": [{"step": 1, "text": "Cook pasta.", "time": "10 min"}, {"step": 2, "text": "Sauté vegetables in olive oil.", "time": "6 min"}, {"step": 3, "text": "Stir in pesto and pasta water.", "time": "2 min"}, {"step": 4, "text": "Add pasta, tomatoes, salt, pepper.", "time": "3 min"}, {"step": 5, "text": "Top with parmesan.", "time": "1 min"}]
    },
    {
        "name": "Cheesy Baked Macaroni",
        "description": "Golden baked macaroni in cheddar cheese sauce.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "15 min",
        "cook_time": "25 min",
        "total_time": "40 min",
        "calories": 520,
        "servings": 3,
        "ingredients": ["250g macaroni", "2 tbsp butter", "2 tbsp flour", "2 cups milk", "1.5 cups cheddar", "breadcrumbs", "salt", "pepper", "paprika"],
        "steps": [{"step": 1, "text": "Boil macaroni.", "time": "8 min"}, {"step": 2, "text": "Make roux, whisk in milk.", "time": "8 min"}, {"step": 3, "text": "Add cheddar, salt, pepper.", "time": "4 min"}, {"step": 4, "text": "Mix pasta with sauce.", "time": "3 min"}, {"step": 5, "text": "Top with breadcrumbs and bake.", "time": "15 min"}, {"step": 6, "text": "Rest before serving.", "time": "3 min"}]
    },
    {
        "name": "Aglio e Olio",
        "description": "Minimalist pasta with garlic, olive oil, and parsley.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "5 min",
        "cook_time": "12 min",
        "total_time": "17 min",
        "calories": 310,
        "servings": 2,
        "ingredients": ["200g spaghetti", "6 garlic cloves", "1/4 cup olive oil", "1 tsp red chilli flakes", "parsley", "salt", "lemon zest"],
        "steps": [{"step": 1, "text": "Boil spaghetti.", "time": "9 min"}, {"step": 2, "text": "Slowly sauté garlic in olive oil until light gold.", "time": "4 min"}, {"step": 3, "text": "Add chilli flakes off heat.", "time": "1 min"}, {"step": 4, "text": "Toss pasta in oil with parsley and lemon zest.", "time": "2 min"}, {"step": 5, "text": "Serve immediately.", "time": "1 min"}]
    },
    {
        "name": "Pink Sauce Pasta",
        "description": "Creamy tomato-pink sauce pasta – mild and kid-friendly.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "10 min",
        "cook_time": "18 min",
        "total_time": "28 min",
        "calories": 430,
        "servings": 2,
        "ingredients": ["200g pasta", "1/2 cup tomato puree", "1/2 cup cream", "2 tbsp butter", "1 onion", "2 garlic cloves", "oregano", "salt", "pepper"],
        "steps": [{"step": 1, "text": "Boil pasta.", "time": "10 min"}, {"step": 2, "text": "Sauté onion and garlic in butter.", "time": "5 min"}, {"step": 3, "text": "Add tomato puree, cook 5 minutes.", "time": "5 min"}, {"step": 4, "text": "Stir in cream, oregano, salt, pepper.", "time": "4 min"}, {"step": 5, "text": "Toss pasta in pink sauce.", "time": "2 min"}]
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
        "ingredients": ["200g noodles", "2 cups mixed vegetables", "2 tbsp soy sauce", "1 tbsp vinegar", "1 tbsp chilli sauce", "2 tbsp oil", "garlic", "spring onion"],
        "steps": [{"step": 1, "text": "Boil noodles, rinse, toss with oil.", "time": "6 min"}, {"step": 2, "text": "Stir-fry garlic and vegetables.", "time": "4 min"}, {"step": 3, "text": "Add soy sauce, vinegar, chilli sauce.", "time": "1 min"}, {"step": 4, "text": "Add noodles and toss.", "time": "3 min"}, {"step": 5, "text": "Garnish with spring onion.", "time": "1 min"}]
    },
    {
        "name": "Schezwan Noodles",
        "description": "Fiery noodles tossed in schezwan sauce.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "10 min",
        "cook_time": "12 min",
        "total_time": "22 min",
        "calories": 420,
        "servings": 2,
        "ingredients": ["200g noodles", "3 tbsp schezwan sauce", "1 cup vegetables", "2 tbsp soy sauce", "1 tbsp oil", "garlic", "spring onion"],
        "steps": [{"step": 1, "text": "Boil and drain noodles.", "time": "6 min"}, {"step": 2, "text": "Sauté garlic and vegetables.", "time": "4 min"}, {"step": 3, "text": "Add schezwan sauce and soy sauce.", "time": "2 min"}, {"step": 4, "text": "Toss noodles on high flame.", "time": "3 min"}, {"step": 5, "text": "Garnish with spring onion.", "time": "1 min"}]
    },
    {
        "name": "Thai Peanut Noodles",
        "description": "Nutty, tangy noodles with peanut butter and lime.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "10 min",
        "cook_time": "8 min",
        "total_time": "18 min",
        "calories": 380,
        "servings": 2,
        "ingredients": ["200g noodles", "3 tbsp peanut butter", "1 tbsp soy sauce", "1 tbsp lime juice", "1 tsp honey", "vegetables", "crushed peanuts", "chilli flakes"],
        "steps": [{"step": 1, "text": "Whisk peanut butter, soy sauce, lime juice, honey.", "time": "3 min"}, {"step": 2, "text": "Boil noodles.", "time": "6 min"}, {"step": 3, "text": "Stir-fry vegetables briefly.", "time": "3 min"}, {"step": 4, "text": "Toss noodles, vegetables, and peanut sauce.", "time": "2 min"}, {"step": 5, "text": "Top with peanuts and chilli flakes.", "time": "1 min"}]
    },
    {
        "name": "Maggi Masala Noodles",
        "description": "Elevated instant noodles with extra veggies and tadka.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "5 min",
        "cook_time": "8 min",
        "total_time": "13 min",
        "calories": 350,
        "servings": 1,
        "ingredients": ["1 Maggi packet", "1/4 onion", "1/4 tomato", "1 green chilli", "1/2 tsp garam masala", "1 tsp butter", "coriander"],
        "steps": [{"step": 1, "text": "Sauté onion, tomato, chilli in butter.", "time": "3 min"}, {"step": 2, "text": "Add water and tastemaker, bring to boil.", "time": "2 min"}, {"step": 3, "text": "Add noodles and cook until water is absorbed.", "time": "3 min"}, {"step": 4, "text": "Sprinkle garam masala and coriander.", "time": "1 min"}]
    },
    {
        "name": "Garlic Butter Noodles",
        "description": "Simple buttery noodles with loads of garlic.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "5 min",
        "cook_time": "10 min",
        "total_time": "15 min",
        "calories": 360,
        "servings": 2,
        "ingredients": ["200g noodles", "4 tbsp butter", "6 garlic cloves", "parsley", "chilli flakes", "parmesan", "salt", "pepper"],
        "steps": [{"step": 1, "text": "Boil noodles.", "time": "7 min"}, {"step": 2, "text": "Melt butter and sauté garlic until golden.", "time": "3 min"}, {"step": 3, "text": "Toss noodles in garlic butter.", "time": "2 min"}, {"step": 4, "text": "Finish with parsley, chilli flakes, parmesan.", "time": "1 min"}]
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
        "ingredients": ["150g noodles", "3 cups vegetable broth", "1 cup spinach", "1 carrot", "1 tbsp soy sauce", "ginger", "garlic", "spring onion"],
        "steps": [{"step": 1, "text": "Sauté ginger and garlic.", "time": "2 min"}, {"step": 2, "text": "Add broth, soy sauce, carrot; simmer.", "time": "8 min"}, {"step": 3, "text": "Add noodles, cook until tender.", "time": "5 min"}, {"step": 4, "text": "Stir in spinach until wilted.", "time": "2 min"}, {"step": 5, "text": "Top with spring onion.", "time": "1 min"}]
    }
]

# Add RICE recipes (new)
rice_recipes = [
    {
        "name": "Veg Fried Rice",
        "description": "Classic Indo-Chinese fried rice with mixed vegetables.",
        "diet": "veg",
        "healthy": False,
        "prep_time": "10 min",
        "cook_time": "12 min",
        "total_time": "22 min",
        "calories": 380,
        "servings": 2,
        "ingredients": ["2 cups cooked rice", "1 cup mixed vegetables", "2 tbsp soy sauce", "1 tbsp vinegar", "2 tbsp oil", "garlic", "spring onion"],
        "steps": [{"step": 1, "text": "Cook rice and let it cool.", "time": "15 min"}, {"step": 2, "text": "Stir-fry garlic and vegetables.", "time": "4 min"}, {"step": 3, "text": "Add rice, soy sauce, vinegar, toss.", "time": "3 min"}, {"step": 4, "text": "Garnish with spring onion.", "time": "1 min"}]
    },
    {
        "name": "Lemon Rice",
        "description": "Tangy South Indian rice with lemon, peanuts, and curry leaves.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "5 min",
        "cook_time": "10 min",
        "total_time": "15 min",
        "calories": 290,
        "servings": 2,
        "ingredients": ["2 cups cooked rice", "2 tbsp lemon juice", "1 tsp mustard seeds", "1 tbsp peanuts", "curry leaves", "1/2 tsp turmeric", "2 tbsp oil", "salt"],
        "steps": [{"step": 1, "text": "Heat oil, splutter mustard seeds, add peanuts and curry leaves.", "time": "3 min"}, {"step": 2, "text": "Add turmeric and rice.", "time": "2 min"}, {"step": 3, "text": "Add lemon juice and salt, mix well.", "time": "3 min"}, {"step": 4, "text": "Serve hot with papad.", "time": "2 min"}]
    },
    {
        "name": "Tomato Rice",
        "description": "Flavorful rice cooked with tangy tomatoes and spices.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "8 min",
        "cook_time": "15 min",
        "total_time": "23 min",
        "calories": 310,
        "servings": 2,
        "ingredients": ["1 cup rice", "3 tomatoes", "1 onion", "1 tsp ginger-garlic paste", "1 tsp red chilli powder", "1/2 tsp garam masala", "2 tbsp oil", "salt"],
        "steps": [{"step": 1, "text": "Cook rice and keep aside.", "time": "12 min"}, {"step": 2, "text": "Sauté onion, add ginger-garlic paste.", "time": "3 min"}, {"step": 3, "text": "Add tomato puree and spices, cook until oil separates.", "time": "8 min"}, {"step": 4, "text": "Mix in rice and serve.", "time": "2 min"}]
    },
    {
        "name": "Curd Rice",
        "description": "Cooling yogurt rice with pomegranate and coriander.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "10 min",
        "cook_time": "0 min",
        "total_time": "10 min",
        "calories": 250,
        "servings": 2,
        "ingredients": ["2 cups cooked rice", "1 cup curd (yogurt)", "2 tbsp milk", "1 tsp mustard seeds", "1 tbsp pomegranate", "coriander", "salt"],
        "steps": [{"step": 1, "text": "Mash rice slightly and mix with curd, milk, salt.", "time": "3 min"}, {"step": 2, "text": "Temper mustard seeds and pour over rice.", "time": "2 min"}, {"step": 3, "text": "Garnish with pomegranate and coriander.", "time": "2 min"}, {"step": 4, "text": "Serve chilled or at room temperature.", "time": "1 min"}]
    },
    {
        "name": "Jeera Rice",
        "description": "Simple aromatic rice with cumin seeds and ghee.",
        "diet": "veg",
        "healthy": True,
        "prep_time": "3 min",
        "cook_time": "12 min",
        "total_time": "15 min",
        "calories": 280,
        "servings": 2,
        "ingredients": ["1 cup rice", "2 tbsp ghee", "1 tsp cumin seeds", "2 cups water", "salt"],
        "steps": [{"step": 1, "text": "Wash and soak rice for 15 minutes.", "time": "15 min"}, {"step": 2, "text": "Heat ghee, add cumin seeds until they splutter.", "time": "2 min"}, {"step": 3, "text": "Add rice and water, salt, cook until done.", "time": "12 min"}, {"step": 4, "text": "Fluff and serve with dal or raita.", "time": "2 min"}]
    },
    {
        "name": "Egg Fried Rice",
        "description": "Quick egg fried rice with soy sauce and pepper.",
        "diet": "non-veg",
        "healthy": False,
        "prep_time": "8 min",
        "cook_time": "10 min",
        "total_time": "18 min",
        "calories": 410,
        "servings": 2,
        "ingredients": ["2 cups cooked rice", "2 eggs", "1/2 cup mixed vegetables", "2 tbsp soy sauce", "2 tbsp oil", "1/2 tsp pepper", "salt", "spring onion"],
        "steps": [{"step": 1, "text": "Scramble eggs and set aside.", "time": "3 min"}, {"step": 2, "text": "Stir-fry vegetables.", "time": "3 min"}, {"step": 3, "text": "Add rice, soy sauce, pepper, salt.", "time": "3 min"}, {"step": 4, "text": "Add scrambled eggs and mix.", "time": "2 min"}, {"step": 5, "text": "Garnish with spring onion.", "time": "1 min"}]
    }
]

# ----------------------------------------------------------------------
# INGREDIENT MAPPING (including rice)
# ----------------------------------------------------------------------
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
    "maggi": noodle_recipes,
    "rice": rice_recipes,
    "chawal": rice_recipes
}

# ----------------------------------------------------------------------
# GENERATE RECIPES FUNCTION (FIXED FILTERING)
# ----------------------------------------------------------------------
def generate_recipes(item, diet_filter=None, healthy_filter=None):
    item = item.lower().strip()
    recipes = None

    # Look for ingredient in map
    for key in ingredient_map:
        if key in item:
            bank = ingredient_map[key][:]  # copy list
            random.shuffle(bank)
            recipes = bank[:6]
            break

    # If not found, create generic recipes
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
                "steps": [{"step": 1, "text": f"Chop {item} and sauté with onions.", "time": "6 min"}, {"step": 2, "text": "Add tomatoes and spices.", "time": "8 min"}, {"step": 3, "text": f"Add {item} and water, simmer.", "time": "12 min"}, {"step": 4, "text": "Serve hot with rice or roti.", "time": "1 min"}]
            },
            {
                "name": f"Spicy {item.title()} Fry",
                "description": f"Crispy pan-fried {item} with bold spices.",
                "diet": "veg",
                "healthy": False,
                "prep_time": "8 min",
                "cook_time": "12 min",
                "total_time": "20 min",
                "calories": 310,
                "servings": 2,
                "ingredients": [f"2 cups {item}", "1 tsp chilli powder", "1/2 tsp turmeric", "lemon", "oil", "salt"],
                "steps": [{"step": 1, "text": f"Cut {item} into pieces.", "time": "5 min"}, {"step": 2, "text": "Toss with spices and salt.", "time": "2 min"}, {"step": 3, "text": "Shallow fry until crispy.", "time": "10 min"}, {"step": 4, "text": "Squeeze lemon and serve.", "time": "1 min"}]
            },
            {
                "name": f"{item.title()} Salad",
                "description": f"Fresh, light salad with grilled {item}.",
                "diet": "veg",
                "healthy": True,
                "prep_time": "10 min",
                "cook_time": "5 min",
                "total_time": "15 min",
                "calories": 180,
                "servings": 2,
                "ingredients": [f"1 cup {item}", "lettuce", "cucumber", "olive oil", "lemon", "pepper"],
                "steps": [{"step": 1, "text": f"Grill or roast {item}.", "time": "5 min"}, {"step": 2, "text": "Toss with greens and dressing.", "time": "4 min"}, {"step": 3, "text": "Season and serve.", "time": "2 min"}]
            }
        ]
        random.shuffle(generic)
        recipes = generic[:3]  # give at least 3 generic recipes

    # Apply filters (only if not 'all')
    if diet_filter in ("veg", "non-veg"):
        recipes = [r for r in recipes if r.get("diet") == diet_filter]

    if healthy_filter == "healthy":
        recipes = [r for r in recipes if r.get("healthy") is True]
    elif healthy_filter == "unhealthy":
        recipes = [r for r in recipes if r.get("healthy") is False]

    # Return at most 6 recipes, or empty list if none left
    return recipes[:6]

# ----------------------------------------------------------------------
# FLASK ROUTES
# ----------------------------------------------------------------------
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)