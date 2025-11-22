// 1. የቀመሮች ዳታቤዝ (32 ቀመሮች)
const formulas = [
    // --- Algebra / General Math ---
    { name: "Quadratic Formula", formula: "x = [-b ± sqrt(b²-4ac)] / 2a", category: "algebra" },
    { name: "Slope Intercept Form", formula: "y = mx + b", category: "algebra" },
    { name: "Distance Formula (3D)", formula: "d = sqrt((x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²)", category: "algebra" },
    { name: "Compound Interest", formula: "A = P(1 + r/n)^(nt)", category: "algebra" },
    { name: "Logarithm Change of Base", formula: "logₐ(b) = logₓ(b) / logₓ(a)", category: "algebra" },
    { name: "Arithmetic Series Sum", formula: "Sₙ = n/2 * (a₁ + aₙ)", category: "algebra" },
    { name: "Geometric Series Sum", formula: "Sₙ = a₁ * (1 - rⁿ) / (1 - r)", category: "algebra" },
    
    // --- Geometry / Trigonometry ---
    { name: "Pythagorean Theorem", formula: "a² + b² = c²", category: "geometry" },
    { name: "Area of a Circle", formula: "A = πr²", category: "geometry" },
    { name: "Area of a Triangle (Heron's Formula)", formula: "A = sqrt(s(s-a)(s-b)(s-c)), where s = (a+b+c)/2", category: "geometry" },
    { name: "Law of Sines", formula: "a/sin(A) = b/sin(B) = c/sin(C)", category: "geometry" },
    { name: "Law of Cosines", formula: "c² = a² + b² - 2ab cos(C)", category: "geometry" },
    { name: "Volume of a Sphere", formula: "V = (4/3)πr³", category: "geometry" },
    
    // --- Physics / Advanced Mechanics ---
    { name: "Newton's Second Law", formula: "F = ma", category: "physics" },
    { name: "Kinetic Energy", formula: "KE = ½mv²", category: "physics" },
    { name: "Mass-Energy Equivalence", formula: "E = mc²", category: "physics" }, 
    { name: "Lorentz Factor", formula: "γ = 1 / sqrt(1 - v²/c²)", category: "physics" }, 
    { name: "Gravitational Force", formula: "F = G(m₁m₂ / r²)", category: "physics" },
    { name: "Ohm's Law (Electricity)", formula: "V = IR", category: "physics" },
    { name: "Work Done", formula: "W = Fd cos(θ)", category: "physics" }, 

    // --- Calculus / Differential Equations ---
    { name: "Derivative Power Rule", formula: "d/dx (xⁿ) = nxⁿ⁻¹", category: "calculus" },
    { name: "Product Rule (Derivative)", formula: "(fg)' = f'g + fg'", category: "calculus" },
    { name: "Integration by Parts", formula: "∫u dv = uv - ∫v du", category: "calculus" },
    { name: "Chain Rule", formula: "d/dx f(g(x)) = f'(g(x))g'(x)", category: "calculus" },
    
    // --- Chemistry / Thermodynamics ---
    { name: "Ideal Gas Law", formula: "PV = nRT", category: "chemistry" },
    { name: "Gibbs Free Energy", formula: "∆G = ∆H - T∆S", category: "chemistry" },
    { name: "pH Calculation", formula: "pH = -log₁₀[H⁺]", category: "chemistry" },
    { name: "Boyle's Law", formula: "P₁V₁ = P₂V₂", category: "chemistry" },
    { name: "Molarity", formula: "M = moles of solute / liters of solution", category: "chemistry" },
    
    // --- Statistics ---
    { name: "Standard Deviation", formula: "σ = sqrt(Σ(xᵢ - μ)² / N)", category: "statistics" },
    { name: "Z-Score", formula: "z = (x - μ) / σ", category: "statistics" },
    { name: "Probability (Binomial)", formula: "P(k) = C(n, k) * pᵏ * (1-p)ⁿ⁻ᵏ", category: "statistics" }
];


const formulaList = document.getElementById('formula-list');
const searchInput = document.getElementById('search-input');
const categoryButtonsContainer = document.getElementById('category-buttons'); 
let activeCategory = 'all'; 


function displayFormulas(data) {
    formulaList.innerHTML = ''; 
    
    if (data.length === 0) {
        const noResultsMessage = document.createElement('p');
        noResultsMessage.textContent = "No formulas found. Try a different search or category.";
        noResultsMessage.style.textAlign = "center";
        noResultsMessage.style.marginTop = "20px";
        noResultsMessage.style.color = "#BDC3C7";
        formulaList.appendChild(noResultsMessage);
        return; 
    }

    data.forEach(formula => {
        const card = document.createElement('div');
        card.classList.add('formula-card');
        
        card.innerHTML = `
            <h3>${formula.name}</h3>
            <p><strong>Category:</strong> ${formula.category.charAt(0).toUpperCase() + formula.category.slice(1)}</p>
            <p>Formula: ${formula.formula}</p>
        `;
        formulaList.appendChild(card);
    });
}


function filterFormulas() {
    const searchTerm = searchInput.value.toLowerCase();
    
    const filteredFormulas = formulas.filter(formula => {
        const matchesSearch = formula.name.toLowerCase().includes(searchTerm) || 
                              formula.formula.toLowerCase().includes(searchTerm);
        
        const matchesCategory = activeCategory === 'all' || formula.category === activeCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    displayFormulas(filteredFormulas);
}


function shareApp() {
    const appUrl = "https://akalewold15-cloud.github.io/All-formulas2/"; 
    const shareText = "I found the ultimate formula finder! Check out Akalewold Formula Finder for all your study needs! Share this link: " + appUrl;
    
    if (navigator.share) {
        navigator.share({
            title: 'Akalewold Formula Finder',
            text: shareText,
            url: appUrl,
        }).catch((error) => console.log('Error sharing', error));
    } else {
        prompt("Copy this link to share the app:", appUrl);
    }
}


document.addEventListener('DOMContentLoaded', () => {

    // Modal ሎጂክ 
    const inviteCard = document.getElementById('invite-card');
    const modal = document.getElementById('user-modal');
    const closeButton = modal ? modal.querySelector('.close-button') : null; 

    // Invite Card ሲነካ Modal (ማብራሪያ) እንዲከፍት
    if (inviteCard && modal) {
        inviteCard.addEventListener('click', () => {
            modal.style.display = 'block';
        });
    }

    // Modal እንዲዘጋ
    if (closeButton && modal) {
        closeButton.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Modal እንዲዘጋ (ከ Modal ውጭ ሲነካ)
    window.addEventListener('click', (event) => {
        if (modal && event.target === modal) {
            modal.style.display = 'none';
        }
    });

    
    displayFormulas(formulas);
    
    searchInput.addEventListener('input', filterFormulas);
    
    categoryButtonsContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('cat-button')) {
            document.querySelectorAll('.cat-button').forEach(button => {
                button.classList.remove('active');
            });
            
            event.target.classList.add('active');
            
            activeCategory = event.target.dataset.category;
            
            filterFormulas();
        }
    });
});
