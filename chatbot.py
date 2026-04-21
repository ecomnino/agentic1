import os
import json
import time
from typing import Optional, Dict, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIAgent:
    def __init__(self, role: str, instruction: str, model: str = "gpt-4o-mini"):
        self.api_key = os.getenv("api_key")
        if not self.api_key:
            raise ValueError("Geen API-sleutel gevonden. Controleer je .env bestand.")
        self.client = OpenAI(api_key=self.api_key)
        self.role = role
        self.instruction = instruction
        self.model = model

    def _call_api(self, messages: List[Dict[str, str]]) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if "rate_limit" in str(e).lower():
                print(f"[{self.role}] Rate limit bereikt. 60s pauze...")
                time.sleep(60)
                return self._call_api(messages)
            print(f"[{self.role}] Fout: {e}")
            return None

    def ask(self, prompt: str, context: Optional[str] = None) -> Optional[str]:
        messages = [{"role": "system", "content": self.instruction}]
        content = f"CONTEXT VAN COLLEGA:\n{context}\n\nOPDRACHT:\n{prompt}" if context else prompt
        messages.append({"role": "user", "content": content})
        return self._call_api(messages)


class PlannerAgent(AIAgent):
    """Beslist welke agenten nodig zijn op basis van de gebruikersvraag."""
    def __init__(self):
        instruction = (
            "Je bent een technisch projectplanner. "
            "Gegeven een gebruikersvraag, besluit je welke agenten nodig zijn. "
            "Beschikbare agenten: 'data_engineer', 'frontend'. "
            "Regels:\n"
            "- Gebruik 'data_engineer' als er data-verwerking, SQL, transformaties of logica nodig is.\n"
            "- Gebruik 'frontend' als er een UI, dashboard of visualisatie gevraagd wordt.\n"
            "- Je mag beide kiezen als de vraag een volledige app vereist.\n"
            "- Je mag ook slechts één kiezen als de vraag dat toelaat.\n"
            "Antwoord ALLEEN met een JSON-array, bijvoorbeeld: [\"data_engineer\", \"frontend\"] "
            "of [\"data_engineer\"] of [\"frontend\"]. Geen uitleg, geen markdown."
        )
        super().__init__(role="Planner", instruction=instruction)

    def plan(self, user_request: str) -> List[str]:
        result = self.ask(user_request)
        try:
            agents = json.loads(result)
            valid = {"data_engineer", "frontend"}
            agents = [a for a in agents if a in valid]
            if not agents:
                raise ValueError("Geen geldige agenten in plan.")
            return agents
        except Exception as e:
            print(f"[Planner] Fout bij parsen van plan: {e}. Fallback naar beide agenten.")
            return ["data_engineer", "frontend"]


class DataEngineerAgent(AIAgent):
    def __init__(self):
        super().__init__(
            role="Data Engineer",
            instruction=(
                "Je bent een Senior Data Engineer. Je ontwerpt robuuste data-pipelines, "
                "SQL queries en Python (Pandas/Polars) transformaties. "
                "Lever altijd schone, gedocumenteerde code aan."
            )
        )


class FrontendAgent(AIAgent):
    def __init__(self):
        super().__init__(
            role="Frontend Developer",
            instruction=(
                "Je bent een Senior Frontend Ontwikkelaar gespecialiseerd in Streamlit. "
                "Je bouwt interactieve dashboards. Focus op UI/UX, Plotly grafieken "
                "en gebruiksvriendelijkheid."
            )
        )


class ProjectManager:
    """Orchestrator die dynamisch agenten inzet op basis van het plan."""

    AGENT_MAP = {
        "data_engineer": DataEngineerAgent,
        "frontend": FrontendAgent,
    }

    def __init__(self):
        self.planner = PlannerAgent()
        self._agents: Dict[str, AIAgent] = {}

    def _get_agent(self, name: str) -> AIAgent:
        """Lazy-initialiseert agenten zodat we ze alleen aanmaken als nodig."""
        if name not in self._agents:
            self._agents[name] = self.AGENT_MAP[name]()
        return self._agents[name]

    def create_data_app(self, user_request: str) -> str:
        print(f"\n--- Nieuwe opdracht: {user_request} ---")

        # Stap 1: bepaal het plan
        plan = self.planner.plan(user_request)
        print(f"[Planner] Gekozen agenten: {plan}")

        context = None
        result = None

        # Stap 2: voer de agenten sequentieel uit in de geplande volgorde
        for agent_name in plan:
            agent = self._get_agent(agent_name)
            print(f"\n[{agent.role}] Bezig...")

            if agent_name == "data_engineer":
                result = agent.ask(
                    prompt=f"Schrijf de Python-logica voor: {user_request}. "
                           f"Zorg voor een duidelijke functie die de data verwerkt.",
                )
                context = result

            elif agent_name == "frontend":
                prompt = (
                    "Bouw een volledige Streamlit app die gebruikmaakt van de aangeleverde data-logica. "
                    "Zorg voor een sidebar, titels en visuele grafieken."
                    if context else
                    f"Bouw een Streamlit dashboard voor: {user_request}. "
                    f"Geen externe data-logica beschikbaar; genereer zelf voorbeelddata."
                )
                result = agent.ask(prompt=prompt, context=context)

        print("\n--- Klaar ---")
        return result or "Geen output gegenereerd."


def main():
    orchestrator = ProjectManager()
    print("AI Data Team klaar (typ 'exit' om te stoppen)")
    while True:
        vraag = input("\nWat wil je laten bouwen? ").strip()
        if vraag.lower() == "exit":
            break
        if not vraag:
            continue
        resultaat = orchestrator.create_data_app(vraag)
        with open("generated_app.py", "w", encoding="utf-8") as f:
            f.write(resultaat)

        print("\nResultaat opgeslagen in 'generated_app.py'.")


if __name__ == "__main__":
    main()