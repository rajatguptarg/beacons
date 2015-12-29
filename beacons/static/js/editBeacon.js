(function editBeacon(){
    $(document).ready(function(){
        editBeacon.init();
    });

    editBeacon.init = function(){
    	editBeacon.description = $("#description")[0];

    	$("form")[0].onsubmit = editBeacon.validateAndSubmit;
    }

    editBeacon.validateAndSubmit = function(e){
    	if(editBeacon.description.value.length == 0){
    		e.preventDefault();
    	}
    }
})();