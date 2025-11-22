/* ---- 🛑 የመጨረሻ ማስተካከያ: Simple & Compact Dark Theme 🛑 ---- */

body {
    /* በጣም ቀላል ጥቁር ዳራ */
    background-color: #2c3e50; 
    color: #ECF0F1; 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    padding: 10px; 
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    overflow-x: hidden; 
}

#app-container {
    background-color: #34495e; 
    border-radius: 12px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
    padding: 15px; 
    max-width: 550px; 
    width: 100%;
    margin-top: 10px;
}

h1 {
    color: #8E44AD; 
    border-bottom: 2px solid #8E44AD;
    padding-bottom: 8px;
    margin-bottom: 15px;
    font-weight: 700;
    text-align: center;
    font-size: 1.7em; 
}

/* የፍለጋ መስኩን ማሻሻል */
#search-input {
    background-color: #445A6F; 
    color: #ECF0F1;
    border: none;
    border-radius: 20px; 
    padding: 10px 15px; 
    margin-bottom: 15px;
    font-size: 14px; 
}

/* --- የ Category Buttons ዲዛይን --- */
#category-buttons {
    display: flex;
    flex-wrap: wrap; 
    gap: 6px; 
    margin-bottom: 20px;
    justify-content: center; 
}

.cat-button {
    background-color: #445A6F; 
    color: #ECF0F1; 
    border: none;
    border-radius: 15px; 
    padding: 5px 12px; 
    font-size: 13px;
    cursor: pointer;
    transition: background-color 0.3s;
}

/* አሁን የተመረጠው አዝራር ዲዛይን (Active) */
.cat-button.active {
    background-color: #9B59B6; 
    color: white;
    box-shadow: 0 2px 5px rgba(155, 89, 182, 0.5); 
    font-weight: 600;
}

/* የቀመር ካርዶች (Formula Cards) */
.formula-card {
    background-color: #445A6F; 
    border-radius: 10px; 
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3); 
    margin-bottom: 10px;
    padding: 15px; 
}

.formula-card:hover {
    transform: translateY(-2px); 
    box-shadow: 0 5px 12px rgba(0, 0, 0, 0.4);
}

.formula-card h3 {
    color: #9B59B6; 
    font-size: 1.2em; 
    margin-bottom: 4px; 
}

.formula-card p {
    font-size: 0.9em;
    color: #BDC3C7;
    margin: 2px 0;
}

/* --- የስታቲስቲክስ ካርዶች (Invite/Formula Count) --- */
.stats-container {
    display: flex;
    justify-content: space-between;
    gap: 8px; 
    margin-bottom: 15px;
}

.stat-card {
    background-color: #445A6F;
    flex: 1;
    min-width: 45%; 
    text-align: center;
    padding: 10px; 
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
    cursor: pointer; 
    transition: box-shadow 0.3s, transform 0.2s;
    color: white; 
}

.stat-card i {
    font-size: 20px; 
    color: #9B59B6; 
    margin-bottom: 5px; 
}

.stat-card h2 {
    font-size: 1.2em; 
    font-weight: 700;
    margin: 0;
}

.stat-card p {
    font-size: 0.75em;
    color: #BDC3C7;
    margin: 0;
}


/* ================================== */
/* 🛑 Splash Screen & Animation CSS 🛑 */
/* ================================== */
#splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #2c3e50; 
    z-index: 200; 
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

#splash-title {
    font-size: 3.5em; 
    font-weight: 900;
    color: #ECF0F1; 
    text-shadow: 0 0 15px rgba(155, 89, 182, 0.8); 
    margin: 0;
}

#splash-screen p {
    color: #9B59B6; 
    font-size: 1.5em;
    margin-top: 5px;
    font-weight: 300;
}

/* 🛑 Splash Screen የሚጠፋበት አኒሜሽን 🛑 */
.fade-out-splash {
    animation: fadeOut 0.5s ease-out forwards;
    animation-delay: 1.2s; /* ከ 1.2 ሰከንድ በኋላ መጥፋት ይጀምራል */
}

@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}

/* 🛑 App Container ወደ ውስጥ የሚገባበት አኒሜሽን 🛑 */
.app-scale-in {
    opacity: 0;
    transform: scale(0.98); /* ትንሽ ትንሽ ሆኖ ይጀምራል */
    animation: scaleIn 0.5s ease-out forwards;
    animation-delay: 1.6s; /* Splash ከተጠናቀቀ በኋላ ይጀምራል */
}

@keyframes scaleIn {
    0% {
        opacity: 0;
        transform: scale(0.98);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}


/* (የModal CSS አልተነካም) */
.modal {
    position: fixed; 
    z-index: 100; 
    left: 0;
    top: 0;
    width: 100%; 
    height: 100%; 
    overflow: auto; 
    background-color: rgba(0,0,0,0.7); 
    backdrop-filter: blur(5px); 
}

.modal-content {
    background-color: #34495E;
    color: #ECF0F1;
    margin: 15% auto; 
    padding: 25px;
    border-radius: 15px;
    max-width: 400px; 
    text-align: center;
}

.modal-content button {
    background-color: #1ABC9C;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 10px;
    font-weight: 600;
}
