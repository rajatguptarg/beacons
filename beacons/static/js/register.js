(function register(){

    var register = {};

    $(document).ready(function(){
        register.registerEvents();
    });

    register.registerEvents = function(){
        register.beaconType = document.getElementById("type");
        register.iBeaconFormContainer =  $("#iBeaconFormContainer");
        register.eddyStoneFormContainer =  $("#eddystoneFormContainer");
       
        register.beaconType.onchange = function(){
            register.toggleBeaconForm();
        }

        register.toggleBeaconForm();
    }

    register.toggleBeaconForm = function () {
        if(register.beaconType.value == "iBEACON"){
            register.iBeaconFormContainer.removeClass('hidden')
            register.eddyStoneFormContainer.addClass('hidden')
        }else{
            register.iBeaconFormContainer.addClass('hidden')
            register.eddyStoneFormContainer.removeClass('hidden')
        }
    }
})();
