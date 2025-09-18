import pytest
import sys
import os
from fastapi.testclient import TestClient

# Adiciona o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))

from main import app
from mock_data import goals_db, suggestions_db, badges_db

@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)

@pytest.fixture
def clean_db():
    """Limpa e reinicializa dados mock para cada teste"""
    goals_db.clear()
    suggestions_db.clear()
    badges_db.clear()
    
    # Reinicializa dados básicos
    from mock_data import initialize_mock_data
    initialize_mock_data()
    
    yield
    
    # Cleanup após teste
    goals_db.clear()
    suggestions_db.clear()
    badges_db.clear()

@pytest.fixture
def sample_goal_data():
    """Dados de exemplo para criar objetivo"""
    return {
        "title": "Aprender JavaScript",
        "description": "Dominar JavaScript para desenvolvimento web",
        "tags": ["programação", "javascript", "web"]
    }