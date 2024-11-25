// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Genetic Algorithm, Evolving Shakespeare

// A class to describe a pseudo-DNA, i.e. genotype
//   Here, a virtual organism's DNA is an array of character.
//   Functionality:
//      -- convert DNA into a string
//      -- calculate DNA's "fitness"
//      -- mate DNA with another set of DNA
//      -- mutate DNA

function newChar() {
    let c = floor(random(63, 123));
    if (c === 63) c = 32;
    if (c === 64) c = 46;

    return String.fromCharCode(c);
}

// Constructor (makes a random DNA)
class DNA {
    constructor(num) {
        // The genetic sequence
        this.genes = [];
        this.fitness = 0;
        for (let i = 0; i < num; i++) {
            this.genes[i] = newChar(); // Pick from range of chars
        }
    }

    // Converts character array to a String
    getPhrase() {
        return this.genes.join("");
    }

    // Fitness function (returns floating point % of "correct" characters)
    calcFitness(target) {
        let score = 0;
        for (let i = 0; i < this.genes.length; i++) {
            if (this.genes[i] == target.charAt(i)) {
                score++;
            }
        }
        this.fitness = score / target.length;
    }

    // Crossover
    crossover(partner) {
        // A new child
        let child = new DNA(this.genes.length);

        let midpoint = floor(random(this.genes.length)); // Pick a midpoint

        // Half from one, half from the other
        for (let i = 0; i < this.genes.length; i++) {
            if (i > midpoint) child.genes[i] = this.genes[i];
            else child.genes[i] = partner.genes[i];
        }
        return child;
    }

    // Based on a mutation probability, picks a new random character
    mutate(mutationRate) {
        for (let i = 0; i < this.genes.length; i++) {
            if (random(1) < mutationRate) {
                this.genes[i] = newChar();
            }
        }
    }
}


// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Genetic Algorithm, Evolving Shakespeare

// A class to describe a population of virtual organisms
// In this case, each organism is just an instance of a DNA object

class Population {
    constructor(p, m, num) {

        this.population; // Array to hold the current population
        this.matingPool; // ArrayList which we will use for our "mating pool"
        this.generations = 0; // Number of generations
        this.finished = false; // Are we finished evolving?
        this.target = p; // Target phrase
        this.mutationRate = m; // Mutation rate
        this.perfectScore = 1;

        this.best = "";

        this.population = [];
        for (let i = 0; i < num; i++) {
            this.population[i] = new DNA(this.target.length);
        }
        this.matingPool = [];
        this.calcFitness();
    }

    // Fill our fitness array with a value for every member of the population
    calcFitness() {
        for (let i = 0; i < this.population.length; i++) {
            this.population[i].calcFitness(this.target);
        }
    }    

    // Generate a mating pool
    naturalSelection() {
        // Clear the ArrayList
        this.matingPool = [];

        let maxFitness = 0;
        for (let i = 0; i < this.population.length; i++) {
            if (this.population[i].fitness > maxFitness) {
                maxFitness = this.population[i].fitness;
            }
        }

        // Debugging: Check if maxFitness is zero
        if (maxFitness === 0) {
            console.error('Maximum fitness is 0. There might be an issue with fitness calculation.');
            return;
        }

        for (let i = 0; i < this.population.length; i++) {
            let fitnessNormal = map(this.population[i].fitness, 0, maxFitness, 0, 1);
            let n = floor(fitnessNormal * 100);

            // Debugging: Log fitness and scaled fitness
            // console.log(`Member ${i}: Fitness = ${this.population[i].fitness}, Scaled Fitness = ${fitnessNormal}, N = ${n}`);

            for (let j = 0; j < n; j++) {
                this.matingPool.push(this.population[i]);
            }
        }

        // Debugging: Log the size of the mating pool
        // console.log(`Mating Pool Size: ${this.matingPool.length}`);
    }


