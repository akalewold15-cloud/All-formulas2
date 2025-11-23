// 🛑 ፎርሙላዎቹ ከformulas_data.js ይጫናሉ 🛑
// formulaData አሁን ከformulas_data.js ፋይል ይገኛል
const formulaData = typeof formulas !== 'undefined' ? formulas : [];


const formulaList = document.getElementById('formula-list');
const searchInput = document.getElementById('search-input');
const categoryButtonsContainer = document.getElementById('category-buttons'); 
let activeCategory = 'all'; 


function displayFormulas(data) {
    formulaList.innerHTML = ''; 
    
    // የፎርሙላዎችን ቁጥር በ stat-card ላይ ማሳያ
    const countDisplay = document.getElementById('formula-count-display');
    if (countDisplay) {
        if (data.length === formulaData.length) {
            countDisplay.textContent = `${formulaData.length} Formulas Loaded`;
        } else {
            countDisplay.textContent = `${data.length} Results Found`;
        }
    }
    
    if (data.length === 0) {
        const noResultsMessage = document.createElement('p');
        noResultsMessage.textContent = "No formulas found. Try a different search or category.";
        noResultsMessage.style.textAlign = "center";
        noResultsMessage.style.marginTop = "20px";
        noResultsMessage.style.color = "#9cb3c9";
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
    
    const filteredFormulas = formulaData.filter(formula => {
        const matchesSearch = formula.name.toLowerCase().includes(searchTerm) || 
                              formula.formula.toLowerCase().includes(searchTerm);
        
        const matchesCategory = activeCategory === 'all' || formula.category === activeCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    displayFormulas(filteredFormulas);
}


function shareApp() {
    // ንጹህ የGitHub Pages URL
    const appUrl = "https://akalewold15-cloud.github.io/All-formulas2/"; 
    const shareText = "I found the ultimate formula finder! Check out Akalewold Formula Finder for all your study needs! Share this link: " + appUrl;
    
    if (navigator.share) {
        navigator.share({
            title: 'Akalewold Formula Finder',
            text: shareText,
            url: appUrl,
        }).catch((error) => console.log('Error sharing', error));
    } else {
        // ለኮምፒውተር ተጠቃሚዎች
        prompt("Copy this link to share the app:", appUrl);
    }
}


document.addEventListener('DOMContentLoaded', () => {

    // አፕሊኬሽኑ ሲከፈት ወዲያውኑ 1000 ፎርሙላዎችን ያሳያል
    displayFormulas(formulaData);
    
    // Modal ሎጂክ እና Event Listeners
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
