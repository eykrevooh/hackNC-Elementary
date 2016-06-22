function buildURL(page){
    var selectedTerm = document.getElementById('termSelect').value
    var url       = '/courseManagement/'.concat(page).concat('/').concat(selectedTerm)
    window.location.replace(url)
}

function getCurrentTerm() {
        var termCode = document.getElementById('termSelect').value
        return termCode
}
    
$(document).ready(function ($) {
    termCode = getCurrentTerm()
    $("#crossListedLink").attr("href", "/courseManagement/crossListed/" + termCode)
    $("#conflictsLink").attr("href", "/courseManagement/conflicts/" + termCode)
    $("#trackerLink").attr("href", "/courseManagement/tracker/" + termCode)
});