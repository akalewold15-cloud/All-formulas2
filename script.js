// 1. የቀመሮች ዳታቤዝ (አዲስ የምድብ መረጃን ያካተተ)
const formulas = [
    // --- Algebra ---
    { name: "Quadratic Formula", formula: "x = [-b ± sqrt(b²-4ac)] / 2a", category: "algebra" },
    { name: "Slope Intercept Form", formula: "y = mx + b", category: "algebra" },
    { name: "Factoring Difference of Squares", formula: "a² - b² = (a - b)(a + b)", category: "algebra" },
    { name: "Factoring Perfect Square Trinomial", formula: "a² + 2ab + b² = (a + b)²", category: "algebra" },
    { name: "Distance Formula", formula: "d = sqrt((x₂ - x₁)² + (y₂ - y₁)²)", category: "algebra" },
    
    // --- Geometry ---
    { name: "Pythagorean Theorem", formula: "a² + b² = c²", category: "geometry" },
    { name: "Area of a Circle", formula: "A = πr²", category: "geometry" },
    { name: "Circumference of a Circle", formula: "C = 2πr", category: "geometry" },
    { name: "Area of a Triangle", formula: "A = ½bh", category: "geometry" },
    { name: "Area of a Rectangle", formula: "A = lw", category: "geometry" },
    { name: "Volume of a Rectangular Prism", formula: "V = lwh", category: "geometry" },
    
    // --- Physics / Mechanics ---
    { name: "Newton's Second Law", formula: "F = ma", category: "physics" },
    { name: "Velocity Formula", formula: "v = d / t", category: "physics" },
    { name: "Kinetic Energy", formula: "KE = ½mv²", category: "physics" },
    { name: "Potential Energy (Gravity)", formula: "PE = mgh", category: "physics" },
    { name: "Work Done", formula: "W = Fd cos(θ)", category: "physics" },
    { name: "Ohm's Law (Electricity)", formula: "V = IR", category: "physics" },
    
    // --- Calculus ---
    { name: "Derivative of x^n", formula: "d/dx (x^n) = nx^(n-1)", category: "calculus" },
    { name: "Power Rule (Integration)", formula: "∫xⁿ dx = (xⁿ⁺¹)/(n+1) + C, n ≠ -1", category: "calculus" },
    { name: "Product Rule (Derivative)", formula: "(fg)' = f'g + fg'", category: "calculus" },
    { name: "Quotient Rule (Derivative)", formula: "(f/g)' = (f'g - fg') / g²", category: "calculus" },

    // --- Chemistry ---
    { name: "Density Formula", formula: "ρ = m / V", category: "chemistry" },
    { name: "Molar Mass (General)", formula: "M = m / n", category: "chemistry" },
    { name: "Ideal Gas Law", formula: "PV = nRT", category: "chemistry" },
    { name: "Molarity", formula: "Molarity = Moles of Solute / Liters of Solution", category: "chemistry" },
    
    // የድሮው ኮድህ እዚህ ይጨመራል...
    // { name: "..." , formula: "...", category: "..." }
];

const formulaList = document.getElementById('formula-list');
const searchInput = document.getElementById('search-input');
const categoryFilter = document.getElementById('category-filter');

// 2. ቀመሮችን የሚያሳይ ዋና ተግባር (ተመሳሳይ ነው)
function displayFormulas(data) {
    formulaList.innerHTML = ''; 
    
    data.forEach(formula => {
        const card = document.createElement('div');
        card.classList.add('formula-card');
        
        // ምድቡን ካርዱ ላይ እንዲያሳይ ተደርጓል
        card.innerHTML = `
            <h3>${formula.name}</h3>
            <p><strong>Category:</strong> ${formula.category.charAt(0).toUpperCase() + formula.category.slice(1)}</p>
            <p>Formula: ${formula.formula}</p>
        `;
        formulaList.appendChild(card);
    });
}

// 3. የፍለጋ እና የማጣራት ሎጂክ (ተመሳሳይ ነው)
function filterFormulas() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    // በሁለቱም ፍለጋ እና ምድብ ማጣራት
    const filteredFormulas = formulas.filter(formula => {
        const matchesSearch = formula.name.toLowerCase().includes(searchTerm) || 
                              formula.formula.toLowerCase().includes(searchTerm);
        
        const matchesCategory = selectedCategory === 'all' || formula.category === selectedCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    displayFormulas(filteredFormulas);
}

// የፍለጋ እና የምድብ ለውጥ በሚኖርበት ጊዜ ማጣሪያውን ማስኬድ
searchInput.addEventListener('input', filterFormulas);
categoryFilter.addEventListener('change', filterFormulas);

// ገጹ ሲከፈት ሁሉንም ቀመሮች ማሳየት
document.addEventListener('DOMContentLoaded', () => {
    displayFormulas(formulas);
});
