(function register(){

    var register = {};

    $(document).ready(function(){
        register.registerEvents();
    });

    register.registerEvents = function(){
        register.beaconType = document.getElementById("type");
        register.iBeaconFormContainer =  $("#iBeaconFormContainer");
        register.eddyStoneFormContainer =  $("#eddystoneFormContainer");
       
        beaconType.onchange = function(){
            register.toggleBeaconForm();
        }

        register.toggleBeaconForm();
    }

    register.toggleBeaconForm = function () {
        if(register.beaconType.value == "iBEACON"){
            register.iBeaconFormContainer.removeClass('hide')
            register.eddyStoneFormContainer.addClass('hide')
        }else{
            register.iBeaconFormContainer.addClass('hide')
            register.eddyStoneFormContainer.removeClass('hide')
        }
    }
})();
