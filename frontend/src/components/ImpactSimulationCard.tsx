import React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import { ImpactSimulationProps } from "@/types/impactSimulation";
import { useImpactSimulation } from "@/hooks/useImpactSimulation";
import { ImpactScene } from "@/components/ImpactScene";
import { ImpactControls } from "@/components/ImpactControls";
import { Zap } from "lucide-react";

export const ImpactSimulationCard = ({
  asteroid,
  open,
  onOpenChange,
}: ImpactSimulationProps) => {
  const {
    state,
    trajectory,
    startSimulation,
    resetSimulation,
    exportData,
    exportPNG,
  } = useImpactSimulation(asteroid);

  const handleClose = () => {
    resetSimulation();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold gradient-text flex items-center gap-2">
            <Zap className="h-6 w-6" />
            Simulação de Impacto: {asteroid.designation}
          </DialogTitle>
          <DialogDescription>
            Visualize a trajetória e simule o impacto do asteroide{" "}
            {asteroid.designation} com a Terra. A simulação mostra a trajetória
            curva baseada na velocidade e distância atual do objeto.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Cena 3D Principal */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Zap className="h-5 w-5 text-primary" />
              Visualização 3D
            </h3>
            <ImpactScene
              asteroid={asteroid}
              simulationState={state}
              trajectory={trajectory}
            />
          </div>

          {/* Controles e Informações */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Controles */}
            <div className="lg:col-span-1">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Controles
              </h3>
              <ImpactControls
                asteroid={asteroid}
                simulationState={state}
                onStartSimulation={startSimulation}
                onResetSimulation={resetSimulation}
                onExportData={exportData}
                onExportPNG={exportPNG}
                onClose={handleClose}
              />
            </div>

            {/* Informações Detalhadas */}
            <div className="lg:col-span-2 space-y-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Dados da Simulação
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Informações do Asteroide */}
                <div className="glass-card p-4 space-y-3">
                  <h4 className="font-semibold text-sm text-primary">
                    Asteroide
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Designação:</span>
                      <span className="font-medium">
                        {asteroid.designation}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Velocidade:</span>
                      <span className="font-medium">
                        {asteroid.velocity_kms} km/s
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Distância:</span>
                      <span className="font-medium">
                        {asteroid.distance_au} AU
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">
                        Próx. Aproximação:
                      </span>
                      <span className="font-medium">
                        {new Date(
                          asteroid.close_approach_date
                        ).toLocaleDateString("pt-BR")}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Status da Simulação */}
                <div className="glass-card p-4 space-y-3">
                  <h4 className="font-semibold text-sm text-primary">
                    Simulação
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Status:</span>
                      <span
                        className={`font-medium ${
                          state.isAnimating
                            ? "text-primary"
                            : "text-muted-foreground"
                        }`}
                      >
                        {state.isAnimating ? "Em Execução" : "Pausada"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Progresso:</span>
                      <span className="font-medium">
                        {(state.animationProgress * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Posição X:</span>
                      <span className="font-medium">
                        {state.asteroidPosition.x.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Posição Y:</span>
                      <span className="font-medium">
                        {state.asteroidPosition.y.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Instruções */}
              <div className="glass-card p-4 bg-accent/10 border-accent/30">
                <h4 className="font-semibold text-sm text-accent mb-2">
                  Instruções
                </h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>
                    • Use o mouse para rotacionar, fazer zoom e mover a câmera
                  </li>
                  <li>• Clique em "Iniciar" para começar a simulação</li>
                  <li>• A linha laranja mostra a trajetória prevista</li>
                  <li>
                    • O asteroide se move ao longo da trajetória até o impacto
                  </li>
                  <li>
                    • Use "Exportar Dados" para salvar informações da simulação
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
