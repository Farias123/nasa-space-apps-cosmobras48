import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CelestialBodyCloseApproachData } from "@/types/asteroid";
import { Rocket, Plus } from "lucide-react";
import { toast } from "sonner";

interface AsteroidFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (asteroid: CelestialBodyCloseApproachData) => void;
}

export const AsteroidForm = ({
  open,
  onOpenChange,
  onSubmit,
}: AsteroidFormProps) => {
  const [formData, setFormData] = useState({
    designation: "",
    velocity_kms: "",
    distance_au: "",
    close_approach_date: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

        if (
          !formData.designation ||
          !formData.velocity_kms ||
          !formData.distance_au ||
          !formData.close_approach_date
        ) {
          toast.error("Please fill in all required fields");
          return;
        }

    const newAsteroid: CelestialBodyCloseApproachData = {
      designation: formData.designation,
      velocity_kms: formData.velocity_kms,
      distance_au: formData.distance_au,
      close_approach_date: formData.close_approach_date,
    };

        onSubmit(newAsteroid);
        toast.success("Asteroid registered successfully!");
        setFormData({
          designation: "",
          velocity_kms: "",
          distance_au: "",
          close_approach_date: "",
        });
        onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="glass-card border-primary/30 max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
              <DialogTitle className="text-2xl font-bold gradient-text flex items-center gap-2">
                <Rocket className="h-6 w-6" />
                Register New Asteroid
              </DialogTitle>
              <DialogDescription>
                Enter asteroid data to start monitoring
              </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6 mt-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2 col-span-2">
              <Label htmlFor="designation">Asteroid Designation *</Label>
              <Input
                id="designation"
                placeholder="Ex: Apophis"
                value={formData.designation}
                onChange={(e) =>
                  setFormData({ ...formData, designation: e.target.value })
                }
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="velocity_kms">Velocity (km/s) *</Label>
              <Input
                id="velocity_kms"
                type="text"
                placeholder="Ex: 7.4"
                value={formData.velocity_kms}
                onChange={(e) =>
                  setFormData({ ...formData, velocity_kms: e.target.value })
                }
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="distance_au">Distance (AU) *</Label>
              <Input
                id="distance_au"
                type="text"
                placeholder="Ex: 0.19"
                value={formData.distance_au}
                onChange={(e) =>
                  setFormData({ ...formData, distance_au: e.target.value })
                }
                className="bg-input/50 border-border/50 focus:border-primary"
              />
            </div>

            <div className="space-y-2 col-span-2">
              <Label htmlFor="close_approach_date">Approach Date *</Label>
              <Input
                id="close_approach_date"
                type="date"
                value={formData.close_approach_date}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    close_approach_date: e.target.value,
                  })
                }
                className="bg-input/50 border-border/50 focus:border-primary"
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
                  Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground"
            >
              <Plus className="h-4 w-4 mr-2" />
              Register Asteroid
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};
