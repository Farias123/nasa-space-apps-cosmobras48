# ImpactSimulationCard Component

## Visão Geral

O `ImpactSimulationCard` é um componente React unificado que combina funcionalidades de simulação de impacto e visualização de trajetória usando React Three Fiber (@react-three/fiber) e @react-three/drei.

## Estrutura Modular

### 1. **Tipos** (`/types/impactSimulation.ts`)
- `ImpactSimulationProps`: Props do componente principal
- `ImpactSimulationState`: Estado da simulação (animação, progresso, posições)
- `AsteroidTrajectory`: Dados da trajetória (posições inicial, final e pontos de controle)

### 2. **Hook** (`/hooks/useImpactSimulation.ts`)
- Lógica de animação com `requestAnimationFrame`
- Cálculo de trajetória Bézier baseada nos dados do asteroide
- Funções de controle (iniciar, reiniciar, exportar)
- Estado reativo da simulação

### 3. **Componentes**

#### **ImpactScene** (`/components/ImpactScene.tsx`)
- Renderização 3D com React Three Fiber
- Terra como esfera azul em (0,0,0)
- Asteroide com tamanho proporcional à velocidade
- Trajetória curva visualizada como linha laranja
- Eixos x, y, z visíveis
- Controles de câmera (rotação, zoom, pan)

#### **ImpactControls** (`/components/ImpactControls.tsx`)
- Interface de usuário com informações do asteroide
- Botões de controle (Iniciar, Reiniciar, Exportar)
- Status da simulação em tempo real
- Progresso da animação

#### **ImpactSimulationCard** (`/components/ImpactSimulationCard.tsx`)
- Componente principal que unifica tudo
- Dialog modal responsivo
- Layout em grid com cena 3D e controles
- Informações detalhadas da simulação

## Funcionalidades

### ✅ **Implementadas**
- Visualização 3D da Terra e asteroide
- Trajetória curva usando Bézier
- Animação suave do asteroide até o impacto
- Controles de câmera interativos
- Exportação de dados em JSON
- Interface responsiva
- Integração com dados do backend

### 🔄 **Pendentes**
- Exportação PNG (placeholder implementado)
- Texturas mais realistas
- Efeitos visuais de impacto
- Múltiplas trajetórias
- Parâmetros de simulação ajustáveis

## Uso

```tsx
import { ImpactSimulationCard } from '@/components/ImpactSimulationCard';

<ImpactSimulationCard
  asteroid={asteroidData}
  open={isOpen}
  onOpenChange={setIsOpen}
/>
```

## Dependências

- `@react-three/fiber`: Renderização 3D
- `@react-three/drei`: Componentes 3D auxiliares
- `react`: Framework base
- `typescript`: Tipagem
- `tailwindcss`: Estilização

## Compatibilidade

- ✅ Compatível com estrutura de dados do backend
- ✅ Usa `CelestialBodyCloseApproachData`
- ✅ Integrado com `AsteroidDetails`
- ✅ Design consistente com sistema existente
