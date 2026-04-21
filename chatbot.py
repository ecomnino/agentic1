import os
import time
from typing import Optional, Dict, List
from openai import OpenAI
from dotenv import load_dotenv

# Laden van omgevingsvariabelen
load_dotenv()

class AIAgent:
    """
    Abstracte basisklasse voor AI-agenten. 
    Verantwoordelijk voor de communicatie met de OpenAI API.
    """
    def __init__(self, role: str, instruction: str, model: str = "gpt-4o-mini"):
        self.api_key = os.getenv("api_key")
        if not self.api_key:
            raise ValueError("Geen API-sleutel gevonden. Controleer je .env bestand.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.role = role
        self.instruction = instruction
        self.model = model

    def _call_api(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Interne methode voor API-afhandeling met retry-logica."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2, # Lage temperatuur voor technische accuratesse
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit" in str(e).lower():
                print(f"[{self.role}] Rate limit bereikt. 60s pauze...")
                time.sleep(60)
                return self._call_api(messages)
            print(f"[{self.role}] Fout opgetreden: {e}")
            return None

    def ask(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        """Verwerkt een prompt, eventueel verrijkt met context van een andere agent."""
        messages = [{"role": "system", "content": self.instruction}]
        
        content = prompt
        if context:
            content = f"CONTEXT VAN COLLEGA:\n{context}\n\nOPDRACHT:\n{prompt}"
            
        messages.append({"role": "user", "content": content})
        return self._call_api(messages)


class DataEngineerAgent(AIAgent):
    """Gespecialiseerde agent voor data engineering taken."""
    def __init__(self):
        instruction = (
            "Je bent een Senior Data Engineer. Je taak is het ontwerpen van robuuste "
            "data-pipelines, SQL queries en Python (Pandas/Polars) transformaties. "
            "Lever altijd schone, gedocumenteerde code aan."
        )
        super().__init__(role="Data Engineer", instruction=instruction)


class FrontendAgent(AIAgent):
    """Gespecialiseerde agent voor Streamlit UI-ontwikkeling."""
    def __init__(self):
        instruction = (
            "Je bent een Senior Frontend Ontwikkelaar gespecialiseerd in Streamlit. "
            "Je bouwt interactieve dashboards gebaseerd op data-logica van je collega's. "
            "Focus op UI/UX, Plotly grafieken en gebruiksvriendelijkheid."
        )
        super().__init__(role="Frontend Developer", instruction=instruction)


class ProjectManager:
    """
    De Orchestrator. Beheert de workflow tussen de verschillende agenten.
    """
    def __init__(self):
        self.engineer = DataEngineerAgent()
        self.frontend = FrontendAgent()

    def create_data_app(self, user_request: str) -> str:
        """Beheert de sequentiële workflow voor het maken van een app."""
        print(f"\n--- 🚀 Start Project: {user_request} ---")

        # Stap 1: Data Engineering Fase
        print("\n[Fase 1] Data Engineer ontwerpt de logica...")
        data_logic = self.engineer.ask(
            prompt=f"Schrijf de Python-logica voor de volgende data-vraag: {user_request}. "
                   f"Zorg dat er een duidelijke functie is die de data verwerkt."
        )

        if not data_logic:
            return "Project gestopt: Data Engineer kon geen logica genereren."

        # Stap 2: Frontend Fase
        print("[Fase 2] Frontend Developer bouwt het Streamlit dashboard...")
        final_app_code = self.frontend.ask(
            prompt="Bouw een volledige Streamlit app die gebruikmaakt van de aangeleverde data-logica. "
                   "Zorg voor een sidebar, titels en visuele grafieken.",
            context=data_logic
        )

        if not final_app_code:
            return "Project gestopt: Frontend Developer kon geen code genereren."

        print("\n--- ✅ Project Succesvol Afgerond ---")
        return final_app_code


# --- Main Execution Loop ---
def main():
    orchestrator = ProjectManager()
    
    print("AI Data Team Ready (typ 'exit' om te stoppen)")
    while True:
        vraag = input("\nWat wil je laten bouwen? ").strip()
        
        if vraag.lower() == 'exit':
            break
            
        if not vraag:
            continue

        resultaat = orchestrator.create_data_app(vraag)
        
        # Opslaan van de resultaten voor inspectie
        with open("generated_app.py", "w", encoding="utf-8") as f:
            f.write(resultaat)
        
        print("\nDe volledige code is opgeslagen in 'generated_app.py'.")

if __name__ == "__main__":
    main()