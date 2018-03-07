function radioIsCompany() {
    if (document.getElementById('radioCompany').checked) {
        
        document.getElementById('isCompany').style.display = 'block';
        
        document.getElementById("company").required = true;
        
        document.getElementById('hasInsc_est').style.display = 'block';
        
        document.getElementById("insc_est").required = true;
        
    } else {
        document.getElementById('isCompany').style.display = 'None';
        
        document.getElementById("company").required = false;
        
        document.getElementById('hasInsc_est').style.display = 'None';
        
        document.getElementById("insc_est").required = false;
        
    }
}