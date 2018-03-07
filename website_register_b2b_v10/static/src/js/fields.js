function radioIsCompany() {
    if (document.getElementById('radioCompany').checked) {
        
        document.getElementById('isCompany').style.display = 'block';
        
        document.getElementById("company").required = true;
        
        document.getElementById("company").value = "";
        
        document.getElementById('hasInsc_est').style.display = 'block';
        
        document.getElementById("insc_est").required = true;
        
        document.getElementById("insc_est").value = "";
        
    } else {
        document.getElementById('isCompany').style.display = 'None';
        
        document.getElementById("company").required = false;
        
        document.getElementById('hasInsc_est').style.display = 'None';
        
        document.getElementById("insc_est").required = false;
        
    }
}

function submitFormCheck() {
    
    if (document.getElementById("radioPerson").checked) {
        
        document.getElementById("company").value = document.getElementById("contact_name_a").value;
        
        document.getElementById("insc_est").value = "";
        
    }
}