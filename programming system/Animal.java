package petcare;

import java.util.Objects;

public class Animal {
    private String name;
    private AnimalSize size;
    private int lowerTemp;
    private int upperTemp;

    // Task 1a: Constructor [cite: 87]
    public Animal(String name, AnimalSize size, int lowerTemp, int upperTemp) {
        validateInputs(name, lowerTemp, upperTemp); // Task 1c validation
        this.name = name;
        this.size = size;
        this.lowerTemp = lowerTemp;
        this.upperTemp = upperTemp;
    }

    // Task 1c: Validation Logic [cite: 92]
    private void validateInputs(String name, int lower, int upper) {
        // Name must be at least 3 chars [cite: 80]
        if (name == null || name.length() < 3) {
            throw new IllegalArgumentException("Name must be at least 3 characters long."); [cite: 93]
        }
        // Temp range 0 to 50 [cite: 83]
        if (lower < 0 || lower > 50 || upper < 0 || upper > 50 || lower > upper) {
            throw new IllegalArgumentException("Temperature values must be between 0 and 50, and lower must be <= upper."); [cite: 93]
        }
    }
    
    // Task 1b: Getters and Setters [cite: 89]
    public String getName() { return name; }
    
    public void setName(String name) {
        if (name == null || name.length() < 3) throw new IllegalArgumentException("Invalid name");
        this.name = name;
    }

    public AnimalSize getSize() { return size; }
    
    public void setSize(AnimalSize size) { this.size = size; }

    public int getLowerTemp() { return lowerTemp; }
    
    public void setLowerTemp(int lowerTemp) {
        if (lowerTemp < 0 || lowerTemp > 50 || lowerTemp > this.upperTemp) throw new IllegalArgumentException("Invalid temp");
        this.lowerTemp = lowerTemp;
    }

    public int getUpperTemp() { return upperTemp; }
    
    public void setUpperTemp(int upperTemp) {
        if (upperTemp < 0 || upperTemp > 50 || upperTemp < this.lowerTemp) throw new IllegalArgumentException("Invalid temp");
        this.upperTemp = upperTemp;
    }

    // Task 1b: toString [cite: 89]
    @Override
    public String toString() {
        return "Animal{name='" + name + "', size=" + size + "}";
    }

    // Task 1b: equals and hashCode [cite: 90]
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Animal animal = (Animal) o;
        // True when size and name are same [cite: 90]
        return size == animal.size && Objects.equals(name, animal.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, size);
    }
}