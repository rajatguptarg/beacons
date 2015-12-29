(function register(){

    UUID_REJEX = '^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$';

    $(document).ready(function(){
        register.init();
    });

    register.init = function(){
        register.registerForm = $("form")[0];
        register.beaconType = $("#type")[0];

        register.iBeaconFormContainer =  $("#iBeaconFormContainer");
        register.uuid = $("#uuid")[0];
        register.major = $("#major")[0];
        register.minor = $("#minor")[0];

        register.eddyStoneFormContainer =  $("#eddystoneFormContainer");
        register.namespace = $("#namespace")[0];
        register.instanceId = $("#instanceId")[0];

        register.description = $("#description")[0];
       
        register.beaconType.onchange = register.toggleBeaconForm;
        register.registerForm.onsubmit = register.validateAndSubmitForm;

        register.toggleBeaconForm();
    }

    register.toggleBeaconForm = function () {
        if(register.beaconType.value == "iBEACON"){
            register.iBeaconFormContainer.removeClass('hidden');
            register.eddyStoneFormContainer.addClass('hidden');
        }else{
            register.iBeaconFormContainer.addClass('hidden');
            register.eddyStoneFormContainer.removeClass('hidden');
        }
    }

    register.validateAndSubmitForm = function(e){
        if(!isFormValid()){
            console.log("dont submit");
            e.preventDefault();
        }
    }

    function isFormValid(){
        if(register.beaconType.value == "iBEACON"){
            return isValidiBeacon() && hasDescription();
        }else{
            return isValidEddyStone() && hasDescription();
        }
    }

    function isValidiBeacon(){
        var uuid = register.uuid.value;
        var major = register.major.value;
        var minor = register.minor.value;
        return uuid.match(UUID_REJEX) && major.length != 0 && minor.length != 0;
    }

    function isValidEddyStone(){
        var namespace = register.namespace.value;
        var instanceId = register.instanceId.value;
        return namespace.length == 20 && instanceId.length == 12;
    }

    function hasDescription(){
        return register.description.value.length > 0;
    }

})();
