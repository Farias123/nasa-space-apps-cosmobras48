import { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Asteroid, ThreatLevel } from '@/types/asteroid';
import { Rocket, Plus } from 'lucide-react';
import { toast } from 'sonner';

interface AsteroidFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (asteroid: Asteroid) => void;
}

export const AsteroidForm = ({ open, onOpenChange, onSubmit }: AsteroidFormProps) => {
  const [formData, setFormData] = useState({
    name: '',
    size: '',
    velocity: '',
    orbit: '',
    distance: '',
    threatLevel: 'safe' as ThreatLevel,
    description: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.size || !formData.velocity || !formData.orbit || !formData.distance) {
      toast.error('Preencha todos os campos obrigatórios');
      return;
    }

    const newAsteroid: Asteroid = {
      id: `custom-${Date.now()}`,
      name: formData.name,
      size: parseFloat(formData.size),
      velocity: parseFloat(formData.velocity),
      orbit: formData.orbit,
      distance: parseFloat(formData.distance),
      threatLevel: formData.threatLevel,
      discoveryDate: new Date().toISOString(),
      nextApproach: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(),
      description: formData.description,
      isFavorite: false,
    };

    onSubmit(newAsteroid);
    toast.success('Asteroide cadastrado com sucesso!');
    setFormData({
      name: '',
      size: '',
      velocity: '',
      orbit: '',
      distance: '',
      threatLevel: 'safe',
      description: '',
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl font-bold gradient-text flex items-center gap-2">
            <Rocket className="h-6 w-6" />
            Cadastrar Novo Asteroide
          </DialogTitle>
          <DialogDescription>
            Insira os dados do asteroide para iniciar o monitoramento
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6 mt-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2 col-span-2">
              <Label htmlFor="name">Nome do Asteroide *</Label>
              <Input
                id="name"
                placeholder="Ex: Apophis"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="size">Tamanho (metros) *</Label>
              <Input
                id="size"
                type="number"
                placeholder="Ex: 370"
                value={formData.size}
                onChange={(e) => setFormData({ ...formData, size: e.target.value })}
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="velocity">Velocidade (km/s) *</Label>
              <Input
                id="velocity"
                type="number"
                step="0.1"
                placeholder="Ex: 7.4"
                value={formData.velocity}
                onChange={(e) => setFormData({ ...formData, velocity: e.target.value })}
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="orbit">Tipo de Órbita *</Label>
              <Select
                value={formData.orbit}
                onValueChange={(value) => setFormData({ ...formData, orbit: value })}
              >
                <SelectTrigger className="bg-input/50 border-border/50 focus:border-primary">
                  <SelectValue placeholder="Selecione o tipo" />
                </SelectTrigger>
                <SelectContent className="glass-card border-primary/30">
                  <SelectItem value="Apollo">Apollo</SelectItem>
                  <SelectItem value="Aten">Aten</SelectItem>
                  <SelectItem value="Amor">Amor</SelectItem>
                  <SelectItem value="Atira">Atira</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="distance">Distância (milhões de km) *</Label>
              <Input
                id="distance"
                type="number"
                step="0.01"
                placeholder="Ex: 0.19"
                value={formData.distance}
                onChange={(e) => setFormData({ ...formData, distance: e.target.value })}
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="threatLevel">Nível de Ameaça</Label>
              <Select
                value={formData.threatLevel}
                onValueChange={(value) => setFormData({ ...formData, threatLevel: value as ThreatLevel })}
              >
                <SelectTrigger className="bg-input/50 border-border/50 focus:border-primary">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="glass-card border-primary/30">
                  <SelectItem value="safe">Seguro</SelectItem>
                  <SelectItem value="low">Baixo</SelectItem>
                  <SelectItem value="medium">Médio</SelectItem>
                  <SelectItem value="high">Alto</SelectItem>
                  <SelectItem value="critical">Crítico</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2 col-span-2">
              <Label htmlFor="description">Descrição (opcional)</Label>
              <Textarea
                id="description"
                placeholder="Adicione informações adicionais sobre o asteroide..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="bg-input/50 border-border/50 focus:border-primary min-h-[100px]"
              />
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              className="flex-1 border-border/50"
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground"
            >
              <Plus className="h-4 w-4 mr-2" />
              Cadastrar Asteroide
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};
