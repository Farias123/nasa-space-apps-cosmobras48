import { useState } from 'react';
import { Asteroid } from '@/types/asteroid';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Separator } from '@/components/ui/separator';
import { Badge } from '@/components/ui/badge';
import { Activity, Target, Zap } from 'lucide-react';
import { toast } from 'sonner';

interface SimulationPanelProps {
  asteroid: Asteroid | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const SimulationPanel = ({
  asteroid,
  open,
  onOpenChange,
}: SimulationPanelProps) => {
  const [impactAngle, setImpactAngle] = useState(45);
  const [impactVelocity, setImpactVelocity] = useState(
    asteroid?.velocity || 20
  );
  const [simulationRun, setSimulationRun] = useState(false);
  const [results, setResults] = useState<{
    craterDiameter: number;
    affectedArea: number;
    energyRelease: number;
    tsunamiRisk: boolean;
  } | null>(null);

  if (!asteroid) return null;

  const runSimulation = () => {
    // Cálculos simplificados de simulação
    const craterDiameter = Math.round(
      (asteroid.size * impactVelocity * Math.sin((impactAngle * Math.PI) / 180)) / 10
    );
    const affectedArea = Math.round(Math.PI * Math.pow(craterDiameter * 2, 2));
    const energyRelease = Math.round(
      (asteroid.size / 100) * Math.pow(impactVelocity, 2) * 0.5
    );
    const tsunamiRisk = asteroid.size > 500 && impactVelocity > 15;

    setResults({
      craterDiameter,
      affectedArea,
      energyRelease,
      tsunamiRisk,
    });
    setSimulationRun(true);
    toast.success('Simulação concluída!');
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold gradient-text">
            Simulação de Impacto
          </DialogTitle>
          <DialogDescription>
            Ajuste os parâmetros para simular cenários de impacto do asteroide{' '}
            {asteroid.name}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Parâmetros de Simulação */}
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label className="text-sm font-semibold flex items-center gap-2">
                  <Target className="h-4 w-4 text-primary" />
                  Ângulo de Impacto
                </Label>
                <span className="text-sm text-muted-foreground">
                  {impactAngle}°
                </span>
              </div>
              <Slider
                value={[impactAngle]}
                onValueChange={(v) => setImpactAngle(v[0])}
                min={0}
                max={90}
                step={5}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                0° = rasante | 90° = perpendicular
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label className="text-sm font-semibold flex items-center gap-2">
                  <Zap className="h-4 w-4 text-primary" />
                  Velocidade de Impacto
                </Label>
                <span className="text-sm text-muted-foreground">
                  {impactVelocity} km/s
                </span>
              </div>
              <Slider
                value={[impactVelocity]}
                onValueChange={(v) => setImpactVelocity(v[0])}
                min={5}
                max={50}
                step={1}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                Velocidade atual do asteroide: {asteroid.velocity} km/s
              </p>
            </div>
          </div>

          <Separator className="bg-border/50" />

          {/* Botão de Simulação */}
          <Button
            onClick={runSimulation}
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground h-12"
          >
            <Activity className="h-5 w-5 mr-2" />
            Executar Simulação
          </Button>

          {/* Resultados */}
          {simulationRun && results && (
            <>
              <Separator className="bg-border/50" />
              <div className="space-y-4">
                <h4 className="font-semibold text-lg flex items-center gap-2">
                  <Activity className="h-5 w-5 text-primary" />
                  Resultados da Simulação
                </h4>

                <div className="grid grid-cols-2 gap-4">
                  <div className="glass-card p-4 space-y-1">
                    <p className="text-sm text-muted-foreground">
                      Diâmetro da Cratera
                    </p>
                    <p className="text-2xl font-bold text-primary">
                      {results.craterDiameter} km
                    </p>
                  </div>

                  <div className="glass-card p-4 space-y-1">
                    <p className="text-sm text-muted-foreground">Área Afetada</p>
                    <p className="text-2xl font-bold text-primary">
                      {results.affectedArea.toLocaleString()} km²
                    </p>
                  </div>

                  <div className="glass-card p-4 space-y-1">
                    <p className="text-sm text-muted-foreground">
                      Energia Liberada
                    </p>
                    <p className="text-2xl font-bold text-primary">
                      {results.energyRelease} Mt
                    </p>
                  </div>

                  <div className="glass-card p-4 space-y-1">
                    <p className="text-sm text-muted-foreground">Risco de Tsunami</p>
                    <Badge
                      className={
                        results.tsunamiRisk
                          ? 'bg-destructive/20 text-destructive'
                          : 'bg-success/20 text-success'
                      }
                    >
                      {results.tsunamiRisk ? 'Alto' : 'Baixo'}
                    </Badge>
                  </div>
                </div>

                <div className="bg-accent/10 border border-accent/30 rounded-lg p-4">
                  <p className="text-sm text-muted-foreground">
                    {results.energyRelease > 100
                      ? '⚠️ Impacto catastrófico: Efeitos globais esperados.'
                      : results.energyRelease > 50
                      ? '⚠️ Impacto severo: Danos regionais significativos.'
                      : '✓ Impacto moderado: Danos localizados.'}
                  </p>
                </div>
              </div>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};