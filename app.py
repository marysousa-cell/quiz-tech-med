"""
Tech & Med Quiz - Aplicação Web com Flask
==========================================
API backend para o quiz interativo
"""

from flask import Flask, render_template, request, jsonify
from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@dataclass
class Question:
    """Representa uma pergunta do quiz."""
    id: int
    category: str
    prompt: str
    options: List[str]
    answer: str


def get_questions() -> List[Question]:
    """Retorna o banco de dados de perguntas."""
    return [
        Question(
            id=1,
            category="Tecnologia",
            prompt="Qual linguagem de programação é a principal escolha para inteligência artificial e ciência de dados?",
            options=["Java", "C++", "Python", "PHP"],
            answer="Python"
        ),
        Question(
            id=2,
            category="Tecnologia",
            prompt="O que significa a sigla 'HTTP' no contexto da web?",
            options=[
                "HyperText Transfer Protocol",
                "High Technical Transfer Process",
                "Hyperlink Text Tools Program",
                "Hard Traffic Thread Protocol"
            ],
            answer="HyperText Transfer Protocol"
        ),
        Question(
            id=3,
            category="Tecnologia",
            prompt="Qual é o propósito principal de um banco de dados?",
            options=[
                "Armazenar e recuperar dados de forma eficiente",
                "Compilar código em linguagem de máquina",
                "Criar interfaces gráficas",
                "Gerenciar sistemas operacionais"
            ],
            answer="Armazenar e recuperar dados de forma eficiente"
        ),
        Question(
            id=4,
            category="Medicina",
            prompt="Qual órgão do corpo humano é o principal responsável por filtrar o sangue e produzir a urina?",
            options=["Fígado", "Rins", "Pâncreas", "Pulmão"],
            answer="Rins"
        ),
        Question(
            id=5,
            category="Medicina",
            prompt="Como é chamada a pressão arterial quando os valores medidos estão consistentemente elevados?",
            options=["Arritmia", "Hipoglicemia", "Hipertensão", "Anemia"],
            answer="Hipertensão"
        ),
        Question(
            id=6,
            category="Medicina",
            prompt="Qual é a função principal do sistema imunológico?",
            options=[
                "Transportar oxigênio pelo corpo",
                "Defender o corpo contra infecções e doenças",
                "Digerir alimentos",
                "Controlar a temperatura corporal"
            ],
            answer="Defender o corpo contra infecções e doenças"
        ),
        Question(
            id=7,
            category="Tecnologia & Medicina",
            prompt="Qual tecnologia permite a realização de cirurgias de alta precisão operadas remotamente por médicos?",
            options=[
                "Impressão 3D de órgãos",
                "Cirurgia Robótica",
                "Sequenciamento Genético",
                "Eletrocardiograma Digital"
            ],
            answer="Cirurgia Robótica"
        ),
        Question(
            id=8,
            category="Tecnologia & Medicina",
            prompt="O que é telemedicina?",
            options=[
                "Cirurgia tradicional em hospital",
                "Prestação de serviços de saúde à distância usando tecnologia",
                "Medicamentos eletrônicos",
                "Máquinas de ressonância magnética"
            ],
            answer="Prestação de serviços de saúde à distância usando tecnologia"
        ),
    ]


@app.route('/')
def index():
    """Página inicial do quiz."""
    return render_template('index.html')


@app.route('/api/questions')
def get_all_questions():
    """API que retorna todas as perguntas."""
    questions = get_questions()
    return jsonify([asdict(q) for q in questions])


@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    """API que verifica se a resposta está correta."""
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    questions = {q.id: q for q in get_questions()}
    question = questions.get(question_id)
    
    if not question:
        return jsonify({'error': 'Pergunta não encontrada'}), 404
    
    is_correct = user_answer.strip().lower() == question.answer.strip().lower()
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question.answer
    })


@app.route('/api/save-result', methods=['POST'])
def save_result():
    """API que salva o resultado do quiz."""
    data = request.json
    
    results_file = Path('quiz_results.json')
    result = {
        'timestamp': datetime.now().isoformat(),
        'score': data.get('score'),
        'total': data.get('total'),
        'percentage': round((data.get('score') / data.get('total')) * 100, 1)
    }
    
    all_results = []
    if results_file.exists():
        with open(results_file, 'r') as f:
            all_results = json.load(f)
    
    all_results.append(result)
    
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    return jsonify({'success': True, 'result': result})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
