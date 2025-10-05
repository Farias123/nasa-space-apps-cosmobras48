import { Asteroid } from '@/types/asteroid';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Orbit, MapPin, Calendar, TrendingUp } from 'lucide-react';

interface TrajectoryViewProps {
  asteroid: Asteroid | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const TrajectoryView = ({
  asteroid,
  open,
  onOpenChange,
}: TrajectoryViewProps) => {
  if (!asteroid) return null;

  // Dados simplificados de órbita
  const orbitData = {
    perihelion: (asteroid.distance * 0.7).toFixed(2),
    aphelion: (asteroid.distance * 1.3).toFixed(2),
    eccentricity: (Math.random() * 0.3 + 0.1).toFixed(3),
    inclination: (Math.random() * 15 + 5).toFixed(1),
    period: (asteroid.distance * 0.5).toFixed(1),
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold gradient-text">
            Trajetória Orbital
          </DialogTitle>
          <DialogDescription>
            Visualização da órbita e trajetória do asteroide {asteroid.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Visualização da Órbita (Simplificada) */}
          <div className="relative bg-gradient-to-br from-background via-accent/5 to-primary/10 rounded-lg border border-primary/20 p-8 min-h-[300px] flex items-center justify-center">
            <div className="relative w-full max-w-md aspect-square">
              {/* Sol no centro */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-warning rounded-full glow-primary animate-pulse" />
              
              {/* Órbita da Terra */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 border-2 border-primary/20 rounded-full" />
              <div className="absolute top-1/2 left-1/2 translate-x-16 -translate-y-1/2 w-4 h-4 bg-primary rounded-full" />
              
              {/* Órbita do Asteroide */}
              <div 
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border-2 border-accent rounded-full"
                style={{
                  width: `${Math.min(asteroid.distance * 30, 280)}px`,
                  height: `${Math.min(asteroid.distance * 25, 240)}px`,
                }}
              />
              <div 
                className="absolute top-0 left-1/2 -translate-x-1/2 w-3 h-3 bg-accent rounded-full glow-primary"
                style={{
                  transform: `translateX(-50%) translateY(${Math.min(asteroid.distance * 15, 140)}px)`,
                }}
              />
            </div>

            {/* Legenda */}
            <div className="absolute bottom-4 left-4 space-y-1">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-warning rounded-full" />
                <span className="text-xs text-muted-foreground">Sol</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-primary rounded-full" />
                <span className="text-xs text-muted-foreground">Terra</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-accent rounded-full" />
                <span className="text-xs text-muted-foreground">{asteroid.name}</span>
              </div>
            </div>
          </div>

          <Separator className="bg-border/50" />

          {/* Parâmetros Orbitais */}
          <div className="space-y-4">
            <h4 className="font-semibold text-lg flex items-center gap-2">
              <Orbit className="h-5 w-5 text-primary" />
              Parâmetros Orbitais
            </h4>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Periélio</span>
                </div>
                <p className="text-xl font-bold">{orbitData.perihelion}M km</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Afélio</span>
                </div>
                <p className="text-xl font-bold">{orbitData.aphelion}M km</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  <span className="text-sm">Excentricidade</span>
                </div>
                <p className="text-xl font-bold">{orbitData.eccentricity}</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Orbit className="h-4 w-4 text-primary" />
                  <span className="text-sm">Inclinação</span>
                </div>
                <p className="text-xl font-bold">{orbitData.inclination}°</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Calendar className="h-4 w-4 text-primary" />
                  <span className="text-sm">Período Orbital</span>
                </div>
                <p className="text-xl font-bold">{orbitData.period} anos</p>
              </div>

              <div className="glass-card p-4 space-y-1">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <MapPin className="h-4 w-4 text-primary" />
                  <span className="text-sm">Tipo de Órbita</span>
                </div>
                <Badge className="bg-accent/20 text-accent mt-1">
                  {asteroid.orbit}
                </Badge>
              </div>
            </div>
          </div>

          <Separator className="bg-border/50" />

          {/* Informações de Aproximação */}
          <div className="space-y-3">
            <h4 className="font-semibold flex items-center gap-2">
              <Calendar className="h-4 w-4 text-primary" />
              Próximas Aproximações
            </h4>
            <div className="bg-accent/10 border border-accent/30 rounded-lg p-4 space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Próxima Aproximação:</span>
                <span className="font-semibold text-warning">
                  {new Date(asteroid.nextApproach).toLocaleDateString('pt-BR')}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Distância Mínima:</span>
                <span className="font-semibold">{asteroid.distance}M km</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-muted-foreground">Velocidade Relativa:</span>
                <span className="font-semibold">{asteroid.velocity} km/s</span>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
