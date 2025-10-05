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
            Impact Simulation: {asteroid.designation}
          </DialogTitle>
          <DialogDescription>
            Visualize the trajectory and simulate the impact of asteroid{" "}
            {asteroid.designation} with Earth. The simulation shows the curved
            trajectory based on the current velocity and distance of the object.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 mt-6">
          {/* Main 3D Scene */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Zap className="h-5 w-5 text-primary" />
              3D Visualization
            </h3>
            <ImpactScene
              asteroid={asteroid}
              simulationState={state}
              trajectory={trajectory}
            />
          </div>

          {/* Controls and Information */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Controls */}
            <div className="lg:col-span-1">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Controls
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

            {/* Instructions */}
            <div className="lg:col-span-2 space-y-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Instructions
              </h3>

              <div className="glass-card p-4 bg-accent/10 border-accent/30">
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>
                    • Use the mouse to rotate, zoom, and move the camera
                  </li>
                  <li>• Click "Start" to begin the simulation</li>
                  <li>• The orange line shows the predicted trajectory</li>
                  <li>
                    • The asteroid moves along the trajectory until impact
                  </li>
                  <li>
                    • Use "Export Data" to save simulation information
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
