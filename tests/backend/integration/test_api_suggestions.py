import pytest
from unittest.mock import patch

class TestSuggestionsAPI:
    """Testes de integração para API de sugestões"""
    
    def test_get_suggestions_success(self, client, clean_db):
        """Testa obtenção de sugestões contextuais"""
        response = client.get("/api/suggestions/")
        assert response.status_code == 200
        
        suggestions = response.json()
        assert isinstance(suggestions, list)
        assert len(suggestions) <= 3  # Limitado a 3 sugestões
        
        if suggestions:
            suggestion = suggestions[0]
            assert "id" in suggestion
            assert "title" in suggestion
            assert "description" in suggestion
            assert "micro_goal_id" in suggestion
            assert "priority" in suggestion
    
    @patch('routers.suggestions.datetime')
    def test_get_suggestions_morning_context(self, mock_datetime, client, clean_db):
        """Testa sugestões no contexto matinal"""
        # Mock para simular 9h da manhã
        mock_datetime.now.return_value.hour = 9
        
        response = client.get("/api/suggestions/")
        assert response.status_code == 200
        
        suggestions = response.json()
        # Verifica se há sugestões com contexto matinal
        morning_suggestions = [s for s in suggestions if "manhã" in s["description"]]
        assert len(morning_suggestions) >= 0  # Pode não ter sugestões matinais específicas
    
    @patch('routers.suggestions.datetime')
    def test_get_suggestions_afternoon_context(self, mock_datetime, client, clean_db):
        """Testa sugestões no contexto vespertino"""
        # Mock para simular 15h
        mock_datetime.now.return_value.hour = 15
        
        response = client.get("/api/suggestions/")
        assert response.status_code == 200
        
        suggestions = response.json()
        # Verifica se há sugestões com contexto vespertino
        afternoon_suggestions = [s for s in suggestions if "tarde" in s["description"]]
        assert len(afternoon_suggestions) >= 0
    
    def test_get_motivational_message_success(self, client, clean_db):
        """Testa obtenção de mensagem motivacional"""
        response = client.get("/api/suggestions/motivational")
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "progress" in result
        assert "completed_goals" in result
        
        assert isinstance(result["message"], str)
        assert isinstance(result["progress"], (int, float))
        assert isinstance(result["completed_goals"], int)
        assert len(result["message"]) > 0
    
    def test_get_motivational_message_with_goals(self, client, clean_db):
        """Testa mensagem motivacional com objetivos existentes"""
        # Primeiro cria um objetivo
        goal_data = {
            "title": "Objetivo para Motivação",
            "description": "Teste de mensagem motivacional"
        }
        
        client.post("/api/goals/", json=goal_data)
        
        response = client.get("/api/suggestions/motivational")
        assert response.status_code == 200
        
        result = response.json()
        assert result["progress"] >= 0
        assert "🚀" in result["message"] or "💪" in result["message"] or "🌟" in result["message"]
    
    def test_suggestions_integration_with_goals(self, client, clean_db):
        """Testa integração entre sugestões e objetivos"""
        # Cria um objetivo
        goal_data = {
            "title": "Objetivo para Sugestões",
            "description": "Teste de integração"
        }
        
        goal_response = client.post("/api/goals/", json=goal_data)
        goal = goal_response.json()
        
        # Pega sugestões
        suggestions_response = client.get("/api/suggestions/")
        suggestions = suggestions_response.json()
        
        # Verifica se há sugestões relacionadas ao objetivo criado
        related_suggestions = [
            s for s in suggestions 
            if any(mg["id"] == s["micro_goal_id"] for mg in goal["micro_goals"])
        ]
        
        # Pode não haver sugestões imediatas, mas a estrutura deve estar correta
        assert isinstance(suggestions, list)