    // Create a new generation
    generate() {
        // Check if mating pool is empty
        if (this.matingPool.length === 0) {
            console.error('Mating pool is empty');
            return;
        }

        for (let i = 0; i < this.population.length; i++) {
            let a = floor(random() * this.matingPool.length);
            let b = floor(random() * this.matingPool.length);
            let partnerA = this.matingPool[a];
            let partnerB = this.matingPool[b];

            // Debugging logs
            // console.log(`Mating Pool Size: ${this.matingPool.length}, Indices: a=${a}, b=${b}`);

            if (!partnerA || !partnerB) {
                console.error('Undefined partner found', { partnerA, partnerB });
                continue;
            }

            let child = partnerA.crossover(partnerB);
            child.mutate(this.mutationRate);
            this.population[i] = child;
        }
        this.generations++;
    }



    getBest() {
        return this.best;
    }

    // Compute the current "most fit" member of the population
    evaluate() {
        let worldrecord = 0.0;
        let index = 0;
        for (let i = 0; i < this.population.length; i++) {
            if (this.population[i].fitness > worldrecord) {
                index = i;
                worldrecord = this.population[i].fitness;
            }
        }

        this.best = this.population[index].getPhrase();
        if (worldrecord === this.perfectScore) {
            this.finished = true;
        }
    }

    isFinished() {
        return this.finished;
    }

    getGenerations() {
        return this.generations;
    }

    // Compute average fitness for the population
    getAverageFitness() {
        let total = 0;
        for (let i = 0; i < this.population.length; i++) {
            total += this.population[i].fitness;
        }
        return total / (this.population.length);
    }

    allPhrases() {
        let everything = "";

        let displayLimit = min(this.population.length, 51);

        for (let i = 0; i < displayLimit; i++) {
            everything += this.population[i].getPhrase();
            if (i % 3 == 2) everything += "\n";
            else everything += " ";
        }
        return everything;
    }
}


// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

// Genetic Algorithm, Evolving Shakespeare

// Demonstration of using a genetic algorithm to perform a search

// setup()
//  # Step 1: The Population
//    # Create an empty population (an array or ArrayList)
//    # Fill it with DNA encoded objects (pick random values to start)

// draw()
//  # Step 1: Selection
//    # Create an empty mating pool (an empty ArrayList)
//    # For every member of the population, evaluate its fitness based on some criteria / function,
//      and add it to the mating pool in a manner consistant with its fitness, i.e. the more fit it
//      is the more times it appears in the mating pool, in order to be more likely picked for reproduction.

//  # Step 2: Reproduction Create a new empty population
//    # Fill the new population by executing the following steps:
//       1. Pick two "parent" objects from the mating pool.
//       2. Crossover -- create a "child" object by mating these two parents.
//       3. Mutation -- mutate the child's DNA based on a given probability.
//       4. Add the child object to the new population.
//    # Replace the old population with the new population
//
//   # Rinse and repeat

let target;
let popmax;
let mutationRate;
let population;

let bestPhrase;
let allPhrases;
let stats;

function setup() {
    createCanvas(640, 240);
    //createCanvas(640, 360);
    target = "Knowledge is everything";
    popmax = 200;
    mutationRate = 0.01;

    // Create a population with a target phrase, mutation rate, and population max
    population = new Population(target, mutationRate, popmax);
}

function draw() {
    // Generate mating pool
    population.naturalSelection();
    //Create next generation
    population.generate();
    // Calculate fitness
    population.calcFitness();

    population.evaluate();

    // If we found the target phrase, stop
    if (population.isFinished()) {
        //println(millis()/1000.0);
        noLoop();
    }
    background(255);
    let answer = population.getBest();
    fill(0);
    textFont("Courier");
    textSize(12);
    text("Best phrase:", 10, 32);
    textSize(24);
    text(answer, 10, 64);
    let statstext =
        "total generations:     " + population.getGenerations() + "\n";
    statstext +=
        "average fitness:       " + nf(population.getAverageFitness(), 0, 2) + "\n";
    statstext += "total population:      " + popmax + "\n";
    statstext += "mutation rate:         " + floor(mutationRate * 100) + "%";

    textSize(12);
    text(statstext, 10, 96);
    textSize(8);
    text(population.allPhrases(), width / 2, 24);
}
