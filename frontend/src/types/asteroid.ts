export type ThreatLevel = 'safe' | 'low' | 'medium' | 'high' | 'critical';

export interface Asteroid {
  id: string;
  name: string;
  size: number; // em metros
  velocity: number; // km/s
  orbit: string;
  distance: number; // em milhões de km
  threatLevel: ThreatLevel;
  discoveryDate: string;
  nextApproach: string;
  isFavorite?: boolean;
  description?: string;
}

export interface SimulationParams {
  asteroidId: string;
  impactAngle: number;
  impactVelocity: number;
  targetLocation: {
    lat: number;
    lng: number;
  };
}

export interface SimulationResult {
  craterDiameter: number;
  affectedArea: number;
  energyRelease: number; // megatons
  tsunamiRisk: boolean;
}
