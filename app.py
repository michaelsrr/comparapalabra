from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Oraciones correctas
sentences = [
    "es un gusto tenerlo en crea",
    "exactamente qué tipo de producto está buscando",
    "con qué tipo de producto en diseño se identifica normalmente"
]

# Estado inicial del juego
user_progress = {
    "current_sentence": 0,  # Índice de la oración actual
    "correct_count": 0,     # Contador de oraciones correctas
    "total_attempts": 0     # Contador de intentos totales
}

@app.route('/', methods=['GET', 'POST'])
def index():
    global user_progress
    
    if request.method == 'POST':
        user_input = request.form['sentence_input'].lower().strip()
        correct_sentence = sentences[user_progress['current_sentence']]
        
        # Incrementar el número de intentos
        user_progress['total_attempts'] += 1

        if user_input == correct_sentence:
            # Si la oración es correcta, pasar a la siguiente
            user_progress['correct_count'] += 1
            user_progress['current_sentence'] += 1
            
            # Si ya completó todas las oraciones
            if user_progress['current_sentence'] >= len(sentences):
                return redirect(url_for('results'))
        else:
            # Si es incorrecto, no avanzar y mostrar un mensaje de error
            error = "La oración es incorrecta, por favor intente de nuevo."
            return render_template('index.html', sentence=correct_sentence, error=error)

    # Mostrar la oración actual
    sentence = sentences[user_progress['current_sentence']]
    return render_template('index.html', sentence=sentence)

@app.route('/results')
def results():
    global user_progress
    
    # Calcular el porcentaje de aciertos
    percentage = (user_progress['correct_count'] / user_progress['total_attempts']) * 100

    # Mostrar resultados y resetear el progreso
    result = {
        "correct_count": user_progress['correct_count'],
        "total_attempts": user_progress['total_attempts'],
        "percentage": percentage
    }
    
    # Resetear el progreso
    user_progress['current_sentence'] = 0
    user_progress['correct_count'] = 0
    user_progress['total_attempts'] = 0

    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
