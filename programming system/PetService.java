package petcare;

import java.util.ArrayList;
import java.util.List;

public class PetService {
    // Task 3a: Collection of enclosures [cite: 120]
    private List<Enclosure> enclosures;

    public PetService() {
        this.enclosures = new ArrayList<>();
    }

    // Task 3b: addEnclosure [cite: 123]
    public void addEnclosure(Enclosure enclosure) {
        this.enclosures.add(enclosure);
    }

    // Task 3b: printAllEnclosures [cite: 126]
    public void printAllEnclosures() {
        for (Enclosure e : enclosures) {
            System.out.println(e.toString());
        }
    }

    // Task 3c: allocateAnimal [cite: 130]
    public boolean allocateAnimal(Animal animal) {
        Enclosure bestEnclosure = null;
        
        for (Enclosure e : enclosures) {
            // Check criteria: compatible and empty [cite: 132, 133]
            if (e.getOccupant() == null && e.checkCompatibility(animal)) {
                // Logic for cheapest [cite: 134]
                if (bestEnclosure == null || e.getRunningCosts() < bestEnclosure.getRunningCosts()) {
                    bestEnclosure = e;
                }
            }
        }

        if (bestEnclosure != null) {
            bestEnclosure.addAnimal(animal);
            return true; [cite: 134]
        }
        
        return false; [cite: 135]
    }

    // Task 3d: removeAnimal [cite: 138]
    public void removeAnimal(Animal animal) {
        boolean found = false;
        
        // Search for matching animal [cite: 139]
        for (Enclosure e : enclosures) {
            if (e.getOccupant() != null && e.getOccupant().equals(animal)) {
                e.removeAnimal(); // Remove from enclosure [cite: 140]
                found = true;
                break; // Assuming unique animals, we can stop
            }
        }

        if (!found) {
            throw new IllegalArgumentException("Animal not found in the service."); [cite: 141]
        }
    }
}