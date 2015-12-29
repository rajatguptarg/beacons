(function attachment(){
    $(document).ready(function(){
        attachment.init();
    });

    attachment.init = function(){
    	attachment.form = $("form")[0];
    	attachment.description = $("#description")[0];

    	attachment.form.onsubmit = attachment.validateAndSubmit;
    }

    attachment.validateAndSubmit = function(e){
    	if(!isValidAttachment()){
    		e.preventDefault();
    	}
    }

    function isValidAttachment(){
    	var description = attachment.description.value;
    	if(description.length != 0){
    		try{
    			JSON.parse(description);
    			return true;
    		}catch(e){
    			return false;
    		}
    	}
    	return false;
    }
})();