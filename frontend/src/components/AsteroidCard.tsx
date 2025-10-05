import { Asteroid } from '@/types/asteroid';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Star, Info, Rocket, AlertTriangle } from 'lucide-react';
import { cn } from '@/helpers/utils';

interface AsteroidCardProps {
  asteroid: Asteroid;
  onToggleFavorite: (id: string) => void;
  onViewDetails: (asteroid: Asteroid) => void;
}

const threatColors = {
  safe: 'bg-success/20 text-success border-success/50',
  low: 'bg-primary/20 text-primary border-primary/50',
  medium: 'bg-warning/20 text-warning border-warning/50',
  high: 'bg-destructive/20 text-destructive border-destructive/50',
  critical: 'bg-destructive text-destructive-foreground border-destructive',
};

const threatLabels = {
  safe: 'Seguro',
  low: 'Baixo',
  medium: 'Médio',
  high: 'Alto',
  critical: 'Crítico',
};

export const AsteroidCard = ({ asteroid, onToggleFavorite, onViewDetails }: AsteroidCardProps) => {
  const showWarning = asteroid.threatLevel === 'high' || asteroid.threatLevel === 'critical';

  return (
    <Card className="glass-card transition-all duration-300 hover:scale-[1.02] hover:shadow-lg hover:shadow-primary/20 group">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-xl font-bold flex items-center gap-2">
              {asteroid.name}
              {showWarning && (
                <AlertTriangle className="h-5 w-5 text-destructive animate-pulse" />
              )}
            </CardTitle>
            <CardDescription className="text-muted-foreground mt-1">
              ID: {asteroid.id} • Órbita: {asteroid.orbit}
            </CardDescription>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onToggleFavorite(asteroid.id)}
            className={cn(
              "transition-colors",
              asteroid.isFavorite && "text-warning"
            )}
          >
            <Star className={cn("h-5 w-5", asteroid.isFavorite && "fill-current")} />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="space-y-1">
            <p className="text-muted-foreground">Tamanho</p>
            <p className="font-semibold text-foreground">{asteroid.size}m</p>
          </div>
          <div className="space-y-1">
            <p className="text-muted-foreground">Velocidade</p>
            <p className="font-semibold text-foreground">{asteroid.velocity} km/s</p>
          </div>
          <div className="space-y-1">
            <p className="text-muted-foreground">Distância</p>
            <p className="font-semibold text-foreground">{asteroid.distance}M km</p>
          </div>
          <div className="space-y-1">
            <p className="text-muted-foreground">Próx. Aproximação</p>
            <p className="font-semibold text-foreground">
              {new Date(asteroid.nextApproach).toLocaleDateString('pt-BR')}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2">
          <Badge className={cn("font-medium", threatColors[asteroid.threatLevel])}>
            <Rocket className="h-3 w-3 mr-1" />
            {threatLabels[asteroid.threatLevel]}
          </Badge>
          <Button
            variant="outline"
            size="sm"
            onClick={() => onViewDetails(asteroid)}
            className="border-primary/50 hover:bg-primary/10 hover:text-primary hover:border-primary transition-all"
          >
            <Info className="h-4 w-4 mr-1" />
            Ver Detalhes
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};