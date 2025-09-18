# Arquitetura do Proactive Goal Coach

## Visão Geral

O Proactive Goal Coach é uma aplicação web que ajuda usuários a atingir objetivos de longo prazo através de micro-metas inteligentes e sugestões contextuais.

## Arquitetura Atual (MVP)

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   React + TS    │◄──►│  FastAPI + Python│
│   Material-UI   │    │   Mock Data     │
└─────────────────┘    └─────────────────┘
```

## Componentes Principais

### Frontend (React + TypeScript)
- **Dashboard**: Visão geral com progresso e sugestões
- **GoalList**: Gerenciamento de objetivos e micro-metas
- **Services**: Comunicação com API
- **Types**: Definições TypeScript compartilhadas

### Backend (FastAPI + Python)
- **Goals Router**: CRUD de objetivos e micro-metas
- **Suggestions Router**: IA contextual e motivacional
- **Stats Router**: Estatísticas e dashboard
- **Mock Data**: Dados simulados para desenvolvimento

## Funcionalidades Core

### 1. Gestão de Objetivos
- Criação de objetivos de longo prazo
- IA quebra objetivos em micro-metas gerenciáveis
- Tracking de progresso visual

### 2. IA Proativa
- **Geração de Micro-metas**: Baseada em templates inteligentes
- **Sugestões Contextuais**: Considera horário e hábitos
- **Mensagens Motivacionais**: Foco em conquistas positivas

### 3. Gamificação
- Sistema de distintivos (badges)
- Tracking de sequências (streaks)
- Progresso visual e celebrações

### 4. Dashboard Inteligente
- Estatísticas em tempo real
- Objetivos em destaque
- Sugestões personalizadas

## Fluxo de Dados

1. **Criação de Objetivo**:
   ```
   User Input → IA Analysis → Micro-goals Generation → Storage
   ```

2. **Sugestões Contextuais**:
   ```
   Time Context + User Habits → AI Suggestions → Personalized Messages
   ```

3. **Progresso Tracking**:
   ```
   Micro-goal Completion → Progress Update → Badge Check → Dashboard Refresh
   ```

## Preparação para Serverless

### Estrutura Futura (AWS)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CloudFront    │    │   API Gateway   │    │     Lambda      │
│   + S3 Static   │◄──►│   + Cognito     │◄──►│   Functions     │
│   Website       │    │   Auth          │    │   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │   DynamoDB      │
                                               │   + EventBridge │
                                               │   Scheduling    │
                                               └─────────────────┘
```

### Migração Planejada
1. **Backend → Lambda Functions**
   - Cada router vira uma função Lambda
   - API Gateway para roteamento
   
2. **Storage → DynamoDB**
   - Tabelas: Goals, MicroGoals, Users, Badges
   - Índices para queries eficientes
   
3. **Frontend → S3 + CloudFront**
   - Build estático no S3
   - CDN global via CloudFront
   
4. **Proatividade → EventBridge**
   - Triggers automáticos para sugestões
   - Notificações baseadas em tempo

## Tecnologias Utilizadas

### Desenvolvimento
- **Frontend**: React 18, TypeScript, Material-UI
- **Backend**: FastAPI, Python 3.9+, Pydantic
- **Comunicação**: Axios, REST API

### Futuro (Serverless)
- **Compute**: AWS Lambda
- **Storage**: DynamoDB
- **API**: API Gateway
- **Frontend**: S3 + CloudFront
- **Auth**: Cognito
- **Scheduling**: EventBridge
- **Monitoring**: CloudWatch

## Padrões de Design

### Backend
- **Repository Pattern**: Separação de dados e lógica
- **Service Layer**: Lógica de negócio isolada
- **DTO Pattern**: Pydantic models para validação

### Frontend
- **Component Composition**: Componentes reutilizáveis
- **Service Layer**: Abstração da API
- **Type Safety**: TypeScript em toda aplicação

## Próximos Passos

1. **Melhorias na IA**:
   - Algoritmos mais sofisticados para micro-metas
   - Machine Learning para sugestões personalizadas
   
2. **Funcionalidades Avançadas**:
   - Colaboração entre usuários
   - Integração com calendários
   - Notificações push
   
3. **Migração Serverless**:
   - Infraestrutura como código (Terraform)
   - CI/CD pipeline
   - Monitoramento e alertas