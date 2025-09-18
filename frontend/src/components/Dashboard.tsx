import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
} from '@mui/material';
import { TrendingUp, EmojiEvents, Flag } from '@mui/icons-material';
import { statsService, suggestionService } from '../services/api';
import { DashboardData, Suggestion } from '../types';

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    loadSuggestions();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await statsService.getDashboardData();
      setDashboardData(data);
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSuggestions = async () => {
    try {
      const data = await suggestionService.getSuggestions();
      setSuggestions(data);
    } catch (error) {
      console.error('Erro ao carregar sugestões:', error);
    }
  };

  if (loading || !dashboardData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Carregando...</Typography>
      </Box>
    );
  }

  const { stats, overall_progress, featured_goals, recent_badges, motivational_message } = dashboardData;

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      {/* Mensagem Motivacional */}
      <Card sx={{ mb: 3, background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)' }}>
        <CardContent>
          <Typography variant="h5" component="div" color="white" textAlign="center">
            {motivational_message}
          </Typography>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Estatísticas Principais */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={2}>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography color="textSecondary" gutterBottom>
                    Objetivos Ativos
                  </Typography>
                  <Typography variant="h4" component="div">
                    {stats.active_goals}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography color="textSecondary" gutterBottom>
                    Progresso Geral
                  </Typography>
                  <Typography variant="h4" component="div">
                    {Math.round(overall_progress)}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography color="textSecondary" gutterBottom>
                    Sequência
                  </Typography>
                  <Typography variant="h4" component="div">
                    {stats.current_streak}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    dias
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography color="textSecondary" gutterBottom>
                    Distintivos
                  </Typography>
                  <Typography variant="h4" component="div">
                    {stats.badges.length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Objetivos em Destaque */}
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Flag sx={{ mr: 1, verticalAlign: 'middle' }} />
                Objetivos em Destaque
              </Typography>
              {featured_goals.map((goal) => (
                <Box key={goal.id} sx={{ mb: 2 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="subtitle1">{goal.title}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      {Math.round(goal.progress)}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={goal.progress}
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                  <Box display="flex" gap={1} mt={1}>
                    {goal.tags.map((tag) => (
                      <Chip key={tag} label={tag} size="small" />
                    ))}
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          {/* Sugestões */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
                Sugestões para Você
              </Typography>
              <List>
                {suggestions.map((suggestion) => (
                  <ListItem key={suggestion.id} divider>
                    <ListItemText
                      primary={suggestion.title}
                      secondary={suggestion.description}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>

          {/* Distintivos Recentes */}
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <EmojiEvents sx={{ mr: 1, verticalAlign: 'middle' }} />
                Conquistas Recentes
              </Typography>
              <List>
                {recent_badges.map((badge) => (
                  <ListItem key={badge.id}>
                    <ListItemAvatar>
                      <Avatar>{badge.icon}</Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={badge.name}
                      secondary={badge.description}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;