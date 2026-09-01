"""
Tech & Med Quiz CLI App - Engine
=================================
Um programa de terminal interativo sobre Tecnologia e Medicina
com integração GitHub e estilo Copilot.
"""

from dataclasses import dataclass
from typing import List
import time
import json
from pathlib import Path


@dataclass
class Question:
    """Representa uma pergunta do quiz."""
    category: str
    prompt: str
    options: List[str]
    answer: str

    def is_correct(self, user_answer: str) -> bool:
        """Valida se a resposta do usuário está correta."""
        return user_answer.strip().upper() == self.answer.upper()


class QuizEngine:
    """Motor principal do quiz com sistema de pontuação e histórico."""
    
    def __init__(self, questions: List[Question]):
        self.questions = questions
        self.score = 0
        self.results_file = Path("quiz_results.json")

    def run(self) -> None:
        """Inicia a execução do quiz no terminal."""
        total = len(self.questions)
        self.score = 0

        self._print_header()

        for idx, q in enumerate(self.questions, start=1):
            self._display_question(idx, total, q)
            user_input = self._get_valid_input()

            if q.is_correct(user_input):
                print("✨ Resposta correta!\n")
                self.score += 1
            else:
                print(f"❌ Incorreto! A resposta certa era: **{q.answer}**\n")
            
            time.sleep(0.8)

        self._print_results(total)
        self._save_results(total)

    def _print_header(self) -> None:
        """Exibe o cabeçalho do quiz."""
        print("\n" + "=" * 60)
        print(" 🏥 💻 QUIZ INTERATIVO: TECNOLOGIA & MEDICINA")
        print("=" * 60)
        print("📝 Responda digitando apenas a letra (A, B, C ou D).\n")
        time.sleep(1)

    def _display_question(self, current: int, total: int, question: Question) -> None:
        """Exibe uma pergunta formatada."""
        print(f"--- Pergunta {current}/{total} [{question.category}] ---")
        print(f"{question.prompt}\n")
        for option in question.options:
            print(f"  {option}")
        print()

    def _get_valid_input(self) -> str:
        """Obtém uma entrada válida do usuário."""
        valid_choices = {"A", "B", "C", "D"}
        while True:
            choice = input("Sua resposta (A/B/C/D): ").strip().upper()
            if choice in valid_choices:
                return choice
            print("⚠️ Opção inválida! Por favor, escolha A, B, C ou D.")

    def _print_results(self, total: int) -> None:
        """Exibe os resultados finais."""
        percentage = (self.score / total) * 100
        print("=" * 60)
        print("📊 RESULTADO FINAL")
        print(f"Pontuação: {self.score} de {total} ({percentage:.1f}%)")
        
        if percentage == 100:
            print("🏆 Excelente! Desempenho perfeito!")
        elif percentage >= 80:
            print("⭐ Muito bem! Excelente nível de conhecimento.")
        elif percentage >= 60:
            print("👍 Bom! Você tem um bom conhecimento.")
        else:
            print("📚 Vale a pena revisar alguns conceitos e tentar novamente!")
        print("=" * 60 + "\n")

    def _save_results(self, total: int) -> None:
        """Salva os resultados em um arquivo JSON."""
        import datetime
        
        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "score": self.score,
            "total": total,
            "percentage": round((self.score / total) * 100, 1)
        }
        
        all_results = []
        if self.results_file.exists():
            with open(self.results_file, 'r') as f:
                all_results = json.load(f)
        
        all_results.append(results)
        
        with open(self.results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"💾 Resultado salvo em: {self.results_file}")
