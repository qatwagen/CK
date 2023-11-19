from flask import Flask, render_template, request

import openai


openai.api_key = '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'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate_recommendations', methods=['POST'])
def generate_recommendations():
    cuisine = request.form['cuisine']
    items = request.form['items'].split(',')
    prompt = f"I want recipe with the given food iten only and step-by-step procedure to make a dish from {cuisine} cuisine using the following items:"
    for item in items:
        prompt += f"\n- {item}"

    prompt += "\nIdentify the food items and Please include the recipe and step-by-step instructions with the given food items only for making tasty and easy dish. Show the procedure in a clear and understandable format. If no food item name found return message please enter food item name"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500  
    )

    generated_text = response.choices[0].text.strip()
    recommended_dishes = [dish.strip() for dish in generated_text.split('\n')]

    return render_template('home.html', recommended_dishes=recommended_dishes)


@app.route('/gen')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_recipe():
    dish_name = request.form['dish_name']

    recipe = generate_recipe_with_openai(dish_name)

    ingredients = recipe.get('ingredients', [])
    steps = recipe.get('steps', [])

    return render_template('recipe.html', dish_name=dish_name, ingredients=ingredients, steps=steps)

def generate_recipe_with_openai(dish_name):
    prompt = f"Generate a recipe for {dish_name}."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )

    recipe_text = response['choices'][0]['text'].strip()

    parts = recipe_text.split('Instructions:')
    
    if len(parts) > 1:
        ingredients = parts[0].split('\n')
        steps = parts[1].split('\n')
    else:
        ingredients = parts[0].split('\n')
        steps = []

    return {'ingredients': ingredients, 'steps': steps}

if __name__ == '__main__':
    app.run(debug=True)
