// Tipos para Close Approach (Asteroides) 
export interface CelestialBodyCloseApproachData {
  designation: string;       
  close_approach_date: string; 
  distance_au: string;      
  velocity_kms: string;      
}

// Tipos para Horizon Data (Planetas) 
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
