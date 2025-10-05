// Tipos para Close Approach (Asteroides) - compatível com backend
export interface CelestialBodyCloseApproachData {
  designation: string;        // ao invés de 'name'
  close_approach_date: string; // ao invés de 'nextApproach'
  distance_au: string;       // ao invés de 'distance' (number)
  velocity_kms: string;      // ao invés de 'velocity' (number)
}

// Tipos para Horizon Data (Planetas) - compatível com backend
export type Planet = 'Mercury' | 'Venus' | 'Earth' | 'Mars' | 'Jupiter' | 'Saturn' | 'Uranus' | 'Neptune' | 'Sun';

export interface HorizonData {
  mass?: number;
  radius?: number;
  x?: number[];
  y?: number[];
  z?: number[];
  vx?: number[];
  vy?: number[];
  vz?: number[];
  dates?: string[];
}

export interface HorizonDataResponse {
  body_name?: Planet;
  horizon_data: HorizonData;
  metadata: {
    units: {
      distance: string;
      mass: string;
      velocity: string;
    };
  };
}

// Manter tipos de simulação (podem ser adaptados depois)
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
