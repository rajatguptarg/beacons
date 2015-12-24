(function register(){

    var register = {};

    $(document).ready(function(){
        register.registerEvents();
    });

    register.registerEvents = function(){
        var beaconType = document.getElementById("type");
        beaconType.onchange = function(){
            register.toggleBeaconForm();
        }
    }

    register.toggleBeaconForm = function () {
        $("#iBeaconFormContainer").toggleClass("hide");
        $("#eddystoneFormContainer").toggleClass("hide")
    }
})();