import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Checkbox,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
} from '@mui/material';
import { Add, CheckCircle } from '@mui/icons-material';
import { goalService } from '../services/api';
import { Goal, MicroGoal, MicroGoalStatus } from '../types';

const GoalList: React.FC = () => {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newGoal, setNewGoal] = useState({ title: '', description: '', tags: '' });

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    try {
      const data = await goalService.getGoals();
      setGoals(data);
    } catch (error) {
      console.error('Erro ao carregar objetivos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGoal = async () => {
    try {
      const goalData = {
        title: newGoal.title,
        description: newGoal.description,
        tags: newGoal.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
      };
      
      await goalService.createGoal(goalData);
      setNewGoal({ title: '', description: '', tags: '' });
      setOpenDialog(false);
      loadGoals();
    } catch (error) {
      console.error('Erro ao criar objetivo:', error);
    }
  };

  const handleCompleteMicroGoal = async (goalId: string, microGoalId: string) => {
    try {
      await goalService.completeMicroGoal(goalId, microGoalId);
      loadGoals();
    } catch (error) {
      console.error('Erro ao completar micro-meta:', error);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Carregando objetivos...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Meus Objetivos
      </Typography>

      {goals.map((goal) => (
        <Card key={goal.id} sx={{ mb: 3 }}>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
              <Box>
                <Typography variant="h6" gutterBottom>
                  {goal.title}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  {goal.description}
                </Typography>
                <Box display="flex" gap={1} mb={2}>
                  {goal.tags.map((tag) => (
                    <Chip key={tag} label={tag} size="small" />
                  ))}
                </Box>
              </Box>
              <Box textAlign="right">
                <Typography variant="h6" color="primary">
                  {Math.round(goal.progress)}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {goal.micro_goals.filter(mg => mg.status === MicroGoalStatus.COMPLETED).length}/
                  {goal.micro_goals.length} concluídas
                </Typography>
              </Box>
            </Box>

            <LinearProgress
              variant="determinate"
              value={goal.progress}
              sx={{ mb: 2, height: 8, borderRadius: 4 }}
            />

            <Typography variant="subtitle1" gutterBottom>
              Próximos Passos:
            </Typography>
            <List dense>
              {goal.micro_goals
                .filter(mg => mg.status !== MicroGoalStatus.COMPLETED)
                .slice(0, 3)
                .map((microGoal: MicroGoal) => (
                <ListItem key={microGoal.id} disablePadding>
                  <ListItemButton
                    onClick={() => handleCompleteMicroGoal(goal.id, microGoal.id)}
                  >
                    <Checkbox
                      edge="start"
                      checked={microGoal.status === MicroGoalStatus.COMPLETED}
                      tabIndex={-1}
                      disableRipple
                    />
                    <ListItemText
                      primary={microGoal.title}
                      secondary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="body2" color="textSecondary">
                            ≈{microGoal.estimated_time}min
                          </Typography>
                          <Chip
                            label={microGoal.priority}
                            size="small"
                            color={getPriorityColor(microGoal.priority) as any}
                          />
                        </Box>
                      }
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>

            {goal.micro_goals.filter(mg => mg.status === MicroGoalStatus.COMPLETED).length > 0 && (
              <Box mt={2}>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  <CheckCircle sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
                  Concluídas: {goal.micro_goals.filter(mg => mg.status === MicroGoalStatus.COMPLETED).length}
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      ))}

      {/* FAB para adicionar novo objetivo */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => setOpenDialog(true)}
      >
        <Add />
      </Fab>

      {/* Dialog para criar novo objetivo */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Criar Novo Objetivo</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Título do Objetivo"
            fullWidth
            variant="outlined"
            value={newGoal.title}
            onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Descrição"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={newGoal.description}
            onChange={(e) => setNewGoal({ ...newGoal, description: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Tags (separadas por vírgula)"
            fullWidth
            variant="outlined"
            value={newGoal.tags}
            onChange={(e) => setNewGoal({ ...newGoal, tags: e.target.value })}
            placeholder="programação, carreira, python"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancelar</Button>
          <Button onClick={handleCreateGoal} variant="contained">
            Criar Objetivo
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default GoalList;