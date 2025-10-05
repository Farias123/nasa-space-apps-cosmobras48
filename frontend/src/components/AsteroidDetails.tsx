import { useState } from 'react';
import { Asteroid } from '@/types/asteroid';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Calendar, Gauge, Orbit, Ruler, MapPin, Star } from 'lucide-react';
import { cn } from '@/lib/utils';
import { SimulationPanel } from './SimulationPanel';
import { TrajectoryView } from './TrajectoryView';

interface AsteroidDetailsProps {
  asteroid: Asteroid | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onToggleFavorite: (id: string) => void;
}

const threatColors = {
  safe: 'bg-success/20 text-success',
  low: 'bg-primary/20 text-primary',
  medium: 'bg-warning/20 text-warning',
  high: 'bg-destructive/20 text-destructive',
  critical: 'bg-destructive text-destructive-foreground',
};

const threatLabels = {
  safe: 'Seguro',
  low: 'Baixo',
  medium: 'Médio',
  high: 'Alto',
  critical: 'Crítico',
};

export const AsteroidDetails = ({
  asteroid,
  open,
  onOpenChange,
  onToggleFavorite,
}: AsteroidDetailsProps) => {
  const [simulationOpen, setSimulationOpen] = useState(false);
  const [trajectoryOpen, setTrajectoryOpen] = useState(false);

  if (!asteroid) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-start justify-between">
            <div>
              <DialogTitle className="text-2xl font-bold gradient-text">
                {asteroid.name}
              </DialogTitle>
              <DialogDescription className="mt-2">
                Asteroide ID: {asteroid.id} • Classificação: {asteroid.orbit}
              </DialogDescription>
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
              <Star className={cn("h-6 w-6", asteroid.isFavorite && "fill-current")} />
            </Button>
          </div>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          <div className="flex items-center gap-2">
            <Badge className={cn("font-medium text-sm px-3 py-1", threatColors[asteroid.threatLevel])}>
              Ameaça: {threatLabels[asteroid.threatLevel]}
            </Badge>
          </div>

          <Separator className="bg-border/50" />

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Ruler className="h-4 w-4 text-primary" />
                <span className="text-sm">Tamanho</span>
              </div>
              <p className="text-2xl font-bold">{asteroid.size} metros</p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Gauge className="h-4 w-4 text-primary" />
                <span className="text-sm">Velocidade</span>
              </div>
              <p className="text-2xl font-bold">{asteroid.velocity} km/s</p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <MapPin className="h-4 w-4 text-primary" />
                <span className="text-sm">Distância Atual</span>
              </div>
              <p className="text-2xl font-bold">{asteroid.distance}M km</p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Orbit className="h-4 w-4 text-primary" />
                <span className="text-sm">Tipo de Órbita</span>
              </div>
              <p className="text-2xl font-bold">{asteroid.orbit}</p>
            </div>
          </div>

          <Separator className="bg-border/50" />

          <div className="space-y-4">
            <div className="flex items-center gap-2 text-muted-foreground">
              <Calendar className="h-4 w-4 text-primary" />
              <span className="text-sm font-semibold">Cronologia</span>
            </div>
            <div className="space-y-3 ml-6">
              <div>
                <p className="text-sm text-muted-foreground">Data de Descoberta</p>
                <p className="font-semibold">
                  {new Date(asteroid.discoveryDate).toLocaleDateString('pt-BR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Próxima Aproximação à Terra</p>
                <p className="font-semibold text-warning">
                  {new Date(asteroid.nextApproach).toLocaleDateString('pt-BR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                </p>
              </div>
            </div>
          </div>

          {asteroid.description && (
            <>
              <Separator className="bg-border/50" />
              <div className="space-y-2">
                <h4 className="font-semibold text-sm">Descrição</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {asteroid.description}
                </p>
              </div>
            </>
          )}

          <div className="flex gap-3 pt-4">
            <Button 
              className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground"
              onClick={() => setSimulationOpen(true)}
            >
              Iniciar Simulação
            </Button>
            <Button 
              variant="outline" 
              className="flex-1 border-accent/50 hover:bg-accent/10"
              onClick={() => setTrajectoryOpen(true)}
            >
              Ver Trajetória
            </Button>
          </div>
        </div>
      </DialogContent>

      {/* Sub-modals */}
      <SimulationPanel
        asteroid={asteroid}
        open={simulationOpen}
        onOpenChange={setSimulationOpen}
      />
      
      <TrajectoryView
        asteroid={asteroid}
        open={trajectoryOpen}
        onOpenChange={setTrajectoryOpen}
      />
    </Dialog>
  );
};
