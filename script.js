// ... (የኮዱ መጀመሪያ እንደነበረው ይቆያል)

// የማጋራት ተግባር
function shareApp() {
    // 🛑 የእርስዎን ትክክለኛ GitHub Pages URL እዚህ ይጠቀሙ 🛑
    // በሪፖዚተሪ ስም (All-formulas2) በትክክል እንዲሄድ ተደርጓል
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

// ... (የኮዱ መጨረሻ እንደነበረው ይቆያል)
