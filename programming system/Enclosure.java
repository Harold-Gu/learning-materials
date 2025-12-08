package petcare;

public class Enclosure {
    private AnimalSize size;
    private int temperature;
    private int runningCosts;
    private Animal occupant; // [cite: 99]

    // Task 2a: Constructor [cite: 102]
    public Enclosure(AnimalSize size, int temperature, int runningCosts) {
        this.size = size;
        this.temperature = temperature;
        this.runningCosts = runningCosts;
        this.occupant = null; // Set occupant to null
    }

    // Task 2a: Getters only, no setters [cite: 103]
    public AnimalSize getSize() { return size; }
    public int getTemperature() { return temperature; }
    public int getRunningCosts() { return runningCosts; }
    public Animal getOccupant() { return occupant; }

    // Task 2b: checkCompatibility [cite: 105]
    public boolean checkCompatibility(Animal animal) {
        if (animal == null) return false;

        // Check size: Animal must be same size or smaller than enclosure [cite: 108]
        // Using ordinal(): SMALL=0, MEDIUM=1, LARGE=2. Animal <= Enclosure
        boolean sizeCompatible = animal.getSize().ordinal() <= this.size.ordinal();

        // Check temperature: Enclosure temp must fall within animal's range [cite: 108]
        boolean tempCompatible = this.temperature >= animal.getLowerTemp() && 
                                 this.temperature <= animal.getUpperTemp();

        return sizeCompatible && tempCompatible;
    }

    // Task 2c: addAnimal [cite: 111]
    public void addAnimal(Animal animal) {
        if (this.occupant != null) {
            throw new IllegalArgumentException("Enclosure is already occupied.");
        }
        if (checkCompatibility(animal)) {
            this.occupant = animal; // Add animal [cite: 113]
        } else {
            throw new IllegalArgumentException("Animal is not compatible with this enclosure."); [cite: 114]
        }
    }

    // Task 2c: removeAnimal [cite: 112]
    public void removeAnimal() {
        // If empty, nothing happens [cite: 115]
        this.occupant = null; 
    }
    
    @Override
    public String toString() {
        return "Enclosure{size=" + size + ", temp=" + temperature + 
               ", cost=" + runningCosts + ", occupant=" + occupant + "}";
    }
}