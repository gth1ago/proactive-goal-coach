import pytest
from fastapi.testclient import TestClient

class TestGoalsAPI:
    """Testes de integração para API de objetivos"""
    
    def test_get_goals_empty_list(self, client, clean_db):
        """Testa listagem de objetivos quando não há dados"""
        # Limpa dados mock
        from mock_data import goals_db
        goals_db.clear()
        
        response = client.get("/api/goals/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_goals_with_data(self, client, clean_db):
        """Testa listagem de objetivos com dados mock"""
        response = client.get("/api/goals/")
        assert response.status_code == 200
        
        goals = response.json()
        assert len(goals) >= 2  # Dados mock têm pelo menos 2 objetivos
        
        # Verifica estrutura do primeiro objetivo
        goal = goals[0]
        assert "id" in goal
        assert "title" in goal
        assert "description" in goal
        assert "progress" in goal
        assert "micro_goals" in goal
        assert isinstance(goal["micro_goals"], list)
    
    def test_get_goal_by_id_success(self, client, clean_db):
        """Testa busca de objetivo por ID existente"""
        # Primeiro pega lista para ter um ID válido
        response = client.get("/api/goals/")
        goals = response.json()
        
        if goals:
            goal_id = goals[0]["id"]
            response = client.get(f"/api/goals/{goal_id}")
            assert response.status_code == 200
            
            goal = response.json()
            assert goal["id"] == goal_id
    
    def test_get_goal_by_id_not_found(self, client, clean_db):
        """Testa busca de objetivo por ID inexistente"""
        response = client.get("/api/goals/invalid_id")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]
    
    def test_create_goal_success(self, client, clean_db, sample_goal_data):
        """Testa criação de objetivo com sucesso"""
        response = client.post("/api/goals/", json=sample_goal_data)
        assert response.status_code == 200
        
        goal = response.json()
        assert goal["title"] == sample_goal_data["title"]
        assert goal["description"] == sample_goal_data["description"]
        assert goal["progress"] == 0.0
        assert len(goal["micro_goals"]) > 0  # IA deve gerar micro-metas
        
        # Verifica se micro-metas foram geradas corretamente
        micro_goals = goal["micro_goals"]
        assert all(mg["goal_id"] == goal["id"] for mg in micro_goals)
        assert all(mg["status"] == "pending" for mg in micro_goals)
    
    def test_create_goal_with_tags(self, client, clean_db):
        """Testa criação de objetivo com tags"""
        goal_data = {
            "title": "Objetivo com Tags",
            "description": "Teste de tags",
            "tags": ["tag1", "tag2", "tag3"]
        }
        
        response = client.post("/api/goals/", json=goal_data)
        assert response.status_code == 200
        
        goal = response.json()
        assert set(goal["tags"]) == set(goal_data["tags"])
    
    def test_complete_micro_goal_success(self, client, clean_db):
        """Testa conclusão de micro-meta"""
        # Primeiro cria um objetivo
        goal_data = {
            "title": "Teste Conclusão",
            "description": "Para testar conclusão de micro-meta"
        }
        
        response = client.post("/api/goals/", json=goal_data)
        goal = response.json()
        goal_id = goal["id"]
        micro_goal_id = goal["micro_goals"][0]["id"]
        
        # Completa a micro-meta
        response = client.put(f"/api/goals/{goal_id}/micro-goals/{micro_goal_id}/complete")
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "progress" in result
        assert result["progress"] > 0
    
    def test_complete_micro_goal_invalid_goal(self, client, clean_db):
        """Testa conclusão de micro-meta com objetivo inválido"""
        response = client.put("/api/goals/invalid_goal/micro-goals/invalid_micro/complete")
        assert response.status_code == 404
        assert "Objetivo não encontrado" in response.json()["detail"]
    
    def test_complete_micro_goal_invalid_micro_goal(self, client, clean_db):
        """Testa conclusão de micro-meta inválida"""
        # Pega um objetivo válido
        response = client.get("/api/goals/")
        goals = response.json()
        
        if goals:
            goal_id = goals[0]["id"]
            response = client.put(f"/api/goals/{goal_id}/micro-goals/invalid_micro/complete")
            assert response.status_code == 404
            assert "Micro-meta não encontrada" in response.json()["detail"]