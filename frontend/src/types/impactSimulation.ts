import { CelestialBodyCloseApproachData } from './asteroid';

export interface ImpactSimulationProps {
  asteroid: CelestialBodyCloseApproachData;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export interface ImpactSimulationState {
  isAnimating: boolean;
  animationProgress: number;
  impactPoint: {
    x: number;
    y: number;
    z: number;
  };
  asteroidPosition: {
    x: number;
    y: number;
    z: number;
  };
}

export interface ImpactSimulationControls {
  startSimulation: () => void;
  resetSimulation: () => void;
  exportData: () => void;
  exportPNG: () => void;
  closeSimulation: () => void;
}

export interface AsteroidTrajectory {
  startPosition: {
    x: number;
    y: number;
    z: number;
  };
  endPosition: {
    x: number;
    y: number;
    z: number;
  };
  controlPoints: Array<{
    x: number;
    y: number;
    z: number;
  }>;
}
