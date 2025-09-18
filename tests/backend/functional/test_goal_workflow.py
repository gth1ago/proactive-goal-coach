import pytest

class TestGoalWorkflow:
    """Testes funcionais para fluxo completo de objetivos"""
    
    def test_complete_goal_creation_workflow(self, client, clean_db):
        """Testa fluxo completo: criar objetivo → completar micro-metas → atingir 100%"""
        
        # 1. Criar objetivo
        goal_data = {
            "title": "Aprender FastAPI",
            "description": "Dominar desenvolvimento de APIs com FastAPI",
            "tags": ["programação", "api", "python"]
        }
        
        response = client.post("/api/goals/", json=goal_data)
        assert response.status_code == 200
        
        goal = response.json()
        goal_id = goal["id"]
        initial_progress = goal["progress"]
        micro_goals = goal["micro_goals"]
        
        assert initial_progress == 0.0
        assert len(micro_goals) > 0
        
        # 2. Completar primeira micro-meta
        first_micro_id = micro_goals[0]["id"]
        response = client.put(f"/api/goals/{goal_id}/micro-goals/{first_micro_id}/complete")
        assert response.status_code == 200
        
        result = response.json()
        first_progress = result["progress"]
        assert first_progress > initial_progress
        
        # 3. Verificar atualização do objetivo
        response = client.get(f"/api/goals/{goal_id}")
        updated_goal = response.json()
        assert updated_goal["progress"] == first_progress
        
        # Verifica se micro-meta foi marcada como completa
        completed_micro = next(mg for mg in updated_goal["micro_goals"] if mg["id"] == first_micro_id)
        assert completed_micro["status"] == "completed"
        assert completed_micro["completed_at"] is not None
        
        # 4. Completar todas as micro-metas restantes
        remaining_micros = [mg for mg in updated_goal["micro_goals"] if mg["status"] == "pending"]
        
        for micro_goal in remaining_micros:
            response = client.put(f"/api/goals/{goal_id}/micro-goals/{micro_goal['id']}/complete")
            assert response.status_code == 200
        
        # 5. Verificar objetivo 100% completo
        response = client.get(f"/api/goals/{goal_id}")
        final_goal = response.json()
        assert final_goal["progress"] == 100.0
        
        # Todas micro-metas devem estar completas
        all_completed = all(mg["status"] == "completed" for mg in final_goal["micro_goals"])
        assert all_completed
    
    def test_goal_progress_calculation(self, client, clean_db):
        """Testa cálculo correto do progresso baseado em micro-metas"""
        
        # Criar objetivo
        goal_data = {
            "title": "Teste Progresso",
            "description": "Para testar cálculo de progresso"
        }
        
        response = client.post("/api/goals/", json=goal_data)
        goal = response.json()
        goal_id = goal["id"]
        total_micros = len(goal["micro_goals"])
        
        # Completar metade das micro-metas
        micros_to_complete = total_micros // 2
        
        for i in range(micros_to_complete):
            micro_id = goal["micro_goals"][i]["id"]
            client.put(f"/api/goals/{goal_id}/micro-goals/{micro_id}/complete")
        
        # Verificar progresso
        response = client.get(f"/api/goals/{goal_id}")
        updated_goal = response.json()
        
        expected_progress = (micros_to_complete / total_micros) * 100
        assert abs(updated_goal["progress"] - expected_progress) < 0.1  # Tolerância para float
    
    def test_ai_micro_goal_generation_quality(self, client, clean_db):
        """Testa qualidade da geração de micro-metas pela IA"""
        
        test_cases = [
            {
                "title": "Aprender React",
                "description": "Dominar desenvolvimento frontend com React",
                "expected_keywords": ["tutorial", "projeto", "prática"]
            },
            {
                "title": "Escrever artigo técnico",
                "description": "Publicar artigo sobre boas práticas",
                "expected_keywords": ["estrutura", "rascunho", "revisar"]
            },
            {
                "title": "Melhorar condicionamento físico",
                "description": "Começar rotina de exercícios",
                "expected_keywords": ["rotina", "exercício", "consistência"]
            }
        ]
        
        for case in test_cases:
            response = client.post("/api/goals/", json=case)
            goal = response.json()
            
            micro_goals = goal["micro_goals"]
            assert len(micro_goals) >= 3  # Deve gerar pelo menos 3 micro-metas
            
            # Verifica se micro-metas contêm palavras-chave relevantes
            all_titles = " ".join(mg["title"].lower() for mg in micro_goals)
            keyword_found = any(keyword in all_titles for keyword in case["expected_keywords"])
            assert keyword_found, f"Nenhuma palavra-chave encontrada para: {case['title']}"
            
            # Verifica estrutura das micro-metas
            for mg in micro_goals:
                assert mg["estimated_time"] > 0
                assert mg["status"] == "pending"
                assert mg["goal_id"] == goal["id"]
                assert len(mg["title"]) > 5  # Título não muito curto
    
    def test_suggestion_system_integration(self, client, clean_db):
        """Testa integração do sistema de sugestões com objetivos"""
        
        # 1. Criar objetivo
        goal_data = {
            "title": "Objetivo para Sugestões",
            "description": "Teste de integração com sugestões"
        }
        
        response = client.post("/api/goals/", json=goal_data)
        goal = response.json()
        
        # 2. Obter sugestões
        response = client.get("/api/suggestions/")
        suggestions = response.json()
        
        # 3. Verificar se há sugestões relacionadas ao objetivo
        goal_micro_ids = [mg["id"] for mg in goal["micro_goals"]]
        related_suggestions = [
            s for s in suggestions 
            if s["micro_goal_id"] in goal_micro_ids
        ]
        
        # Pode não haver sugestões imediatas, mas estrutura deve estar correta
        for suggestion in suggestions:
            assert "title" in suggestion
            assert "description" in suggestion
            assert "micro_goal_id" in suggestion
            assert suggestion["priority"] in ["low", "medium", "high"]
        
        # 4. Obter mensagem motivacional
        response = client.get("/api/suggestions/motivational")
        motivational = response.json()
        
        assert "message" in motivational
        assert motivational["progress"] >= 0
        assert isinstance(motivational["message"], str)