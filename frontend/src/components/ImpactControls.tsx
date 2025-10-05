import React from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  RotateCcw,
  Download,
  Image,
  X,
  Play,
  Pause,
  Target,
  Zap,
} from "lucide-react";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import { ImpactSimulationState } from "@/types/impactSimulation";

interface ImpactControlsProps {
  asteroid: CelestialBodyCloseApproachData;
  simulationState: ImpactSimulationState;
  onStartSimulation: () => void;
  onResetSimulation: () => void;
  onExportData: () => void;
  onExportPNG: () => void;
  onClose: () => void;
}

export const ImpactControls = ({
  asteroid,
  simulationState,
  onStartSimulation,
  onResetSimulation,
  onExportData,
  onExportPNG,
  onClose,
}: ImpactControlsProps) => {
  // Calcular informações do asteroide
  const asteroidInfo = {
    diameter: Math.max(50, parseFloat(asteroid.velocity_kms) * 10), // Estimativa
    velocity: parseFloat(asteroid.velocity_kms),
    distance: parseFloat(asteroid.distance_au),
  };

  return (
    <div className="space-y-4">
      {/* Informações do Asteroide */}
      <Card className="glass-card">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2">
            <Target className="h-5 w-5 text-primary" />
            {asteroid.designation}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="space-y-1">
              <p className="text-muted-foreground">Diâmetro Estimado</p>
              <p className="font-semibold">
                {asteroidInfo.diameter.toFixed(0)}m
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Velocidade</p>
              <p className="font-semibold">{asteroidInfo.velocity} km/s</p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Distância Atual</p>
              <p className="font-semibold">{asteroidInfo.distance} AU</p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Próx. Aproximação</p>
              <p className="font-semibold">
                {new Date(asteroid.close_approach_date).toLocaleDateString("pt-BR")}
              </p>
            </div>
          </div>

          {/* Status da Simulação */}
          <div className="flex items-center justify-between pt-2">
            <Badge
              className={
                simulationState.isAnimating
                  ? "bg-primary/20 text-primary"
                  : "bg-muted/20 text-muted-foreground"
              }
            >
              {simulationState.isAnimating ? (
                <>
                  <Pause className="h-3 w-3 mr-1" />
                  Animando
                </>
              ) : (
                <>
                  <Play className="h-3 w-3 mr-1" />
                  Pausado
                </>
              )}
            </Badge>

            <div className="text-xs text-muted-foreground">
              Progresso: {(simulationState.animationProgress * 100).toFixed(0)}%
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Controles */}
      <div className="grid grid-cols-2 gap-2">
        <Button
          onClick={onStartSimulation}
          disabled={simulationState.isAnimating}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          size="sm"
        >
          <Play className="h-4 w-4 mr-1" />
          Iniciar
        </Button>

        <Button
          onClick={onResetSimulation}
          variant="outline"
          className="border-border/50 hover:bg-muted/50"
          size="sm"
        >
          <RotateCcw className="h-4 w-4 mr-1" />
          Reiniciar
        </Button>
      </div>

      {/* Botões de Exportação */}
      <div className="grid grid-cols-2 gap-2">
        <Button
          onClick={onExportData}
          variant="outline"
          className="border-accent/50 hover:bg-accent/10"
          size="sm"
        >
          <Download className="h-4 w-4 mr-1" />
          Exportar Dados
        </Button>

        <Button
          onClick={onExportPNG}
          variant="outline"
          className="border-accent/50 hover:bg-accent/10"
          size="sm"
        >
          <Image className="h-4 w-4 mr-1" />
          Exportar PNG
        </Button>
      </div>

      {/* Botão Fechar */}
      <Button
        onClick={onClose}
        variant="outline"
        className="w-full border-destructive/50 hover:bg-destructive/10 hover:text-destructive"
        size="sm"
      >
        <X className="h-4 w-4 mr-1" />
        Fechar
      </Button>
    </div>
  );
};
