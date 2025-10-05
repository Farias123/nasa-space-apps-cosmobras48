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
  // Calculate asteroid information
  const asteroidInfo = {
    diameter: Math.max(50, parseFloat(asteroid.velocity_kms) * 10), // Estimate
    velocity: parseFloat(asteroid.velocity_kms),
    distance: parseFloat(asteroid.distance_au),
  };

  return (
    <div className="space-y-4">
      {/* Asteroid Information */}
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
              <p className="text-muted-foreground">Estimated Diameter</p>
              <p className="font-semibold">
                {asteroidInfo.diameter.toFixed(0)}m
              </p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Velocity</p>
              <p className="font-semibold">{asteroidInfo.velocity} km/s</p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Current Distance</p>
              <p className="font-semibold">{asteroidInfo.distance} AU</p>
            </div>
            <div className="space-y-1">
              <p className="text-muted-foreground">Next Approach</p>
              <p className="font-semibold">
                {new Date(asteroid.close_approach_date).toLocaleDateString(
                  "en-US"
                )}
              </p>
            </div>
          </div>

          {/* Simulation Status */}
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
                  Animating
                </>
              ) : (
                <>
                  <Play className="h-3 w-3 mr-1" />
                  Paused
                </>
              )}
            </Badge>

            <div className="text-xs text-muted-foreground">
              Progress: {(simulationState.animationProgress * 100).toFixed(0)}%
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Controls */}
      <div className="grid grid-cols-2 gap-2">
        <Button
          onClick={onStartSimulation}
          disabled={simulationState.isAnimating}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
          size="sm"
        >
          <Play className="h-4 w-4 mr-1" />
          Start
        </Button>

        <Button
          onClick={onResetSimulation}
          variant="outline"
          className="border-border/50 hover:bg-muted/50"
          size="sm"
        >
          <RotateCcw className="h-4 w-4 mr-1" />
          Reset
        </Button>
      </div>

      {/* Export Buttons */}
      <div className="grid grid-cols-2 gap-2">
        <Button
          onClick={onExportData}
          variant="outline"
          className="border-accent/50 hover:bg-accent/10"
          size="sm"
        >
          <Download className="h-4 w-4 mr-1" />
          Export Data
        </Button>

        <Button
          onClick={onExportPNG}
          variant="outline"
          className="border-accent/50 hover:bg-accent/10"
          size="sm"
        >
          <Image className="h-4 w-4 mr-1" />
          Export PNG
        </Button>
      </div>

      {/* Close Button */}
      <Button
        onClick={onClose}
        variant="outline"
        className="w-full border-destructive/50 hover:bg-destructive/10 hover:text-destructive"
        size="sm"
      >
        <X className="h-4 w-4 mr-1" />
        Close
      </Button>
    </div>
  );
};
